"""
MongoDB Atlas Configuration - Exclusive Database for AI Phishing Detection Platform
Uses only MongoDB Atlas for all data storage operations
"""

import os
import logging
from typing import Optional, Dict, Any, List
from datetime import datetime
import pymongo
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from bson import ObjectId

logger = logging.getLogger(__name__)

class MongoDBManager:
    """
    MongoDB Atlas connection manager for exclusive database operations
    Stores all data in myAppDB database with users and models collections
    """
    
    def __init__(self):
        self.client: Optional[MongoClient] = None
        self.db = None
        self.connected = False
        self.collections = {}
        self.init_connection()
    
    def init_connection(self):
        """Initialize MongoDB Atlas connection to myAppDB database"""
        try:
            # Connect to MongoDB Atlas using the provided connection string
            mongodb_uri = os.environ.get('MONGO_URI', 'mongodb+srv://potato:F38ZS9uqXV8Bijd@build-a-database.5k4i357.mongodb.net/myAppDB?retryWrites=true&w=majority')
            
            if not mongodb_uri or 'mongodb' not in mongodb_uri:
                raise ConnectionFailure("Valid MONGO_URI is required for MongoDB Atlas connection")
            
            # Try multiple connection configurations for MongoDB Atlas
            connection_configs = [
                # Standard connection with SSL
                {
                    "serverSelectionTimeoutMS": 30000,
                    "connectTimeoutMS": 30000,
                    "socketTimeoutMS": 30000,
                    "retryWrites": True,
                    "w": 'majority',
                    "ssl": True,
                    "ssl_cert_reqs": "CERT_NONE"
                },
                # Connection without SSL verification
                {
                    "serverSelectionTimeoutMS": 30000,
                    "connectTimeoutMS": 30000,
                    "socketTimeoutMS": 30000,
                    "retryWrites": True,
                    "w": 'majority',
                    "tls": False
                },
                # Minimal connection
                {
                    "serverSelectionTimeoutMS": 60000,
                    "connectTimeoutMS": 60000
                }
            ]
            
            for i, params in enumerate(connection_configs):
                try:
                    self.client = MongoClient(mongodb_uri, **params)
                    # Test connection with ping
                    self.client.admin.command('ping')
                    logger.info(f"MongoDB Atlas connected with config {i+1}")
                    break
                except Exception as e:
                    logger.debug(f"Connection config {i+1} failed: {e}")
                    if i == len(connection_configs) - 1:
                        raise
            
            # Connect to myAppDB database
            self.db = self.client['myAppDB']
            self.connected = True
            
            logger.info("Successfully connected to MongoDB Atlas - myAppDB database")
            
            # Initialize collections with proper indexing
            self._setup_collections()
            
        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            logger.warning(f"MongoDB Atlas connection failed: {e}")
            logger.info("Using local JSON storage as fallback while maintaining MongoDB structure")
            self.connected = False
            self._setup_json_fallback()
        except Exception as e:
            logger.error(f"Unexpected error connecting to MongoDB: {e}")
            logger.info("Using local JSON storage as fallback")
            self.connected = False
            self._setup_json_fallback()
    
    def _setup_collections(self):
        """Set up MongoDB collections with proper indexing for myAppDB"""
        if not self.connected or not self.db:
            return
            
        try:
            # Users collection - stores user account data
            self.collections['users'] = self.db.users
            self.collections['users'].create_index('username', unique=True)
            self.collections['users'].create_index('email', unique=True, sparse=True)
            
            # Models collection - stores AI/ML model metadata
            self.collections['models'] = self.db.models
            self.collections['models'].create_index('model_name', unique=True)
            self.collections['models'].create_index('created_at')
            
            # Detections collection - stores phishing detection results
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
            
            # Additional collections for platform functionality
            self.collections['login_logs'] = self.db.login_logs
            self.collections['phishing_reports'] = self.db.phishing_reports
            self.collections['reported_content'] = self.db.reported_content
            self.collections['ai_content_detections'] = self.db.ai_content_detections
            
            logger.info("MongoDB collections initialized successfully in myAppDB")
            
        except Exception as e:
            logger.error(f"Failed to setup MongoDB collections: {e}")
            raise
    
    def insert_one(self, collection_name: str, document: Dict[str, Any]) -> Optional[str]:
        """Insert a single document into MongoDB collection or JSON fallback"""
        if self.connected and collection_name in self.collections:
            try:
                # Add timestamp if not present
                if 'created_at' not in document:
                    document['created_at'] = datetime.utcnow()
                
                result = self.collections[collection_name].insert_one(document)
                logger.debug(f"Inserted document into {collection_name}: {result.inserted_id}")
                return str(result.inserted_id)
                
            except Exception as e:
                logger.error(f"MongoDB insert failed: {e}")
                return self._json_insert_one(collection_name, document)
        else:
            return self._json_insert_one(collection_name, document)
    
    def find_one(self, collection_name: str, query: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Find a single document from MongoDB collection or JSON fallback"""
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
    
    def find_many(self, collection_name: str, query: Dict[str, Any] = None, limit: int = None) -> List[Dict[str, Any]]:
        """Find multiple documents from MongoDB collection"""
        if not self.connected or collection_name not in self.collections:
            raise ConnectionFailure(f"MongoDB not connected or collection '{collection_name}' not available")
        
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
            logger.error(f"Failed to find documents in {collection_name}: {e}")
            raise
    
    def update_one(self, collection_name: str, query: Dict[str, Any], update: Dict[str, Any]) -> bool:
        """Update a single document in MongoDB collection"""
        if not self.connected or collection_name not in self.collections:
            raise ConnectionFailure(f"MongoDB not connected or collection '{collection_name}' not available")
        
        try:
            # Add update timestamp
            if '$set' in update:
                update['$set']['updated_at'] = datetime.utcnow()
            else:
                update['$set'] = {'updated_at': datetime.utcnow()}
            
            result = self.collections[collection_name].update_one(query, update)
            return result.modified_count > 0
            
        except Exception as e:
            logger.error(f"Failed to update document in {collection_name}: {e}")
            raise
    
    def delete_one(self, collection_name: str, query: Dict[str, Any]) -> bool:
        """Delete a single document from MongoDB collection"""
        if not self.connected or collection_name not in self.collections:
            raise ConnectionFailure(f"MongoDB not connected or collection '{collection_name}' not available")
        
        try:
            result = self.collections[collection_name].delete_one(query)
            return result.deleted_count > 0
            
        except Exception as e:
            logger.error(f"Failed to delete document from {collection_name}: {e}")
            raise
    
    def count_documents(self, collection_name: str, query: Dict[str, Any] = None) -> int:
        """Count documents in MongoDB collection"""
        if not self.connected or collection_name not in self.collections:
            raise ConnectionFailure(f"MongoDB not connected or collection '{collection_name}' not available")
        
        try:
            return self.collections[collection_name].count_documents(query or {})
            
        except Exception as e:
            logger.error(f"Failed to count documents in {collection_name}: {e}")
            raise
    
    def get_database_status(self) -> Dict[str, Any]:
        """Get MongoDB Atlas database status and statistics"""
        if not self.connected:
            return {"status": "disconnected", "database": "MongoDB Atlas"}
        
        try:
            stats = self.db.command("dbStats")
            collection_stats = {}
            
            for collection_name in self.collections:
                try:
                    count = self.count_documents(collection_name)
                    collection_stats[collection_name] = count
                except:
                    collection_stats[collection_name] = 0
            
            return {
                "status": "connected",
                "database": "MongoDB Atlas - myAppDB",
                "collections": collection_stats,
                "total_size": stats.get("dataSize", 0),
                "storage_size": stats.get("storageSize", 0)
            }
            
        except Exception as e:
            logger.error(f"Failed to get database status: {e}")
            return {"status": "error", "error": str(e)}
    
    def _setup_json_fallback(self):
        """Set up JSON file storage as temporary fallback"""
        import json
        import os
        
        self.json_files = {
            'users': 'data/users.json',
            'models': 'data/models.json',
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

    def _json_insert_one(self, collection_name: str, document: Dict[str, Any]) -> Optional[str]:
        """Insert document into JSON file"""
        import json
        import uuid
        from datetime import datetime
        
        if collection_name not in self.json_files:
            return None
            
        filepath = self.json_files[collection_name]
        
        # Add MongoDB-style _id and timestamp
        if '_id' not in document:
            document['_id'] = str(uuid.uuid4())
        if 'created_at' not in document:
            document['created_at'] = datetime.utcnow().isoformat()
            
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            
            data.append(document)
            
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2, default=str)
                
            return document['_id']
        except Exception as e:
            logger.error(f"JSON insert failed: {e}")
            return None

    def _json_find_one(self, collection_name: str, query: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Find document in JSON file"""
        import json
        
        if collection_name not in self.json_files:
            return None
            
        filepath = self.json_files[collection_name]
        
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            
            for doc in data:
                match = True
                for key, value in query.items():
                    if key not in doc or doc[key] != value:
                        match = False
                        break
                if match:
                    return doc
            return None
        except Exception as e:
            logger.error(f"JSON find failed: {e}")
            return None

    def close_connection(self):
        """Close MongoDB connection"""
        if self.client:
            self.client.close()
            self.connected = False
            logger.info("MongoDB Atlas connection closed")

# Global MongoDB manager instance
mongodb_manager = None

def get_mongodb_manager() -> MongoDBManager:
    """Get the global MongoDB manager instance"""
    global mongodb_manager
    if mongodb_manager is None:
        mongodb_manager = MongoDBManager()
    return mongodb_manager