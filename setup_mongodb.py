#!/usr/bin/env python3
"""
MongoDB Setup Script for Local Development
==========================================

This script sets up MongoDB connection for local development.
It creates the .env file with your MongoDB credentials.

Usage:
    python setup_mongodb.py

Author: Bigendra Shrestha
"""

import os

def setup_mongodb():
    """Setup MongoDB configuration for local development"""
    print("🔧 AI Phishing Detection Platform - MongoDB Setup")
    print("=" * 55)
    
    # Your MongoDB URI
    mongodb_uri = "mongodb+srv://potato:potato123@phishingcluster.19pf3wn.mongodb.net/?retryWrites=true&w=majority&appName=PhishingCluster"
    
    # Create .env file content
    env_content = f"""# AI Phishing Detection Platform - Local Environment Configuration
MONGODB_URI={mongodb_uri}
SECRET_KEY=local-dev-secret-key-2024
SESSION_SECRET=local-dev-session-secret-2024
DEBUG=True
PORT=8080
"""
    
    # Write .env file
    try:
        with open('.env', 'w') as f:
            f.write(env_content)
        print("✅ .env file created successfully")
    except Exception as e:
        print(f"❌ Failed to create .env file: {e}")
        return False
    
    # Set environment variables for current session
    os.environ['MONGODB_URI'] = mongodb_uri
    os.environ['SECRET_KEY'] = 'local-dev-secret-key-2024'
    os.environ['SESSION_SECRET'] = 'local-dev-session-secret-2024'
    
    print("\n📋 MongoDB Configuration:")
    print(f"Database: phishingcluster.19pf3wn.mongodb.net")
    print(f"Username: potato")
    print(f"App Name: PhishingCluster")
    
    print("\n🚀 Ready to run:")
    print("python main.py")
    
    return True

if __name__ == "__main__":
    setup_mongodb()