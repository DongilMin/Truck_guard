# config.py
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
DB_NAME = "foodtruck_guard"

client = MongoClient(MONGODB_URI)
db = client[DB_NAME]

API_KEY = os.getenv("API_KEY")
