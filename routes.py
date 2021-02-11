from flask import Flask, request, url_for, render_template, redirect, session, sessions, send_file, send_from_directory, safe_join, abort
import requests
from functions import hashPassword, verifyPasswordHash, addLoggedUser, delLoggedUser, checkIfLoggedIn, checkIfUser, createPdfs, deletePdfs
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
app.config["CLIENT_PDF"] = "C:/Users/Geops/Desktop/BD Project/BD_Project/static/client/pdf"
app.config["UPLOAD_FOLDER"] = "C:/Users/Geops/Desktop/BD Project/BD_Project/static/client/uploads"
# app.config['UPLOAD_EXTENSIONS'] = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

fileNameArr = []

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
            if checkIfUser(login):
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
            else:
                response = requests.get("http://127.0.0.1:5000/api/employees?username="+login)
                if response.status_code == 200 and checkIfLoggedIn(login) == False:
                    responseJson = response.json()
                    isPasswordValid = verifyPasswordHash(responseJson['password'], password)
                    if isPasswordValid:
                        session['login'] = login
                        addLoggedUser(login)
                        return redirect("adminPage")
                    else:
                        render_template("LoginPage.html", error=error)     
            
    return render_template("LoginPage.html")

@app.route('/adminPage',methods=['POST','GET'])
def adminPage():
    headings = ("PESEL Pacjenta", "Dodaj badanie", "Usuń Pacjenta")
    response = requests.get("http://127.0.0.1:5000/api/users").json()
    peselArr = []
    dataTuple = ()
    dataArr = []
    for elem in response:
        dataArr.append([elem['pesel'], "upload_file/","usuń"])
    dataTuple = tuple(dataArr)

    return render_template('AdminPage.html', headings=headings, data=dataTuple)

@app.route('/patientPage')
def patientPage():
    responseUser = requests.get("http://127.0.0.1:5000/api/users?pesel=" + session['login'])
    responseJson = responseUser.json()
    user_id = responseJson['id']
    first_name = responseJson['first_name']
    last_name = responseJson['last_name']
    pesel = responseJson['pesel']
    responseResult = requests.get("http://127.0.0.1:5000/api/results?pesel=" + session['login']).json()
    headings = ("Id", "Imię i nazwisko pracownika", "Data badania", "Otwórz")
    dataTuple = ()
    dataArr = []
    idArr = []
    usernameArr = []
    dateArr = []
    fileBlobArr = []
    
    for i in range(len(responseResult)):
        elem = responseResult[i]
        idArr.append(elem['id'])
        usernameArr.append(elem['username'])
        dateArr.append(elem['result_date'].replace("T"," "))
        fileNameArr.append(elem['pesel'] + "___" + elem['result_date'].replace(":","_")+".pdf")
        fileBlobArr.append(elem['result_file'])
    
    createPdfs(fileBlobArr,fileNameArr)
    for i in range(len(idArr)):
        response = requests.get("http://127.0.0.1:5000/api/employees?username=" + usernameArr[i]).json()
        fullName = response['first_name'] + " " + response['last_name']
        dataArr.append([idArr[i], fullName, dateArr[i],"get-file/" + fileNameArr[i]])
    dataTuple = tuple(dataArr)

    return render_template('PatientPage.html', user_id = user_id, first_name = first_name, last_name = last_name, pesel = pesel, headings=headings, data=dataTuple)

@app.route("/get-file/<file_name>")
def get_image(file_name):
    try:
        return send_from_directory(app.config["CLIENT_PDF"], filename=file_name, as_attachment=True)
    except FileNotFoundError:
        abort(404)

@app.route('/upload_file', methods=['POST','GET'])
def upload_file():
        if request.method == 'POST':
        # check if the post request has the file part
            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)
            file = request.files['file']
            # if user does not select file, browser also
            # submit a empty part without filename
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                return redirect(url_for('uploaded_file',
                                        filename=filename))
        return

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
    deletePdfs(session['login'], fileNameArr)
    delLoggedUser(session['login'])
    session.pop('login', None)
    return redirect(url_for('login'))

if __name__=='__main__': 
    app.run(port=5001) 