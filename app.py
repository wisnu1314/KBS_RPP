from flask import Flask, request, render_template
import pandas as pd
import joblib
df_lk = pd.read_csv("AHH lk.csv")
df_pr = pd.read_csv("AHH pr.csv")
model_lk = joblib.load("AHH_LK.pkl")
model_pr =  joblib.load("AHH_PR.pkl")
provinsi_name = df_lk['Provinsi'].values.reshape(-1).tolist()
provinsi_dict = {}
i = 0
for provinsi in provinsi_name:
    provinsi_dict[provinsi] = i
    i += 1
humanize_province = {}
for provinsi in provinsi_name:
    humanized = provinsi[0]
    for i in range (1, len(provinsi)):
        if(provinsi[i - 1] != ' '):
            humanized += provinsi[i].lower()
        else:
            humanized += provinsi[i]
    humanize_province[provinsi] = humanized

# Declare a Flask app
app = Flask(__name__)

# Main function here
# ------------------
@app.route("/")
def hello():
    return render_template('template.html') 
@app.route('/', methods=['GET', 'POST'])
def main():
    
    # If a form is submitted
    if request.method == "POST":
        tahun = request.form.get("tahun")
        prov = request.form.get("provinsi")
        gender = request.form.get("gender")
        prov = prov.upper()
        prediction = 0
        if(gender == "pria"):
            if int(tahun) <= 2021:
                prediction = df_lk[str(tahun)][provinsi_dict[prov]]
            else:
                prediction = df_lk['2021'][provinsi_dict[prov]]
                for j in range(int(tahun)-2021):
                    prediction = model_lk.predict([[prediction]]).reshape(-1)[0]
            prediction = "Angka Harapan Hidup pria di provinsi " +  humanize_province[prov] + " adalah " + str(prediction)
        elif(gender == 'wanita'):
            if int(tahun) <= 2021:
                prediction = df_pr[str(tahun)][provinsi_dict[prov]]
            else:
                prediction = df_pr['2021'][provinsi_dict[prov]]
                for j in range(int(tahun)-2021):
                    prediction = model_pr.predict([[prediction]]).reshape(-1)[0]
            prediction = "Angka Harapan Hidup wanita di provinsi " +  humanize_province[prov] + " adalah " + str(prediction)
    else:
        prediction = ""
        
    return render_template("template.html", output = prediction)
# Running the app
if __name__ == '__main__':
    app.run(debug = True)