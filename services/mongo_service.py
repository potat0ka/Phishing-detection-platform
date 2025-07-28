"""
MongoDB Service
==============

Centralized MongoDB connection and operations for the AI Phishing Detection Platform.
"""

import os
import logging
import bcrypt
from datetime import datetime
from typing import Dict, List, Optional, Any
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database

logger = logging.getLogger(__name__)

class MongoService:
    """Centralized MongoDB service for the platform"""
    
    def __init__(self):
        self.client: Optional[MongoClient] = None
        self.db: Optional[Database] = None
        self.connected = False
        self._connect()
    
    def _connect(self) -> bool:
        """Establish MongoDB connection"""
        try:
            # Get MongoDB URI from environment
            mongo_uri = os.getenv("MONGO_URI") or os.getenv("MONGODB_URI")
            
            if not mongo_uri:
                logger.error("No MongoDB URI found in environment variables")
                return False
            
            # Connect to MongoDB
            self.client = MongoClient(
                mongo_uri,
                serverSelectionTimeoutMS=10000,
                tlsAllowInvalidCertificates=True,
                retryWrites=True
            )
            
            # Test connection
            self.client.admin.command('ping')
            self.db = self.client['phishing_detector']
            self.connected = True
            
            logger.info("MongoDB connected successfully")
            return True
            
        except Exception as e:
            logger.error(f"MongoDB connection failed: {e}")
            self.connected = False
            return False
    
    def get_collection(self, collection_name: str) -> Optional[Collection]:
        """Get a MongoDB collection"""
        if not self.connected or self.db is None:
            return None
        return self.db[collection_name]
    
    def is_connected(self) -> bool:
        """Check if MongoDB is connected"""
        return self.connected and self.client is not None
    
    def close(self):
        """Close MongoDB connection"""
        if self.client:
            self.client.close()
            self.connected = False
            logger.info("MongoDB connection closed")

# Global instance
mongo_service = MongoService()

def get_mongo_collection(collection_name: str) -> Optional[Collection]:
    """Get a MongoDB collection (convenience function)"""
    return mongo_service.get_collection(collection_name)

def is_mongo_connected() -> bool:
    """Check MongoDB connection status (convenience function)"""
    return mongo_service.is_connected()

def hash_password(password: str) -> str:
    """Hash password using bcrypt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password: str, hashed_password: str) -> bool:
    """Verify password against bcrypt hash"""
    try:
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
    except Exception as e:
        logger.error(f"Password verification error: {e}")
        return False