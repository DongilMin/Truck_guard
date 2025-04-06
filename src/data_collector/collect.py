# data_collector/collect.py 업데이트
# 기존 코드에 preprocess 함수를 활용하는 부분 추가

import requests
from config import db, API_KEY
import math
from preprocess import preprocess
from datetime import datetime
from bson import ObjectId

def get_foodtruck_data(page_no=1, num_of_rows=100):
    url = "http://apis.data.go.kr/1471000/FoodTruckDsgnStusService/getFoodTruckDsgnStusService"

    params = {
        "serviceKey": API_KEY,
        "type": "json",
        "pageNo": page_no,
        "numOfRows": num_of_rows
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print("API 요청 실패:", response.text)
        return None

def insert_to_db(items):
    if not items:
        print("저장할 데이터가 없습니다.")
        return
        
    # 데이터 전처리
    cleaned_items = preprocess(items)
    
    # 각 항목에 ObjectId와 생성 시간 추가
    for item in cleaned_items:
        item["_id"] = ObjectId()
        item["created_at"] = datetime.now()
        item["last_updated"] = datetime.now()
        
        # 초기 리뷰 관련 필드 추가
        item["avg_rating"] = 0.0
        item["review_count"] = 0
    
    collection = db["foodtrucks"]
    collection.insert_many(cleaned_items)
    print(f"{len(cleaned_items)}개 데이터 저장 완료")

def update_existing_data():
    """
    이미 수집된 데이터와 새로 수집된 데이터를 비교하여 업데이트합니다.
    """
    collection = db["foodtrucks"]
    
    # 첫 페이지 데이터 수집
    response = get_foodtruck_data(page_no=1, num_of_rows=100)
    if not response or 'body' not in response or 'items' not in response['body']:
        print("데이터를 가져오지 못했습니다.")
        return
        
    # 데이터 전처리
    cleaned_items = preprocess(response['body']['items'])
    
    # 각 항목에 대해 업데이트 수행
    update_count = 0
    for item in cleaned_items:
        # 라이센스 번호로 기존 데이터 찾기
        existing = collection.find_one({"license_no": item["license_no"]})
        
        if existing:
            # 기존 데이터 업데이트
            result = collection.update_one(
                {"license_no": item["license_no"]},
                {
                    "$set": {
                        "address": item["address"],
                        "business_name": item["business_name"],
                        "tel_no": item["tel_no"],
                        "ceo_name": item["ceo_name"],
                        "last_updated": datetime.now()
                    }
                }
            )
            if result.modified_count > 0:
                update_count += 1
        else:
            # 새 데이터 추가
            item["_id"] = ObjectId()
            item["created_at"] = datetime.now()
            item["last_updated"] = datetime.now()
            item["avg_rating"] = 0.0
            item["review_count"] = 0
            collection.insert_one(item)
            update_count += 1
            
    print(f"{update_count}개 데이터 업데이트 완료")

if __name__ == "__main__":
    # 첫 번째 페이지 호출 (데이터 및 총 개수 얻기)
    first_response = get_foodtruck_data(page_no=1, num_of_rows=100)
    if first_response:
        total_count = first_response['body']['totalCount']
        num_of_rows = 100
        total_pages = math.ceil(total_count / num_of_rows)
        
        print(f"전체 데이터 개수: {total_count}, 총 페이지 수: {total_pages}")

        # 첫 페이지 데이터 저장
        insert_to_db(first_response['body']['items'])

        # 나머지 페이지 데이터 저장
        for page in range(2, total_pages + 1):
            print(f"{page} 페이지 데이터를 요청중...")
            response = get_foodtruck_data(page_no=page, num_of_rows=num_of_rows)
            if response and 'body' in response and 'items' in response['body']:
                insert_to_db(response['body']['items'])
            else:
                print(f"{page} 페이지에서 데이터를 얻지 못했습니다.")