from flask import Flask, request, url_for, render_template, redirect

print("elo")

url = 'http://127.0.0.1:5000/'

app = Flask(__name__)  

@app.route('/')
def renderLoginPage():
    return render_template('LoginPage.html')

@app.route('/', methods =["POST"]) 
def getLogin():
    if request.method == "POST":
        login = request.form["login_pesel"]
        password = request.form["login_password"]
        print(login+" : "+password)
        return render_template("PatientPage.html")

print(__name__)
if __name__=='__main__': 
    app.run() 