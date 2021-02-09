from flask import Flask, request, url_for, render_template, redirect, session, sessions
import requests
from functions import hashPassword, verifyPasswordHash, addLoggedUser, delLoggedUser, checkIfLoggedIn
import json
import os
import base64
from markupsafe import escape

print("elo")

url = 'http://127.0.0.1:5001/'

app = Flask(__name__)
# app.secret_key = os.urandom(16) 
app.secret_key = "a chuj"

@app.route('/')
def renderLoginPage():
    if 'username' in session:
        return escape(session['login'])
    return render_template('LoginPage.html')

@app.route('/', methods =["POST"]) 
@app.route('/getLoginUrl', methods=["POST"])
def getLogin():
    if request.method == "POST":
        error = "Invalid credentials motherfuckers"
        login = request.form["loginPage_login"]
        password = request.form["loginPage_password"]
        
        if login == "" or password == "": 
            return render_template("LoginPage.html", error=error)
        else:
            response = requests.get("http://127.0.0.1:5000/api/users?pesel="+login)
            if response.status_code == 200 and checkIfLoggedIn(login) == False:
                responseJson = response.json()
                isPasswordValid = verifyPasswordHash(responseJson['password'], password)
                if isPasswordValid:
                    session['login']=login 
                    print(session)
                    addLoggedUser(login)
                    return render_template("PatientPage.html")
                else:
                    return render_template("LoginPage.html", error=error)
            else:
                return render_template("LoginPage.html", error=error)
       

@app.route('/getRegisterUrl', methods=["POST"])
def getRegister():
    if request.method == "POST":
        error = "Invalid register data motherfuckers"
        login = request.form["register_pesel"]
        password = request.form["register_password"]
        passwordRep = request.form["register_password_rep"]
       
        if password!=passwordRep:
            return render_template("RegisterPage.html", error=error)
        
        files = {"first_name" : "firstName1", "last_name" : "lastName1", "pesel" : login, "password" : hashPassword(password)}
        response = requests.post('http://127.0.0.1:5000/api/users',
                     data=json.dumps(files),
                     headers={'Content-Type':'application/json'})

        if response.status_code == 201:
            addLoggedUser(login)
            session['login']=login 
            return render_template("PatientPage.html")
        else: 
            return render_template("RegisterPage.html", error=error)

@app.route('/getRegisterUrl', methods=["GET", "POST"])
def getRegisterUrl():
    return render_template('RegisterPage.html')

@app.route('/getLoginUrl', methods=["GET", "POST"])
def getLoginUrl():
    return render_template('LoginPage.html')

@app.route('/logOut', methods=["GET","POST"])
def logOut():
    delLoggedUser(session['login'])
    session.pop('login',None)  
    return redirect(url_for('getLoginUrl'))

if __name__=='__main__': 
    app.run(port=5001) 