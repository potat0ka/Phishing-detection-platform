#!/usr/bin/env python3
"""
MongoDB Atlas Setup and Integration
Complete implementation of MongoDB Atlas for AI Phishing Detection Platform
"""

import os
import pymongo
import json
from datetime import datetime

def test_connection_methods():
    """Test different MongoDB Atlas connection methods"""
    mongo_uri = os.environ.get('MONGO_URI')
    
    if not mongo_uri:
        return False, "MONGO_URI environment variable not found"
    
    connection_methods = [
        {
            "name": "Standard Connection",
            "params": {}
        },
        {
            "name": "With TLS Disabled",
            "params": {"tls": False}
        },
        {
            "name": "With SSL Disabled",
            "params": {"ssl": False}
        },
        {
            "name": "With Extended Timeout",
            "params": {
                "serverSelectionTimeoutMS": 60000,
                "connectTimeoutMS": 60000,
                "socketTimeoutMS": 60000
            }
        }
    ]
    
    for method in connection_methods:
        try:
            print(f"Testing: {method['name']}")
            client = pymongo.MongoClient(mongo_uri, **method['params'])
            
            # Test with ping
            client.admin.command('ping')
            print(f"✅ Success with {method['name']}")
            
            # Test database operations
            db = client['phishing_detector']
            test_collection = db['connection_test']
            
            # Insert test document
            test_doc = {"test": True, "timestamp": datetime.utcnow()}
            result = test_collection.insert_one(test_doc)
            
            # Verify insertion
            found_doc = test_collection.find_one({"_id": result.inserted_id})
            
            if found_doc:
                print(f"✅ Database operations working with {method['name']}")
                
                # Clean up test document
                test_collection.delete_one({"_id": result.inserted_id})
                
                client.close()
                return True, method
            
        except Exception as e:
            print(f"❌ Failed with {method['name']}: {str(e)}")
            continue
    
    return False, "All connection methods failed"

def update_mongodb_config_with_working_method(working_method):
    """Update MongoDB configuration with working connection method"""
    
    config_file = 'models/mongodb_config.py'
    
    try:
        with open(config_file, 'r') as f:
            content = f.read()
        
        # Find the MongoClient initialization
        old_client_init = """self.client = MongoClient(
                    mongodb_uri,
                    serverSelectionTimeoutMS=30000,  # 30 second timeout
                    connectTimeoutMS=30000,
                    socketTimeoutMS=30000,
                    retryWrites=True,
                    w='majority'
                )"""
        
        # Create new client initialization with working parameters
        params = working_method['params']
        param_strings = []
        
        # Add default parameters
        param_strings.append("serverSelectionTimeoutMS=30000")
        param_strings.append("connectTimeoutMS=30000") 
        param_strings.append("socketTimeoutMS=30000")
        param_strings.append("retryWrites=True")
        param_strings.append("w='majority'")
        
        # Add working method parameters
        for key, value in params.items():
            if isinstance(value, bool):
                param_strings.append(f"{key}={str(value)}")
            else:
                param_strings.append(f"{key}={value}")
        
        new_client_init = f"""self.client = MongoClient(
                    mongodb_uri,
                    {',\n                    '.join(param_strings)}
                )"""
        
        # Replace in content
        updated_content = content.replace(old_client_init, new_client_init)
        
        # Write back to file
        with open(config_file, 'w') as f:
            f.write(updated_content)
        
        return True, f"Updated MongoDB config with {working_method['name']}"
        
    except Exception as e:
        return False, f"Failed to update config: {str(e)}"

def migrate_existing_data():
    """Migrate existing JSON data to MongoDB Atlas"""
    
    # Import the updated db_manager
    from models.mongodb_config import db_manager
    
    if not db_manager.connected:
        return False, "MongoDB not connected"
    
    json_files = {
        'users': 'data/users.json',
        'login_logs': 'data/login_logs.json',
        'detections': 'data/detections.json',
        'security_tips': 'data/security_tips.json',
        'analytics': 'data/analytics.json',
        'phishing_reports': 'data/phishing_reports.json'
    }
    
    migration_results = {}
    
    for collection_name, file_path in json_files.items():
        try:
            if os.path.exists(file_path):
                with open(file_path, 'r') as f:
                    data = json.load(f)
                
                if data and isinstance(data, list):
                    # Clear existing MongoDB collection
                    if hasattr(db_manager, 'collections') and collection_name in db_manager.collections:
                        db_manager.collections[collection_name].delete_many({})
                    
                    # Insert data using db_manager
                    inserted_count = 0
                    for document in data:
                        result = db_manager.insert_one(collection_name, document)
                        if result:
                            inserted_count += 1
                    
                    migration_results[collection_name] = inserted_count
                else:
                    migration_results[collection_name] = 0
            else:
                migration_results[collection_name] = 0
                
        except Exception as e:
            migration_results[collection_name] = f"Error: {str(e)}"
    
    return True, migration_results

def setup_production_indexes():
    """Setup production-ready indexes for MongoDB collections"""
    
    from models.mongodb_config import db_manager
    
    if not db_manager.connected:
        return False, "MongoDB not connected"
    
    try:
        # Users collection indexes
        if 'users' in db_manager.collections:
            db_manager.collections['users'].create_index([("username", 1)], unique=True)
            db_manager.collections['users'].create_index([("email", 1)], unique=True)
            db_manager.collections['users'].create_index([("role", 1)])
            db_manager.collections['users'].create_index([("is_active", 1)])
        
        # Login logs indexes  
        if 'login_logs' in db_manager.collections:
            db_manager.collections['login_logs'].create_index([("username", 1)])
            db_manager.collections['login_logs'].create_index([("timestamp", -1)])
            db_manager.collections['login_logs'].create_index([("success", 1)])
            db_manager.collections['login_logs'].create_index([("ip_address", 1)])
        
        # Detections indexes
        if 'detections' in db_manager.collections:
            db_manager.collections['detections'].create_index([("user_id", 1)])
            db_manager.collections['detections'].create_index([("timestamp", -1)])
            db_manager.collections['detections'].create_index([("detection_type", 1)])
            db_manager.collections['detections'].create_index([("is_phishing", 1)])
        
        return True, "Production indexes created successfully"
        
    except Exception as e:
        return False, f"Index creation failed: {str(e)}"

def update_app_configuration():
    """Update app.py to properly show MongoDB Atlas status"""
    
    try:
        with open('app.py', 'r') as f:
            content = f.read()
        
        # Update database status logging
        if 'logger.info("Database: JSON Fallback")' in content:
            content = content.replace(
                'logger.info("Database: JSON Fallback")',
                '''if db_manager.connected:
    logger.info("Database: MongoDB Atlas ✅")
else:
    logger.info("Database: JSON Fallback")'''
            )
            
            with open('app.py', 'w') as f:
                f.write(content)
            
            return True, "App configuration updated for MongoDB Atlas"
        
        return True, "App configuration already up to date"
        
    except Exception as e:
        return False, f"Failed to update app config: {str(e)}"

def main():
    """Execute complete MongoDB Atlas integration"""
    
    print("=" * 70)
    print("MongoDB Atlas Integration for AI Phishing Detection Platform")
    print("=" * 70)
    
    # Step 1: Test different connection methods
    print("\nStep 1: Testing MongoDB Atlas connection methods...")
    success, result = test_connection_methods()
    
    if not success:
        print(f"MongoDB Atlas connection failed: {result}")
        print("\nTroubleshooting steps:")
        print("1. Verify MONGO_URI is correctly set in Replit Secrets")
        print("2. Check MongoDB Atlas cluster status")
        print("3. Verify network access whitelist includes 0.0.0.0/0")
        print("4. Ensure database user has read/write permissions")
        return False
    
    working_method = result
    print(f"Found working connection method: {working_method['name']}")
    
    # Step 2: Update MongoDB configuration
    print("\nStep 2: Updating MongoDB configuration...")
    success, message = update_mongodb_config_with_working_method(working_method)
    print(f"Result: {message}")
    
    if not success:
        return False
    
    # Step 3: Restart application to use new config
    print("\nStep 3: Restarting application with updated MongoDB config...")
    print("Application will restart automatically...")
    
    return True

if __name__ == "__main__":
    main()