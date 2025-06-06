#!/usr/bin/env python3
"""
MongoDB Atlas Connection Test
Test the MONGO_URI connection and demonstrate basic operations
"""

import os
import pymongo
from datetime import datetime

def test_mongodb_connection():
    """Test MongoDB Atlas connection with sample operations"""
    
    # Get Mongo URI securely from environment
    mongo_uri = os.environ.get('MONGO_URI')
    
    if not mongo_uri:
        print("❌ MONGO_URI not found in environment variables")
        return False
    
    try:
        print("🔗 Connecting to MongoDB Atlas...")
        
        # Connect to MongoDB with proper SSL configuration
        client = pymongo.MongoClient(
            mongo_uri,
            serverSelectionTimeoutMS=30000,  # 30 second timeout
            connectTimeoutMS=30000,
            socketTimeoutMS=30000,
            retryWrites=True,
            w='majority'
        )
        
        # Test connection
        client.admin.command('ping')
        print("✅ Successfully connected to MongoDB Atlas!")
        
        # Get database
        db = client['phishing_detector']
        print(f"📊 Connected to database: {db.name}")
        
        # Test basic operations
        collection = db['test_collection']
        
        # Sample operation
        sample_document = {
            "name": "Test User", 
            "project": "AI Phishing Detection Platform",
            "timestamp": datetime.utcnow(),
            "test_type": "connection_verification"
        }
        
        # Insert document
        result = collection.insert_one(sample_document)
        print(f"📝 Inserted document ID: {result.inserted_id}")
        
        # Read documents
        print("\n📋 Documents in test collection:")
        for doc in collection.find():
            print(f"  - {doc}")
        
        # Count documents
        count = collection.count_documents({})
        print(f"\n📊 Total documents in collection: {count}")
        
        # Clean up test data
        collection.delete_many({"test_type": "connection_verification"})
        print("🧹 Cleaned up test data")
        
        # Close connection
        client.close()
        print("🔒 Connection closed successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ MongoDB Connection Error: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("🚀 AI Phishing Detection Platform - MongoDB Atlas Test")
    print("=" * 60)
    
    success = test_mongodb_connection()
    
    if success:
        print("\n✅ MongoDB Atlas integration is working perfectly!")
        print("🎉 Ready to migrate from JSON fallback to MongoDB Atlas")
    else:
        print("\n❌ MongoDB Atlas connection failed")
        print("🔄 Will continue using JSON fallback system")