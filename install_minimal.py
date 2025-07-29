#!/usr/bin/env python3
"""
Minimal Installation Script for AI Phishing Detection Platform
=============================================================

This script installs only the core dependencies needed to run the platform.
Use this if the full installer fails due to compatibility issues.

Usage:
    python install_minimal.py

Author: Bigendra Shrestha
"""

import subprocess
import sys

def install_core_only():
    """Install only the core dependencies needed to run the app"""
    print("🚀 Installing CORE dependencies only")
    print("=" * 50)
    
    # Absolute minimum to run the Flask app
    core_packages = [
        "Flask",
        "Flask-Login", 
        "Flask-PyMongo",
        "pymongo",
        "bcrypt",
        "requests"
    ]
    
    print("Installing core packages...")
    for package in core_packages:
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", package], 
                         check=True, capture_output=True)
            print(f"✅ {package} installed")
        except subprocess.CalledProcessError:
            print(f"❌ Failed to install {package}")
            return False
    
    print("\n🎉 Core installation complete!")
    print("\n📋 What works with minimal install:")
    print("✅ Basic phishing detection")
    print("✅ User authentication")
    print("✅ Core web interface")
    print("✅ MongoDB integration")
    
    print("\n⚠️  Advanced features disabled:")
    print("- File upload analysis")
    print("- AI content detection") 
    print("- Image processing")
    print("- Audio analysis")
    
    print("\n🚀 Ready to run: python main.py")
    return True

if __name__ == "__main__":
    success = install_core_only()
    sys.exit(0 if success else 1)