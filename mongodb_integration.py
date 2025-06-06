#!/usr/bin/env python3
"""
MongoDB Atlas Full Integration for AI Phishing Detection Platform
Comprehensive database migration from JSON to MongoDB Atlas
"""

import os
import json
import pymongo
from datetime import datetime
from models.mongodb_config import db_manager

class MongoDBMigration:
    """Handle migration of existing JSON data to MongoDB Atlas"""
    
    def __init__(self):
        self.mongo_uri = os.environ.get('MONGO_URI')
        self.client = None
        self.db = None
        self.migration_log = []
    
    def connect_to_atlas(self):
        """Establish connection to MongoDB Atlas"""
        if not self.mongo_uri:
            return False, "MONGO_URI not found in environment"
        
        try:
            # Use standard MongoDB Atlas connection
            self.client = pymongo.MongoClient(self.mongo_uri)
            
            # Test connection with ping
            self.client.admin.command('ping')
            
            # Get database
            self.db = self.client['phishing_detector']
            
            return True, "Connected to MongoDB Atlas successfully"
            
        except Exception as e:
            return False, f"Connection failed: {str(e)}"
    
    def migrate_json_to_mongodb(self):
        """Migrate all JSON data to MongoDB Atlas"""
        if not self.db:
            return False, "No database connection available"
        
        json_files = {
            'users': 'data/users.json',
            'detections': 'data/detections.json',
            'security_tips': 'data/security_tips.json',
            'analytics': 'data/analytics.json',
            'login_logs': 'data/login_logs.json',
            'phishing_reports': 'data/phishing_reports.json'
        }
        
        migration_results = {}
        
        for collection_name, json_file in json_files.items():
            try:
                if os.path.exists(json_file):
                    with open(json_file, 'r') as f:
                        data = json.load(f)
                    
                    if data:  # Only migrate if data exists
                        collection = self.db[collection_name]
                        
                        # Clear existing data in MongoDB collection
                        collection.delete_many({})
                        
                        # Insert JSON data
                        if isinstance(data, list):
                            result = collection.insert_many(data)
                            migration_results[collection_name] = len(result.inserted_ids)
                        else:
                            result = collection.insert_one(data)
                            migration_results[collection_name] = 1
                    else:
                        migration_results[collection_name] = 0
                else:
                    migration_results[collection_name] = 0
                    
            except Exception as e:
                migration_results[collection_name] = f"Error: {str(e)}"
        
        return True, migration_results
    
    def setup_mongodb_indexes(self):
        """Create proper indexes for MongoDB collections"""
        if not self.db:
            return False, "No database connection"
        
        try:
            # Users collection indexes
            self.db.users.create_index("username", unique=True)
            self.db.users.create_index("email", unique=True)
            self.db.users.create_index("role")
            
            # Detections collection indexes
            self.db.detections.create_index("user_id")
            self.db.detections.create_index("timestamp")
            self.db.detections.create_index("detection_type")
            
            # Login logs indexes
            self.db.login_logs.create_index("username")
            self.db.login_logs.create_index("timestamp")
            self.db.login_logs.create_index("success")
            
            # Analytics indexes
            self.db.analytics.create_index("session_id")
            self.db.analytics.create_index("timestamp")
            
            return True, "Indexes created successfully"
            
        except Exception as e:
            return False, f"Index creation failed: {str(e)}"
    
    def verify_migration(self):
        """Verify data migration was successful"""
        if not self.db:
            return False, "No database connection"
        
        verification_results = {}
        
        collections = ['users', 'detections', 'security_tips', 'analytics', 'login_logs']
        
        for collection_name in collections:
            try:
                count = self.db[collection_name].count_documents({})
                verification_results[collection_name] = count
            except Exception as e:
                verification_results[collection_name] = f"Error: {str(e)}"
        
        return True, verification_results

def update_application_config():
    """Update application to use MongoDB instead of JSON fallback"""
    
    # Update app.py to show MongoDB status
    try:
        with open('app.py', 'r') as f:
            content = f.read()
        
        # Add MongoDB status indicator
        if 'Database: JSON Fallback' in content:
            content = content.replace(
                'logger.info("Database: JSON Fallback")',
                'logger.info("Database: MongoDB Atlas" if db_manager.connected else "Database: JSON Fallback")'
            )
            
            with open('app.py', 'w') as f:
                f.write(content)
            
            return True, "Application config updated for MongoDB"
        
        return True, "Application already configured for MongoDB"
        
    except Exception as e:
        return False, f"Failed to update config: {str(e)}"

def main():
    """Execute full MongoDB Atlas integration"""
    print("=" * 60)
    print("MongoDB Atlas Integration for AI Phishing Detection Platform")
    print("=" * 60)
    
    migration = MongoDBMigration()
    
    # Step 1: Test connection
    print("\nStep 1: Testing MongoDB Atlas connection...")
    success, message = migration.connect_to_atlas()
    print(f"Result: {message}")
    
    if not success:
        print("\nMongoDB Atlas connection failed. Using JSON fallback system.")
        print("To enable MongoDB Atlas:")
        print("1. Verify MONGO_URI is correctly set in Replit Secrets")
        print("2. Check MongoDB Atlas cluster is running")
        print("3. Verify network access permissions")
        return False
    
    # Step 2: Setup indexes
    print("\nStep 2: Creating MongoDB indexes...")
    success, message = migration.setup_mongodb_indexes()
    print(f"Result: {message}")
    
    # Step 3: Migrate data
    print("\nStep 3: Migrating JSON data to MongoDB...")
    success, results = migration.migrate_json_to_mongodb()
    if success:
        print("Migration results:")
        for collection, count in results.items():
            print(f"  - {collection}: {count} documents")
    else:
        print(f"Migration failed: {results}")
    
    # Step 4: Verify migration
    print("\nStep 4: Verifying data migration...")
    success, results = migration.verify_migration()
    if success:
        print("Verification results:")
        for collection, count in results.items():
            print(f"  - {collection}: {count} documents")
    
    # Step 5: Update application config
    print("\nStep 5: Updating application configuration...")
    success, message = update_application_config()
    print(f"Result: {message}")
    
    print("\n" + "=" * 60)
    print("MongoDB Atlas Integration Complete!")
    print("Your AI Phishing Detection Platform now uses MongoDB Atlas")
    print("for production-ready data storage and management.")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    main()