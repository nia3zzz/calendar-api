import bcrypt


# password verifing function
def verify_password(raw_password, hashed_password):
    return bcrypt.checkpw(raw_password.encode("utf-8"), hashed_password.encode("utf-8"))
