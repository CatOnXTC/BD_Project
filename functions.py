import hashlib, binascii, os
import base64
import os

#============ Hashing password =============

def hashPassword(password):
    """Hash a password for storing."""
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')
 
def verifyPasswordHash(stored_password, provided_password):
    """Verify a stored password against one provided by user"""
    if(provided_password == None):
        return False
    else:
        salt = stored_password[:64]
        stored_password = stored_password[64:]
        pwdhash = hashlib.pbkdf2_hmac('sha512', 
                                    provided_password.encode('utf-8'), 
                                    salt.encode('ascii'), 
                                    100000)
        pwdhash = binascii.hexlify(pwdhash).decode('ascii')
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

def createPdfs(fileBlobArr,fileNameArr):
    for i in range(len(fileBlobArr)):     
        blob = base64.b64decode(fileBlobArr[i])
        pdf_file = open("C:/Users/Geops/Desktop/BD Project/BD_Project/static/client/pdf/"+fileNameArr[i],"wb")
        pdf_file.write(blob)
        pdf_file.close()

def deletePdfs(pesel, fileNameArr):
    for fName in fileNameArr:
        if os.path.exists("C:/Users/Geops/Desktop/BD Project/BD_Project/static/client/pdf/"+fName) and pesel in fName:
            print(fName)
            os.remove("C:/Users/Geops/Desktop/BD Project/BD_Project/static/client/pdf/"+fName)
