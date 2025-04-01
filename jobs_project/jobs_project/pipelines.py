import logging
import hashlib
import json
from pymongo.errors import DuplicateKeyError
from datetime import datetime

from infra.mongodb_connector import MongoDBConnector
from infra.redis_connector import RedisConnector

class MongoDBPipeline:
    collection_name = 'jobs'
    
    def __init__(self):
        self.mongo_connector = None
    
    def open_spider(self, spider):
        self.mongo_connector = MongoDBConnector()
        if not self.mongo_connector.connect():
            raise Exception("Failed to connect to MongoDB")
    
    def close_spider(self, spider):
        if self.mongo_connector:
            self.mongo_connector.close()
    
    def process_item(self, item, spider):
        job_dict = dict(item)
        
        # Add processing timestamp
        job_dict['processed_at'] = datetime.now().isoformat()
        
        # Insert into MongoDB, using job_id as a unique identifier
        try:
            # Deduplication with job_id (req_id in json file)
            unique_fields = ['job_id']
            
            # Insert the document
            inserted_id = self.mongo_connector.insert_one(
                self.collection_name, 
                job_dict,
                unique_fields
            )
            
            if inserted_id:
                spider.logger.info(f"Job inserted into MongoDB: {job_dict['job_id']}")
            else:
                spider.logger.info(f"Job already exists in MongoDB: {job_dict['job_id']}")
                
        except Exception as e:
            spider.logger.error(f"Error inserting job into MongoDB: {str(e)}")
        
        return item


class RedisPipeline:
    def __init__(self):
        self.redis_connector = None
    
    def open_spider(self, spider):
        try:
            self.redis_connector = RedisConnector()
            if not self.redis_connector.connect():
                spider.logger.warning("Failed to connect to Redis, continuing without caching")
                self.redis_connector = None
        except Exception as e:
            spider.logger.warning(f"Redis initialization error: {str(e)}")
            self.redis_connector = None
    
    def close_spider(self, spider):
        if self.redis_connector:
            self.redis_connector.close()
    
    def process_item(self, item, spider):
        if not self.redis_connector:
            return item
            
        try:
            # Generate a cache key based on job_id
            job_id = item.get('job_id', '')
            if not job_id:
                return item
                
            cache_key = f"job:{job_id}"
            
            # Check if this job has been processed before
            if self.redis_connector.item_exists(cache_key):
                spider.logger.info(f"Job already processed (Redis cache): {job_id}")
            else:
                # Cache this job for future reference
                self.redis_connector.cache_item(cache_key, {'processed': True}, expire=86400)  # 24 hours
                spider.logger.info(f"Job added to Redis cache: {job_id}")
                
        except Exception as e:
            spider.logger.error(f"Redis error: {str(e)}")
            
        return item