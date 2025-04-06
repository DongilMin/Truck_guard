# main.py
import uvicorn
import schedule
import time
import threading
from fastapi import FastAPI
from src.api.controllers import foodtruck_controller, review_controller
from src.data_collector.services.api_service import update_existing_data
from src.config.settings import SETTINGS

app = FastAPI(title="FoodTruck Guard API")

# CORS 설정
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(foodtruck_controller.router)
app.include_router(review_controller.router)

@app.get("/")
async def root():
    return {"message": "환영합니다!"}

def run_schedule():
    """
    스케줄러를 실행하는 함수
    """
    schedule.every().day.at("00:00").do(update_existing_data)
    
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    # 주기적인 데이터 업데이트를 위한 스케줄러 스레드 시작
    scheduler_thread = threading.Thread(target=run_schedule)
    scheduler_thread.daemon = True
    scheduler_thread.start()
    
    # FastAPI 서버 실행
    uvicorn.run(app, host=SETTINGS.HOST, port=SETTINGS.PORT)