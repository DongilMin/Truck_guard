import requests
from config import db, API_KEY
import math

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
    collection = db["foodtrucks"]
    if items:
        collection.insert_many(items)
        print(f"{len(items)}개 데이터 저장 완료")
    else:
        print("저장할 데이터가 없습니다.")

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
