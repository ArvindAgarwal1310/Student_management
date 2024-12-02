from pymongo import MongoClient
from pymongo.server_api import ServerApi
import os
import dotenv

dotenv.load_dotenv()


class Database_ops:
    def __init__(self):
        # MongoDB connection URL
        MONGO_URI = os.getenv("MONGO_URI")
        # Initialize MongoDB client
        client = MongoClient(MONGO_URI, server_api=ServerApi("1"))
        print("Client", client)
        # Access the database
        self.db = client["students"]
        print("db", self.db)
        # Access the collection
        students_collection = self.db["Students_data"]

        self.students_collection = students_collection
