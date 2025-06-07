"""
MongoDB Atlas Configuration for AI Phishing Detection Platform
Uses MongoDB Atlas as primary database with intelligent fallback
"""

import os
import logging
import json
import uuid
from typing import Optional, Dict, Any, List
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)

# Try importing MongoDB
try:
    import pymongo
    from pymongo import MongoClient
    from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
    MONGODB_AVAILABLE = True
except ImportError:
    MONGODB_AVAILABLE = False
    logger.warning("PyMongo not available - using local storage")

class MongoDBManager:
    """
    MongoDB Atlas manager with intelligent fallback to local storage
    Maintains consistent API regardless of connection status
    """
    
    def __init__(self):
        self.client = None
        self.db = None
        self.connected = False
        self.collections = {}
        self.json_files = {}
        self.init_connection()
    
    def init_connection(self):
        """Initialize MongoDB Atlas connection with fallback"""
        if not MONGODB_AVAILABLE:
            logger.info("MongoDB libraries not available - using local storage")
            self._setup_local_storage()
            return
        
        # MongoDB Atlas connection string
        mongodb_uri = os.environ.get('MONGO_URI', 
            'mongodb+srv://potato:F38ZS9uqXV8Bijd@build-a-database.5k4i357.mongodb.net/myAppDB?retryWrites=true&w=majority')
        
        if mongodb_uri and 'mongodb' in mongodb_uri:
            try:
                # Try connecting with optimized settings
                self.client = MongoClient(
                    mongodb_uri,
                    serverSelectionTimeoutMS=5000,
                    connectTimeoutMS=5000,
                    socketTimeoutMS=5000,
                    retryWrites=True
                )
                
                # Test connection
                self.client.admin.command('ping')
                self.db = self.client['myAppDB']
                self.connected = True
                self._setup_collections()
                logger.info("Connected to MongoDB Atlas - myAppDB database")
                return
                
            except Exception as e:
                logger.warning(f"MongoDB Atlas connection failed: {e}")
        
        # Fallback to local storage
        logger.info("Using local storage with MongoDB structure")
        self._setup_local_storage()
    
    def _setup_collections(self):
        """Setup MongoDB collections with indexes"""
        if not self.connected or not self.db:
            return
        
        try:
            # Users collection
            self.collections['users'] = self.db.users
            self.collections['users'].create_index('username', unique=True)
            self.collections['users'].create_index('email', unique=True, sparse=True)
            
            # Models collection for AI/ML metadata
            self.collections['models'] = self.db.models
            self.collections['models'].create_index('model_name', unique=True)
            self.collections['models'].create_index('created_at')
            
            # Additional collections
            self.collections['detections'] = self.db.detections
            self.collections['security_tips'] = self.db.security_tips
            self.collections['analytics'] = self.db.analytics
            self.collections['login_logs'] = self.db.login_logs
            self.collections['phishing_reports'] = self.db.phishing_reports
            self.collections['reported_content'] = self.db.reported_content
            self.collections['ai_content_detections'] = self.db.ai_content_detections
            
            logger.info("MongoDB collections initialized")
            
        except Exception as e:
            logger.error(f"Failed to setup collections: {e}")
    
    def _setup_local_storage(self):
        """Setup local JSON storage maintaining MongoDB structure"""
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
        Path('data').mkdir(exist_ok=True)
        
        # Initialize JSON files
        for collection, filepath in self.json_files.items():
            if not Path(filepath).exists():
                with open(filepath, 'w') as f:
                    json.dump([], f)
        
        logger.info("Local storage initialized with MongoDB structure")
    
    def insert_one(self, collection_name: str, document: Dict[str, Any]) -> Optional[str]:
        """Insert document into MongoDB or local storage"""
        # Add timestamp if not present
        if 'created_at' not in document:
            document['created_at'] = datetime.utcnow()
        
        if self.connected and collection_name in self.collections:
            try:
                result = self.collections[collection_name].insert_one(document)
                return str(result.inserted_id)
            except Exception as e:
                logger.error(f"MongoDB insert failed: {e}")
        
        # Local storage fallback
        return self._local_insert_one(collection_name, document)
    
    def find_one(self, collection_name: str, query: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Find document in MongoDB or local storage"""
        if self.connected and collection_name in self.collections:
            try:
                result = self.collections[collection_name].find_one(query)
                if result:
                    result['_id'] = str(result['_id'])
                return result
            except Exception as e:
                logger.error(f"MongoDB find failed: {e}")
        
        # Local storage fallback
        return self._local_find_one(collection_name, query)
    
    def find_many(self, collection_name: str, query: Dict[str, Any] = None, limit: int = None) -> List[Dict[str, Any]]:
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
        
        # Local storage fallback
        return self._local_find_many(collection_name, query, limit)
    
    def update_one(self, collection_name: str, query: Dict[str, Any], update: Dict[str, Any]) -> bool:
        """Update document in MongoDB or local storage"""
        if self.connected and collection_name in self.collections:
            try:
                if '$set' not in update:
                    update = {'$set': update}
                update['$set']['updated_at'] = datetime.utcnow()
                
                result = self.collections[collection_name].update_one(query, update)
                return result.modified_count > 0
            except Exception as e:
                logger.error(f"MongoDB update failed: {e}")
        
        # Local storage fallback
        return self._local_update_one(collection_name, query, update)
    
    def delete_one(self, collection_name: str, query: Dict[str, Any]) -> bool:
        """Delete document from MongoDB or local storage"""
        if self.connected and collection_name in self.collections:
            try:
                result = self.collections[collection_name].delete_one(query)
                return result.deleted_count > 0
            except Exception as e:
                logger.error(f"MongoDB delete failed: {e}")
        
        # Local storage fallback
        return self._local_delete_one(collection_name, query)
    
    def count_documents(self, collection_name: str, query: Dict[str, Any] = None) -> int:
        """Count documents in collection"""
        if self.connected and collection_name in self.collections:
            try:
                return self.collections[collection_name].count_documents(query or {})
            except Exception as e:
                logger.error(f"MongoDB count failed: {e}")
        
        # Local storage fallback
        return self._local_count_documents(collection_name, query)
    
    def _local_insert_one(self, collection_name: str, document: Dict[str, Any]) -> Optional[str]:
        """Insert into local JSON storage"""
        if collection_name not in self.json_files:
            return None
        
        filepath = self.json_files[collection_name]
        
        # Add MongoDB-style _id
        if '_id' not in document:
            document['_id'] = str(uuid.uuid4())
        if isinstance(document.get('created_at'), datetime):
            document['created_at'] = document['created_at'].isoformat()
        
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            
            data.append(document)
            
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2, default=str)
            
            return document['_id']
        except Exception as e:
            logger.error(f"Local insert failed: {e}")
            return None
    
    def _local_find_one(self, collection_name: str, query: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Find in local JSON storage"""
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
            logger.error(f"Local find failed: {e}")
            return None
    
    def _local_find_many(self, collection_name: str, query: Dict[str, Any] = None, limit: int = None) -> List[Dict[str, Any]]:
        """Find multiple in local JSON storage"""
        if collection_name not in self.json_files:
            return []
        
        filepath = self.json_files[collection_name]
        
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            
            if not query:
                results = data
            else:
                results = []
                for doc in data:
                    match = True
                    for key, value in query.items():
                        if key not in doc or doc[key] != value:
                            match = False
                            break
                    if match:
                        results.append(doc)
            
            if limit:
                results = results[:limit]
            
            return results
        except Exception as e:
            logger.error(f"Local find_many failed: {e}")
            return []
    
    def _local_update_one(self, collection_name: str, query: Dict[str, Any], update: Dict[str, Any]) -> bool:
        """Update in local JSON storage"""
        if collection_name not in self.json_files:
            return False
        
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
                    # Apply update
                    if '$set' in update:
                        doc.update(update['$set'])
                    else:
                        doc.update(update)
                    doc['updated_at'] = datetime.utcnow().isoformat()
                    
                    with open(filepath, 'w') as f:
                        json.dump(data, f, indent=2, default=str)
                    return True
            
            return False
        except Exception as e:
            logger.error(f"Local update failed: {e}")
            return False
    
    def _local_delete_one(self, collection_name: str, query: Dict[str, Any]) -> bool:
        """Delete from local JSON storage"""
        if collection_name not in self.json_files:
            return False
        
        filepath = self.json_files[collection_name]
        
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            
            for i, doc in enumerate(data):
                match = True
                for key, value in query.items():
                    if key not in doc or doc[key] != value:
                        match = False
                        break
                if match:
                    data.pop(i)
                    with open(filepath, 'w') as f:
                        json.dump(data, f, indent=2, default=str)
                    return True
            
            return False
        except Exception as e:
            logger.error(f"Local delete failed: {e}")
            return False
    
    def _local_count_documents(self, collection_name: str, query: Dict[str, Any] = None) -> int:
        """Count documents in local JSON storage"""
        if collection_name not in self.json_files:
            return 0
        
        filepath = self.json_files[collection_name]
        
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            
            if not query:
                return len(data)
            
            count = 0
            for doc in data:
                match = True
                for key, value in query.items():
                    if key not in doc or doc[key] != value:
                        match = False
                        break
                if match:
                    count += 1
            
            return count
        except Exception as e:
            logger.error(f"Local count failed: {e}")
            return 0
    
    def get_database_status(self) -> Dict[str, Any]:
        """Get database status and statistics"""
        if self.connected:
            try:
                stats = self.db.command("dbStats")
                collection_stats = {}
                for collection_name in self.collections:
                    collection_stats[collection_name] = self.count_documents(collection_name)
                
                return {
                    "status": "connected",
                    "database": "MongoDB Atlas - myAppDB", 
                    "collections": collection_stats,
                    "total_size": stats.get("dataSize", 0)
                }
            except:
                pass
        
        # Local storage status
        collection_stats = {}
        for collection_name in self.json_files:
            collection_stats[collection_name] = self.count_documents(collection_name)
        
        return {
            "status": "local_storage",
            "database": "Local JSON with MongoDB structure",
            "collections": collection_stats
        }
    
    def close_connection(self):
        """Close MongoDB connection"""
        if self.client:
            self.client.close()
            self.connected = False

# Global instance
_mongodb_manager = None

def get_mongodb_manager() -> MongoDBManager:
    """Get global MongoDB manager instance"""
    global _mongodb_manager
    if _mongodb_manager is None:
        _mongodb_manager = MongoDBManager()
    return _mongodb_manager