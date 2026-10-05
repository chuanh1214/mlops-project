import os
from motor.motor_asyncio import AsyncIOMotorClient

#URL kết nối MongoDB
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
DATABASE_NAME = "mlops_db"

client = AsyncIOMotorClient(MONGO_URL)
db = client[DATABASE_NAME]

def get_database():
    return db