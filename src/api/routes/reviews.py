# api/routes/reviews.py
from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Optional
from bson import ObjectId
from datetime import datetime

from api.models import Review, ReviewCreate
from data_collector.config import db

router = APIRouter(
    prefix="/reviews",
    tags=["reviews"],
    responses={404: {"description": "Not found"}},
)

# 컬렉션 설정
review_collection = db["reviews"]
foodtruck_collection = db["foodtrucks"]

def format_review(review):
    review["_id"] = str(review["_id"])
    return review

@router.get("/", response_model=List[Review])
async def get_reviews(
    foodtruck_id: Optional[str] = None,
    skip: int = 0,
    limit: int = 20
):
    """
    리뷰 목록을 가져옵니다. 푸드트럭 ID로 필터링 가능합니다.
    """
    query = {}
    if foodtruck_id:
        query["foodtruck_id"] = foodtruck_id
        
    cursor = review_collection.find(query).sort("created_at", -1).skip(skip).limit(limit)
    reviews = [format_review(review) for review in cursor]
    
    return reviews

@router.post("/", response_model=Review)
async def create_review(review: ReviewCreate):
    """
    새로운 리뷰를 작성합니다.
    """
    # 해당 푸드트럭이 존재하는지 확인
    try:
        truck_id = ObjectId(review.foodtruck_id)
        truck = foodtruck_collection.find_one({"_id": truck_id})
    except:
        truck = foodtruck_collection.find_one({"license_no": review.foodtruck_id})
        if truck:
            review.foodtruck_id = str(truck["_id"])
    
    if not truck:
        raise HTTPException(status_code=404, detail="해당 푸드트럭을 찾을 수 없습니다")
    
    # 리뷰 저장
    review_dict = review.dict()
    review_dict["created_at"] = datetime.now()
    review_dict["_id"] = ObjectId()
    
    # 리뷰 저장
    review_collection.insert_one(review_dict)
    
    # 푸드트럭의 평균 평점 업데이트
    pipeline = [
        {"$match": {"foodtruck_id": review.foodtruck_id}},
        {"$group": {
            "_id": "$foodtruck_id",
            "avg_rating": {"$avg": "$rating"},
            "count": {"$sum": 1}
        }}
    ]
    
    result = list(review_collection.aggregate(pipeline))
    
    if result:
        foodtruck_collection.update_one(
            {"_id": truck["_id"]},
            {
                "$set": {
                    "avg_rating": result[0]["avg_rating"],
                    "review_count": result[0]["count"]
                }
            }
        )
    
    return format_review(review_dict)

@router.get("/{review_id}", response_model=Review)
async def get_review(review_id: str):
    """
    특정 리뷰의 상세 정보를 가져옵니다.
    """
    try:
        review = review_collection.find_one({"_id": ObjectId(review_id)})
    except:
        raise HTTPException(status_code=400, detail="잘못된 리뷰 ID 형식입니다")
        
    if not review:
        raise HTTPException(status_code=404, detail="리뷰를 찾을 수 없습니다")
    
    return format_review(review)

@router.delete("/{review_id}")
async def delete_review(review_id: str):
    """
    특정 리뷰를 삭제합니다.
    """
    try:
        result = review_collection.delete_one({"_id": ObjectId(review_id)})
    except:
        raise HTTPException(status_code=400, detail="잘못된 리뷰 ID 형식입니다")
        
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="리뷰를 찾을 수 없습니다")
    
    return {"success": True, "message": "리뷰가 삭제되었습니다"}