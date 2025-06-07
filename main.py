#!/usr/bin/env python3
"""
AI Phishing Detection Platform - Main Entry Point
================================================

This is the main file to start the web application.
It imports the Flask app from the src directory and starts the server.

Author: Bigendra Shrestha
Project: Final Semester - Cybersecurity & AI Detection Platform
College: Saraswati Multiple Campus (8th Semester)

How to run:
1. Open terminal/command prompt
2. Navigate to this project folder
3. Run: python main.py
4. Open browser and go to: http://localhost:8080
"""

import sys
import os

# Add the src directory to Python path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import the Flask application from src directory
from app import app

if __name__ == "__main__":
    print("=" * 60)
    print("🚀 AI Phishing Detection Platform")
    print("=" * 60)
    print("📝 Author: Bigendra Shrestha")
    print("🎓 Project: Final Semester - Cybersecurity & AI")
    print("=" * 60)
    print("🌐 Starting web server...")
    print("📖 For beginners: This creates a website on your computer")
    print("🔗 Once started, open: http://localhost:8080")
    print("🛑 Press Ctrl+C to stop the server")
    print("=" * 60)
    
    # Start the Flask web server
    # host='0.0.0.0' allows access from other devices on network
    # port=8080 is the port number where website runs
    # debug=True shows detailed error messages (helpful for development)
    app.run(host='0.0.0.0', port=8080, debug=True)