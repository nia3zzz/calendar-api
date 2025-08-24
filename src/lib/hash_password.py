import bcrypt


# password hashing function
def hash_password(raw_password):
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(raw_password.encode("utf-8"), salt)
    return hash.decode("utf-8")
