# api/models.py
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class FoodTruckBase(BaseModel):
    license_no: str
    business_name: str
    address: str
    organization: Optional[str] = None
    ceo_name: Optional[str] = None
    tel_no: Optional[str] = None
    permission_date: Optional[str] = None
    
class FoodTruck(FoodTruckBase):
    id: str = Field(alias="_id")
    location: Optional[dict] = None
    avg_rating: Optional[float] = 0.0
    review_count: Optional[int] = 0
    
    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            datetime: lambda dt: dt.isoformat()
        }

class ReviewBase(BaseModel):
    foodtruck_id: str
    user_id: str
    rating: float = Field(ge=1, le=5)
    comment: Optional[str] = None
    
class ReviewCreate(ReviewBase):
    pass
    
class Review(ReviewBase):
    id: str = Field(alias="_id")
    created_at: datetime
    
    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            datetime: lambda dt: dt.isoformat()
        }
        
class UserBase(BaseModel):
    username: str
    email: str
    
class UserCreate(UserBase):
    password: str
    
class User(UserBase):
    id: str = Field(alias="_id")
    created_at: datetime
    
    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            datetime: lambda dt: dt.isoformat()
        }