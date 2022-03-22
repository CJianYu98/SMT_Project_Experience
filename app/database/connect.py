import os

from dotenv import load_dotenv
from pymongo import MongoClient

# Load environment variables
load_dotenv()

# Constant
DB_URL = os.getenv("DB_URL")
DB_TABLE_NAME = os.getenv("DB_TABLE_NAME")

client = MongoClient(DB_URL)
db = client[DB_TABLE_NAME]
