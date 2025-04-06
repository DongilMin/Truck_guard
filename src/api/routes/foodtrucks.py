# api/routes/foodtrucks.py
from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List, Optional
from pymongo import GEOSPHERE
from bson import ObjectId
from datetime import datetime
import math

from api.models import FoodTruck
from data_collector.config import db

router = APIRouter(
    prefix="/foodtrucks",
    tags=["foodtrucks"],
    responses={404: {"description": "Not found"}},
)

# 컬렉션 및 인덱스 설정
collection = db["foodtrucks"]
collection.create_index([("location", GEOSPHERE)])

def format_foodtruck(truck):
    truck["_id"] = str(truck["_id"])
    return truck

@router.get("/", response_model=List[FoodTruck])
async def get_foodtrucks(
    skip: int = 0, 
    limit: int = 20,
    search: Optional[str] = None
):
    """
    푸드트럭 목록을 가져옵니다.
    """
    query = {}
    if search:
        query = {
            "$or": [
                {"business_name": {"$regex": search, "$options": "i"}},
                {"address": {"$regex": search, "$options": "i"}}
            ]
        }
    
    cursor = collection.find(query).skip(skip).limit(limit)
    trucks = [format_foodtruck(truck) for truck in cursor]
    
    return trucks

@router.get("/{foodtruck_id}", response_model=FoodTruck)
async def get_foodtruck(foodtruck_id: str):
    """
    특정 푸드트럭 상세 정보를 가져옵니다.
    """
    try:
        truck = collection.find_one({"_id": ObjectId(foodtruck_id)})
    except:
        truck = collection.find_one({"license_no": foodtruck_id})
        
    if not truck:
        raise HTTPException(status_code=404, detail="푸드트럭을 찾을 수 없습니다")
    
    return format_foodtruck(truck)

@router.get("/nearby/", response_model=List[FoodTruck])
async def get_nearby_foodtrucks(
    lat: float = Query(..., description="위도"),
    lng: float = Query(..., description="경도"),
    distance: int = Query(1000, description="검색 반경(미터)")
):
    """
    현재 위치 주변의 푸드트럭을 검색합니다.
    """
    # MongoDB GeoJSON 형식으로 쿼리
    query = {
        "location": {
            "$near": {
                "$geometry": {
                    "type": "Point",
                    "coordinates": [lng, lat]
                },
                "$maxDistance": distance
            }
        }
    }
    
    trucks = [format_foodtruck(truck) for truck in collection.find(query)]
    return trucks

@router.put("/{license_no}/location")
async def update_location(
    license_no: str,
    lat: float = Query(..., description="위도"),
    lng: float = Query(..., description="경도")
):
    """
    푸드트럭의 현재 위치를 업데이트합니다.
    """
    location = {
        "type": "Point",
        "coordinates": [lng, lat]
    }
    
    result = collection.update_one(
        {"license_no": license_no},
        {
            "$set": {
                "location": location,
                "last_updated": datetime.now()
            }
        }
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="푸드트럭을 찾을 수 없습니다")
    
    return {"success": True, "message": "위치가 업데이트되었습니다"}