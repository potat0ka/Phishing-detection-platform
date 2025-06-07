#!/usr/bin/env python3
"""
AI Phishing Detection Platform - Dependency Installer
====================================================

This script automatically installs all required dependencies for the platform.
It works on Windows, macOS, and Linux systems.

Usage:
    python install_dependencies.py

Features:
- Automatic virtual environment creation
- Cross-platform compatibility
- Dependency verification
- Error handling and troubleshooting
"""

import subprocess
import sys
import os
import platform
from pathlib import Path

# Required packages with versions
REQUIRED_PACKAGES = [
    "flask==2.3.3",
    "pymongo==4.5.0", 
    "requests==2.31.0",
    "scikit-learn==1.3.2",
    "nltk==3.8.1",
    "beautifulsoup4==4.12.2",
    "bcrypt==4.0.1",
    "pillow==9.5.0",
    "email-validator==2.1.0",
    "trafilatura==1.6.4",
    "dnspython==2.4.2",
    "passlib==1.7.4",
    "cryptography==41.0.7",
    "werkzeug==2.3.7"
]

def print_banner():
    """Print installation banner"""
    print("=" * 60)
    print("AI Phishing Detection Platform - Dependency Installer")
    print("=" * 60)
    print(f"Platform: {platform.system()} {platform.release()}")
    print(f"Python: {sys.version}")
    print("=" * 60)

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("ERROR: Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        print("Please upgrade Python and try again")
        sys.exit(1)
    
    print(f"✓ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro} - Compatible")

def create_virtual_environment():
    """Create virtual environment if it doesn't exist"""
    venv_path = Path("venv")
    
    if venv_path.exists():
        print("✓ Virtual environment already exists")
        return True
    
    print("Creating virtual environment...")
    try:
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
        print("✓ Virtual environment created successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to create virtual environment: {e}")
        return False

def get_pip_command():
    """Get the correct pip command for the platform"""
    system = platform.system()
    
    if system == "Windows":
        return os.path.join("venv", "Scripts", "pip.exe")
    else:
        return os.path.join("venv", "bin", "pip")

def install_packages():
    """Install all required packages"""
    pip_cmd = get_pip_command()
    
    if not os.path.exists(pip_cmd):
        print("✗ Virtual environment pip not found")
        print("Please ensure virtual environment was created successfully")
        return False
    
    print("Installing required packages...")
    print("This may take a few minutes...")
    
    # Upgrade pip first
    try:
        subprocess.run([pip_cmd, "install", "--upgrade", "pip"], check=True, capture_output=True)
        print("✓ pip upgraded successfully")
    except subprocess.CalledProcessError:
        print("⚠ Warning: Could not upgrade pip, continuing...")
    
    # Install packages
    failed_packages = []
    
    for package in REQUIRED_PACKAGES:
        try:
            print(f"Installing {package}...")
            subprocess.run([pip_cmd, "install", package], check=True, capture_output=True)
            print(f"✓ {package} installed")
        except subprocess.CalledProcessError as e:
            print(f"✗ Failed to install {package}")
            failed_packages.append(package)
    
    if failed_packages:
        print(f"\n⚠ Warning: {len(failed_packages)} packages failed to install:")
        for package in failed_packages:
            print(f"  - {package}")
        
        print("\nTrying alternative installation method...")
        try:
            subprocess.run([pip_cmd, "install"] + failed_packages, check=True)
            print("✓ Alternative installation successful")
            failed_packages = []
        except subprocess.CalledProcessError:
            print("✗ Alternative installation also failed")
    
    return len(failed_packages) == 0

def verify_installation():
    """Verify that packages are properly installed"""
    pip_cmd = get_pip_command()
    
    print("\nVerifying installation...")
    
    essential_packages = ["flask", "pymongo", "scikit-learn", "nltk", "beautifulsoup4"]
    
    for package in essential_packages:
        try:
            subprocess.run([pip_cmd, "show", package], check=True, capture_output=True)
            print(f"✓ {package} verified")
        except subprocess.CalledProcessError:
            print(f"✗ {package} not found")
            return False
    
    return True

def print_next_steps():
    """Print instructions for next steps"""
    system = platform.system()
    
    print("\n" + "=" * 60)
    print("Installation Complete!")
    print("=" * 60)
    
    print("\nTo activate the virtual environment:")
    if system == "Windows":
        print("  venv\\Scripts\\activate")
    else:
        print("  source venv/bin/activate")
    
    print("\nTo run the application:")
    print("  python main.py")
    
    print("\nTo deactivate the virtual environment when done:")
    print("  deactivate")
    
    print("\nDefault login credentials:")
    print("  Super Admin: super_admin / SuperAdmin123!")
    print("  Sub Admin: potato / potato123")
    print("  Regular User: user / user123")
    
    print("\nThe application will be available at: http://localhost:8080")

def main():
    """Main installation process"""
    print_banner()
    
    # Check Python version
    check_python_version()
    
    # Create virtual environment
    if not create_virtual_environment():
        print("\nInstallation failed at virtual environment creation")
        sys.exit(1)
    
    # Install packages
    if not install_packages():
        print("\nInstallation completed with warnings")
        print("Some packages may not have installed correctly")
        print("The application may still work with reduced functionality")
    
    # Verify installation
    if verify_installation():
        print("\n✓ All essential packages verified successfully")
    else:
        print("\n⚠ Some essential packages could not be verified")
        print("The application may not work correctly")
    
    # Print next steps
    print_next_steps()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInstallation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nUnexpected error during installation: {e}")
        print("Please check your Python installation and try again")
        sys.exit(1)