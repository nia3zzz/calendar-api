from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# check if the database key exists
database_key = os.getenv("DATABASE_KEY")

if database_key == None:
    raise ValueError("DATABASE_KEY is not defined in .env file.")


# create the engine
engine = create_engine(database_key, echo=True)

# create the session loader
session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# create the base for the models
base = declarative_base()
