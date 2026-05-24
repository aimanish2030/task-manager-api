from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL")

client = AsyncIOMotorClient(MONGODB_URL)
db = client["taskmanager"]

task_collection = db["tasks"]
user_collection = db["users"]