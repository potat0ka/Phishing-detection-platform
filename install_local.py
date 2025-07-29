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
    
    # Essential dependencies only (avoiding problematic packages)
    essential_deps = [
        "Flask",
        "Flask-Login", 
        "Flask-PyMongo",
        "pymongo",
        "Werkzeug",
        "bcrypt",
        "passlib",
        "email-validator",
        "dnspython",
        "requests",
        "python-dotenv"
    ]
    
    # Optional dependencies (install separately, skip if they fail)
    optional_deps = [
        "beautifulsoup4",
        "nltk", 
        "python-docx",
        "scikit-learn",
        "openai",
        "Pillow",
        "imagehash"
    ]
    
    print(f"\n📦 Installing essential dependencies...")
    
    # Install essential dependencies first
    essential_command = f"pip install {' '.join(essential_deps)}"
    if not run_command(essential_command, "Installing essential dependencies"):
        print("\n❌ Essential installation failed. Please check the error above.")
        return False
    
    print(f"\n📦 Installing optional dependencies (may skip some)...")
    
    # Install optional dependencies one by one (skip failures)
    failed_packages = []
    for package in optional_deps:
        command = f"pip install {package}"
        if not run_command(command, f"Installing {package}"):
            failed_packages.append(package)
            print(f"⚠️  Skipping {package} (not critical for basic functionality)")
    
    if failed_packages:
        print(f"\n⚠️  Some optional packages failed to install: {', '.join(failed_packages)}")
        print("The application will still work with reduced functionality.")
    
    print("\n🎉 All dependencies installed successfully!")
    print("\n📋 Next steps:")
    print("1. Set up your MongoDB connection string in a .env file")
    print("2. Run: python main.py")
    print("3. Open your browser to http://localhost:8080")
    
    return True

if __name__ == "__main__":
    success = install_dependencies()
    sys.exit(0 if success else 1)