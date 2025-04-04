import requests
from config import db, API_KEY
import math
from preprocess import preprocess
import logging
import time

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def get_foodtruck_data(page_no=1, num_of_rows=100):
    url = "http://apis.data.go.kr/1471000/FoodTruckDsgnStusService/getFoodTruckDsgnStusService"

    params = {
        "serviceKey": API_KEY,
        "type": "json",
        "pageNo": page_no,
        "numOfRows": num_of_rows
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()  # 에러 발생시 예외 발생
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        logger.error(f"API 요청 중 오류 발생: {e}")
        return None

def insert_to_db(items):
    if not items:
        logger.warning("저장할 데이터가 없습니다.")
        return
    
    collection = db["foodtrucks"]
    processed_items = preprocess(items)
    
    # 이미 있는 데이터는 업데이트, 없는 데이터는 삽입 (upsert)
    for item in processed_items:
        collection.update_one(
            {"license_no": item["license_no"]},
            {"$set": item},
            upsert=True
        )
    
    logger.info(f"{len(processed_items)}개 데이터 처리 완료")

def collect_all_data():
    # 첫 번째 페이지 호출 (데이터 및 총 개수 얻기)
    first_response = get_foodtruck_data(page_no=1, num_of_rows=100)
    if not first_response:
        logger.error("초기 데이터를 가져오는데 실패했습니다.")
        return False

    try:
        total_count = first_response['body']['totalCount']
        num_of_rows = 100
        total_pages = math.ceil(total_count / num_of_rows)
        
        logger.info(f"전체 데이터 개수: {total_count}, 총 페이지 수: {total_pages}")

        # 첫 페이지 데이터 저장
        if 'items' in first_response['body']:
            insert_to_db(first_response['body']['items'])

        # 나머지 페이지 데이터 저장
        for page in range(2, total_pages + 1):
            logger.info(f"{page}/{total_pages} 페이지 데이터를 요청중...")
            response = get_foodtruck_data(page_no=page, num_of_rows=num_of_rows)
            
            if response and 'body' in response and 'items' in response['body']:
                insert_to_db(response['body']['items'])
            else:
                logger.warning(f"{page} 페이지에서 데이터를 얻지 못했습니다.")
            
            # API 요청 간격 조절
            time.sleep(0.5)
        
        return True
    except Exception as e:
        logger.error(f"데이터 수집 중 오류 발생: {e}")
        return False

if __name__ == "__main__":
    collect_all_data()