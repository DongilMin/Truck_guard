# src/config/database.py
from pymongo import MongoClient
from src.config.settings import SETTINGS

client = MongoClient(SETTINGS.MONGODB_URI)
db = client[SETTINGS.DB_NAME]

# 컬렉션 정의
foodtruck_collection = db["foodtrucks"]
review_collection = db["reviews"]