import requests
from config import db, API_KEY

def get_foodtruck_data(page_no=1, num_of_rows=3):
    url = "http://apis.data.go.kr/1471000/FoodTruckDsgnStusService/getFoodTruckDsgnStusService"

    params = {
        "serviceKey": API_KEY,
        "type": "json",
        "pageNo": page_no,
        "numOfRows": num_of_rows
    }

    response = requests.get(url, params=params)

    print("상태코드:", response.status_code)
    print("응답내용:", response.text[:500])

    if response.status_code == 200:
        try:
            data = response.json()
            items = data['body']['items']
            return items
        except Exception as e:
            print("JSON 구조가 예상과 다릅니다:", e, response.text)
            return []
    else:
        print("API 요청 실패", response.text)
        return []

def insert_to_db(items):
    collection = db["foodtrucks"]
    if items:
        result = collection.insert_many(items)
        print(f"{len(result.inserted_ids)}건의 데이터를 삽입했습니다.")
    else:
        print("삽입할 데이터가 없습니다.")

if __name__ == "__main__":
    data = get_foodtruck_data()
    insert_to_db(data)
