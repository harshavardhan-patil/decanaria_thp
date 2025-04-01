import redis
import os
import logging
import json

class RedisConnector:
    def __init__(self, url=None):
        self.url = url or os.getenv('REDIS_URL', 'redis://localhost:6379/0')
        self.client = None
        
    def connect(self):
        try:
            self.client = redis.from_url(self.url)
            # Check if connection is successful
            self.client.ping()
            logging.info(f"Connected to Redis at {self.url}")
            return True
        except redis.ConnectionError as e:
            logging.error(f"Could not connect to Redis: {e}")
            return False
            
    def cache_item(self, key, item, expire=3600):
        """
        Cache an item with an optional expiration time (in seconds)
        """
        if not self.client:
            return False
            
        try:
            self.client.setex(key, expire, json.dumps(item))
            return True
        except Exception as e:
            logging.error(f"Error caching item: {e}")
            return False
            
    def get_cached_item(self, key):
        """
        Retrieve a cached item by key
        """
        if not self.client:
            return None
            
        try:
            data = self.client.get(key)
            if data:
                return json.loads(data)
            return None
        except Exception as e:
            logging.error(f"Error retrieving cached item: {e}")
            return None
            
    def item_exists(self, key):
        """
        Check if an item exists in the cache
        """
        if not self.client:
            return False
            
        return bool(self.client.exists(key))
        
    def close(self):
        if self.client:
            self.client.close()
            logging.info("Closed Redis connection")