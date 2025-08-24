import jwt
import os

# check if the jwt is provided
secret_key = os.getenv("JWT_SECRET_KEY")

if secret_key == None:
    raise ValueError("JWT_SECRET_KEY is not defined in .env file.")


# assign jwt function that will return created jwt from secret key and provided payload
def assign_jwt(user_id):
    return jwt.encode({"user_id": str(user_id)}, str(secret_key), algorithm="HS256")
