# src/api/controllers/foodtruck_controller.py
from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List, Optional
from src.api.services.foodtruck_service import FoodtruckService
from src.api.dtos.foodtruck_dto import FoodTruck

router = APIRouter(
    prefix="/foodtrucks",
    tags=["foodtrucks"],
    responses={404: {"description": "Not found"}},
)

foodtruck_service = FoodtruckService()

@router.get("/", response_model=List[FoodTruck])
async def get_foodtrucks(
    skip: int = 0, 
    limit: int = 20,
    search: Optional[str] = None
):
    """
    푸드트럭 목록을 가져옵니다.
    """
    return foodtruck_service.get_foodtrucks(skip, limit, search)

@router.get("/{foodtruck_id}", response_model=FoodTruck)
async def get_foodtruck(foodtruck_id: str):
    """
    특정 푸드트럭 상세 정보를 가져옵니다.
    """
    truck = foodtruck_service.get_foodtruck_by_id(foodtruck_id)
    if not truck:
        raise HTTPException(status_code=404, detail="푸드트럭을 찾을 수 없습니다")
    return truck

@router.get("/nearby/", response_model=List[FoodTruck])
async def get_nearby_foodtrucks(
    lat: float = Query(..., description="위도"),
    lng: float = Query(..., description="경도"),
    distance: int = Query(1000, description="검색 반경(미터)")
):
    """
    현재 위치 주변의 푸드트럭을 검색합니다.
    """
    return foodtruck_service.get_nearby_foodtrucks(lat, lng, distance)

@router.put("/{license_no}/location")
async def update_location(
    license_no: str,
    lat: float = Query(..., description="위도"),
    lng: float = Query(..., description="경도")
):
    """
    푸드트럭의 현재 위치를 업데이트합니다.
    """
    success = foodtruck_service.update_location(license_no, lat, lng)
    if not success:
        raise HTTPException(status_code=404, detail="푸드트럭을 찾을 수 없습니다")
    return {"success": True, "message": "위치가 업데이트되었습니다"}