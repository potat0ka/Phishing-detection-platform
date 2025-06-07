#!/usr/bin/env python3
"""
MongoDB Atlas Connection Test for AI Phishing Detection Platform
Tests connection and creates sample data in users and models collections
"""

import os
import pymongo
from datetime import datetime

def test_mongodb_connection():
    """Test MongoDB Atlas connection and create sample data"""
    
    # Use the provided MongoDB URI
    mongo_uri = os.environ.get('MONGO_URI', 
        'mongodb+srv://potato:F38ZS9uqXV8Bijd@build-a-database.5k4i357.mongodb.net/myAppDB?retryWrites=true&w=majority')
    
    print(f"Testing MongoDB Atlas connection...")
    print(f"URI: {mongo_uri[:50]}...")
    
    try:
        # Test different connection configurations
        configs = [
            {"serverSelectionTimeoutMS": 5000},
            {"serverSelectionTimeoutMS": 5000, "ssl": False},
            {"serverSelectionTimeoutMS": 5000, "tls": False}
        ]
        
        for i, config in enumerate(configs):
            try:
                print(f"\nTrying connection config {i+1}...")
                client = pymongo.MongoClient(mongo_uri, **config)
                
                # Test connection
                client.admin.command('ping')
                print(f"✅ Connected with config {i+1}")
                
                # Access myAppDB database
                db = client['myAppDB']
                print(f"✅ Accessed database: {db.name}")
                
                # Test users collection
                users_collection = db.users
                sample_user = {
                    "username": "alice",
                    "email": "alice@example.com", 
                    "role": "user",
                    "created_at": datetime.utcnow()
                }
                
                # Check if user already exists
                existing_user = users_collection.find_one({"username": "alice"})
                if not existing_user:
                    user_result = users_collection.insert_one(sample_user)
                    print(f"✅ Inserted user: {user_result.inserted_id}")
                else:
                    print(f"✅ User 'alice' already exists: {existing_user['_id']}")
                
                # Test models collection
                models_collection = db.models
                sample_model = {
                    "model_name": "linear_regression_v1",
                    "created_at": datetime.utcnow(),
                    "model_type": "phishing_detection",
                    "accuracy": 0.95
                }
                
                # Check if model already exists
                existing_model = models_collection.find_one({"model_name": "linear_regression_v1"})
                if not existing_model:
                    model_result = models_collection.insert_one(sample_model)
                    print(f"✅ Inserted model: {model_result.inserted_id}")
                else:
                    print(f"✅ Model 'linear_regression_v1' already exists: {existing_model['_id']}")
                
                # Verify data
                user_count = users_collection.count_documents({})
                model_count = models_collection.count_documents({})
                
                print(f"\n📊 Database Statistics:")
                print(f"  - Users collection: {user_count} documents")
                print(f"  - Models collection: {model_count} documents")
                
                client.close()
                return True
                
            except Exception as e:
                print(f"❌ Config {i+1} failed: {e}")
                continue
        
        print("❌ All connection attempts failed")
        return False
        
    except Exception as e:
        print(f"❌ Connection test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_mongodb_connection()
    if success:
        print("\n🎉 MongoDB Atlas is ready for your AI Phishing Detection Platform!")
    else:
        print("\n⚠️  MongoDB Atlas connection failed - using local storage fallback")