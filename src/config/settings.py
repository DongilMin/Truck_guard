# src/config/settings.py
from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # 서버 설정
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # 데이터베이스 설정
    MONGODB_URI: str = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
    DB_NAME: str = "foodtruck_guard"
    
    # API 설정
    API_KEY: str = os.getenv("API_KEY")
    
    class Config:
        env_file = ".env"

SETTINGS = Settings()