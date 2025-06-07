#!/usr/bin/env python3
"""
Cross-Platform Setup Script for AI Phishing Detection Platform
==============================================================

This script automatically detects your operating system and installs
the appropriate dependencies for optimal compatibility.

Usage:
    python setup.py

Author: Bigendra Shrestha
Project: AI Phishing Detection Platform (BCA Final Semester)
"""

import os
import sys
import platform
import subprocess
import venv
from pathlib import Path

def detect_platform():
    """Detect the current platform and return appropriate requirements file"""
    system = platform.system().lower()
    
    if system == "windows":
        return "requirements-windows-basic.txt", "Windows (Basic)"
    elif system == "darwin":  # macOS
        return "requirements-macos.txt", "macOS"
    elif system == "linux":
        return "requirements-linux.txt", "Linux"
    else:
        print(f"⚠️  Unknown platform: {system}")
        print("Falling back to generic requirements...")
        return "requirements-local.txt", "Generic"

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python {version.major}.{version.minor} is not supported")
        print("Please install Python 3.8 or higher")
        sys.exit(1)
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detected")
    return True

def create_virtual_environment():
    """Create virtual environment if it doesn't exist"""
    venv_path = Path("venv")
    
    if venv_path.exists():
        print("✅ Virtual environment already exists")
        return True
    
    print("📦 Creating virtual environment...")
    try:
        venv.create("venv", with_pip=True)
        print("✅ Virtual environment created successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to create virtual environment: {e}")
        return False

def get_pip_command():
    """Get the appropriate pip command for the platform"""
    system = platform.system().lower()
    if system == "windows":
        return [os.path.join("venv", "Scripts", "python.exe"), "-m", "pip"]
    else:
        return [os.path.join("venv", "bin", "python"), "-m", "pip"]

def install_requirements(requirements_file):
    """Install requirements using pip"""
    pip_cmd = get_pip_command()
    
    print("📥 Upgrading pip...")
    try:
        subprocess.run(pip_cmd + ["install", "--upgrade", "pip"], 
                      check=True, capture_output=True, text=True)
        print("✅ Pip upgraded successfully")
    except subprocess.CalledProcessError as e:
        print(f"⚠️  Warning: Could not upgrade pip: {e}")
    
    print(f"📦 Installing packages from {requirements_file}...")
    try:
        result = subprocess.run(pip_cmd + ["install", "-r", requirements_file], 
                               check=True, capture_output=True, text=True)
        print("✅ All packages installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install packages: {e}")
        print("Error output:", e.stderr)
        return False

def create_env_file():
    """Create .env file if it doesn't exist"""
    env_file = Path(".env")
    env_example = Path(".env.example")
    
    if env_file.exists():
        print("✅ .env file already exists")
        return True
    
    if env_example.exists():
        print("📝 Creating .env file from template...")
        try:
            with open(env_example, 'r') as f:
                content = f.read()
            
            with open(env_file, 'w') as f:
                f.write(content)
            
            print("✅ .env file created successfully")
            print("📋 Please edit .env file with your MongoDB Atlas credentials")
            return True
        except Exception as e:
            print(f"❌ Failed to create .env file: {e}")
            return False
    else:
        print("⚠️  .env.example not found, skipping .env creation")
        return True

def test_installation():
    """Test if the installation was successful"""
    python_cmd = get_pip_command()[0]
    
    print("🧪 Testing installation...")
    test_script = """
import flask
import pymongo
print("✅ Core packages imported successfully")

# Test optional ML packages
try:
    import numpy
    import sklearn
    print("✅ ML packages available")
except ImportError:
    print("ℹ️  ML packages not available - using rule-based detection")
"""
    
    try:
        result = subprocess.run([python_cmd, "-c", test_script], 
                               check=True, capture_output=True, text=True)
        print(result.stdout.strip())
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Installation test failed: {e}")
        print("Error output:", e.stderr)
        return False

def print_activation_instructions():
    """Print instructions for activating the virtual environment"""
    system = platform.system().lower()
    
    print("\n" + "="*60)
    print("🚀 SETUP COMPLETE!")
    print("="*60)
    print("\nTo activate the virtual environment and run the application:")
    print()
    
    if system == "windows":
        print("1. Activate virtual environment:")
        print("   venv\\Scripts\\activate")
        print()
        print("2. Run the application:")
        print("   python main.py")
    else:
        print("1. Activate virtual environment:")
        print("   source venv/bin/activate")
        print()
        print("2. Run the application:")
        print("   python main.py")
    
    print()
    print("3. Open your browser and go to:")
    print("   http://localhost:8080")
    print()
    print("4. To deactivate virtual environment:")
    print("   deactivate")
    print()
    print("📋 Don't forget to configure your .env file with MongoDB credentials!")
    print("="*60)

def offer_windows_options():
    """Offer Windows users different installation options"""
    print("\n🪟 Windows Installation Options:")
    print("1. Basic Installation (Recommended for most Windows users)")
    print("   - No compilation required")
    print("   - Uses rule-based phishing detection")
    print("   - Fastest setup, works on all Windows systems")
    print("\n2. Full Installation (Advanced users with build tools)")
    print("   - Includes machine learning libraries")
    print("   - Requires Microsoft Visual C++ Build Tools")
    print("   - Better detection accuracy")
    
    while True:
        choice = input("\nChoose installation type (1 or 2): ").strip()
        if choice == "1":
            return "requirements-windows-basic.txt", "Windows (Basic - Recommended)"
        elif choice == "2":
            return "requirements-windows.txt", "Windows (Full ML)"
        else:
            print("Please enter 1 or 2")

def main():
    """Main setup function"""
    print("="*60)
    print("🚀 AI Phishing Detection Platform - Cross-Platform Setup")
    print("="*60)
    print("📝 Author: Bigendra Shrestha")
    print("🎓 Project: Final Semester - Cybersecurity & AI")
    print("="*60)
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Detect platform and get appropriate requirements file
    system = platform.system().lower()
    
    if system == "windows":
        requirements_file, platform_name = offer_windows_options()
    else:
        requirements_file, platform_name = detect_platform()
    
    print(f"\n🔍 Platform: {platform_name}")
    print(f"📦 Requirements file: {requirements_file}")
    
    # Check if requirements file exists
    if not Path(requirements_file).exists():
        print(f"❌ Requirements file {requirements_file} not found!")
        print("Please ensure all requirements files are present.")
        return False
    
    # Create virtual environment
    if not create_virtual_environment():
        return False
    
    # Install requirements with fallback for Windows
    success = install_requirements(requirements_file)
    
    # If Windows full installation fails, offer basic installation
    if not success and system == "windows" and requirements_file == "requirements-windows.txt":
        print("\n⚠️  Full installation failed (likely due to missing build tools)")
        print("🔄 Falling back to basic installation...")
        requirements_file = "requirements-windows-basic.txt"
        success = install_requirements(requirements_file)
    
    if not success:
        return False
    
    # Create .env file
    create_env_file()
    
    # Test installation
    if test_installation():
        print("\n🎉 Setup completed successfully!")
        print_activation_instructions()
        return True
    else:
        print("\n❌ Setup completed with errors.")
        print("Please check the installation and try running the application manually.")
        return False

    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            print("\n❌ Setup failed. Please check the error messages above.")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n⏹️  Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error during setup: {e}")
        sys.exit(1)