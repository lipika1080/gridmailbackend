from pymongo import MongoClient 
import os
from dotenv import load_dotenv

load_dotenv()

# ✅ Correct: Get the value of the environment variable named "MONGO_URI"
MONGO_URI = os.getenv("MONGO_URI")

# Optional: print to verify it loads correctly
print("Using Mongo URI:", MONGO_URI)

client = MongoClient(MONGO_URI)
db = client["carworkshop"]  # make sure this matches your DB name in Cosmos
collection = db["appointments"]
