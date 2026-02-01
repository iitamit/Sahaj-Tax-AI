# database.py
import pymongo
from datetime import datetime
import streamlit as st

# --- CONNECTION SETTINGS ---
# This connects to the MongoDB running on your laptop
DB_URI = "mongodb://localhost:27017/"
DB_NAME = "sahaj_tax_db"
COLLECTION_NAME = "user_records"

def get_connection():
    """Establishes connection to MongoDB"""
    try:
        client = pymongo.MongoClient(DB_URI, serverSelectionTimeoutMS=2000)
        # Check if server is available
        client.server_info()
        db = client[DB_NAME]
        return db[COLLECTION_NAME]
    except Exception:
        return None

def save_tax_record(data):
    """Saves a user's tax calculation to the DB"""
    collection = get_connection()
    if collection is not None:
        # Add a timestamp
        data["created_at"] = datetime.now()
        collection.insert_one(data)
        return True
    return False

def get_all_records():
    """Fetches all history for the Dashboard"""
    collection = get_connection()
    if collection is not None:
        # Get records, hide the internal MongoDB '_id', and sort by newest first
        records = list(collection.find({}, {"_id": 0}).sort("created_at", -1))
        return records
    return []