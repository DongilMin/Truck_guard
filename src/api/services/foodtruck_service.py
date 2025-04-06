# src/api/services/foodtruck_service.py
from src.api.repositories.foodtruck_repository import FoodtruckRepository
from datetime import datetime

class FoodtruckService:
    def __init__(self):
        self.repository = FoodtruckRepository()
    
    def get_foodtrucks(self, skip=0, limit=20, search=None):
        """
        푸드트럭 목록을 가져옵니다.
        """
        return self.repository.find_all(skip, limit, search)
    
    def get_foodtruck_by_id(self, foodtruck_id):
        """
        ID로 푸드트럭을 찾습니다.
        """
        return self.repository.find_by_id(foodtruck_id)
    
    def get_nearby_foodtrucks(self, lat, lng, distance=1000):
        """
        주변 푸드트럭을 찾습니다.
        """
        return self.repository.find_nearby(lat, lng, distance)
    
    def update_location(self, license_no, lat, lng):
        """
        푸드트럭 위치를 업데이트합니다.
        """
        location = {
            "type": "Point",
            "coordinates": [lng, lat]
        }
        
        return self.repository.update_location(license_no, location)