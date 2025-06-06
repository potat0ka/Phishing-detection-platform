# AI Phishing Detection Platform

A comprehensive AI-powered cybersecurity platform that detects phishing attacks and AI-generated threats using machine learning algorithms.

**Author**: Bigendra Shrestha  
**Purpose**: Final Semester Project - Cybersecurity & AI  
**Institution**: [Your Institution Name]  
**Year**: 2024-2025

## 📋 Overview

This platform provides real-time protection against:
- Phishing URLs and malicious websites
- Suspicious email content
- AI-generated content (images, videos, audio, text)
- Social engineering attacks
- Educational cybersecurity resources

## 🔧 System Requirements

- **Python**: 3.11 or higher
- **RAM**: 2GB minimum, 4GB recommended
- **Storage**: 1GB free space
- **Internet**: Required for MongoDB Atlas (optional)
- **Browser**: Chrome, Firefox, Safari, or Edge

## 🚀 Cross-Platform Installation Guide

### Windows Installation

#### Step 1: Install Python
```powershell
# Option 1: Download from python.org
# Visit https://python.org/downloads and download Python 3.11+
# During installation, check "Add Python to PATH"

# Option 2: Using winget (Windows 10/11)
winget install Python.Python.3.11

# Verify installation
python --version
pip --version
```

#### Step 2: Clone Repository
```powershell
# Install Git if not already installed
winget install Git.Git

# Clone the project
git clone https://github.com/your-username/ai-phishing-detection-platform.git
cd ai-phishing-detection-platform
```

#### Step 3: Setup Virtual Environment (Recommended)
```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# You should see (venv) in your command prompt
```

#### Step 4: Install Dependencies
```powershell
# Install all required packages
pip install -r requirements-local.txt

# If you encounter permission errors, try:
pip install --user -r requirements-local.txt
```

#### Step 5: Run the Application
```powershell
# Start the backend server
python main.py

# You should see output like:
# * Running on http://127.0.0.1:5000
# * Debug mode: on
```

### macOS Installation

#### Step 1: Install Python and Git
```bash
# Install Homebrew (if not already installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python 3.11
brew install python@3.11

# Install Git
brew install git

# Verify installation
python3 --version
pip3 --version
```

#### Step 2: Clone Repository
```bash
# Clone the project
git clone https://github.com/your-username/ai-phishing-detection-platform.git
cd ai-phishing-detection-platform
```

#### Step 3: Setup Virtual Environment (Recommended)
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# You should see (venv) in your terminal prompt
```

#### Step 4: Install Dependencies
```bash
# Install all required packages
pip install -r requirements-local.txt

# If you encounter issues with some packages:
brew install cmake  # For some ML packages
pip install -r requirements-local.txt
```

#### Step 5: Run the Application
```bash
# Start the backend server
python main.py

# Open browser to http://localhost:5000
open http://localhost:5000
```

### Ubuntu/Debian Linux Installation

#### Step 1: Update System and Install Dependencies
```bash
# Update package list
sudo apt update && sudo apt upgrade -y

# Install Python 3.11 and dependencies
sudo apt install python3.11 python3.11-pip python3.11-venv python3.11-dev
sudo apt install git build-essential

# Create symbolic links (if needed)
sudo ln -sf /usr/bin/python3.11 /usr/bin/python3
sudo ln -sf /usr/bin/pip3 /usr/bin/pip

# Verify installation
python3 --version
pip --version
```

#### Step 2: Clone Repository
```bash
# Clone the project
git clone https://github.com/your-username/ai-phishing-detection-platform.git
cd ai-phishing-detection-platform
```

#### Step 3: Setup Virtual Environment (Recommended)
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# You should see (venv) in your terminal prompt
```

#### Step 4: Install Dependencies
```bash
# Update pip first
pip install --upgrade pip

# Install all required packages
pip install -r requirements-local.txt

# If you encounter build errors:
sudo apt install python3-dev libpq-dev
pip install -r requirements-local.txt
```

#### Step 5: Run the Application
```bash
# Start the backend server
python main.py

# Open browser manually to http://localhost:5000
```

### Arch Linux Installation

#### Step 1: Install Python and Dependencies
```bash
# Update system
sudo pacman -Syu

# Install Python and Git
sudo pacman -S python python-pip git base-devel

# Install additional dependencies for ML packages
sudo pacman -S python-numpy python-scipy python-pillow

# Verify installation
python --version
pip --version
```

#### Step 2: Clone Repository
```bash
# Clone the project
git clone https://github.com/your-username/ai-phishing-detection-platform.git
cd ai-phishing-detection-platform
```

#### Step 3: Setup Virtual Environment (Recommended)
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate

# You should see (venv) in your terminal prompt
```

#### Step 4: Install Dependencies
```bash
# Update pip first
pip install --upgrade pip

# Install all required packages
pip install -r requirements-local.txt

# If you encounter issues:
sudo pacman -S python-wheel python-setuptools
pip install -r requirements-local.txt
```

#### Step 5: Run the Application
```bash
# Start the backend server
python main.py

# Application will be available at http://localhost:5000
```

## 🗄️ MongoDB Database Setup

### Option 1: Local MongoDB Installation

#### Windows
```powershell
# Download MongoDB Community Server from mongodb.com
# Install using the .msi installer
# Start MongoDB service
net start MongoDB

# Verify installation
mongosh --version
```

#### macOS
```bash
# Install MongoDB using Homebrew
brew tap mongodb/brew
brew install mongodb-community

# Start MongoDB service
brew services start mongodb/brew/mongodb-community

# Verify installation
mongosh --version
```

#### Linux (Ubuntu/Debian)
```bash
# Import MongoDB public GPG key
wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | sudo apt-key add -

# Add MongoDB repository
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/6.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list

# Update package list and install
sudo apt update
sudo apt install mongodb-org

# Start MongoDB service
sudo systemctl start mongod
sudo systemctl enable mongod

# Verify installation
mongosh --version
```

#### Arch Linux
```bash
# Install MongoDB from AUR
yay -S mongodb-bin  # or use your preferred AUR helper

# Start MongoDB service
sudo systemctl start mongodb
sudo systemctl enable mongodb

# Verify installation
mongosh --version
```

### Option 2: MongoDB Atlas (Cloud Database)

1. **Create Account**: Visit [mongodb.com/atlas](https://mongodb.com/atlas) and create free account
2. **Create Cluster**: Click "Build a Database" and choose free tier
3. **Setup Access**: 
   - Create database user with username and password
   - Add your IP address to whitelist (or use 0.0.0.0/0 for all IPs)
4. **Get Connection String**: Click "Connect" → "Connect your application" → Copy connection string

### Database Configuration

#### Step 1: Create Environment File
```bash
# Create .env file in project root
touch .env
```

#### Step 2: Add Database Configuration
```env
# For Local MongoDB
MONGODB_URI=mongodb://localhost:27017/phishing_detection

# For MongoDB Atlas (replace with your connection string)
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/phishing_detection

# Security Settings (optional - auto-generated if not provided)
SESSION_SECRET=your-secure-session-secret-key-here
USER_ENCRYPTION_SECRET=your-32-character-encryption-key

# External Services (optional)
SENDGRID_API_KEY=your-sendgrid-api-key
ANTHROPIC_API_KEY=your-anthropic-api-key
```

#### Step 3: Database Collections

The application automatically creates these collections:
- **users**: User accounts and profiles
- **detections**: Phishing detection history
- **reports**: Reported content for moderation
- **tips**: Security tips and educational content
- **analytics**: System usage statistics

#### Step 4: Verify Database Connection
```bash
# The application will automatically create collections on first run
# Check console output for:
# "Database: MongoDB Connected" or "Database: JSON Fallback"
```

## 📁 Project Structure

```
ai-phishing-detection-platform/
├── 📁 Frontend & Backend (Single Application)
│   ├── app.py                    # Flask application configuration
│   ├── main.py                   # 🚀 ENTRY POINT - Start here!
│   ├── routes.py                 # Main web routes (home, detection)
│   ├── auth_routes.py            # User authentication (login, register)
│   ├── admin_routes.py           # Admin dashboard functionality
│   └── ml_detector.py            # AI/ML detection algorithms
├── 📁 Database & Models
│   ├── models/
│   │   ├── mongodb_config.py     # Database connection management
│   │   └── user_models.py        # User data structures
│   └── data/                     # JSON fallback storage (auto-created)
├── 📁 Utilities & Helpers
│   ├── utils/
│   │   ├── encryption_utils.py   # AES-256 data encryption
│   │   ├── file_utils.py         # File upload handling
│   │   └── validation_utils.py   # Input validation
│   ├── offline_threat_intel.py   # Threat intelligence database
│   └── security_tips_updater.py  # Educational content system
├── 📁 Frontend Assets
│   ├── templates/                # HTML templates (Jinja2)
│   │   ├── base.html            # Base template with Bootstrap
│   │   ├── auth/                # Login/register pages
│   │   └── admin/               # Admin dashboard pages
│   └── static/                  # CSS, JavaScript, Images
│       ├── css/                 # Stylesheets and animations
│       ├── js/                  # Modular JavaScript components
│       └── images/              # Static images and assets
├── 📁 Dependencies & Config
│   ├── requirements-local.txt    # Python dependencies
│   ├── pyproject.toml           # Project configuration
│   └── .env                     # Environment variables (create this)
└── 📁 Documentation
    ├── README.md                 # This file
    ├── DEPENDENCIES.md           # Detailed dependency info
    └── CODEBASE_CLEANUP_SUMMARY.md # Project organization notes
```

## 🔑 Default Login Credentials

The application creates default accounts on first startup:

### Admin Account (Full Access)
- **Username**: `admin`
- **Password**: `admin123`
- **Access**: User management, system configuration, analytics

### Regular User Account
- **Username**: `user`  
- **Password**: `user123`
- **Access**: Detection tools, personal dashboard

**⚠️ IMPORTANT**: Change these passwords immediately after first login!

## 🖥️ Starting the Application

### Step 1: Activate Virtual Environment (if using)
```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### Step 2: Start Backend Server
```bash
# Navigate to project directory
cd ai-phishing-detection-platform

# Start the application (this is the main entry point)
python main.py
```

### Step 3: Access the Application
1. **Open Browser**: Navigate to `http://localhost:5000`
2. **Home Page**: You'll see the AI Phishing Detection Platform homepage
3. **Login**: Click "Login" and use the default credentials above
4. **Start Detecting**: Use the detection tools to analyze URLs, emails, or files

### Application URLs
- **Homepage**: `http://localhost:5000`
- **Login**: `http://localhost:5000/login`
- **Register**: `http://localhost:5000/register`
- **Detection Tool**: `http://localhost:5000/check`
- **Admin Dashboard**: `http://localhost:5000/admin/` (admin only)
- **User Dashboard**: `http://localhost:5000/dashboard`

## 🛠️ Usage Instructions

### For Regular Users

#### 1. URL Analysis
- Go to Detection Tool (`/check`)
- Select "URL Analysis" tab
- Enter suspicious URL
- Click "Analyze" to get threat assessment

#### 2. Email Protection
- Go to Detection Tool (`/check`)
- Select "Email Analysis" tab  
- Paste email content
- Get detailed threat analysis

#### 3. File Analysis
- Go to Detection Tool (`/check`)
- Select "File Upload" tab
- Upload image, video, audio, or document
- AI analyzes for generated content

#### 4. View History
- Go to User Dashboard (`/dashboard`)
- See all your previous scans
- View detailed results and explanations

### For Administrators

#### 1. Access Admin Panel
- Login with admin credentials
- Click profile menu → "Admin Dashboard"
- Full system management interface

#### 2. User Management
- Create, edit, or delete user accounts
- Manage user roles and permissions
- View user activity and statistics

#### 3. System Analytics
- Monitor detection statistics
- View system performance metrics
- Export data for analysis

#### 4. Content Moderation
- Review reported content
- Manage safety tips and educational content
- Configure system settings

## 🔧 Troubleshooting

### Common Installation Issues

#### Python Not Found
```bash
# Check if Python is installed
python --version
# or
python3 --version

# If not found, reinstall Python and ensure it's added to PATH
```

#### Permission Denied Errors
```bash
# Windows: Run command prompt as administrator
# macOS/Linux: Use --user flag
pip install --user -r requirements-local.txt
```

#### Virtual Environment Issues
```bash
# If activation fails, try:
# Windows:
venv\Scripts\activate.bat
# or
venv\Scripts\activate.ps1

# macOS/Linux:
source venv/bin/activate
```

#### Module Not Found Errors
```bash
# Ensure virtual environment is activated
# Reinstall dependencies
pip install --upgrade pip
pip install -r requirements-local.txt
```

#### Port 5000 Already in Use
```bash
# Windows: Find and kill process
netstat -ano | findstr :5000
taskkill /PID <PID_NUMBER> /F

# macOS/Linux: Kill process using port
lsof -ti:5000 | xargs kill -9

# Or run on different port
python main.py --port 8080
```

### Database Issues

#### MongoDB Connection Failed
- **Local MongoDB**: Ensure MongoDB service is running
- **MongoDB Atlas**: Check connection string and network access
- **Automatic Fallback**: Application uses JSON files if MongoDB unavailable

#### JSON Fallback Mode
- If you see "Database: JSON Fallback" in console, it's working correctly
- Data is stored in `data/` directory
- No setup required, works out of the box

### Application Issues

#### Blank Page or Errors
```bash
# Check console output for error messages
# Ensure all dependencies are installed
# Verify Python version is 3.11+
# Clear browser cache and cookies
```

#### Login Issues
- Use default credentials: admin/admin123 or user/user123
- Clear browser cookies
- Check if user exists in database

## 🚀 Advanced Configuration

### Custom Environment Variables
```env
# Custom database name
MONGODB_URI=mongodb://localhost:27017/custom_database_name

# Custom security keys
SESSION_SECRET=your-ultra-secure-session-key-here
USER_ENCRYPTION_SECRET=your-32-character-encryption-key

# File upload settings
MAX_CONTENT_LENGTH=16777216  # 16MB max file size
UPLOAD_FOLDER=uploads

# External API services (optional)
SENDGRID_API_KEY=your-sendgrid-api-key-for-emails
ANTHROPIC_API_KEY=your-anthropic-api-key-for-ai
```

### Production Deployment
```bash
# Install production server
pip install gunicorn

# Run with Gunicorn (production-ready)
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# Or with specific configuration
gunicorn --workers 4 --bind 0.0.0.0:5000 --timeout 120 app:app
```

### Development Mode
```bash
# Enable debug mode (development only)
export FLASK_ENV=development
export DEBUG=True
python main.py
```

## 🎯 Key Features Explained

### 🔍 AI Detection Capabilities
- **Machine Learning Models**: Uses scikit-learn for pattern recognition
- **Computer Vision**: OpenCV for image and video analysis  
- **Natural Language Processing**: NLTK for text analysis
- **Deep Learning**: TensorFlow for advanced AI detection

### 🛡️ Security Features
- **AES-256 Encryption**: All sensitive data encrypted at rest
- **Secure Sessions**: Flask session management with timeout
- **Input Validation**: Comprehensive sanitization of user inputs
- **Role-Based Access**: Admin and user permission levels

### 📊 User Interface
- **Bootstrap 5**: Modern, responsive design
- **Dark Theme**: Professional appearance
- **Mobile Friendly**: Works on all devices
- **Accessibility**: Screen reader compatible

## 📚 Learning Resources

### For Beginners
This project demonstrates:
- **Web Development**: Flask framework, HTML/CSS/JavaScript
- **Database Management**: MongoDB operations and data modeling
- **Security**: Authentication, encryption, secure coding practices
- **Machine Learning**: AI algorithms and threat detection
- **Software Engineering**: Project structure and best practices

### Code Comments
Every file includes detailed comments explaining:
- What each function does
- How algorithms work
- Why specific approaches were chosen
- How to modify or extend functionality

## 🤝 Contributing

### Development Setup
1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Make changes with proper documentation
4. Test thoroughly on multiple platforms
5. Submit pull request with detailed description

### Code Standards
- Follow PEP 8 for Python code formatting
- Add comprehensive comments for complex logic
- Include docstrings for all functions
- Test all new features across platforms

## 📄 License

This project is created for educational purposes as a final semester project. Feel free to use it for learning and educational purposes.

## 🆘 Support & Help

### Getting Help
1. **Check Troubleshooting Section**: Most common issues are covered above
2. **Review Console Output**: Error messages provide valuable debugging info
3. **Verify Setup Steps**: Ensure all installation steps were followed correctly
4. **Test with Default Credentials**: Use admin/admin123 to verify functionality

### Contact Information
- **Author**: Bigendra Shrestha
- **Project**: Final Semester - AI Phishing Detection Platform
- **Institution**: [Your Institution Name]
- **Year**: 2024-2025

---

**🎉 Congratulations!** You now have a fully functional AI Phishing Detection Platform running on your system. Start by logging in with the default credentials and exploring the detection capabilities.