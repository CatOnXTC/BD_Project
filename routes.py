from flask import Flask, request, url_for, render_template, redirect, session, sessions
import requests
from functions import hashPassword, verifyPasswordHash, addLoggedUser, delLoggedUser, checkIfLoggedIn, checkIfUser
import json
import os
import base64
from markupsafe import escape
from flask_session.__init__ import Session

print("elo")

url = 'http://127.0.0.1:5001/'

app = Flask(__name__)
# Session(app)
app.secret_key = os.urandom(16) 

headings = ("Id", "Imię i nazwisko pracownika", "Data badania", "Otwórz")

data = (
    ("1","Zbyszko","1899","<a href=pliczek></a>"),
    ("2","SzymonSądownia","1869","pliczek"),
    ("3","CJ","1799","pliczek"),
)

@app.route('/',methods=['GET'])
def home():
    if 'login' in session:
        login = session['login']
        return redirect("patientPage")
    return render_template('loginPage.html')

@app.route('/',methods=['POST'])
@app.route('/login',methods=['POST','GET'])
def login():
    if request.method == "POST":
        error = "Invalid credentials!!!"
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
                    session['login'] = login
                    addLoggedUser(login)
                    return redirect("patientPage")
                else:
                    render_template("LoginPage.html", error=error)   
    return render_template("LoginPage.html")


@app.route('/patientPage')
def patientPage():
    response = requests.get("http://127.0.0.1:5000/api/users?pesel=" + session['login'])
    responseJson = response.json()
    user_id = responseJson['id']
    first_name = responseJson['first_name']
    last_name = responseJson['last_name']
    pesel = responseJson['pesel']
    return render_template('PatientPage.html', user_id = user_id, first_name = first_name, last_name = last_name, pesel = pesel, headings=headings, data=data)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        error = "Invalid register data!!!"
        login = request.form["register_login"]
        name = request.form["register_name"]
        surname = request.form["register_surname"]
        password = request.form["register_password"]
        passwordRep = request.form["register_password_rep"]
       
        if password!=passwordRep:
            return render_template("RegisterPage.html", error=error)
        

        if(checkIfUser(login)) == True:
            files = {"first_name" : name, "last_name" : surname, "pesel" : login, "password" : hashPassword(password)}
            response = requests.post('http://127.0.0.1:5000/api/users',
                    data=json.dumps(files),
                    headers={'Content-Type':'application/json'})
        else:
            files = {"first_name" : name, "last_name" : surname, "username" : login, "password" : hashPassword(password)}
            response = requests.post('http://127.0.0.1:5000/api/employees',
                    data=json.dumps(files),
                    headers={'Content-Type':'application/json'})  

        if response.status_code == 201:
            return redirect("login")
        else: 
            return render_template("RegisterPage.html", error=error)
    return render_template('RegisterPage.html')
   
@app.route('/logout', methods=['GET'])    
def logout():
    delLoggedUser(session['login'])
    session.pop('login', None)
    return redirect(url_for('login'))

if __name__=='__main__': 
    app.run(port=5001) 