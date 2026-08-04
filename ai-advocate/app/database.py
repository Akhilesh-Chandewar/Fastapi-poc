from pymongo import MongoClient
from app.config import MONGODB_URI

client = MongoClient(MONGODB_URI)
db = client["ai-advocate"]

contracts_collection = db["contracts"]
analysis_collection = db["analysis"]

def init_db():
    contracts_collection.create_index("contract_id", unique=True)
    analysis_collection.create_index("contract_id", unique=True)

