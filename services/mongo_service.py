"""
MongoDB Service - Centralized Database Operations
================================================

Unified MongoDB connection and operations for the AI Phishing Detection Platform.
This service handles all database operations with proper error handling and fallbacks.

Author: Bigendra Shrestha
"""

import os
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError

logger = logging.getLogger(__name__)

class MongoService:
    """Centralized MongoDB service for the platform"""
    
    def __init__(self):
        self.client: Optional[MongoClient] = None
        self.db: Optional[Database] = None
        self.connected = False
        self.collections = {
            'users': 'users',
            'scan_history': 'scan_history',
            'phishing_data': 'phishing_data',
            'safety_tips': 'safety_tips',
            'system_stats': 'system_stats',
            'admin_logs': 'admin_logs',
            'password_resets': 'password_resets'
        }
        self._connect()
    
    def _connect(self) -> bool:
        """Establish MongoDB connection with comprehensive error handling"""
        try:
            # Get MongoDB URI from environment variables
            mongo_uri = os.getenv("MONGO_URI") or os.getenv("MONGODB_URI")
            
            if not mongo_uri:
                logger.error("No MongoDB URI found in environment variables")
                return False
            
            # Connect to MongoDB with optimized settings
            self.client = MongoClient(
                mongo_uri,
                serverSelectionTimeoutMS=10000,
                tlsAllowInvalidCertificates=True,
                retryWrites=True,
                maxPoolSize=50,
                minPoolSize=5
            )
            
            # Test connection with ping
            self.client.admin.command('ping')
            self.db = self.client['phishing_detector']
            self.connected = True
            
            logger.info("MongoDB connected successfully")
            return True
            
        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            logger.error(f"MongoDB connection failed: {e}")
            self.connected = False
            return False
        except Exception as e:
            logger.error(f"Unexpected MongoDB error: {e}")
            self.connected = False
            return False
    
    def get_collection(self, collection_name: str) -> Optional[Collection]:
        """Get a MongoDB collection with automatic reconnection"""
        if not self.connected:
            self._connect()
        
        if self.connected and self.db is not None:
            return self.db[collection_name]
        return None
    
    def is_connected(self) -> bool:
        """Check if MongoDB is connected"""
        return self.connected and self.client is not None
    
    # CRUD Operations
    def insert_document(self, collection_name: str, document: Dict[str, Any]) -> Optional[str]:
        """Insert a document into specified collection"""
        try:
            collection = self.get_collection(collection_name)
            if collection is not None:
                document['created_at'] = datetime.utcnow()
                result = collection.insert_one(document)
                logger.info(f"Document inserted into {collection_name}: {result.inserted_id}")
                return str(result.inserted_id)
        except Exception as e:
            logger.error(f"Failed to insert document into {collection_name}: {e}")
            return None
    
    def find_document(self, collection_name: str, query: Dict[str, Any] = None) -> Optional[Dict[str, Any]]:
        """Find single document in specified collection"""
        try:
            collection = self.get_collection(collection_name)
            if collection is not None:
                return collection.find_one(query or {})
        except Exception as e:
            logger.error(f"Failed to find document in {collection_name}: {e}")
        return None
    
    def find_documents(self, collection_name: str, query: Dict[str, Any] = None, 
                      sort: List = None, limit: int = None, skip: int = None) -> List[Dict[str, Any]]:
        """Find documents in specified collection with advanced options"""
        try:
            collection = self.get_collection(collection_name)
            if collection is not None:
                cursor = collection.find(query or {})
                
                if sort:
                    cursor = cursor.sort(sort)
                if skip:
                    cursor = cursor.skip(skip)
                if limit:
                    cursor = cursor.limit(limit)
                
                documents = list(cursor)
                logger.debug(f"Found {len(documents)} documents in {collection_name}")
                return documents
            return []
        except Exception as e:
            logger.error(f"Failed to find documents in {collection_name}: {e}")
            return []
    
    def update_document(self, collection_name: str, query: Dict[str, Any], 
                       update_doc: Dict[str, Any], upsert: bool = False) -> int:
        """Update document(s) in specified collection"""
        try:
            collection = self.get_collection(collection_name)
            if collection is not None:
                # Add update timestamp
                if '$set' not in update_doc:
                    update_doc = {'$set': update_doc}
                update_doc['$set']['updated_at'] = datetime.utcnow()
                
                if upsert:
                    result = collection.update_one(query, update_doc, upsert=True)
                    return 1 if result.upserted_id else result.modified_count
                else:
                    result = collection.update_many(query, update_doc)
                    return result.modified_count
            return 0
        except Exception as e:
            logger.error(f"Failed to update documents in {collection_name}: {e}")
            return 0
    
    def delete_documents(self, collection_name: str, query: Dict[str, Any]) -> int:
        """Delete documents from specified collection"""
        try:
            collection = self.get_collection(collection_name)
            if collection is not None:
                result = collection.delete_many(query)
                logger.info(f"Deleted {result.deleted_count} documents from {collection_name}")
                return result.deleted_count
            return 0
        except Exception as e:
            logger.error(f"Failed to delete documents from {collection_name}: {e}")
            return 0
    
    def count_documents(self, collection_name: str, query: Dict[str, Any] = None) -> int:
        """Count documents in specified collection"""
        try:
            collection = self.get_collection(collection_name)
            if collection is not None:
                return collection.count_documents(query or {})
            return 0
        except Exception as e:
            logger.error(f"Failed to count documents in {collection_name}: {e}")
            return 0
    
    def close(self):
        """Close MongoDB connection"""
        if self.client:
            self.client.close()
            self.connected = False
            logger.info("MongoDB connection closed")

# Global MongoDB service instance
mongo_service = MongoService()

# Global instance
mongo_service = MongoService()

def get_mongo_collection(collection_name: str) -> Optional[Collection]:
    """Get a MongoDB collection (convenience function)"""
    return mongo_service.get_collection(collection_name)

def is_mongo_connected() -> bool:
    """Check MongoDB connection status (convenience function)"""
    return mongo_service.is_connected()

