"""
MongoDB Connection Manager
=========================

Professional MongoDB connection with proper error handling and configuration.
"""

import os
import logging
from typing import Optional
from pymongo import MongoClient
from pymongo.database import Database

logger = logging.getLogger(__name__)

# Global connection instance
_client: Optional[MongoClient] = None
_database: Optional[Database] = None


def get_mongo_uri() -> str:
    """Get MongoDB connection URI from environment or use default"""
    return os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')


def get_database_name() -> str:
    """Get database name from environment or use default"""
    return os.getenv('DB_NAME', 'phishing_detector')


def connect_to_database() -> Database:
    """Establish connection to MongoDB"""
    global _client, _database
    
    if _database is not None:
        return _database
    
    try:
        mongo_uri = get_mongo_uri()
        db_name = get_database_name()
        
        _client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
        
        # Test connection
        _client.admin.command('ping')
        
        _database = _client[db_name]
        
        # Create indexes for better performance
        _create_indexes()
        
        logger.info(f"Connected to MongoDB database: {db_name}")
        return _database
        
    except Exception as e:
        logger.error(f"Failed to connect to MongoDB: {e}")
        raise ConnectionError(f"Database connection failed: {e}")


def _create_indexes():
    """Create database indexes for optimal performance"""
    try:
        if _database is None:
            return
        
        # Users collection indexes
        _database.users.create_index("username", unique=True, sparse=True)
        _database.users.create_index("email", unique=True, sparse=True)
        _database.users.create_index("created_at")
        
        # Detections collection indexes
        _database.detections.create_index("user_id")
        _database.detections.create_index("created_at")
        _database.detections.create_index([("user_id", 1), ("created_at", -1)])
        
        # Security tips collection indexes
        _database.security_tips.create_index("category")
        _database.security_tips.create_index("priority")
        
        logger.info("Database indexes created successfully")
        
    except Exception as e:
        logger.warning(f"Error creating indexes: {e}")


def get_database() -> Database:
    """Get database instance, connecting if necessary"""
    if _database is None:
        return connect_to_database()
    return _database


def close_connection():
    """Close database connection"""
    global _client, _database
    
    if _client:
        _client.close()
        _client = None
        _database = None
        logger.info("Database connection closed")


def health_check() -> bool:
    """Check database connection health"""
    try:
        db = get_database()
        db.admin.command('ping')
        return True
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        return False