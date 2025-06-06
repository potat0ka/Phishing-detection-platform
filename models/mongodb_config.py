"""
MongoDB Configuration and Connection Management
Professional database setup with error handling and fallback options
"""

import os
import logging
from typing import Optional, Dict, Any
import json

# Try importing MongoDB with fallback for compatibility issues
try:
    from pymongo import MongoClient
    from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
    MONGODB_AVAILABLE = True
except ImportError as e:
    logging.warning(f"MongoDB not available: {e}")
    MONGODB_AVAILABLE = False
    # Mock classes for fallback
    class MongoClient:
        def __init__(self, *args, **kwargs):
            raise ConnectionFailure("MongoDB not available")
    
    class ConnectionFailure(Exception):
        pass
    
    class ServerSelectionTimeoutError(Exception):
        pass

logger = logging.getLogger(__name__)

class MongoDBManager:
    """
    Professional MongoDB connection manager with automatic fallback
    Handles connection pooling, error recovery, and data operations
    """
    
    def __init__(self):
        self.client: Optional[MongoClient] = None
        self.db = None
        self.connected = False
        self.collections = {}
        self.init_connection()
    
    def init_connection(self):
        """Initialize MongoDB connection with fallback to JSON storage"""
        if not MONGODB_AVAILABLE:
            logger.info("MongoDB libraries not available, using JSON file storage")
            self.connected = False
            self._setup_json_fallback()
            return
            
        try:
            # Try to connect to MongoDB Atlas using MONGO_URI secret
            mongodb_uri = os.environ.get('MONGO_URI') or os.environ.get('MONGODB_URI') or os.environ.get('DATABASE_URL')
            
            if mongodb_uri and 'mongodb' in mongodb_uri:
                self.client = MongoClient(
                    mongodb_uri,
                    serverSelectionTimeoutMS=30000,  # 30 second timeout
                    connectTimeoutMS=30000,
                    socketTimeoutMS=30000,
                    retryWrites=True,
                    w='majority'
                )
                
                # Test connection
                self.client.admin.command('ismaster')
                
                # Get database name from URI or use default
                db_name = mongodb_uri.split('/')[-1].split('?')[0] if '/' in mongodb_uri else 'phishing_detector'
                self.db = self.client[db_name]
                self.connected = True
                
                logger.info(f"Connected to MongoDB database: {db_name}")
                
                # Initialize collections
                self._setup_collections()
                
            else:
                raise ConnectionFailure("No MongoDB URI provided")
                
        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            logger.warning(f"MongoDB connection failed: {e}")
            logger.info("Falling back to JSON file storage")
            self.connected = False
            self._setup_json_fallback()
    
    def _setup_collections(self):
        """Set up MongoDB collections with proper indexing"""
        if not self.connected or not self.db:
            return
            
        try:
            # Users collection
            self.collections['users'] = self.db.users
            self.collections['users'].create_index('username', unique=True)
            self.collections['users'].create_index('email', unique=True)
            
            # Detections collection
            self.collections['detections'] = self.db.detections
            self.collections['detections'].create_index('user_id')
            self.collections['detections'].create_index('timestamp')
            
            # Security tips collection
            self.collections['security_tips'] = self.db.security_tips
            self.collections['security_tips'].create_index('category')
            
            # Analytics collection
            self.collections['analytics'] = self.db.analytics
            self.collections['analytics'].create_index('session_id')
            self.collections['analytics'].create_index('timestamp')
            
            logger.info("MongoDB collections initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to setup collections: {e}")
    
    def _setup_json_fallback(self):
        """Set up JSON file storage as fallback"""
        self.json_files = {
            'users': 'data/users.json',
            'detections': 'data/detections.json',
            'security_tips': 'data/security_tips.json',
            'analytics': 'data/analytics.json',
            'login_logs': 'data/login_logs.json',
            'phishing_reports': 'data/phishing_reports.json',
            'reported_content': 'data/reported_content.json',
            'ai_content_detections': 'data/ai_content_detections.json'
        }
        
        # Create data directory
        os.makedirs('data', exist_ok=True)
        
        # Initialize JSON files if they don't exist
        for collection, filepath in self.json_files.items():
            if not os.path.exists(filepath):
                with open(filepath, 'w') as f:
                    json.dump([], f)
        
        logger.info("JSON fallback storage initialized")
    
    def insert_one(self, collection_name: str, document: Dict[str, Any]) -> Optional[str]:
        """Insert a single document"""
        if self.connected and collection_name in self.collections:
            try:
                result = self.collections[collection_name].insert_one(document)
                return str(result.inserted_id)
            except Exception as e:
                logger.error(f"MongoDB insert failed: {e}")
                return self._json_insert_one(collection_name, document)
        else:
            return self._json_insert_one(collection_name, document)
    
    def find_one(self, collection_name: str, query: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Find a single document"""
        if self.connected and collection_name in self.collections:
            try:
                result = self.collections[collection_name].find_one(query)
                if result:
                    result['_id'] = str(result['_id'])
                return result
            except Exception as e:
                logger.error(f"MongoDB find failed: {e}")
                return self._json_find_one(collection_name, query)
        else:
            return self._json_find_one(collection_name, query)
    
    def find_many(self, collection_name: str, query: Dict[str, Any] = None, limit: int = None) -> list:
        """Find multiple documents"""
        if self.connected and collection_name in self.collections:
            try:
                cursor = self.collections[collection_name].find(query or {})
                if limit:
                    cursor = cursor.limit(limit)
                
                results = []
                for doc in cursor:
                    doc['_id'] = str(doc['_id'])
                    results.append(doc)
                return results
            except Exception as e:
                logger.error(f"MongoDB find_many failed: {e}")
                return self._json_find_many(collection_name, query, limit)
        else:
            return self._json_find_many(collection_name, query, limit)
    
    def update_one(self, collection_name: str, query: Dict[str, Any], update: Dict[str, Any]) -> bool:
        """Update a single document"""
        if self.connected and collection_name in self.collections:
            try:
                result = self.collections[collection_name].update_one(query, {'$set': update})
                return result.modified_count > 0
            except Exception as e:
                logger.error(f"MongoDB update failed: {e}")
                return self._json_update_one(collection_name, query, update)
        else:
            return self._json_update_one(collection_name, query, update)
    
    def delete_one(self, collection_name: str, query: Dict[str, Any]) -> bool:
        """Delete a single document"""
        if self.connected and collection_name in self.collections:
            try:
                result = self.collections[collection_name].delete_one(query)
                return result.deleted_count > 0
            except Exception as e:
                logger.error(f"MongoDB delete failed: {e}")
                return self._json_delete_one(collection_name, query)
        else:
            return self._json_delete_one(collection_name, query)
    
    def count_documents(self, collection_name: str, query: Dict[str, Any] = None) -> int:
        """Count documents matching query"""
        if self.connected and collection_name in self.collections:
            try:
                return self.collections[collection_name].count_documents(query or {})
            except Exception as e:
                logger.error(f"MongoDB count failed: {e}")
                return self._json_count_documents(collection_name, query)
        else:
            return self._json_count_documents(collection_name, query)
    
    # JSON fallback methods
    def _json_insert_one(self, collection_name: str, document: Dict[str, Any]) -> Optional[str]:
        """Insert document into JSON file"""
        filepath = self.json_files.get(collection_name)
        if not filepath:
            return None
            
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            
            # Generate unique ID
            document['_id'] = f"{collection_name}_{len(data) + 1}_{int(os.urandom(4).hex(), 16)}"
            data.append(document)
            
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2, default=str)
            
            return document['_id']
        except Exception as e:
            logger.error(f"JSON insert failed: {e}")
            return None
    
    def _json_find_one(self, collection_name: str, query: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Find document in JSON file"""
        filepath = self.json_files.get(collection_name)
        if not filepath or not os.path.exists(filepath):
            return None
            
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            
            for doc in data:
                if self._matches_query(doc, query):
                    return doc
            return None
        except Exception as e:
            logger.error(f"JSON find failed: {e}")
            return None
    
    def _json_find_many(self, collection_name: str, query: Dict[str, Any] = None, limit: int = None) -> list:
        """Find multiple documents in JSON file"""
        filepath = self.json_files.get(collection_name)
        if not filepath or not os.path.exists(filepath):
            return []
            
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            
            results = []
            for doc in data:
                if not query or self._matches_query(doc, query):
                    results.append(doc)
                    if limit and len(results) >= limit:
                        break
            return results
        except Exception as e:
            logger.error(f"JSON find_many failed: {e}")
            return []
    
    def _json_update_one(self, collection_name: str, query: Dict[str, Any], update: Dict[str, Any]) -> bool:
        """Update document in JSON file"""
        filepath = self.json_files.get(collection_name)
        if not filepath or not os.path.exists(filepath):
            return False
            
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            
            for doc in data:
                if self._matches_query(doc, query):
                    doc.update(update)
                    
                    with open(filepath, 'w') as f:
                        json.dump(data, f, indent=2, default=str)
                    return True
            return False
        except Exception as e:
            logger.error(f"JSON update failed: {e}")
            return False
    
    def _json_delete_one(self, collection_name: str, query: Dict[str, Any]) -> bool:
        """Delete document from JSON file"""
        filepath = self.json_files.get(collection_name)
        if not filepath or not os.path.exists(filepath):
            return False
            
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            
            for i, doc in enumerate(data):
                if self._matches_query(doc, query):
                    data.pop(i)
                    
                    with open(filepath, 'w') as f:
                        json.dump(data, f, indent=2, default=str)
                    return True
            return False
        except Exception as e:
            logger.error(f"JSON delete failed: {e}")
            return False
    
    def _json_count_documents(self, collection_name: str, query: Dict[str, Any] = None) -> int:
        """Count documents in JSON file"""
        filepath = self.json_files.get(collection_name)
        if not filepath or not os.path.exists(filepath):
            return 0
            
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            
            if not query:
                return len(data)
            
            count = 0
            for doc in data:
                if self._matches_query(doc, query):
                    count += 1
            return count
        except Exception as e:
            logger.error(f"JSON count failed: {e}")
            return 0
    
    def _matches_query(self, document: Dict[str, Any], query: Dict[str, Any]) -> bool:
        """Check if document matches query (simple implementation)"""
        for key, value in query.items():
            if key not in document or document[key] != value:
                return False
        return True
    
    def close(self):
        """Close database connection"""
        if self.connected and self.client:
            self.client.close()
            logger.info("MongoDB connection closed")

# Global database manager instance
db_manager = MongoDBManager()