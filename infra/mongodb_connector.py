from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, DuplicateKeyError
import os
import logging

class MongoDBConnector:
    def __init__(self, uri=None, db_name=None):
        self.uri = uri or os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
        self.db_name = db_name or os.getenv('MONGO_DATABASE', 'jobs_db')
        self.client = None
        self.db = None
        
    def connect(self):
        try:
            self.client = MongoClient(self.uri)
            # Check if connection is successful
            self.client.admin.command('ping')
            self.db = self.client[self.db_name]
            logging.info(f"Connected to MongoDB at {self.uri}")
            return True
        except ConnectionFailure as e:
            logging.error(f"Could not connect to MongoDB: {e}")
            return False
            
    def insert_one(self, collection_name, document, unique_fields=None):
        """
        Insert a single document into a collection with optional duplicate checking
        """
        collection = self.db[collection_name]
        
        # Check for duplicates if unique_fields is provided
        if unique_fields:
            query = {field: document[field] for field in unique_fields if field in document}
            if query and collection.find_one(query):
                logging.info(f"Duplicate document found: {query}")
                return None
        
        try:
            result = collection.insert_one(document)
            return result.inserted_id
        except DuplicateKeyError:
            logging.warning(f"Duplicate key error when inserting document")
            return None
            
    def find_all(self, collection_name, query=None, projection=None):
        """
        Find all documents in a collection that match the query
        """
        collection = self.db[collection_name]
        return list(collection.find(query or {}, projection))
        
    def close(self):
        if self.client:
            self.client.close()
            logging.info("Closed MongoDB connection")