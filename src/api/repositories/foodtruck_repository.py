# src/api/repositories/foodtruck_repository.py
from datetime import datetime
from bson import ObjectId
from src.config.database import foodtruck_collection

class FoodtruckRepository:
    def __init__(self):
        self.collection = foodtruck_collection
    
    def format_foodtruck(self, truck):
        """MongoDB 문서를 API 응답 형식으로 변환"""
        if truck:
            truck["_id"] = str(truck["_id"])
        return truck
    
    def find_all(self, skip=0, limit=20, search=None):
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
        
        cursor = self.collection.find(query).skip(skip).limit(limit)
        return [self.format_foodtruck(truck) for truck in cursor]
    
    def find_by_id(self, foodtruck_id):
        """
        ID로 푸드트럭을 찾습니다.
        """
        try:
            truck = self.collection.find_one({"_id": ObjectId(foodtruck_id)})
        except:
            truck = self.collection.find_one({"license_no": foodtruck_id})
            
        return self.format_foodtruck(truck) if truck else None
    
    def find_nearby(self, lat, lng, distance=1000):
        """
        주변 푸드트럭을 찾습니다.
        """
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
        
        trucks = self.collection.find(query)
        return [self.format_foodtruck(truck) for truck in trucks]
    
    def update_location(self, license_no, location):
        """
        푸드트럭 위치를 업데이트합니다.
        """
        result = self.collection.update_one(
            {"license_no": license_no},
            {
                "$set": {
                    "location": location,
                    "last_updated": datetime.now()
                }
            }
        )
        
        return result.matched_count > 0