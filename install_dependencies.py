#!/usr/bin/env python3
"""
AI Phishing Detection Platform - Dependency Installer
====================================================

This script automatically installs all required dependencies for the AI Phishing Detection Platform.
It creates a virtual environment and installs packages with proper error handling.

Usage:
    python install_dependencies.py

Author: Bigendra Shrestha
Project: AI Phishing Detection Platform
"""

import subprocess
import sys
import os
import platform
from pathlib import Path

class DependencyInstaller:
    def __init__(self):
        self.python_cmd = self._get_python_command()
        self.pip_cmd = f"{self.python_cmd} -m pip"
        self.system = platform.system().lower()
        self.venv_path = Path("venv")
        
        # Core dependencies with specific versions for stability
        self.dependencies = [
            # Core web framework
            "flask==2.3.3",
            "werkzeug==2.3.7",
            
            # Database connectivity
            "flask-pymongo==2.3.0", 
            "pymongo==4.5.0",
            "dnspython==2.4.2",
            
            # Security and authentication
            "bcrypt==4.0.1",
            "passlib==1.7.4",
            "cryptography==41.0.7",
            
            # Machine learning and AI
            "scikit-learn==1.3.2",
            "nltk==3.8.1",
            "numpy==1.24.3",
            
            # Web scraping and processing
            "requests==2.31.0",
            "beautifulsoup4==4.12.2",
            "trafilatura==1.6.4",
            
            # Image and file processing
            "pillow==9.5.0",
            
            # Data validation
            "email-validator==2.1.0",
            "bleach==6.1.0"
        ]
        
        # Optional dependencies for enhanced features
        self.optional_dependencies = [
            "python-dotenv==1.0.0",
            "openai==0.28.1"
        ]

    def _get_python_command(self):
        """Determine the correct Python command for the system"""
        try:
            # Try python3 first (preferred on Unix systems)
            subprocess.run([sys.executable, "--version"], check=True, capture_output=True)
            return sys.executable
        except:
            # Fallback to python
            return "python"

    def _run_command(self, command, description="Running command"):
        """Execute a command with error handling"""
        print(f"🔄 {description}...")
        print(f"   Command: {command}")
        
        try:
            result = subprocess.run(
                command.split(),
                check=True,
                capture_output=True,
                text=True
            )
            print(f"✅ {description} completed successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ {description} failed:")
            print(f"   Error: {e.stderr}")
            return False
        except Exception as e:
            print(f"❌ Unexpected error during {description}: {e}")
            return False

    def check_python_version(self):
        """Verify Python version compatibility"""
        print("🔍 Checking Python version...")
        
        version = sys.version_info
        if version.major < 3 or (version.major == 3 and version.minor < 8):
            print(f"❌ Python {version.major}.{version.minor} detected")
            print("   This project requires Python 3.8 or higher")
            print("   Please install a newer version of Python")
            return False
        
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} detected - Compatible")
        return True

    def create_virtual_environment(self):
        """Create a virtual environment for the project"""
        if self.venv_path.exists():
            print("📁 Virtual environment already exists")
            return True
            
        print("🏗️  Creating virtual environment...")
        return self._run_command(
            f"{self.python_cmd} -m venv venv",
            "Creating virtual environment"
        )

    def get_venv_python(self):
        """Get the Python executable from virtual environment"""
        if self.system == "windows":
            return str(self.venv_path / "Scripts" / "python.exe")
        else:
            return str(self.venv_path / "bin" / "python")

    def get_venv_pip(self):
        """Get the pip executable from virtual environment"""
        venv_python = self.get_venv_python()
        return f"{venv_python} -m pip"

    def upgrade_pip(self):
        """Upgrade pip to the latest version"""
        venv_pip = self.get_venv_pip()
        return self._run_command(
            f"{venv_pip} install --upgrade pip",
            "Upgrading pip"
        )

    def install_dependencies(self):
        """Install all required dependencies"""
        print("📦 Installing core dependencies...")
        venv_pip = self.get_venv_pip()
        
        # Install dependencies one by one for better error reporting
        failed_packages = []
        
        for package in self.dependencies:
            print(f"   Installing {package}...")
            success = self._run_command(
                f"{venv_pip} install {package}",
                f"Installing {package}"
            )
            if not success:
                failed_packages.append(package)
        
        if failed_packages:
            print(f"⚠️  Some packages failed to install: {failed_packages}")
            print("   The application may still work with reduced functionality")
            return False
        
        print("✅ All core dependencies installed successfully")
        return True

    def install_optional_dependencies(self):
        """Install optional dependencies with error tolerance"""
        print("🔧 Installing optional dependencies...")
        venv_pip = self.get_venv_pip()
        
        for package in self.optional_dependencies:
            print(f"   Installing optional package {package}...")
            success = self._run_command(
                f"{venv_pip} install {package}",
                f"Installing optional {package}"
            )
            if not success:
                print(f"   ⚠️  Optional package {package} failed - continuing...")

    def verify_installation(self):
        """Verify that key packages are installed correctly"""
        print("🔍 Verifying installation...")
        venv_python = self.get_venv_python()
        
        test_imports = [
            "flask",
            "pymongo", 
            "sklearn",
            "nltk",
            "requests",
            "bcrypt"
        ]
        
        failed_imports = []
        
        for module in test_imports:
            try:
                result = subprocess.run(
                    [venv_python, "-c", f"import {module}; print(f'{module}: OK')"],
                    check=True,
                    capture_output=True,
                    text=True
                )
                print(f"   ✅ {module}: OK")
            except subprocess.CalledProcessError:
                print(f"   ❌ {module}: Failed to import")
                failed_imports.append(module)
        
        if failed_imports:
            print(f"⚠️  Some modules failed verification: {failed_imports}")
            return False
        
        print("✅ All modules verified successfully")
        return True

    def create_activation_scripts(self):
        """Create convenient activation scripts"""
        print("📝 Creating activation scripts...")
        
        # Windows activation script
        if self.system == "windows":
            activate_script = """@echo off
echo Activating AI Phishing Detection Platform environment...
call venv\\Scripts\\activate.bat
echo Environment activated! You can now run: python main.py
cmd /k
"""
            with open("activate.bat", "w") as f:
                f.write(activate_script)
            print("   ✅ Created activate.bat for Windows")
        
        # Unix activation script
        activate_script = """#!/bin/bash
echo "Activating AI Phishing Detection Platform environment..."
source venv/bin/activate
echo "Environment activated! You can now run: python main.py"
exec bash
"""
        with open("activate.sh", "w") as f:
            f.write(activate_script)
        
        # Make executable on Unix systems
        if self.system != "windows":
            os.chmod("activate.sh", 0o755)
            print("   ✅ Created activate.sh for Unix systems")

    def print_next_steps(self):
        """Print instructions for next steps"""
        print("\n" + "="*60)
        print("🎉 INSTALLATION COMPLETED SUCCESSFULLY!")
        print("="*60)
        print("\n📋 Next Steps:")
        print("1. Activate the virtual environment:")
        
        if self.system == "windows":
            print("   Windows: Double-click activate.bat OR run 'venv\\Scripts\\activate'")
        else:
            print("   Unix/Linux/macOS: Run './activate.sh' OR 'source venv/bin/activate'")
        
        print("\n2. Configure environment (optional):")
        print("   Copy .env.template to .env and edit with your settings")
        
        print("\n3. Run the application:")
        if self.system == "windows":
            print("   venv\\Scripts\\python main.py")
        else:
            print("   venv/bin/python main.py")
        
        print("\n4. Access the platform:")
        print("   Open http://localhost:8080 in your browser")
        
        print("\n5. Default login credentials:")
        print("   Email: testuser@example.com")
        print("   Password: password123")
        
        print("\n🔧 Troubleshooting:")
        print("   - If packages fail to install, try updating pip: pip install --upgrade pip")
        print("   - For permission issues on Unix, try: sudo python install_dependencies.py")
        print("   - For network issues, try: pip install --trusted-host pypi.org --trusted-host pypi.python.org")
        
        print("\n📚 Documentation:")
        print("   Check README.md for detailed setup and usage instructions")

def main():
    """Main installation function"""
    print("🛡️  AI Phishing Detection Platform - Dependency Installer")
    print("="*60)
    print("This script will install all required dependencies for the platform.")
    print("Estimated time: 2-5 minutes depending on your internet connection.")
    print("="*60)
    
    installer = DependencyInstaller()
    
    # Step 1: Check Python version
    if not installer.check_python_version():
        sys.exit(1)
    
    # Step 2: Create virtual environment
    if not installer.create_virtual_environment():
        print("❌ Failed to create virtual environment")
        sys.exit(1)
    
    # Step 3: Upgrade pip
    if not installer.upgrade_pip():
        print("⚠️  Failed to upgrade pip, continuing anyway...")
    
    # Step 4: Install dependencies
    if not installer.install_dependencies():
        print("❌ Critical dependencies failed to install")
        response = input("Continue with optional dependencies? (y/n): ").lower()
        if response != 'y':
            sys.exit(1)
    
    # Step 5: Install optional dependencies
    installer.install_optional_dependencies()
    
    # Step 6: Verify installation
    if not installer.verify_installation():
        print("⚠️  Some modules failed verification")
        print("The application may still work, but some features might be limited")
    
    # Step 7: Create activation scripts
    installer.create_activation_scripts()
    
    # Step 8: Print next steps
    installer.print_next_steps()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n❌ Installation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error during installation: {e}")
        print("Please check the error message above and try again")
        sys.exit(1)