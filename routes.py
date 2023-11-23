import functools
import os
import json
import aiofiles
from services.common_functions import *
from click import File
from fastapi import APIRouter, Body, Depends, Form, Request, Response, HTTPException, UploadFile, status
from fastapi.encoders import jsonable_encoder
from typing import Annotated, List
from fastapi import APIRouter, Request, HTTPException, status
from models.user import User
from fastapi import HTTPException, Request
from fastapi.routing import APIRouter
from starlette import status
from models.property import *
from models.token_utils import *
from models.user import *
from models.jwt_handler import signJWT


router = APIRouter()


users = []

@router.post("/", response_description="Create a new property", status_code=status.HTTP_201_CREATED)
def create_property(request: Request, files: Annotated[List[UploadFile], File(...)], property: Property = Body(...)):
    property = jsonable_encoder(property)
    new_property = request.app.database["properties"].insert_one(property)
    created_property = request.app.database["properties"].find_one(
        {"_id": new_property.inserted_id}
    )
    save_files(files)

    return created_property

@router.get("/", response_description="List all properties", response_model=List[Property])
def list_properties(request: Request):
    properties = list(request.app.database["properties"].find(limit=100))
    return properties

@router.get("/{id}", response_description="Get a single property by id", response_model=Property)
def find_property(id: str, request: Request):
    if (property := request.app.database["properties"].find_one({"_id": id})) is not None:
        return property
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Property with ID {id} not found")

@router.put("/{id}", response_description="Update a property", response_model=Property)
def update_property(id: str, request: Request, property: Property = Body(...)):
    property = {k: v for k, v in property.dict().items() if v is not None}
    if len(property) >= 1:
        update_result = request.app.database["properties"].update_one(
            {"_id": id}, {"$set": property}
        )

        if update_result.modified_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Property with ID {id} not found")

    if (
        existing_property := request.app.database["properties"].find_one({"_id": id})
    ) is not None:
        return existing_property

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Property with ID {id} not found")

@router.delete("/{id}", response_description="Delete a property")
def delete_property(id: str, request: Request, response: Response):
    delete_result = request.app.database["properties"].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Properties with ID {id} not found")

@router.post("/uploadfile/")
async def create_upload_file(id: str, files: List[UploadFile] = File(...) , property: Property = Depends() ):
    i = 0
    for file in files:
        try:
            if file.content_type not in ["image/jpeg", "image/png"]:
                raise HTTPException(400, detail="Invalid document type")
            if file.content_type == "image/jpeg":
                ext=".jpg"
            elif file.content_type == "image/png":
                ext=".png"
            out_path = f'files/image_{i}{ext}'
            async with aiofiles.open(out_path, 'wb') as out_file:
                while content := await file.read(1024):
                    await out_file.write(content)
            i+=1
        except Exception:
            return {"message": "There was an error uploading the file(s)"}
        finally:
            file.file.close()
    
    return {"message": f"Successfuly uploaded {[file.filename for file in files]}"} 

# @router.post("/users/", response_description="Register a new user", status_code=status.HTTP_201_CREATED)
# def register_user(user: User, request: Request):

#     new_user = request.app.database["users"].insert_one(user.dict())
#     created_user = request.app.database["users"].find_one({"_id": new_user.inserted_id})

#     if created_user is not None and "username" in created_user:
        
#         token = create_access_token(created_user["username"]) 
#         return {"user": created_user, "token": token}
#     else:
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error creating user or generating token")

# @router.get("/", status_code=status.HTTP_200_OK)
# async def user(user: None,)

# @app.post("/register")
# def register_user(user: schemas.UserCreate, session: Session = Depends(get_session)):
#     existing_user = session.query(models.User).filter_by(email=user.email).first()
#     if existing_user:
#         raise HTTPException(status_code=400, detail="Email already registered")

#     encrypted_password =get_hashed_password(user.password)

#     new_user = models.User(username=user.username, email=user.email, password=encrypted_password )

#     session.add(new_user)
#     session.commit()
#     session.refresh(new_user)

# return {"message":"user created successfully"}
@router.post("user/signup", tags=["user"])
def user_signup(user : User = Body(default = None)):
    users.append(user)
    return signJWT(user.email)

def check_user(data: UserLogin):
    for user in users:
        if user.email == data.email and user.password == data.password:
            return True
        else:
            False

@router.post("/user/login", tags=["user"])
def user_login(user: UserLogin = Body(default = None)):
    if check_user(user):
        return signJWT(user.email)
    else:
        return{
            "error" : "Invalid login details!"
        }

# @router.get("/usersall")
# def get_allusers():

