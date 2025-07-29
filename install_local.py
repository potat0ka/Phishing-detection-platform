#!/usr/bin/env python3
"""
Local Installation Script for AI Phishing Detection Platform
============================================================

This script helps install all required dependencies for running the platform locally.
Run this before starting the application on your local machine.

Usage:
    python install_local.py

Author: Bigendra Shrestha
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a shell command and handle errors"""
    print(f"\n{description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error during {description}")
        print(f"Command: {command}")
        print(f"Error: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major == 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor} is compatible")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor} is not compatible. Requires Python 3.8+")
        return False

def install_dependencies():
    """Install all required dependencies"""
    print("🚀 Starting AI Phishing Detection Platform Local Installation")
    print("=" * 60)
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Install core dependencies
    dependencies = [
        "Flask==2.3.3",
        "Flask-Login>=0.6.3",
        "Flask-PyMongo>=2.3.0",
        "pymongo==4.5.0",
        "Werkzeug>=3.1.3",
        "bcrypt==4.0.1",
        "cryptography==41.0.7",
        "passlib==1.7.4",
        "email-validator==2.1.0",
        "dnspython==2.4.2",
        "beautifulsoup4==4.12.2",
        "trafilatura==1.6.4",
        "nltk==3.8.1",
        "python-docx>=1.2.0",
        "pdfplumber>=0.11.7",
        "scikit-learn==1.3.2",
        "openai>=1.97.1",
        "Pillow==9.5.0",
        "opencv-python>=4.11.0.86",
        "imagehash>=4.3.2",
        "librosa>=0.11.0",
        "soundfile>=0.13.1",
        "pytesseract>=0.3.13",
        "requests==2.31.0",
        "python-dotenv>=1.0.0"
    ]
    
    print(f"\n📦 Installing {len(dependencies)} dependencies...")
    
    # Install dependencies in batches to avoid timeout
    batch_size = 5
    for i in range(0, len(dependencies), batch_size):
        batch = dependencies[i:i+batch_size]
        command = f"pip install {' '.join(batch)}"
        
        if not run_command(command, f"Installing batch {i//batch_size + 1}"):
            print("\n❌ Installation failed. Please check the error above.")
            return False
    
    print("\n🎉 All dependencies installed successfully!")
    print("\n📋 Next steps:")
    print("1. Set up your MongoDB connection string in a .env file")
    print("2. Run: python main.py")
    print("3. Open your browser to http://localhost:8080")
    
    return True

if __name__ == "__main__":
    success = install_dependencies()
    sys.exit(0 if success else 1)