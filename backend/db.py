import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)

# Base de datos y colección
db = client["headercheckr"]
analysis_collection = db["analyzed_urls"]
