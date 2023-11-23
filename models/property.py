import uuid
from typing import List
from pydantic import BaseModel, Field

class Location(BaseModel):
    address: str
    city: str
    state: str
    zipcode: str
    country: str

class Contact(BaseModel):
    agentName: str
    agentPhone: str
    agentEmail: str
    
class Property(BaseModel):
    propertyId: str = Field(default_factory=uuid.uuid4, alias="_id")
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

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "propertyId": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "propertyName": "Bla Bla",
                "propertyType": "Single Family House",
                "price": "350,000",
                "bedrooms": 3,
                "bathrooms": 2,
                "area": "1,800 sqft",
                "location": {
                    "address": "36B Trafalgar st.",
                    "city": "Villa Park",
                    "state": "CA",
                    "zipcode": "12345",
                    "country": "United States"
                },
                "description": "Property located in the countryside between Santa Gertrudis and San Miguel, surrounded by meadows and fruit fields, close to the beaches of the north of the island.\n\n",
                "features": [
                    "Open-concept layout",
                    "Hardwood floors",
                    "Walk-in closets",
                    "Two-car garage",
                    "Central heating and cooling",
                    "Fenced backyard"
                ],
                "images": ["image_url_1.jpg", "image_url_2.jpg", "image_url_3.jpg"],
                "contact": {
                    "agentName": "John Smith",
                    "agentPhone": "(123) 456-7890",
                    "agentEmail": "john.smith@example.com"
                }
            }
        }

    