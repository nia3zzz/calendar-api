from dotenv import load_dotenv

# load the .env variables into runtime environment
load_dotenv()

from fastapi import FastAPI
from db.engine import session_local

app = FastAPI()


# health check route
@app.get("/")
async def read_root():
    db = session_local()

    try:
        print("Database Session: ", db)

    finally:
        db.close()

    return {
        "Health": "Check",
    }
