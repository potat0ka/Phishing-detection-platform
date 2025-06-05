# AI Phishing Detection Platform

A comprehensive phishing detection system that identifies potential phishing content from websites, emails, messages, and links using advanced AI and machine learning algorithms. Built with Flask, Python, HTML, CSS, and JavaScript for a complete web-based security solution.

## 📋 Project Overview

This platform is a full-featured phishing detection system designed to help users identify and avoid phishing attempts across multiple communication channels. The system combines traditional rule-based detection with modern AI/ML techniques to provide accurate threat assessment.

**Key Capabilities:**
- Analyze URLs, emails, and text messages for phishing indicators
- AI-powered content detection for images, videos, audio, and documents
- Real-time threat intelligence and security assessment
- User authentication and detection history management
- Educational content and security awareness training

**Technologies Used:**
- **Backend**: Python (Flask framework)
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Database**: MongoDB with JSON fallback
- **Security**: AES-256 encryption, secure session management
- **AI/ML**: Scikit-learn, OpenCV, TensorFlow (optional)
- **UI Framework**: Bootstrap 5 with responsive design

## 🚀 Features

### Core Detection Capabilities

#### 🛡️ Phishing Detection
- **URL Analysis**: Scan suspicious links and websites for phishing indicators
- **Email Content Analysis**: Detect phishing attempts in email messages
- **Message Scanning**: Analyze text messages and social media content for threats
- **Link Verification**: Real-time assessment of hyperlinks and redirects
- **Confidence Scoring**: Percentage-based threat assessment with detailed explanations

#### 🤖 AI Content Detection
- **Image Analysis**: Detect AI-generated vs authentic photos (supports up to 500MB files)
- **Video Analysis**: Identify deepfakes and AI-generated video content
- **Audio Detection**: Recognize synthetic speech and voice cloning attempts
- **Document Scanning**: Analyze text documents for AI writing patterns
- **Device Photo Recognition**: EXIF metadata analysis to verify authentic device photos
- **Source Identification**: Identify likely AI generation tools and software used

### User Management System

#### 👤 User Authentication
- **Secure Registration**: Account creation with strong password requirements
- **Encrypted Login**: AES-256 encrypted user sessions and data storage
- **Password Security**: Visual strength indicators and secure hash storage
- **Session Management**: Automatic timeout and secure session handling
- **Privacy Protection**: Zero-knowledge architecture protecting user data

#### 📊 User Dashboard
- **Detection History**: View all previous scans and analysis results
- **Bulk Operations**: Select and delete multiple detection records
- **User Profile**: Manage account settings and preferences
- **Activity Logs**: Track usage patterns and security events
- **Export Data**: Download detection history in various formats

### Administrative Features

#### 🔧 Admin Dashboard
- **User Management**: View and manage registered users (without accessing personal data)
- **System Monitoring**: Track platform usage and performance metrics
- **Security Oversight**: Monitor threat detection patterns and system health
- **Content Management**: Update security tips and educational content
- **Database Administration**: Backup and maintenance operations

#### 📈 Analytics and Reporting
- **Detection Statistics**: Track phishing and AI detection rates
- **User Analytics**: Understand platform usage patterns
- **Threat Intelligence**: Monitor emerging phishing trends
- **Performance Metrics**: System response times and accuracy rates

### Educational and Safety Features

#### 📚 Security Education
- **39+ Security Tips**: Comprehensive cybersecurity awareness content
- **Interactive Learning**: Real-world examples and prevention techniques
- **Threat Updates**: Latest phishing trends and attack methods
- **Best Practices**: Guidelines for safe online behavior
- **Mobile-Friendly**: Optimized educational content for all devices

#### 🎯 Safety Guidelines
- **Phishing Prevention**: Step-by-step guides to avoid common threats
- **Email Security**: How to identify suspicious emails and attachments
- **Social Engineering**: Recognize manipulation tactics and scams
- **Password Security**: Create and manage strong, unique passwords
- **Safe Browsing**: Tips for secure web navigation

### Technical Features

#### 🔒 Security Infrastructure
- **AES-256 Encryption**: All user data encrypted at rest and in transit
- **MongoDB with JSON Fallback**: Reliable database architecture with automatic failover
- **Offline Threat Intelligence**: Local threat detection without external dependencies
- **Field-Level Encryption**: Individual encryption of sensitive data fields
- **Audit Logging**: Comprehensive activity tracking and security monitoring

#### 🌐 User Interface and Experience
- **Responsive Design**: Mobile-optimized interface with touch-friendly controls
- **Bootstrap Framework**: Professional, consistent UI across all devices
- **Real-time Feedback**: Instant results and progress indicators
- **Interactive Elements**: Drag-and-drop file uploads and dynamic content
- **Accessibility**: WCAG-compliant design for users with disabilities

#### 🔌 API and Integration
- **REST API**: Programmatic access to detection services
- **File Upload API**: Support for images, videos, audio, and documents
- **Bulk Processing**: Analyze multiple files or URLs simultaneously
- **Export Functions**: JSON, CSV, and PDF report generation
- **Webhook Support**: Real-time notifications for detection events

## 🚀 How to Run Locally (Any Device)

### Prerequisites
- **Python**: 3.8 or higher (3.11+ recommended for best performance)
- **Operating System**: Windows, macOS, or Linux
- **Memory**: 512MB RAM minimum (1GB recommended)
- **Storage**: 500MB free space
- **Internet**: Required for initial setup and dependency installation

### Step-by-Step Installation Guide

#### Step 1: Clone the Repository
```bash
# Clone the project to your local machine
git clone <repository-url>
cd ai-phishing-detection-platform

# Alternative: Download ZIP file and extract
# Then navigate to the extracted folder in terminal/command prompt
```

#### Step 2: Set Up Python Virtual Environment (Recommended)

**For Windows:**
```cmd
# Open Command Prompt or PowerShell
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# You should see (venv) in your command prompt
```

**For macOS/Linux:**
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# You should see (venv) in your terminal prompt
```

#### Step 3: Install Dependencies
```bash
# Upgrade pip first (important for compatibility)
pip install --upgrade pip

# Install required packages
pip install flask werkzeug pillow numpy scikit-learn nltk beautifulsoup4 requests trafilatura dnspython email-validator opencv-python-headless cryptography pymongo flask-pymongo psycopg2-binary

# Alternative: Create requirements.txt file and install
# pip install -r requirements.txt
```

#### Step 4: Start the Local Server
```bash
# Start the Flask development server
python main.py

# Alternative startup command
# python app.py  (if main.py doesn't work)
# flask run  (alternative Flask command)
```

#### Step 5: View in Browser
1. **Open your web browser** (Chrome, Firefox, Safari, Edge)
2. **Navigate to**: `http://localhost:5000`
3. **Alternative addresses** (if localhost doesn't work):
   - `http://127.0.0.1:5000`
   - `http://0.0.0.0:5000`

#### Step 6: Create Your Account
1. Click "Register" to create a new account
2. Fill in username, email, and secure password
3. Login with your credentials
4. Start using the phishing detection features

### Quick Start Commands (All Platforms)

```bash
# One-line setup (after cloning repository)
pip install flask werkzeug pillow numpy scikit-learn nltk beautifulsoup4 requests trafilatura dnspython email-validator opencv-python-headless cryptography pymongo flask-pymongo psycopg2-binary && python main.py
```

### Configuration Options (Optional)

#### Environment Variables
Create a `.env` file in the project root directory:
```bash
# Security Configuration
USER_ENCRYPTION_SECRET=your-32-character-encryption-key
SESSION_SECRET=your-session-secret-key

# Database Configuration (optional - uses JSON fallback by default)
DATABASE_URL=mongodb://localhost:27017/phishing_detector

# Application Settings
FLASK_ENV=development
FLASK_DEBUG=True
```

#### Custom Port Configuration
```bash
# Run on different port (if 5000 is busy)
python main.py --port 8080

# Or set environment variable
export PORT=8080
python main.py
```

## 📋 Project Structure

```
ai-phishing-detection-platform/
├── main.py                    # Application entry point
├── app.py                     # Flask application configuration
├── routes.py                  # Web routes and request handlers
├── simple_models.py           # MongoDB models with encryption
├── encryption_utils.py        # AES-256 encryption utilities
├── ml_detector.py             # Phishing detection algorithms
├── ai_content_detector.py     # AI content detection system
├── offline_threat_intel.py    # Local threat intelligence
├── security_tips_updater.py   # Security awareness content
├── utils.py                   # Utility functions
├── templates/                 # HTML templates
│   ├── base.html              # Base template with Bootstrap
│   ├── index.html             # Home page
│   ├── check.html             # Phishing detection interface
│   ├── ai_content_check.html  # AI content analysis
│   ├── dashboard.html         # User dashboard
│   └── tips.html              # Security education
├── static/                    # Static assets
│   ├── css/                   # Custom styles
│   ├── js/                    # JavaScript functionality
│   └── uploads/               # Temporary file uploads
└── instance/                  # Instance-specific files
    ├── users.json             # Encrypted user data (JSON fallback)
    ├── detections.json        # Encrypted detection history
    └── tips.json              # Security tips database
```

## 🗄️ Database Setup

### Database Architecture
The platform uses a hybrid database approach for maximum reliability:
- **Primary**: MongoDB for scalable document storage
- **Fallback**: JSON files for automatic failover
- **Security**: AES-256 encryption for all stored data

### MongoDB Setup (Recommended)

#### Step 1: Install MongoDB
**Windows:**
```bash
# Download MongoDB Community Server from mongodb.com
# Install using the MSI installer
# MongoDB will start automatically as a service
```

**macOS:**
```bash
# Install using Homebrew
brew tap mongodb/brew
brew install mongodb-community

# Start MongoDB service
brew services start mongodb/brew/mongodb-community
```

**Linux (Ubuntu/Debian):**
```bash
# Import MongoDB public key
curl -fsSL https://pgp.mongodb.com/server-6.0.asc | sudo gpg -o /usr/share/keyrings/mongodb-server-6.0.gpg --dearmor

# Add MongoDB repository
echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-6.0.gpg ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/6.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list

# Update and install
sudo apt update
sudo apt install -y mongodb-org

# Start MongoDB service
sudo systemctl start mongod
sudo systemctl enable mongod
```

#### Step 2: Configure Database Connection
Create a `.env` file in the project root:
```bash
# MongoDB Configuration
DATABASE_URL=mongodb://localhost:27017/phishing_detector

# For MongoDB with authentication
DATABASE_URL=mongodb://username:password@localhost:27017/phishing_detector

# For MongoDB Atlas (cloud)
DATABASE_URL=mongodb+srv://username:password@cluster.mongodb.net/phishing_detector
```

#### Step 3: Database Collections
The platform automatically creates these collections:
- **users**: Encrypted user accounts and profiles
- **detections**: Analysis history and results
- **tips**: Security education content
- **threat_intel**: Offline threat intelligence data
- **audit_logs**: System activity and security logs

### JSON Fallback Setup (Automatic)
If MongoDB is unavailable, the platform automatically uses JSON files:
```
instance/
├── users.json          # Encrypted user data
├── detections.json     # Detection history
├── tips.json          # Security tips
└── audit_logs.json    # Activity logs
```

### Sample Data Creation

#### Create Admin User
```python
# Run this in Python after starting the application
import requests

# Register admin user
admin_data = {
    "username": "admin",
    "email": "admin@yourcompany.com",
    "password": "SecureAdminPass123!",
    "confirm_password": "SecureAdminPass123!"
}

response = requests.post("http://localhost:5000/auth/register", data=admin_data)
```

#### Create Test Users
```python
# Create sample test users for development
test_users = [
    {
        "username": "testuser1",
        "email": "test1@example.com",
        "password": "TestPass123!",
        "confirm_password": "TestPass123!"
    },
    {
        "username": "testuser2", 
        "email": "test2@example.com",
        "password": "TestPass123!",
        "confirm_password": "TestPass123!"
    }
]

for user in test_users:
    requests.post("http://localhost:5000/auth/register", data=user)
```

### Database Maintenance

#### Backup Commands
```bash
# MongoDB backup
mongodump --db phishing_detector --out backup/

# JSON files backup
cp -r instance/ backup/json_backup/
```

#### Restore Commands
```bash
# MongoDB restore
mongorestore --db phishing_detector backup/phishing_detector/

# JSON files restore
cp -r backup/json_backup/* instance/
```

## 👥 Admin and User Roles

### User Role System
The platform supports two main user types with different permission levels:

#### Regular Users
**Capabilities:**
- Create account and login
- Analyze URLs, emails, and messages for phishing
- Upload and analyze files for AI-generated content
- View personal detection history
- Access security education content
- Manage personal profile and settings
- Export personal detection data

**Restrictions:**
- Cannot access other users' data
- Cannot view system-wide analytics
- Cannot manage other users
- Cannot modify system settings

#### Admin Users
**Capabilities:**
- All regular user capabilities
- View system-wide usage statistics
- Monitor platform performance metrics
- Access aggregated detection analytics
- Manage system security settings
- View audit logs and security events
- Update security tips and educational content
- Backup and restore system data

**Important Security Note:**
- Admins cannot view encrypted user personal data
- Zero-knowledge architecture protects user privacy
- Admin access is logged and audited

### Accessing Admin Panel

#### Method 1: Direct Admin Registration
```python
# Create admin user programmatically
from mongodb_config import MongoDBManager
from encryption_utils import encrypt_sensitive_data

db = MongoDBManager()
admin_data = {
    "username": "admin",
    "email": "admin@yourcompany.com", 
    "role": "admin",  # Special admin role
    "is_admin": True
}

# Encrypt and store admin user
encrypted_data = encrypt_sensitive_data("user", admin_data)
db.insert_one("users", encrypted_data)
```

#### Method 2: Promote Existing User
```python
# Promote existing user to admin
from mongodb_config import MongoDBManager

db = MongoDBManager()
db.update_one(
    "users", 
    {"username": "existing_username"}, 
    {"$set": {"role": "admin", "is_admin": True}}
)
```

### Admin Dashboard Features

#### User Management
- **View Users**: See list of registered users (usernames only, no personal data)
- **User Statistics**: Track registration trends and active users
- **Account Status**: Monitor user activity and login patterns
- **Bulk Operations**: Mass user management and maintenance

#### System Analytics
- **Detection Metrics**: Success rates and accuracy statistics
- **Usage Patterns**: Peak usage times and popular features
- **Threat Intelligence**: Emerging phishing trends and patterns
- **Performance Monitoring**: System response times and errors

#### Security Oversight
- **Audit Logs**: Complete activity tracking and security events
- **Threat Monitoring**: Real-time security alert management
- **Data Encryption**: Monitor encryption key status and rotation
- **Backup Status**: Database backup and recovery monitoring

### Permission Management

#### Role-Based Access Control
```python
# Check user permissions in routes
from functools import wraps
from flask import session, redirect, url_for

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('is_admin'):
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

# Usage in routes
@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    # Admin-only functionality
    pass
```

#### Access Control Examples
```python
# Regular user access
@app.route('/dashboard')
@login_required
def user_dashboard():
    # User can only see their own data
    user_id = session['user_id']
    user_detections = get_user_detections(user_id)
    
# Admin access
@app.route('/admin/users')
@admin_required
def admin_users():
    # Admin can see aggregated user statistics
    # But not individual user personal data
    user_stats = get_user_statistics()
```

## 🔐 Security Configuration

### Environment Variables

For production deployment, set these environment variables:

```bash
# Encryption Configuration
export USER_ENCRYPTION_SECRET="your-secure-encryption-key-32-chars"
export SESSION_SECRET="your-session-secret-key"

# Database Configuration
export DATABASE_URL="mongodb://username:password@host:port/database"
export PGUSER="postgres_username"
export PGPASSWORD="postgres_password"
export PGHOST="postgres_host"
export PGPORT="postgres_port"
export PGDATABASE="postgres_database"
```

### Data Encryption Details

- **Encryption Algorithm**: AES-256 with PBKDF2 key derivation
- **Encrypted Fields**: Usernames, emails, IP addresses, user agents, file paths
- **Key Management**: Environment-based with automatic generation fallback
- **Encryption Scope**: All user personal information and activity logs

## 🎯 Feature Overview

### 🛡️ Phishing Detection
- **URL Analysis**: Scan suspicious links with confidence scoring
- **Email Detection**: Analyze email content for phishing indicators  
- **Message Scanning**: Check text messages and social media content
- **Threat Intelligence**: Offline database with 1000+ known threats

### 🤖 AI Content Detection
- **Image Analysis**: Detect AI-generated vs real photos (up to 500MB)
- **Video Detection**: Analyze video content for deepfakes and AI generation
- **Audio Analysis**: Identify synthetic speech and voice cloning
- **Document Scanning**: Check text documents for AI writing patterns
- **Device Photo Recognition**: EXIF metadata analysis for authentic photos

### 👤 User Management
- **Encrypted Accounts**: AES-256 encrypted user registration and login
- **Detection History**: View and manage analysis results with bulk operations
- **Privacy Protection**: Zero-knowledge architecture - admins cannot access user data
- **Session Security**: Encrypted session management with automatic timeout

### 📚 Security Education
- **39+ Security Tips**: Comprehensive cybersecurity awareness content
- **Threat Updates**: Latest phishing trends and attack methods
- **Interactive Learning**: Real-world examples and prevention techniques
- **Mobile-Optimized**: Touch-friendly interface for all devices

### 🔌 API Access
- `POST /api/quick-check` - Phishing analysis endpoint
- `GET /tips` - Security education content
- `POST /ai-content-check` - AI detection analysis
- `DELETE /delete-detection/<id>` - Remove detection records

## 🚀 Deployment Options

### Local Development (Recommended)
```bash
# Simple startup for development and testing
python main.py
# Platform runs on http://localhost:5000
```

### Production Deployment
```bash
# Set production environment variables
export USER_ENCRYPTION_SECRET="your-secure-32-char-key"
export SESSION_SECRET="your-session-secret"
export FLASK_ENV="production"

# Install production dependencies
pip install -r requirements-minimal.txt

# Run with production settings
python main.py
```

### Cloud Platform Deployment

**Heroku**
```bash
# Add Procfile: web: python main.py
# Set environment variables in Heroku dashboard
# Deploy using Heroku CLI
```

**Railway/Render**
```bash
# Use build command: pip install -r requirements-minimal.txt
# Use start command: python main.py
# Set PORT=5000 in environment variables
```

**VPS/Server Deployment**
```bash
# Install dependencies
pip install -r requirements-minimal.txt

# Set up systemd service (optional)
# Run behind nginx/Apache reverse proxy for HTTPS
# Configure domain and SSL certificate

# Start application
python main.py
```

### Docker Deployment
```bash
# Build container
docker build -t phishing-detector .

# Run with environment variables
docker run -p 5000:5000 \
  -e USER_ENCRYPTION_SECRET="your-key" \
  -e SESSION_SECRET="your-secret" \
  phishing-detector
```

## 🖥️ Platform-Specific Installation

### Windows Installation

#### Prerequisites
- Download Python 3.11+ from [python.org](https://python.org)
- Install Git from [git-scm.com](https://git-scm.com)

#### Installation Steps
```cmd
# Open Command Prompt or PowerShell as Administrator
# Clone the repository
git clone <repository-url>
cd ai-phishing-detection-platform

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Upgrade pip first
python -m pip install --upgrade pip

# Install core dependencies (without TensorFlow)
pip install flask werkzeug pillow numpy scikit-learn nltk beautifulsoup4 requests trafilatura dnspython email-validator opencv-python-headless cryptography pymongo flask-pymongo psycopg2-binary

# Run the application (TensorFlow-free version)
python main.py
```

#### TensorFlow Installation (Optional)
```cmd
# Check your Python version first
python --version

# Install TensorFlow based on your Python version:
# Python 3.8-3.11: pip install tensorflow==2.13.0
# Python 3.9-3.12: pip install tensorflow==2.15.0
# For CPU only: pip install tensorflow-cpu
# If installation fails, skip it - the platform works without TensorFlow
```

#### Troubleshooting Windows
- **TensorFlow Error**: Skip TensorFlow installation - the platform works perfectly without it
- **pip install fails**: Try `python -m pip install --upgrade pip`
- **OpenCV issues**: Use `pip install opencv-python-headless` instead
- **Permission errors**: Run Command Prompt as Administrator

### macOS Installation

#### Prerequisites
```bash
# Install Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python 3.11+
brew install python@3.11 git
```

#### Installation Steps
```bash
# Clone the repository
git clone <repository-url>
cd ai-phishing-detection-platform

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Upgrade pip first
pip install --upgrade pip

# Install core dependencies (TensorFlow-free)
pip install flask gunicorn werkzeug pillow numpy scikit-learn nltk beautifulsoup4 requests trafilatura dnspython email-validator opencv-python-headless cryptography pymongo flask-pymongo psycopg2-binary

# Run the application
python main.py
```

#### TensorFlow Installation (Optional)
```bash
# For M1/M2 Macs: pip install tensorflow-macos
# For Intel Macs: pip install tensorflow==2.13.0
# Skip if installation fails - platform works without TensorFlow
```

#### Troubleshooting macOS
- **TensorFlow Error**: Skip TensorFlow - the platform works perfectly without it
- **M1/M2 Macs**: Use `pip install tensorflow-macos` if needed
- **OpenCV issues**: Try `brew install opencv` or use `opencv-python-headless`
- **Permission issues**: Use `pip install --user` instead

### Linux Installation (Ubuntu/Debian)

#### Prerequisites
```bash
# Update package list
sudo apt update

# Install Python 3.11 and dependencies
sudo apt install python3.11 python3.11-pip python3.11-venv python3.11-dev git

# Install system dependencies for computer vision
sudo apt install libgl1-mesa-glx libglib2.0-0 libsm6 libxext6 libxrender-dev libgomp1
```

#### Installation Steps
```bash
# Clone the repository
git clone <repository-url>
cd ai-phishing-detection-platform

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install core dependencies (TensorFlow-free)
pip install flask gunicorn werkzeug pillow numpy scikit-learn nltk beautifulsoup4 requests trafilatura dnspython email-validator opencv-python-headless cryptography pymongo flask-pymongo psycopg2-binary

# Run the application
python main.py
```

#### For Other Linux Distributions

**CentOS/RHEL/Fedora:**
```bash
# Install Python and dependencies
sudo dnf install python3.11 python3.11-pip python3.11-devel git
# or for older versions: sudo yum install python3.11 python3.11-pip python3.11-devel git

# Follow the same installation steps as Ubuntu
```

**Arch Linux:**
```bash
# Install Python and dependencies
sudo pacman -S python python-pip git

# Follow the same installation steps as Ubuntu
```

#### TensorFlow Installation (Optional)
```bash
# Install TensorFlow based on your Python version:
# Python 3.8-3.11: pip install tensorflow==2.13.0
# Python 3.9-3.12: pip install tensorflow==2.15.0
# For GPU: pip install tensorflow-gpu (requires CUDA)
# Skip if installation fails - platform works without TensorFlow
```

#### Troubleshooting Linux
- **TensorFlow Error**: Skip TensorFlow installation - the platform works perfectly without it
- **OpenCV issues**: `sudo apt install python3-opencv` or use `opencv-python-headless`
- **Permission issues**: Use virtual environment or `pip install --user`
- **Missing system libraries**: Install with `sudo apt install build-essential python3-dev`

### Docker Installation (All Platforms)

```dockerfile
# Create Dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY . .

RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx libglib2.0-0 libsm6 libxext6 libxrender-dev libgomp1 \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir flask werkzeug pillow numpy scikit-learn nltk beautifulsoup4 requests trafilatura dnspython email-validator opencv-python-headless cryptography pymongo flask-pymongo psycopg2-binary

EXPOSE 5000
CMD ["python", "main.py"]
```

```bash
# Build and run with Docker
docker build -t ai-phishing-detector .
docker run -p 5000:5000 ai-phishing-detector
```

## 🔧 Quick Fix for TensorFlow Installation Error

If you're getting the TensorFlow installation error on your local device, follow these steps:

### Option 1: Install Without TensorFlow (Recommended)
```bash
# Clone the repository
git clone <repository-url>
cd ai-phishing-detection-platform

# Create virtual environment
python -m venv venv
# On Windows: venv\Scripts\activate
# On Mac/Linux: source venv/bin/activate

# Install core dependencies only (skip TensorFlow)
pip install flask werkzeug pillow numpy scikit-learn nltk beautifulsoup4 requests trafilatura dnspython email-validator opencv-python-headless cryptography pymongo flask-pymongo psycopg2-binary

# Run the application
python main.py
```

### Option 2: Use the Minimal Requirements File
```bash
# Use the provided minimal requirements
pip install -r requirements-minimal.txt
python main.py
```

### Option 3: Install TensorFlow Separately (If Needed)
```bash
# Check your Python version first
python --version

# Install compatible TensorFlow version:
# Python 3.8-3.11: pip install tensorflow==2.13.0
# Python 3.9-3.12: pip install tensorflow==2.15.0
# Python 3.12+: pip install tensorflow (latest)

# If still fails, use CPU-only version:
pip install tensorflow-cpu
```

### Common Installation Issues and Solutions

**Error: "No matching distribution found for tensorflow"**
- Solution: Skip TensorFlow installation - the platform works perfectly without it
- The AI detection features use scikit-learn and don't require TensorFlow

**Error: "Microsoft Visual C++ 14.0 is required" (Windows)**
- Solution: Install Microsoft C++ Build Tools or Visual Studio

**Error: "Failed building wheel for psycopg2" (Windows)**
- Solution: Use `pip install psycopg2-binary` instead

**Error: OpenCV issues**
- Solution: Use `pip install opencv-python-headless` instead of `opencv-python`

## 🤝 Contribution Guide

### Getting Started with Contributions
We welcome contributions from developers of all skill levels! This section provides guidelines for contributing to the AI Phishing Detection Platform.

### Development Environment Setup

#### Fork and Clone
```bash
# Fork the repository on GitHub first, then clone your fork
git clone https://github.com/your-username/ai-phishing-detection-platform.git
cd ai-phishing-detection-platform

# Add upstream remote for syncing
git remote add upstream https://github.com/original-repo/ai-phishing-detection-platform.git
```

#### Development Setup
```bash
# Create development environment
python -m venv dev-env
source dev-env/bin/activate  # On Windows: dev-env\Scripts\activate

# Install development dependencies
pip install -r requirements-dev.txt

# Install pre-commit hooks (optional but recommended)
pip install pre-commit
pre-commit install
```

### Code Style and Standards

#### Python Code Guidelines
- **PEP 8**: Follow Python PEP 8 style guidelines
- **Docstrings**: Use Google-style docstrings for all functions and classes
- **Type Hints**: Include type hints for function parameters and return values
- **Comments**: Write clear, concise comments explaining complex logic

#### Example Code Style
```python
def analyze_phishing_url(url: str, user_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Analyze a URL for phishing indicators using ML algorithms.
    
    Args:
        url: The URL to analyze for phishing content
        user_id: Optional user ID for logging purposes
        
    Returns:
        Dictionary containing analysis results with confidence scores
        
    Raises:
        ValueError: If URL format is invalid
        ConnectionError: If URL cannot be accessed
    """
    # Implementation here
    pass
```

#### Frontend Guidelines
- **HTML**: Use semantic HTML5 elements
- **CSS**: Follow BEM methodology for class naming
- **JavaScript**: Use ES6+ features, avoid jQuery dependencies
- **Bootstrap**: Use Bootstrap classes consistently, avoid custom CSS when possible

### Project Structure and Architecture

#### Backend Architecture
```
├── app.py                     # Flask application factory
├── routes.py                  # URL route definitions
├── models/                    # Database models and schemas
│   ├── user_model.py         # User authentication model
│   └── detection_model.py    # Detection history model
├── services/                  # Business logic layer
│   ├── phishing_service.py   # Phishing detection logic
│   ├── ai_service.py         # AI content detection
│   └── encryption_service.py # Data encryption utilities
├── utils/                     # Helper functions
│   ├── validators.py         # Input validation
│   └── formatters.py         # Data formatting
└── tests/                     # Test suite
    ├── test_routes.py        # Route testing
    ├── test_services.py      # Service testing
    └── test_utils.py         # Utility testing
```

#### Frontend Architecture
```
static/
├── css/
│   ├── style.css            # Main stylesheet
│   ├── components/          # Component-specific styles
│   └── animations.css       # Animation definitions
├── js/
│   ├── modules/            # Modular JavaScript components
│   │   ├── auth.js         # Authentication handling
│   │   ├── detection.js    # Detection interface logic
│   │   └── ui.js           # UI interaction handlers
│   └── main.js             # Application entry point
└── images/
    ├── icons/              # SVG icons and graphics
    └── uploads/            # Temporary file storage
```

### Contribution Workflow

#### 1. Issue Creation
Before starting work, create or find an existing issue:
- **Bug Reports**: Use the bug report template
- **Feature Requests**: Use the feature request template
- **Documentation**: Use the documentation improvement template

#### 2. Branch Strategy
```bash
# Create feature branch from main
git checkout main
git pull upstream main
git checkout -b feature/your-feature-name

# For bug fixes
git checkout -b bugfix/issue-description

# For documentation
git checkout -b docs/documentation-improvement
```

#### 3. Development Process
```bash
# Make your changes following the coding standards
# Write tests for new functionality
# Update documentation as needed

# Run tests locally
python -m pytest tests/

# Check code style
flake8 .
black --check .

# Run the application to test
python main.py
```

#### 4. Commit Guidelines
Use conventional commit messages:
```bash
# Features
git commit -m "feat: add AI video detection capability"

# Bug fixes
git commit -m "fix: resolve session timeout issue"

# Documentation
git commit -m "docs: update installation instructions"

# Tests
git commit -m "test: add unit tests for phishing detection"

# Refactoring
git commit -m "refactor: improve encryption utility performance"
```

#### 5. Pull Request Process
```bash
# Push your branch
git push origin feature/your-feature-name

# Create pull request with:
# - Clear description of changes
# - Link to related issues
# - Screenshots for UI changes
# - Test results and coverage
```

### Testing Guidelines

#### Unit Tests
```python
import unittest
from services.phishing_service import PhishingDetector

class TestPhishingDetector(unittest.TestCase):
    """Test cases for phishing detection service."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.detector = PhishingDetector()
    
    def test_suspicious_url_detection(self):
        """Test detection of known suspicious URLs."""
        suspicious_url = "http://phishing-example.com"
        result = self.detector.analyze_url(suspicious_url)
        
        self.assertGreater(result['threat_score'], 0.7)
        self.assertEqual(result['classification'], 'suspicious')
    
    def test_legitimate_url_detection(self):
        """Test detection of legitimate URLs."""
        legitimate_url = "https://github.com"
        result = self.detector.analyze_url(legitimate_url)
        
        self.assertLess(result['threat_score'], 0.3)
        self.assertEqual(result['classification'], 'safe')
```

#### Integration Tests
```python
import requests
from app import create_app

class TestAPIEndpoints(unittest.TestCase):
    """Test API endpoint functionality."""
    
    def setUp(self):
        """Set up test client."""
        self.app = create_app(testing=True)
        self.client = self.app.test_client()
    
    def test_phishing_analysis_endpoint(self):
        """Test phishing analysis API endpoint."""
        response = self.client.post('/api/analyze', json={
            'url': 'http://test-url.com',
            'content_type': 'url'
        })
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('threat_score', data)
        self.assertIn('classification', data)
```

### Security Considerations

#### Security Review Checklist
- [ ] Input validation implemented for all user inputs
- [ ] SQL injection protection using parameterized queries
- [ ] XSS protection with proper output encoding
- [ ] CSRF protection enabled for forms
- [ ] Authentication and authorization properly implemented
- [ ] Sensitive data encrypted using AES-256
- [ ] No hardcoded secrets or API keys
- [ ] Proper error handling without information leakage

#### Security Testing
```python
def test_sql_injection_protection(self):
    """Test protection against SQL injection attacks."""
    malicious_input = "'; DROP TABLE users; --"
    response = self.client.post('/search', data={'query': malicious_input})
    
    # Should not cause database error
    self.assertNotEqual(response.status_code, 500)
    
def test_xss_protection(self):
    """Test protection against XSS attacks."""
    xss_payload = "<script>alert('xss')</script>"
    response = self.client.post('/comment', data={'content': xss_payload})
    
    # Should escape malicious content
    self.assertNotIn('<script>', response.data.decode())
```

### Documentation Standards

#### Code Documentation
```python
class AIContentDetector:
    """
    AI Content Detection System for analyzing uploaded files.
    
    This class provides comprehensive analysis of images, videos, audio,
    and documents to determine if they were generated by AI systems.
    
    Attributes:
        confidence_threshold: Minimum confidence score for AI detection
        supported_formats: List of supported file formats
        
    Example:
        detector = AIContentDetector()
        result = detector.analyze_file('image.jpg', 'image')
        if result['is_ai_generated']:
            print(f"AI detected with {result['confidence']}% confidence")
    """
    
    def analyze_file(self, file_path: str, content_type: str) -> Dict[str, Any]:
        """
        Analyze uploaded file for AI-generated content.
        
        Args:
            file_path: Path to the uploaded file
            content_type: Type of content ('image', 'video', 'audio', 'document')
            
        Returns:
            Analysis results containing:
            - is_ai_generated: Boolean indicating AI detection
            - confidence: Confidence score (0-100)
            - explanation: Human-readable explanation
            - source_detection: Likely AI tool used
            
        Raises:
            FileNotFoundError: If file path is invalid
            UnsupportedFormatError: If file format not supported
        """
        pass
```

#### API Documentation
Use clear API documentation with examples:
```markdown
### POST /api/analyze-url

Analyze a URL for phishing indicators.

**Request:**
```json
{
    "url": "https://example.com",
    "user_agent": "optional-user-agent",
    "check_redirects": true
}
```

**Response:**
```json
{
    "threat_score": 0.85,
    "classification": "suspicious",
    "indicators": [
        "Suspicious domain age",
        "Missing SSL certificate",
        "Known phishing pattern"
    ],
    "recommendations": [
        "Do not enter personal information",
        "Verify URL through official channels"
    ]
}
```
```

### Issue Reporting

#### Bug Report Template
```markdown
## Bug Description
A clear and concise description of the bug.

## Steps to Reproduce
1. Go to '...'
2. Click on '...'
3. Enter '...'
4. See error

## Expected Behavior
What you expected to happen.

## Actual Behavior
What actually happened.

## Environment
- OS: [e.g. Windows 10, macOS 12.0, Ubuntu 20.04]
- Python Version: [e.g. 3.11.0]
- Browser: [e.g. Chrome 120.0, Firefox 119.0]

## Additional Context
Add any other context about the problem here.
```

#### Feature Request Template
```markdown
## Feature Description
A clear and concise description of the feature.

## Problem Statement
What problem does this feature solve?

## Proposed Solution
Describe your proposed solution.

## Alternative Solutions
Describe any alternative solutions you've considered.

## Additional Context
Add any other context or screenshots about the feature request.
```

### Review Process

#### Pull Request Review Checklist
- [ ] Code follows style guidelines
- [ ] Tests are included and passing
- [ ] Documentation is updated
- [ ] Security considerations addressed
- [ ] Performance impact considered
- [ ] Backward compatibility maintained
- [ ] Edge cases handled
- [ ] Error handling implemented

#### Code Review Guidelines
- **Be Constructive**: Provide helpful suggestions, not just criticism
- **Focus on Code**: Review code quality, not coding style preferences
- **Ask Questions**: If something is unclear, ask for clarification
- **Suggest Improvements**: Offer specific suggestions for improvement
- **Approve When Ready**: Approve PRs that meet quality standards

### Getting Help

#### Communication Channels
- **GitHub Issues**: For bug reports and feature requests
- **GitHub Discussions**: For general questions and community discussion
- **Documentation**: Check existing documentation first
- **Stack Overflow**: Tag questions with relevant project tags

#### Mentorship Program
New contributors can request mentorship:
- Pair programming sessions
- Code review guidance
- Architecture discussions
- Career development advice

Thank you for contributing to the AI Phishing Detection Platform!

## ❓ Frequently Asked Questions

### Installation & Setup

**Q: Do I need to install a web server like Apache or Nginx?**
A: No, the platform includes Flask's built-in development server. Simply run `python main.py` and access `http://localhost:5000`.

**Q: The TensorFlow installation is failing. What should I do?**
A: Skip TensorFlow installation - the platform works perfectly without it. The AI detection features use scikit-learn instead.

**Q: Can I run this without MongoDB?**
A: Yes, the platform automatically uses secure JSON file storage with AES-256 encryption as a fallback.

**Q: How do I change the port from 5000?**
A: Edit `main.py` and change `app.run(host="0.0.0.0", port=5000, debug=True)` to your desired port.

### Security & Privacy

**Q: Is my data secure?**
A: Yes, all user data is encrypted with AES-256 encryption. Usernames, emails, and activity logs are encrypted at rest.

**Q: Can administrators see my personal information?**
A: No, the platform uses zero-knowledge architecture. Even administrators cannot decrypt user personal data.

**Q: Where is my data stored?**
A: Data is stored locally in encrypted JSON files (or MongoDB if configured). No data is sent to external servers.

### Features & Usage

**Q: What file types can I analyze for AI content?**
A: Images (JPG, PNG, GIF), videos (MP4, AVI, MOV), audio (MP3, WAV), and documents (TXT, PDF) up to 500MB.

**Q: How accurate is the phishing detection?**
A: The system uses multiple detection methods with conservative thresholds: 85% confidence for definitive AI-generated content.

**Q: Can I use this for commercial purposes?**
A: Yes, the platform is designed for educational and commercial use with enterprise-level security features.

### Troubleshooting

**Q: The application won't start. What should I check?**
A: Ensure Python 3.8+ is installed, all dependencies are installed via `pip install -r requirements-minimal.txt`, and port 5000 is available.

**Q: I'm getting import errors. How do I fix this?**
A: Create a virtual environment, activate it, and reinstall dependencies in isolation from system packages.

**Q: The platform is slow. How can I improve performance?**
A: Ensure sufficient RAM (512MB minimum), close unnecessary applications, and consider skipping TensorFlow if not needed.

## Project Structure

```
ai-phishing-detection-platform/
├── main.py                     # Application entry point
├── app.py                      # Flask application configuration
├── routes.py                   # Web routes and API endpoints
├── models.py                   # SQLAlchemy database models
├── ml_detector.py              # Phishing detection AI engine
├── ai_content_detector.py      # AI-generated content detection
├── offline_threat_intel.py     # Local threat intelligence system
├── security_tips_updater.py    # Security awareness content
├── threat_intelligence.py      # Threat analysis utilities
├── utils.py                    # Helper functions and utilities
├── pyproject.toml              # Project dependencies
├── README.md                   # Project documentation
├── .env.example                # Environment variables template
├── uploads/                    # User uploaded files (auto-created)
├── analysis_results/           # AI analysis results (auto-created)
├── instance/                   # Flask instance folder
├── templates/                  # Jinja2 HTML templates
│   ├── base.html              # Base template with navigation
│   ├── index.html             # Landing page
│   ├── check.html             # Phishing detection interface
│   ├── ai_content_check.html  # AI content detection page
│   ├── ai_content_results.html # AI analysis results
│   ├── tips.html              # Security education page
│   ├── dashboard.html         # User dashboard with history
│   ├── login.html             # User authentication
│   └── register.html          # User registration
└── static/                     # Static assets
    ├── css/
    │   └── loading-animations.css # Custom loading animations
    └── uploads/               # Processed upload files
```

## Database Architecture

This project uses a **hybrid database system** combining PostgreSQL for production reliability with JSON fallback for development simplicity.

### Database Features
- **PostgreSQL**: Primary database for user accounts, detection history, and security tips
- **SQLite Fallback**: Automatic fallback when PostgreSQL is unavailable
- **JSON Storage**: Analysis results and file metadata stored as JSON
- **Offline Intelligence**: Local SQLite database for threat intelligence data

### Key Components
- **User Management**: Secure authentication with hashed passwords
- **Detection History**: Comprehensive logging of all security scans
- **AI Analysis Results**: Detailed AI content detection metadata
- **Threat Intelligence**: Local database of malicious domains and IPs
- **Security Tips**: Educational content with categorization

## AI & Machine Learning Features

### Phishing Detection Capabilities
- **URL Analysis**: Domain reputation, suspicious patterns, and redirect detection
- **Email Content Analysis**: NLP-based phishing email detection with grammar analysis
- **Message Analysis**: Text-based threat detection with pattern matching
- **Offline Threat Intelligence**: Local database of malicious domains, IPs, and indicators

### AI Content Detection
- **Image Analysis**: Detect AI-generated images with metadata analysis and pixel patterns
- **Video Analysis**: Deepfake and synthetic video detection with frame consistency analysis
- **Audio Analysis**: AI-generated voice and synthetic speech detection
- **Document Analysis**: AI-written text detection with writing pattern analysis
- **Device Photo Recognition**: EXIF data analysis to identify real camera photos

### Machine Learning Techniques
- **Computer Vision**: PIL and OpenCV for image analysis
- **Statistical Analysis**: Noise patterns, color distribution, and pixel variance
- **Natural Language Processing**: NLTK for text analysis and pattern detection
- **Confidence Scoring**: Multi-factor analysis with conservative thresholds
- **Pattern Recognition**: Rule-based and ML hybrid approaches

## Configuration

### Environment Variables
The application automatically handles most configuration, but you can create a `.env` file for customization:
```env
SESSION_SECRET=your-secret-key-here
DATABASE_URL=postgresql://user:password@localhost/dbname
DEBUG=True
```

### Optional Features
- **Anthropic AI Integration**: Requires `ANTHROPIC_API_KEY` for enhanced AI analysis
- **PostgreSQL**: Automatically uses SQLite fallback if PostgreSQL unavailable

## Troubleshooting

### Common Issues

#### Missing Dependencies
```bash
pip install flask flask-sqlalchemy gunicorn werkzeug pillow numpy scikit-learn nltk beautifulsoup4 requests trafilatura dnspython email-validator anthropic opencv-python tensorflow psycopg2-binary
```

#### Port Already in Use
```bash
# Kill process using port 5000
# Linux/Mac: lsof -ti:5000 | xargs kill -9
# Windows: netstat -ano | findstr :5000, then taskkill /PID <PID> /F
```

#### Python Version Issues
- Ensure Python 3.11 or higher is installed
- Use `python3` on Mac/Linux, `python` on Windows
- Consider using virtual environment for isolation

#### Database Connection
- PostgreSQL is optional - SQLite fallback is automatic
- Check DATABASE_URL if using custom PostgreSQL setup

### Quick Verification
```bash
# Check if everything works
python --version  # Should be 3.11+
cd your-project-directory
python main.py
# Open http://localhost:5000
```

## Support

For issues:
1. Verify all dependencies are installed
2. Check Python version compatibility  
3. Review console output for specific error messages
4. Ensure you're in the correct project directory

This educational platform demonstrates advanced AI security concepts with practical implementation. The project combines phishing detection, AI content analysis, and comprehensive security education in a user-friendly interface.
