# task of this file is to load the tables with out defined schema
from dotenv import load_dotenv

load_dotenv()

from db.engine import base, engine
from models.user_model import User
from models.event_model import Event, RoleEnum

base.metadata.create_all(bind=engine)
print("Tables created successfully!")
