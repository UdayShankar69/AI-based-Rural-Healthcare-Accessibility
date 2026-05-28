# db.py
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
# Load MONGO_URI from a .env file
load_dotenv()
# IMPORTANT: Replace the default with your actual connection string in a .env file!
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "rural_health_db")
# Initialize the MongoDB client and database
try:
    client = AsyncIOMotorClient(MONGO_URI)
    db = client[DATABASE_NAME]
    print(f"✅ MongoDB client configured for: {DATABASE_NAME}")
except Exception as e:
    print(f"❌ Error initializing MongoDB client. Check your MONGO_URI in .env: {e}")
# Recommended: Create a .env file in your backend folder with your connection string:
# MONGO_URI="mongodb://<your_user>:<your_password>@<your_host>:<your_port>/?authSource=admin"
# DATABASE_NAME="rural_health_db"