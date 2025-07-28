#!/usr/bin/env python3
"""
Dependency Installation Script for AI Phishing Detection Platform
===============================================================

This script automatically installs all required dependencies for the
AI Phishing Detection Platform. It handles Python packages, system
dependencies, and environment setup.

Author: Bigendra Shrestha
Created: 2024
License: MIT
"""

import subprocess
import sys
import os
import platform
from pathlib import Path

class DependencyInstaller:
    """Handles automated dependency installation for the platform"""
    
    def __init__(self):
        self.python_cmd = self._get_python_command()
        self.pip_cmd = f"{self.python_cmd} -m pip"
        
    def _get_python_command(self):
        """Detect the correct Python command"""
        commands = ['python3', 'python']
        for cmd in commands:
            try:
                result = subprocess.run([cmd, '--version'], 
                                      capture_output=True, text=True)
                if result.returncode == 0 and 'Python 3' in result.stdout:
                    return cmd
            except FileNotFoundError:
                continue
        raise RuntimeError("Python 3 is required but not found")
    
    def run_command(self, command, description=""):
        """Execute a system command with error handling"""
        print(f"{'='*60}")
        print(f"📦 {description}")
        print(f"🔧 Running: {command}")
        print(f"{'='*60}")
        
        try:
            result = subprocess.run(command, shell=True, check=True,
                                  capture_output=True, text=True)
            if result.stdout:
                print(result.stdout)
            print("✅ Success!")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Error: {e}")
            if e.stderr:
                print(f"Error details: {e.stderr}")
            return False
    
    def check_python_version(self):
        """Verify Python version compatibility"""
        print("🔍 Checking Python version...")
        version = sys.version_info
        if version.major < 3 or (version.major == 3 and version.minor < 8):
            raise RuntimeError(f"Python 3.8+ required, found {version.major}.{version.minor}")
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} found")
    
    def install_pip_dependencies(self):
        """Install Python packages from requirements"""
        requirements = [
            "flask>=2.3.0",
            "pymongo>=4.5.0",
            "flask-login>=0.6.0",
            "bcrypt>=4.0.0",
            "werkzeug>=2.3.0",
            "requests>=2.31.0",
            "beautifulsoup4>=4.12.0",
            "scikit-learn>=1.3.0",
            "nltk>=3.8.0",
            "pillow>=10.0.0",
            "opencv-python>=4.8.0",
            "librosa>=0.10.0",
            "soundfile>=0.12.0",
            "pytesseract>=0.3.10",
            "python-docx>=0.8.11",
            "pdfplumber>=0.10.0",
            "trafilatura>=1.6.0",
            "cryptography>=41.0.0",
            "email-validator>=2.0.0",
            "dnspython>=2.4.0",
            "passlib>=1.7.4",
            "imagehash>=4.3.1",
            "psycopg2-binary>=2.9.7"
        ]
        
        # Upgrade pip first
        self.run_command(f"{self.pip_cmd} install --upgrade pip", 
                        "Upgrading pip to latest version")
        
        # Install packages
        for package in requirements:
            if not self.run_command(f"{self.pip_cmd} install {package}", 
                                   f"Installing {package}"):
                print(f"⚠️  Warning: Failed to install {package}")
    
    def install_system_dependencies(self):
        """Install system-level dependencies based on OS"""
        system = platform.system().lower()
        
        if system == "linux":
            self._install_linux_deps()
        elif system == "darwin":  # macOS
            self._install_macos_deps()
        elif system == "windows":
            self._install_windows_deps()
        else:
            print(f"⚠️  Unknown system: {system}. Manual installation may be required.")
    
    def _install_linux_deps(self):
        """Install Linux system dependencies"""
        deps = [
            "tesseract-ocr",
            "tesseract-ocr-eng",
            "ffmpeg",
            "libsndfile1",
            "portaudio19-dev",
            "python3-dev",
            "build-essential"
        ]
        
        # Try different package managers
        if self._command_exists("apt-get"):
            self.run_command("sudo apt-get update", "Updating package list")
            for dep in deps:
                self.run_command(f"sudo apt-get install -y {dep}", 
                               f"Installing {dep}")
        elif self._command_exists("yum"):
            for dep in deps:
                self.run_command(f"sudo yum install -y {dep}", 
                               f"Installing {dep}")
        elif self._command_exists("pacman"):
            for dep in deps:
                self.run_command(f"sudo pacman -S --noconfirm {dep}", 
                               f"Installing {dep}")
    
    def _install_macos_deps(self):
        """Install macOS system dependencies"""
        if not self._command_exists("brew"):
            print("🍺 Installing Homebrew...")
            install_cmd = '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
            self.run_command(install_cmd, "Installing Homebrew package manager")
        
        deps = ["tesseract", "ffmpeg", "portaudio"]
        for dep in deps:
            self.run_command(f"brew install {dep}", f"Installing {dep}")
    
    def _install_windows_deps(self):
        """Install Windows system dependencies"""
        print("🪟 Windows detected")
        print("Please manually install the following:")
        print("1. Tesseract OCR: https://github.com/UB-Mannheim/tesseract/wiki")
        print("2. FFmpeg: https://ffmpeg.org/download.html")
        print("3. Visual Studio Build Tools: https://visualstudio.microsoft.com/downloads/")
    
    def _command_exists(self, command):
        """Check if a system command exists"""
        try:
            subprocess.run([command, "--version"], 
                          capture_output=True, check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
    
    def create_data_directories(self):
        """Create necessary data directories"""
        directories = [
            "data",
            "logs",
            "uploads",
            "static/uploads",
            "models"
        ]
        
        for directory in directories:
            Path(directory).mkdir(parents=True, exist_ok=True)
            print(f"📁 Created directory: {directory}")
    
    def setup_environment(self):
        """Set up environment variables and configuration"""
        env_example = Path(".env.example")
        env_file = Path(".env")
        
        if env_example.exists() and not env_file.exists():
            print("📝 Creating environment configuration...")
            with open(env_example, 'r') as f:
                content = f.read()
            
            with open(env_file, 'w') as f:
                f.write(content)
            print("✅ Created .env file from template")
            print("⚠️  Please edit .env file with your MongoDB connection string")
    
    def verify_installation(self):
        """Verify that key dependencies are working"""
        print("\n🔍 Verifying installation...")
        
        tests = [
            (f"{self.python_cmd} -c 'import flask; print(flask.__version__)'", "Flask"),
            (f"{self.python_cmd} -c 'import pymongo; print(pymongo.__version__)'", "PyMongo"),
            (f"{self.python_cmd} -c 'import cv2; print(cv2.__version__)'", "OpenCV"),
            (f"{self.python_cmd} -c 'import sklearn; print(sklearn.__version__)'", "Scikit-learn"),
        ]
        
        for test_cmd, name in tests:
            if self.run_command(test_cmd, f"Testing {name}"):
                print(f"✅ {name} working correctly")
            else:
                print(f"❌ {name} test failed")

def main():
    """Main installation process"""
    print("🚀 AI Phishing Detection Platform - Dependency Installer")
    print("=" * 60)
    print("Author: Bigendra Shrestha")
    print("This script will install all required dependencies")
    print("=" * 60)
    
    installer = DependencyInstaller()
    
    try:
        # Check Python version
        installer.check_python_version()
        
        # Install Python dependencies
        print("\n📦 Installing Python packages...")
        installer.install_pip_dependencies()
        
        # Install system dependencies
        print("\n🔧 Installing system dependencies...")
        installer.install_system_dependencies()
        
        # Create directories
        print("\n📁 Setting up directories...")
        installer.create_data_directories()
        
        # Setup environment
        print("\n⚙️  Setting up environment...")
        installer.setup_environment()
        
        # Verify installation
        installer.verify_installation()
        
        print("\n🎉 Installation completed successfully!")
        print("\n📋 Next steps:")
        print("1. Edit .env file with your MongoDB connection string")
        print("2. Run: python main.py")
        print("3. Open browser to: http://localhost:8080")
        
    except Exception as e:
        print(f"\n❌ Installation failed: {e}")
        print("Please check the error messages above and try again.")
        sys.exit(1)

if __name__ == "__main__":
    main()