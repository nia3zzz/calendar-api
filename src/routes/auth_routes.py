from fastapi import APIRouter
from validators.auth_validators import Create_User_Validator
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from db.engine import get_db
from models.user_model import User
from models.event_model import Event
from lib.hash_password import hash_password

# defining a router instance
auth_routes = APIRouter()


# create the sign up route for the user
@auth_routes.post("/signup", tags=["Auth"])
def sign_up(req_data: Create_User_Validator, db: Session = Depends(get_db)):
    # check if an user exists with the provided email
    found_user = db.query(User).filter_by(email=req_data.email).first()

    if found_user != None:
        raise HTTPException(
            409,
            {"status": "error", "message": "User with this email already exists."},
        )

    try:
        # hash the password
        hashed_password = hash_password(req_data.password)

        # save the data in the database
        new_user = User(
            first_name=req_data.first_name,
            last_name=req_data.last_name,
            email=req_data.email,
            password=hashed_password,
        )

        # commit the new user to the main db
        db.add(new_user)
        db.commit()

        return {"status": "success", "message": "User created successfully."}
    except Exception:
        db.rollback()
        raise HTTPException(
            500, {"status": "error", "message": "Internal server error."}
        )
