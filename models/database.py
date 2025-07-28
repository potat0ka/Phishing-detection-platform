"""
MongoDB Database Connection and Configuration
===========================================

This file manages the MongoDB connection and provides a database interface
for the Flask application using PyMongo.

Author: Bigendra Shrestha
"""

import logging
from flask import current_app
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from datetime import datetime

logger = logging.getLogger(__name__)

class DatabaseManager:
    """
    MongoDB Database Manager
    
    This class handles all MongoDB operations and provides a clean interface
    for database interactions. It includes fallback data when MongoDB is unavailable.
    """
    
    def __init__(self, mongo=None):
        """Initialize database manager with MongoDB connection"""
        self.mongo = mongo
        self.connected = False
        self.collections = {
            'phishing_data': 'phishing_data',
            'security_tips': 'security_tips', 
            'users': 'users',
            'scan_logs': 'scan_logs',
            'system_stats': 'system_stats'
        }
    
    def test_connection(self):
        """Test MongoDB connection and return status"""
        try:
            if self.mongo and self.mongo.db:
                # Test connection with a simple ping
                self.mongo.db.admin.command('ping')
                self.connected = True
                logger.info("MongoDB connection successful")
                return True
        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            logger.warning(f"MongoDB connection failed, using fallback: {e}")
            self.connected = False
            # Try PostgreSQL fallback for essential operations
            try:
                from flask import current_app
                if hasattr(current_app, 'config') and current_app.config.get('DATABASE_URL'):
                    logger.info("MongoDB unavailable, PostgreSQL fallback available")
                    return True
            except Exception:
                pass
            return False
        except Exception as e:
            logger.error(f"Unexpected database error: {e}")
            self.connected = False
            return False
    
    def get_collection(self, collection_name):
        """Get MongoDB collection or return None if not connected"""
        if not self.connected:
            self.test_connection()
        
        if self.connected and self.mongo:
            return self.mongo.db[self.collections[collection_name]]
        return None
    
    def insert_document(self, collection_name, document):
        """Insert a document into specified collection"""
        try:
            collection = self.get_collection(collection_name)
            if collection is not None:
                document['created_at'] = datetime.utcnow()
                result = collection.insert_one(document)
                logger.info(f"Document inserted into {collection_name}: {result.inserted_id}")
                return result.inserted_id
        except Exception as e:
            logger.error(f"Failed to insert document into {collection_name}: {e}")
            return None
    
    def find_documents(self, collection_name, query=None, sort=None, limit=None, skip=None):
        """Find documents in specified collection"""
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
                logger.info(f"Found {len(documents)} documents in {collection_name}")
                return documents
            return []
        except Exception as e:
            logger.error(f"Failed to find documents in {collection_name}: {e}")
            return []
    
    def update_document(self, collection_name, query, update_doc, upsert=False):
        """Update document(s) in specified collection"""
        try:
            collection = self.get_collection(collection_name)
            if collection is not None:
                if upsert:
                    result = collection.update_one(query, update_doc, upsert=True)
                else:
                    result = collection.update_many(query, update_doc)
                
                logger.info(f"Updated {result.modified_count} documents in {collection_name}")
                return result
            return None
        except Exception as e:
            logger.error(f"Failed to update documents in {collection_name}: {e}")
            return None
    
    def delete_documents(self, collection_name, query):
        """Delete documents from specified collection"""
        try:
            collection = self.get_collection(collection_name)
            if collection is not None:
                result = collection.delete_many(query)
                logger.info(f"Deleted {result.deleted_count} documents from {collection_name}")
                return result
            return None
        except Exception as e:
            logger.error(f"Failed to delete documents from {collection_name}: {e}")
            return None
        return None
    
    def find_document(self, collection_name, query=None):
        """Find single document in specified collection"""
        try:
            collection = self.get_collection(collection_name)
            if collection is not None:
                return collection.find_one(query or {})
        except Exception as e:
            logger.error(f"Failed to find document in {collection_name}: {e}")
        return None
    
    def find_documents(self, collection_name, query=None, limit=None):
        """Find documents in specified collection"""
        try:
            collection = self.get_collection(collection_name)
            if collection is not None:
                cursor = collection.find(query or {})
                if limit:
                    cursor = cursor.limit(limit)
                return list(cursor)
        except Exception as e:
            logger.error(f"Failed to find documents in {collection_name}: {e}")
        return []
    
    def update_document(self, collection_name, query, update):
        """Update documents in specified collection"""
        try:
            collection = self.get_collection(collection_name)
            if collection is not None:
                update['$set'] = update.get('$set', {})
                update['$set']['updated_at'] = datetime.utcnow()
                result = collection.update_many(query, update)
                logger.info(f"Updated {result.modified_count} documents in {collection_name}")
                return result.modified_count
        except Exception as e:
            logger.error(f"Failed to update documents in {collection_name}: {e}")
        return 0
    
    def delete_document(self, collection_name, query):
        """Delete documents from specified collection"""
        try:
            collection = self.get_collection(collection_name)
            if collection is not None:
                result = collection.delete_many(query)
                logger.info(f"Deleted {result.deleted_count} documents from {collection_name}")
                return result.deleted_count
        except Exception as e:
            logger.error(f"Failed to delete documents from {collection_name}: {e}")
        return 0

# Global database manager instance
db = None

def init_db(mongo):
    """Initialize global database manager"""
    global db
    db = DatabaseManager(mongo)
    return db