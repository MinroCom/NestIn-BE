import uuid
from typing import List
from fastapi import File, UploadFile
from pydantic import BaseModel, Field

from models.property import Contact, Location

class PropertyRequest(BaseModel):
    propertyName: str = Field(...)
    propertyType: str = Field(...)
    price: str = Field(...)
    bedrooms: int = Field(...)
    bathrooms: int = Field(...)
    area: str = Field(...)
    location: Location = Field(...)
    description: str = Field(...)
    features: List[str] = Field(...)
    images: List[str] = Field(...)
    contact: Contact = Field(...)
    files: List[UploadFile] = File(...)