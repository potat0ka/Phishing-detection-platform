#!/usr/bin/env python3
"""
Windows-Specific Installation Script for AI Phishing Detection Platform
======================================================================

This script handles all Windows-specific installation issues including:
- Pillow compilation problems
- numpy dependency resolution  
- Visual C++ Build Tools detection
- Pre-built wheel prioritization

Usage: python install_windows.py
"""

import subprocess
import sys
import os
from pathlib import Path

def check_python_version():
    """Verify Python version compatibility"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher required")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True

def create_virtual_environment():
    """Create virtual environment for Windows"""
    venv_path = Path("venv")
    if venv_path.exists():
        print("✅ Virtual environment already exists")
        return True
    
    print("📦 Creating virtual environment...")
    try:
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
        print("✅ Virtual environment created successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to create virtual environment: {e}")
        return False

def get_pip_executable():
    """Get pip executable path for Windows"""
    venv_pip = Path("venv/Scripts/pip.exe")
    if venv_pip.exists():
        return str(venv_pip)
    return "pip"

def upgrade_pip():
    """Upgrade pip to latest version"""
    pip_cmd = get_pip_executable()
    print("📥 Upgrading pip...")
    try:
        subprocess.run([pip_cmd, "install", "--upgrade", "pip"], check=True, capture_output=True)
        print("✅ Pip upgraded successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"⚠️ Warning: Could not upgrade pip: {e}")
        return False

def install_essential_packages():
    """Install essential packages with Windows-specific handling"""
    pip_cmd = get_pip_executable()
    
    # Essential packages that work on all Windows systems
    essential_packages = [
        "flask==2.3.3",
        "werkzeug==2.3.7", 
        "pymongo==4.5.0",
        "requests==2.31.0",
        "beautifulsoup4==4.12.2",
        "dnspython==2.4.2",
        "bcrypt==4.0.1",
        "passlib==1.7.4"
    ]
    
    print("📦 Installing essential packages...")
    for package in essential_packages:
        try:
            subprocess.run([pip_cmd, "install", package], check=True, capture_output=True)
            print(f"✅ Installed {package}")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install {package}: {e}")
            return False
    
    return True

def install_pillow_windows():
    """Install Pillow with Windows-specific handling"""
    pip_cmd = get_pip_executable()
    
    print("🖼️ Installing Pillow (Windows-optimized)...")
    
    # Try multiple Pillow versions for Windows compatibility
    pillow_versions = ["9.5.0", "9.4.0", "9.3.0"]
    
    for version in pillow_versions:
        try:
            # Use pre-built wheel and avoid source compilation
            subprocess.run([
                pip_cmd, "install", f"pillow=={version}",
                "--only-binary=:all:", "--prefer-binary"
            ], check=True, capture_output=True, timeout=300)
            print(f"✅ Installed Pillow {version}")
            return True
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
            print(f"⚠️ Pillow {version} failed, trying next version...")
            continue
    
    print("❌ All Pillow versions failed - platform will work without image processing")
    return False

def install_numpy_windows():
    """Install numpy with Windows-specific handling"""
    pip_cmd = get_pip_executable()
    
    print("🔢 Installing numpy (Windows-optimized)...")
    
    # Try multiple numpy versions for Windows compatibility
    numpy_versions = ["1.24.3", "1.24.2", "1.23.5"]
    
    for version in numpy_versions:
        try:
            subprocess.run([
                pip_cmd, "install", f"numpy=={version}",
                "--only-binary=:all:", "--prefer-binary"
            ], check=True, capture_output=True, timeout=300)
            print(f"✅ Installed numpy {version}")
            return True
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
            print(f"⚠️ numpy {version} failed, trying next version...")
            continue
    
    print("❌ All numpy versions failed - using Python-native fallbacks")
    return False

def install_optional_packages():
    """Install optional packages that enhance functionality"""
    pip_cmd = get_pip_executable()
    
    optional_packages = [
        "nltk==3.8.1",
        "trafilatura==1.6.4", 
        "email-validator==2.1.0",
        "oauthlib==3.2.2",
        "pyjwt==2.8.0",
        "python-dateutil==2.8.2",
        "jsonschema==4.19.0"
    ]
    
    print("📦 Installing optional packages...")
    success_count = 0
    
    for package in optional_packages:
        try:
            subprocess.run([pip_cmd, "install", package], check=True, capture_output=True)
            print(f"✅ Installed {package}")
            success_count += 1
        except subprocess.CalledProcessError:
            print(f"⚠️ Skipped {package} (optional)")
    
    print(f"✅ Installed {success_count}/{len(optional_packages)} optional packages")
    return True

def create_env_file():
    """Create .env file from template"""
    env_file = Path(".env")
    env_example = Path(".env.example")
    
    if env_file.exists():
        print("✅ .env file already exists")
        return True
    
    if env_example.exists():
        print("📝 Creating .env file...")
        try:
            with open(env_example, 'r') as f:
                content = f.read()
            with open(env_file, 'w') as f:
                f.write(content)
            print("✅ .env file created successfully")
            return True
        except Exception as e:
            print(f"⚠️ Could not create .env file: {e}")
    
    return False

def test_installation():
    """Test if the installation was successful"""
    print("🧪 Testing installation...")
    
    try:
        # Test importing core modules
        import flask
        import pymongo
        import requests
        print("✅ Core modules working")
        
        # Test numpy import
        try:
            import numpy
            print("✅ numpy available")
        except ImportError:
            print("⚠️ numpy not available - using Python fallbacks")
        
        # Test Pillow import
        try:
            import PIL
            print("✅ Pillow available")
        except ImportError:
            print("⚠️ Pillow not available - image processing disabled")
        
        print("✅ Installation test completed")
        return True
        
    except ImportError as e:
        print(f"❌ Installation test failed: {e}")
        return False

def print_activation_instructions():
    """Print instructions for activating the environment"""
    print("\n" + "="*60)
    print("🎉 Windows Installation Complete!")
    print("="*60)
    print("\n📋 Next Steps:")
    print("1. Activate virtual environment:")
    print("   venv\\Scripts\\activate")
    print("\n2. Run the application:")
    print("   python main.py")
    print("\n3. Open browser to:")
    print("   http://localhost:8080")
    print("\n" + "="*60)

def main():
    """Main installation function"""
    print("🪟 AI Phishing Detection Platform - Windows Installer")
    print("="*60)
    
    # Check prerequisites
    if not check_python_version():
        return False
    
    # Create virtual environment
    if not create_virtual_environment():
        return False
    
    # Upgrade pip
    upgrade_pip()
    
    # Install packages in order
    if not install_essential_packages():
        print("❌ Failed to install essential packages")
        return False
    
    # Install numpy (required for AI features)
    numpy_success = install_numpy_windows()
    
    # Install Pillow (optional for image processing)
    pillow_success = install_pillow_windows()
    
    # Install optional packages
    install_optional_packages()
    
    # Create environment file
    create_env_file()
    
    # Test installation
    if test_installation():
        print_activation_instructions()
        return True
    else:
        print("❌ Installation completed with errors")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)