from pymongo import MongoClient
from config import Config

client = MongoClient(Config.MONGO_URI)
db = client['truth_dare_db']
truths_collection = db['truths']
dares_collection = db['dares']
