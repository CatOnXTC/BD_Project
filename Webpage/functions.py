import hashlib, binascii, os
import base64
import os

PDF_PATH = "C:/Users/Geops/Desktop/PROJEKT_BD_MAIN/BD_Project/Webpage/static/client/pdf/"
UPLOADS_PATH = "C:/Users/Geops/Desktop/PROJEKT_BD_MAIN/BD_Project/Webpage/static/client/uploads/"

#============ Hashing password =============

def hashPassword(password):
    """Hash a password for storing."""
    return hashlib.sha256(password.encode('utf-8')).hexdigest()
 
def verifyPasswordHash(stored_password, provided_password):
    """Verify a stored password against one provided by user"""
    if(provided_password == None):
        return False
    else:
        pwdhash = hashlib.sha256(provided_password.encode('utf-8')).hexdigest()
        return pwdhash == stored_password

#============ Others =============

# if True this is Patient else Admin
def checkIfUser(login):
    if len(login) == 11 and login.isdigit():
        return True
    else:
        return False
   

#============ Managing the logged in users =============
currentLoggedInArr = []

def addLoggedUser(user):
    currentLoggedInArr.append(user)

def delLoggedUser(user):
    if user in currentLoggedInArr:
        currentLoggedInArr.remove(user)

def checkIfLoggedIn(user):
    return user in currentLoggedInArr

#============ Converting from and to blob =============

def pdfToBlob(filename):
    # file_path = 'D:\\GitHub\\BD_Project\\Webpage\\static\\client\\uploads\\' #YOUR PATH
    with open(UPLOADS_PATH + filename, 'rb') as f:
        blob = str(base64.b64encode(f.read()))
        blob = blob[2:-1]
    os.remove(UPLOADS_PATH + filename)
    return blob

def createPdfs(fileBlobArr,fileNameArr):
    for i in range(len(fileBlobArr)):     
        blob = base64.b64decode(fileBlobArr[i])
        pdf_file = open(PDF_PATH + fileNameArr[i],"wb")
        pdf_file.write(blob)
        pdf_file.close()

def deletePdfs(pesel, fileNameArr):
    for fName in fileNameArr:
        if os.path.exists(PDF_PATH + fName) and pesel in fName:
            os.remove(PDF_PATH + fName)
