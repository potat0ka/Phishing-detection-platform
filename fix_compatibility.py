#!/usr/bin/env python3
"""
Compatibility Fix Script for Python 3.13
=========================================

This script helps resolve compatibility issues with newer Python versions.
Run this if you're having installation problems.

Usage:
    python fix_compatibility.py

Author: Bigendra Shrestha
"""

import subprocess
import sys
import platform

def check_environment():
    """Check Python version and environment"""
    print(f"Python version: {sys.version}")
    print(f"Platform: {platform.platform()}")
    print(f"Architecture: {platform.architecture()}")
    
    # Check if using conda
    try:
        result = subprocess.run(["conda", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"Conda detected: {result.stdout.strip()}")
            return "conda"
    except:
        pass
    
    return "pip"

def fix_conda_environment():
    """Fix issues in conda environment"""
    print("\n🔧 Applying conda environment fixes...")
    
    commands = [
        "conda update -n base -c defaults conda",
        "conda install -c conda-forge lxml",
        "conda install -c conda-forge flask pymongo bcrypt"
    ]
    
    for cmd in commands:
        print(f"Running: {cmd}")
        try:
            subprocess.run(cmd.split(), check=True)
            print("✅ Success")
        except:
            print("❌ Failed (continuing...)")

def fix_pip_environment():
    """Fix issues in pip environment"""
    print("\n🔧 Applying pip environment fixes...")
    
    commands = [
        f"{sys.executable} -m pip install --upgrade pip",
        f"{sys.executable} -m pip install --upgrade setuptools wheel"
    ]
    
    for cmd in commands:
        print(f"Running: {cmd}")
        try:
            subprocess.run(cmd.split(), check=True)
            print("✅ Success")
        except:
            print("❌ Failed (continuing...)")

def main():
    print("🔧 AI Phishing Detection Platform - Compatibility Fixer")
    print("=" * 60)
    
    env_type = check_environment()
    
    if env_type == "conda":
        fix_conda_environment()
    else:
        fix_pip_environment()
    
    print("\n📋 Next steps:")
    print("1. Try: python install_minimal.py")
    print("2. If that works: python main.py")
    print("3. If issues persist: Use manual installation")
    
    print("\n🔗 Manual installation commands:")
    print("pip install Flask Flask-Login Flask-PyMongo pymongo bcrypt requests")

if __name__ == "__main__":
    main()