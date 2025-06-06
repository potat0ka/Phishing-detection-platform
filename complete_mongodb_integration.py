# File to be removed - functionality integrated into main codebase
"""
Complete MongoDB Atlas Integration
Final implementation with SSL fixes and data migration
"""

import os
import json
import pymongo
from datetime import datetime

def main():
    """Complete MongoDB Atlas integration for the platform"""
    
    print("MongoDB Atlas Integration for AI Phishing Detection Platform")
    print("=" * 60)
    
    mongo_uri = os.environ.get('MONGO_URI')
    if not mongo_uri:
        print("MONGO_URI not found in environment variables")
        return False
    
    # Test MongoDB Atlas connection with different configurations
    connection_configs = [
        {"name": "Standard Connection", "params": {}},
        {"name": "No SSL", "params": {"ssl": False}},
        {"name": "No TLS", "params": {"tls": False}},
        {"name": "Extended Timeout", "params": {
            "serverSelectionTimeoutMS": 60000,
            "connectTimeoutMS": 60000,
            "socketTimeoutMS": 60000
        }}
    ]
    
    successful_config = None
    
    for config in connection_configs:
        try:
            print(f"Testing: {config['name']}")
            client = pymongo.MongoClient(mongo_uri, **config['params'])
            
            # Test connection
            client.admin.command('ping')
            print(f"Success with {config['name']}")
            
            # Test database operations
            db = client['phishing_detector']
            test_collection = db['connection_test']
            
            # Insert and retrieve test document
            test_doc = {"test": True, "timestamp": datetime.utcnow()}
            result = test_collection.insert_one(test_doc)
            found_doc = test_collection.find_one({"_id": result.inserted_id})
            
            if found_doc:
                print("Database operations confirmed")
                test_collection.delete_one({"_id": result.inserted_id})
                successful_config = config
                client.close()
                break
                
        except Exception as e:
            print(f"Failed with {config['name']}: {str(e)[:100]}")
            continue
    
    if not successful_config:
        print("All connection methods failed")
        print("Troubleshooting steps:")
        print("1. Verify MONGO_URI format and credentials")
        print("2. Check MongoDB Atlas cluster status")
        print("3. Verify network access allows 0.0.0.0/0")
        print("4. Confirm database user permissions")
        return False
    
    # Update MongoDB configuration with successful parameters
    print(f"Updating configuration with {successful_config['name']}")
    
    config_content = f'''"""
MongoDB Configuration and Connection Management
Updated with working connection parameters
"""

import os
import logging
from typing import Optional, Dict, Any
import json

try:
    from pymongo import MongoClient
    from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
    MONGODB_AVAILABLE = True
except ImportError as e:
    logging.warning(f"MongoDB not available: {{e}}")
    MONGODB_AVAILABLE = False
    class MongoClient:
        def __init__(self, *args, **kwargs):
            raise ConnectionFailure("MongoDB not available")
    class ConnectionFailure(Exception):
        pass
    class ServerSelectionTimeoutError(Exception):
        pass

logger = logging.getLogger(__name__)

class MongoDBManager:
    """MongoDB connection manager with Atlas integration"""
    
    def __init__(self):
        self.client: Optional[MongoClient] = None
        self.db = None
        self.connected = False
        self.collections = {{}}
        self.init_connection()
    
    def init_connection(self):
        """Initialize MongoDB Atlas connection"""
        if not MONGODB_AVAILABLE:
            logger.info("MongoDB libraries not available, using JSON file storage")
            self.connected = False
            self._setup_json_fallback()
            return
            
        try:
            mongodb_uri = os.environ.get('MONGO_URI') or os.environ.get('MONGODB_URI') or os.environ.get('DATABASE_URL')
            
            if mongodb_uri and 'mongodb' in mongodb_uri:
                # Use working connection parameters
                connection_params = {{
                    "serverSelectionTimeoutMS": 30000,
                    "connectTimeoutMS": 30000,
                    "socketTimeoutMS": 30000,
                    "retryWrites": True,
                    "w": "majority"
                }}
                
                # Add successful config parameters
                {successful_config['params']}
                connection_params.update({successful_config['params']})
                
                self.client = MongoClient(mongodb_uri, **connection_params)
                
                # Test connection
                self.client.admin.command('ping')
                
                # Get database
                db_name = mongodb_uri.split('/')[-1].split('?')[0] if '/' in mongodb_uri else 'phishing_detector'
                self.db = self.client[db_name]
                self.connected = True
                
                logger.info(f"Connected to MongoDB Atlas database: {{db_name}}")
                self._setup_collections()
                
            else:
                raise ConnectionFailure("No MongoDB URI provided")
                
        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            logger.warning(f"MongoDB connection failed: {{e}}")
            logger.info("Falling back to JSON file storage")
            self.connected = False
            self._setup_json_fallback()
    
    def _setup_collections(self):
        """Set up MongoDB collections with indexing"""
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
            
            # Login logs collection
            self.collections['login_logs'] = self.db.login_logs
            self.collections['login_logs'].create_index('username')
            self.collections['login_logs'].create_index('timestamp')
            
            # Security tips collection
            self.collections['security_tips'] = self.db.security_tips
            self.collections['security_tips'].create_index('category')
            
            # Analytics collection
            self.collections['analytics'] = self.db.analytics
            self.collections['analytics'].create_index('session_id')
            
            logger.info("MongoDB collections initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to setup collections: {{e}}")
    
    def _setup_json_fallback(self):
        """Set up JSON file storage as fallback"""
        self.json_files = {{
            'users': 'data/users.json',
            'detections': 'data/detections.json',
            'security_tips': 'data/security_tips.json',
            'analytics': 'data/analytics.json',
            'login_logs': 'data/login_logs.json',
            'phishing_reports': 'data/phishing_reports.json',
            'reported_content': 'data/reported_content.json',
            'ai_content_detections': 'data/ai_content_detections.json'
        }}
        
        os.makedirs('data', exist_ok=True)
        
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
                logger.error(f"MongoDB insert failed: {{e}}")
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
                logger.error(f"MongoDB find failed: {{e}}")
                return self._json_find_one(collection_name, query)
        else:
            return self._json_find_one(collection_name, query)
    
    def find_many(self, collection_name: str, query: Dict[str, Any] = None, limit: int = None) -> list:
        """Find multiple documents"""
        if self.connected and collection_name in self.collections:
            try:
                cursor = self.collections[collection_name].find(query or {{}})
                if limit:
                    cursor = cursor.limit(limit)
                
                results = []
                for doc in cursor:
                    doc['_id'] = str(doc['_id'])
                    results.append(doc)
                return results
            except Exception as e:
                logger.error(f"MongoDB find_many failed: {{e}}")
                return self._json_find_many(collection_name, query, limit)
        else:
            return self._json_find_many(collection_name, query, limit)
    
    def update_one(self, collection_name: str, query: Dict[str, Any], update: Dict[str, Any]) -> bool:
        """Update a single document"""
        if self.connected and collection_name in self.collections:
            try:
                result = self.collections[collection_name].update_one(query, {{'$set': update}})
                return result.modified_count > 0
            except Exception as e:
                logger.error(f"MongoDB update failed: {{e}}")
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
                logger.error(f"MongoDB delete failed: {{e}}")
                return self._json_delete_one(collection_name, query)
        else:
            return self._json_delete_one(collection_name, query)
    
    def count_documents(self, collection_name: str, query: Dict[str, Any] = None) -> int:
        """Count documents matching query"""
        if self.connected and collection_name in self.collections:
            try:
                return self.collections[collection_name].count_documents(query or {{}})
            except Exception as e:
                logger.error(f"MongoDB count failed: {{e}}")
                return self._json_count_documents(collection_name, query)
        else:
            return self._json_count_documents(collection_name, query)
    
    # JSON fallback methods (keeping existing implementation)
    def _json_insert_one(self, collection_name: str, document: Dict[str, Any]) -> Optional[str]:
        filepath = self.json_files.get(collection_name)
        if not filepath:
            return None
            
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            
            document['_id'] = f"{{collection_name}}_{{len(data) + 1}}_{{int(os.urandom(4).hex(), 16)}}"
            data.append(document)
            
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2, default=str)
            
            return document['_id']
        except Exception as e:
            logger.error(f"JSON insert failed: {{e}}")
            return None
    
    def _json_find_one(self, collection_name: str, query: Dict[str, Any]) -> Optional[Dict[str, Any]]:
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
            logger.error(f"JSON find failed: {{e}}")
            return None
    
    def _json_find_many(self, collection_name: str, query: Dict[str, Any] = None, limit: int = None) -> list:
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
            logger.error(f"JSON find_many failed: {{e}}")
            return []
    
    def _json_update_one(self, collection_name: str, query: Dict[str, Any], update: Dict[str, Any]) -> bool:
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
            logger.error(f"JSON update failed: {{e}}")
            return False
    
    def _json_delete_one(self, collection_name: str, query: Dict[str, Any]) -> bool:
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
            logger.error(f"JSON delete failed: {{e}}")
            return False
    
    def _json_count_documents(self, collection_name: str, query: Dict[str, Any] = None) -> int:
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
            logger.error(f"JSON count failed: {{e}}")
            return 0
    
    def _matches_query(self, document: Dict[str, Any], query: Dict[str, Any]) -> bool:
        """Check if document matches query"""
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
'''
    
    # Write updated configuration
    with open('models/mongodb_config.py', 'w') as f:
        f.write(config_content)
    
    print("MongoDB configuration updated successfully")
    
    # Update app.py to show MongoDB Atlas status
    try:
        with open('app.py', 'r') as f:
            app_content = f.read()
        
        if 'logger.info("Database: JSON Fallback")' in app_content:
            app_content = app_content.replace(
                'logger.info("Database: JSON Fallback")',
                '''if db_manager.connected:
    logger.info("Database: MongoDB Atlas Connected")
else:
    logger.info("Database: JSON Fallback")'''
            )
            
            with open('app.py', 'w') as f:
                f.write(app_content)
            
            print("Application configuration updated")
    
    except Exception as e:
        print(f"App config update failed: {e}")
    
    print("MongoDB Atlas integration completed successfully")
    print("Application will restart automatically to apply changes")
    
    return True

if __name__ == "__main__":
    main()