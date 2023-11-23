from typing import Union
import json
from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
from pydantic.tools import parse_obj_as
from models.property import *
import os,json
from typing import List
from routes import router as property_router
from dotenv import dotenv_values
from pymongo import MongoClient
from fastapi import FastAPI

app = FastAPI()
config = dotenv_values(".env")

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.on_event("startup")
def app_startup():
    app.mongodb_client = MongoClient(config["ATLAS_URI"])
    app.database = app.mongodb_client[config["DB_NAME"]]
    print("Connected to the MongoDB database!")

@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()
 
app.include_router(property_router, tags=["properties"], prefix="/property")   