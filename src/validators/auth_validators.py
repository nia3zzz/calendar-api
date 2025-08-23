from pydantic import BaseModel, Field, EmailStr


# signup user validator class
class Create_User_Validator(BaseModel):
    first_name: str = Field(min_length=3, max_length=30)
    last_name: str = Field(min_length=3, max_length=30)
    email: EmailStr
    password: str = Field(min_length=6, max_length=30)
