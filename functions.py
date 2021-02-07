def checkPassword(jsonFile, passwordField):
    if jsonFile['password'] == passwordField:
        return True
    else:
        return False