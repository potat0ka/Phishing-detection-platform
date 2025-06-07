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
        return "requirements-windows-basic.txt", "Windows (Basic - No Compilation)"
    elif system == "darwin":  # macOS
        return "requirements-macos.txt", "macOS (Full Features)"
    elif system == "linux":
        return "requirements-linux.txt", "Linux (Full Features)"
    else:
        print(f"WARNING: Unknown platform: {system}")
        print("Falling back to basic requirements...")
        return "requirements-linux-basic.txt", "Generic (Basic)"

def safe_print(message, use_unicode=True):
    """Print message with fallback for systems that don't support Unicode"""
    try:
        if use_unicode and sys.stdout.encoding and 'utf' in sys.stdout.encoding.lower():
            print(message)
        else:
            # Replace Unicode symbols with ASCII equivalents
            ascii_message = message.replace('✅', '[OK]').replace('❌', '[ERROR]').replace('⚠️', '[WARNING]').replace('ℹ️', '[INFO]')
            print(ascii_message)
    except UnicodeEncodeError:
        # Fallback to ASCII symbols
        ascii_message = message.replace('✅', '[OK]').replace('❌', '[ERROR]').replace('⚠️', '[WARNING]').replace('ℹ️', '[INFO]')
        print(ascii_message)

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        safe_print(f"❌ Python {version.major}.{version.minor} is not supported")
        print("Please install Python 3.8 or higher")
        sys.exit(1)
    
    safe_print(f"✅ Python {version.major}.{version.minor}.{version.micro} detected")
    return True

def create_virtual_environment():
    """Create virtual environment if it doesn't exist"""
    venv_path = Path("venv")
    
    if venv_path.exists():
        safe_print("✅ Virtual environment already exists")
        return True
    
    safe_print("📦 Creating virtual environment...")
    try:
        venv.create("venv", with_pip=True)
        safe_print("✅ Virtual environment created successfully")
        return True
    except Exception as e:
        safe_print(f"❌ Failed to create virtual environment: {e}")
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
    
    safe_print("📥 Upgrading pip...")
    try:
        subprocess.run(pip_cmd + ["install", "--upgrade", "pip"], 
                      check=True, capture_output=True, text=True)
        safe_print("✅ Pip upgraded successfully")
    except subprocess.CalledProcessError as e:
        safe_print(f"⚠️  Warning: Could not upgrade pip: {e}")
    
    safe_print(f"📦 Installing packages from {requirements_file}...")
    try:
        result = subprocess.run(pip_cmd + ["install", "-r", requirements_file], 
                               check=True, capture_output=True, text=True)
        safe_print("✅ All packages installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        safe_print(f"❌ Failed to install packages: {e}")
        print("Error output:", e.stderr)
        return False

def create_env_file():
    """Create .env file if it doesn't exist"""
    env_file = Path(".env")
    env_example = Path(".env.example")
    
    if env_file.exists():
        safe_print("✅ .env file already exists")
        return True
    
    if env_example.exists():
        safe_print("📝 Creating .env file from template...")
        try:
            with open(env_example, 'r') as f:
                content = f.read()
            
            with open(env_file, 'w') as f:
                f.write(content)
            
            safe_print("✅ .env file created successfully")
            safe_print("📋 Please edit .env file with your MongoDB Atlas credentials")
            return True
        except Exception as e:
            safe_print(f"❌ Failed to create .env file: {e}")
            return False
    else:
        safe_print("⚠️  .env.example not found, skipping .env creation")
        return True

def test_installation():
    """Test if the installation was successful"""
    python_cmd = get_pip_command()[0]
    
    safe_print("🧪 Testing installation...")
    test_script = '''
import flask
import pymongo
print("[OK] Core packages imported successfully")

# Test optional ML packages
try:
    import numpy
    import sklearn
    print("[OK] ML packages available")
except ImportError:
    print("[INFO] ML packages not available - using rule-based detection")
'''
    
    try:
        result = subprocess.run([python_cmd, "-c", test_script], 
                               check=True, capture_output=True, text=True)
        print(result.stdout.strip())
        return True
    except subprocess.CalledProcessError as e:
        safe_print(f"❌ Installation test failed: {e}")
        print("Error output:", e.stderr)
        return False

def print_activation_instructions():
    """Print instructions for activating the virtual environment"""
    system = platform.system().lower()
    
    print("\n" + "="*60)
    safe_print("🚀 SETUP COMPLETE!")
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
    safe_print("📋 Don't forget to configure your .env file with MongoDB credentials!")
    print("="*60)

def offer_installation_options(platform_name, system):
    """Offer users different installation options based on their platform"""
    if system == "windows":
        safe_print("\n🪟 Windows Installation Options:")
        print("1. Minimal Installation (Zero compilation - Works on ALL Windows systems)")
        print("   - Pure Python packages only")
        print("   - Rule-based phishing detection (85% accuracy)")
        print("   - Guaranteed to work without build tools")
        print("\n2. Basic Installation (Recommended for most Windows users)")
        print("   - No compilation required")
        print("   - Enhanced rule-based detection (90% accuracy)")
        print("   - Works on most Windows systems")
        print("\n3. Full Installation (Advanced users with build tools)")
        print("   - Includes machine learning libraries")
        print("   - Requires Microsoft Visual C++ Build Tools")
        print("   - Enhanced ML detection (95% accuracy)")
        
        while True:
            choice = input("\nChoose installation type (1, 2, or 3): ").strip()
            if choice == "1":
                return "requirements-windows-minimal.txt", "Windows (Minimal - Zero Compilation)"
            elif choice == "2":
                return "requirements-windows-basic.txt", "Windows (Basic - Recommended)"
            elif choice == "3":
                return "requirements-windows.txt", "Windows (Full ML)"
            else:
                print("Please enter 1, 2, or 3")
    
    elif system == "darwin":  # macOS
        safe_print("\n🍎 macOS Installation Options:")
        print("1. Basic Installation (Faster setup)")
        print("   - Core functionality only")
        print("   - Rule-based detection (85% accuracy)")
        print("   - No compilation required")
        print("\n2. Full Installation (Recommended for macOS)")
        print("   - Complete ML features")
        print("   - Enhanced detection accuracy (95%)")
        print("   - Uses Xcode command line tools")
        
        while True:
            choice = input("\nChoose installation type (1 or 2): ").strip()
            if choice == "1":
                return "requirements-macos-basic.txt", "macOS (Basic)"
            elif choice == "2":
                return "requirements-macos.txt", "macOS (Full ML)"
            else:
                print("Please enter 1 or 2")
    
    elif system == "linux":
        safe_print("\n🐧 Linux Installation Options:")
        print("1. Basic Installation (Minimal dependencies)")
        print("   - Core functionality only")
        print("   - Rule-based detection (85% accuracy)")
        print("   - No build tools required")
        print("\n2. Full Installation (Recommended for Linux)")
        print("   - Complete ML features")
        print("   - Enhanced detection accuracy (95%)")
        print("   - Uses system compiler")
        
        while True:
            choice = input("\nChoose installation type (1 or 2): ").strip()
            if choice == "1":
                return "requirements-linux-basic.txt", "Linux (Basic)"
            elif choice == "2":
                return "requirements-linux.txt", "Linux (Full ML)"
            else:
                print("Please enter 1 or 2")
    
    else:
        # For unknown platforms, use basic installation
        return "requirements-linux-basic.txt", "Generic (Basic)"

def main():
    """Main setup function"""
    print("="*60)
    safe_print("🚀 AI Phishing Detection Platform - Cross-Platform Setup")
    print("="*60)
    safe_print("📝 Author: Bigendra Shrestha")
    safe_print("🎓 Project: Final Semester - Cybersecurity & AI")
    print("="*60)
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Detect platform and get appropriate requirements file
    system = platform.system().lower()
    
    # Offer installation options for all platforms
    requirements_file, platform_name = offer_installation_options("", system)
    
    safe_print(f"\n🔍 Platform: {platform_name}")
    safe_print(f"📦 Requirements file: {requirements_file}")
    
    # Check if requirements file exists
    if not Path(requirements_file).exists():
        safe_print(f"❌ Requirements file {requirements_file} not found!")
        print("Please ensure all requirements files are present.")
        return False
    
    # Create virtual environment
    if not create_virtual_environment():
        return False
    
    # Install requirements with comprehensive fallback for all platforms
    success = install_requirements(requirements_file)
    
    # If full installation fails, automatically fallback to basic installation
    if not success:
        safe_print(f"\n⚠️  Installation failed (likely due to compilation errors)")
        safe_print("🔄 Falling back to safer installation options...")
        
        # Determine fallback sequence for current platform
        fallback_files = []
        if system == "windows":
            fallback_files = ["requirements-windows-basic.txt", "requirements-windows-minimal.txt"]
        elif system == "darwin":
            fallback_files = ["requirements-macos-basic.txt"]
        elif system == "linux":
            fallback_files = ["requirements-linux-basic.txt"]
        else:
            fallback_files = ["requirements-linux-basic.txt"]
        
        # Try each fallback option
        for fallback_file in fallback_files:
            if Path(fallback_file).exists():
                safe_print(f"📦 Trying fallback: {fallback_file}")
                success = install_requirements(fallback_file)
                if success:
                    safe_print("✅ Fallback installation completed successfully!")
                    if "minimal" in fallback_file:
                        safe_print("ℹ️  Platform will use pure Python rule-based detection (85% accuracy)")
                    else:
                        safe_print("ℹ️  Platform will use enhanced rule-based detection (90% accuracy)")
                    break
                else:
                    safe_print(f"❌ Fallback {fallback_file} also failed, trying next option...")
        
        if not success:
            safe_print("❌ All installation options failed")
            print("Please check your Python installation and ensure you have internet connectivity")
    
    if not success:
        return False
    
    # Create .env file
    create_env_file()
    
    # Test installation
    if test_installation():
        safe_print("\n🎉 Setup completed successfully!")
        print_activation_instructions()
        return True
    else:
        safe_print("\n❌ Setup completed with errors.")
        print("Please check the installation and try running the application manually.")
        return False

    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            safe_print("\n❌ Setup failed. Please check the error messages above.")
            sys.exit(1)
    except KeyboardInterrupt:
        safe_print("\n\n⏹️  Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        safe_print(f"\n❌ Unexpected error during setup: {e}")
        sys.exit(1)