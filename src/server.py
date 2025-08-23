from dotenv import load_dotenv

# load the .env variables into runtime environment
load_dotenv()

from fastapi import FastAPI, Depends
from db.engine import get_db
from sqlalchemy.orm import Session
from routes.auth_routes import auth_routes

v1 = FastAPI()

# include auth routes
v1.include_router(router=auth_routes, prefix="/api/v1/auth")


# health check route
@v1.get("/", tags=["Health Check"])
def read_root(db: Session = Depends(get_db)):
    try:
        print("Database Session: ", db)

    finally:
        return {
            "Health": "Check",
        }
