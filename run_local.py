#!/usr/bin/env python3
"""
Local Development Runner for AI Phishing Detection Platform
===========================================================

This script sets up the environment and runs the application locally.
It handles MongoDB connection setup and dependency checks.

Usage:
    python run_local.py

Author: Bigendra Shrestha
"""

import os
import sys
import subprocess

def setup_environment():
    """Set up environment variables for local development"""
    # Your MongoDB connection string
    mongodb_uri = "mongodb+srv://potato:potato123@phishingcluster.19pf3wn.mongodb.net/?retryWrites=true&w=majority&appName=PhishingCluster"
    
    # Set environment variables
    os.environ['MONGODB_URI'] = mongodb_uri
    os.environ['MONGO_URI'] = mongodb_uri
    os.environ['SECRET_KEY'] = 'local-dev-secret-2024'
    os.environ['SESSION_SECRET'] = 'local-dev-session-2024'
    os.environ['DEBUG'] = 'True'
    
    print("✅ Environment variables set")
    return True

def check_dependencies():
    """Check if required dependencies are installed"""
    required_packages = ['flask', 'pymongo', 'bcrypt']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing packages: {', '.join(missing_packages)}")
        print("Run: python install_minimal.py")
        return False
    
    print("✅ All required dependencies found")
    return True

def run_application():
    """Start the Flask application"""
    print("\n🚀 Starting AI Phishing Detection Platform...")
    print("=" * 55)
    print("📊 MongoDB: PhishingCluster (potato@19pf3wn.mongodb.net)")
    print("🌐 Server: http://localhost:8080")
    print("🔧 Environment: Development")
    print("=" * 55)
    
    try:
        # Import and run the main application
        from main import app
        app.run(host='0.0.0.0', port=8080, debug=True)
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure all dependencies are installed.")
        return False
    except Exception as e:
        print(f"❌ Application error: {e}")
        return False

def main():
    """Main function to set up and run the application"""
    print("🔧 AI Phishing Detection Platform - Local Setup")
    print("=" * 55)
    
    # Setup environment
    if not setup_environment():
        print("❌ Environment setup failed")
        sys.exit(1)
    
    # Check dependencies
    if not check_dependencies():
        print("❌ Dependency check failed")
        sys.exit(1)
    
    # Run application
    run_application()

if __name__ == "__main__":
    main()