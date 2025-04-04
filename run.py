# run.py
import uvicorn
import schedule
import time
import threading
from api.main import app
from data_collector.collect import update_existing_data

def run_schedule():
    """
    스케줄러를 실행하는 함수
    """
    # 매일 자정에 데이터 업데이트
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
    uvicorn.run(app, host="0.0.0.0", port=8000)