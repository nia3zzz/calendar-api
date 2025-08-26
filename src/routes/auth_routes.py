from fastapi import APIRouter, Response
from validators.auth_validators import Create_User_Validator, Login_User_Validator
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from db.engine import get_db
from models.user_model import User
from models.event_model import Event
from lib.hash_password import hash_password
from lib.verify_password import verify_password
from lib.assign_jwt import assign_jwt

# defining a router instance
auth_routes = APIRouter()


# create the sign up route for the user
@auth_routes.post("/signup", status_code=201, tags=["Auth"])
def sign_up(req_data: Create_User_Validator, db: Session = Depends(get_db)):
    # check if an user exists with the provided email
    found_user = db.query(User).filter_by(email=req_data.email).first()

    if found_user != None:
        raise HTTPException(
            status_code=409,
            detail={
                "status": "error",
                "message": "User with this email already exists.",
            },
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
            status_code=500,
            detail={"status": "error", "message": "Internal server error."},
        )


# log the user in with required credentials
@auth_routes.post("/login", tags=["Auth"])
def login(
    req_data: Login_User_Validator, response: Response, db: Session = Depends(get_db)
):
    # check if a user already exists with email
    found_user = db.query(User).filter_by(email=req_data.email).first()

    if found_user == None:
        raise HTTPException(
            status_code=409,
            detail={"status": "error", "message": "Invalid data provided."},
        )

    # check if the password matches
    check_password = verify_password(req_data.password, found_user.password)

    if not check_password:
        raise HTTPException(
            status_code=409,
            detail={"status": "error", "message": "Invalid data provided."},
        )

    try:
        # call the the assign jwt function
        generated_jwt = assign_jwt(found_user.id)

        # set the cookie and return this res object
        response.set_cookie(
            key="Access_Cookie",
            httponly=True,
            max_age=30 * 24 * 60 * 60,
            value=generated_jwt,
        )
        return {"status": "success", "message": "User logged in successfully."}
    except:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail={"status": "error", "message": "Internal server error."},
        )


# logout the user by clearing the cookie
@auth_routes.post("/logout", tags=["Auth"])
def logout(response: Response):
    try:
        # clear the cookie and return success message
        response.delete_cookie(key="Access_Cookie")

        return {"status": "success", "message": "User logged out successfully."}
    except:
        raise HTTPException(
            status_code=500,
            detail={"status": "error", "message": "Internal server error."},
        )
