import hashlib, binascii, os
 
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
   

#============ Managing the logged in users =============
currentLoggedInArr = []

def addLoggedUser(user):
    currentLoggedInArr.append(user)

def delLoggedUser(user):
    if user in currentLoggedInArr:
        currentLoggedInArr.remove(user)

def checkIfLoggedIn(user):
    return user in currentLoggedInArr

