import uuid
from typing import List
from pydantic import BaseModel, Field, EmailStr

# class User(BaseModel):
#     userId: str = Field(default_factory=uuid.uuid4, alias="_id")
#     name: str = Field(..., description="User's name")
#     surname: str = Field(..., description="User's surname")
#     citizenship: str = Field(..., description="User's citizenship")
#     phone: str = Field(..., description="User's phone number")
#     email: EmailStr = Field(..., description="User's email")
#     password: str = Field(..., description="User's password")

class User(BaseModel):
    fullname : str = Field(default = None)
    email : EmailStr = Field(default = None)
    password: str = Field(default = None, description="User's password")
    class Config:
        schema_extra = {
            "post_demo" : {
                "name" : "Asad",
                "email" : "asdasdgmail.com",
                "password" : "1234"
            }
        }
    
class UserLogin(BaseModel):
    email : EmailStr = Field(default = None)
    password: str = Field(default = None, description="User's password")
    class Config:
        schema_extra = {
            "post_demo" : {
                "email" : "asdasdgmail.com",
                "password" : "1234"
            }
        }    