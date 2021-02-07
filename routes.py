from flask import Flask, request, url_for, render_template, redirect
import requests
from functions import hashPassword, verifyPasswordHash
import json
import base64

print("elo")

url = 'http://127.0.0.1:5001/'

app = Flask(__name__)  

@app.route('/')
def renderLoginPage():
    return render_template('LoginPage.html')

@app.route('/', methods =["POST"]) 
@app.route('/getLoginUrl', methods=["POST"])
def getLogin():
    if request.method == "POST":
        error = "Invalid credentials motherfuckers"
        login = request.form["login_pesel"]
        password = request.form["login_password"]
        response = requests.get("http://127.0.0.1:5000/api/users?pesel="+login)
        print(response.status_code)
        if response.status_code == 200:
            responseJson = response.json()
            isPasswordValid = verifyPasswordHash(responseJson['password'], password)
            if isPasswordValid:
                return render_template("PatientPage.html")
            else:
                return render_template("LoginPage.html", error=error)
        else:
            return render_template("LoginPage.html", error=error)

@app.route('/getRegisterUrl', methods=["POST"])
def getRegister():
    if request.method == "POST":
        error = "Invalid register data motherfuckers"
        pesel = request.form["register_pesel"]
        password = request.form["register_password"]
        passwordRep = request.form["register_password_rep"]
        if password!=passwordRep:
            return render_template("RegisterPage.html", error=error)
        files = {"first_name" : "firstName1", "last_name" : "lastName1", "pesel" : pesel, "password" : hashPassword(password)}
        response = requests.post('http://127.0.0.1:5000/api/users',
                     data=json.dumps(files),
                     headers={'Content-Type':'application/json'})

        if response.status_code == 201:
            return render_template("PatientPage.html")
        else: 
            return render_template("RegisterPage.html", error=error)

@app.route('/getRegisterUrl', methods=["GET", "POST"])
def getRegisterUrl():
    return render_template('RegisterPage.html')

@app.route('/getLoginUrl', methods=["GET", "POST"])
def getLoginUrl():
    return render_template('LoginPage.html')

if __name__=='__main__': 
    app.run(port=5001) 