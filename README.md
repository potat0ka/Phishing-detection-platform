# 🛡️ AI Phishing Detection Platform

A comprehensive, enterprise-grade cybersecurity platform that detects phishing threats and AI-generated content using advanced machine learning algorithms. This platform provides real-time analysis of URLs, emails, messages, and multimedia content with role-based administration and complete audit capabilities.

## 📋 Project Overview

This platform is a full-featured security solution designed to protect users from phishing attacks and identify AI-generated content across multiple media types. The system combines traditional rule-based detection with modern AI/ML techniques to provide accurate threat assessment and content authenticity verification.

**Key Capabilities:**
- **Phishing Detection**: Analyze URLs, emails, and text messages for phishing indicators
- **AI Content Detection**: Identify AI-generated images, videos, audio, and documents
- **Real-time Analysis**: Instant threat assessment with confidence scoring
- **Role-based Access Control**: Super Admin, Sub Admin, and User roles with granular permissions
- **Comprehensive Analytics**: System-wide monitoring and reporting capabilities
- **Educational Resources**: 39+ security tips and cybersecurity awareness content
- **Data Security**: AES-256 encryption with zero-knowledge architecture

**Technologies Used:**
- **Backend**: Python 3.11+ (Flask framework)
- **Frontend**: HTML5, CSS3, JavaScript (Bootstrap 5 responsive design)
- **Database**: MongoDB with JSON fallback for reliability
- **Security**: AES-256 encryption, secure session management
- **AI/ML**: Scikit-learn, OpenCV, NLTK, PIL for content analysis
- **File Processing**: Support for images, videos, audio, and documents up to 500MB

## 🚀 Quick Start Guide

### Prerequisites
- **Python**: 3.8 or higher (3.11+ recommended)
- **Operating System**: Windows, macOS, or Linux
- **Memory**: 2GB RAM minimum (4GB recommended for AI analysis)
- **Storage**: 2GB free space
- **Internet**: Required for initial setup and threat intelligence updates

### Installation Steps

#### 1. Clone or Download the Project
```bash
# Option A: Clone with Git
git clone <repository-url>
cd ai-phishing-detection-platform

# Option B: Download ZIP file and extract
# Then navigate to the extracted folder in terminal
```

#### 2. Set Up Python Environment (Recommended)

**Windows:**
```cmd
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# You should see (venv) in your prompt
```

**macOS/Linux:**
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# You should see (venv) in your prompt
```

#### 3. Install Required Dependencies
```bash
# Upgrade pip first
pip install --upgrade pip

# Install all required packages
pip install flask werkzeug pillow numpy scikit-learn nltk beautifulsoup4 requests trafilatura dnspython email-validator opencv-python cryptography pymongo flask-pymongo psycopg2-binary
```

#### 4. Start the Application
```bash
# Start the Flask development server
python main.py

# The application will start on http://localhost:5000
```

#### 5. Access the Platform
1. Open your web browser
2. Navigate to: `http://localhost:5000`
3. You'll see the homepage with the security expert avatar and quick detection tools

#### 6. Create Your First Account
1. Click "Register" to create a new account
2. Fill in username, email, and secure password (8+ characters, mixed case, numbers)
3. Login with your credentials
4. Start using the phishing detection and AI content analysis features

## 👥 User Roles and Permissions

### User Role Hierarchy

#### 🔴 Super Admin (Highest Level)
**Full Platform Control:**
- **User Management**: Create, edit, promote, demote, and delete any user
- **System Administration**: Database backups, optimization, health checks
- **Role Management**: Promote users to Sub Admin or demote from any role
- **ML Model Training**: Retrain models, adjust settings, run accuracy tests
- **Security Settings**: Configure encryption, API keys, security policies
- **Data Export**: Export all system data including users and detections
- **Audit Access**: View complete login history and system audit logs
- **Content Moderation**: Manage reported content and safety tips

#### 🟡 Sub Admin (Limited Administrative)
**User Management Only:**
- **User Operations**: Create, edit, and delete regular users only
- **User Monitoring**: View user statistics and detection patterns
- **Content Management**: Add and edit safety tips
- **Report Handling**: Review and moderate reported content
- **Data Export**: Export user lists and detection summaries
- **Restrictions**: Cannot promote/demote users or access Super Admin functions

#### 🟢 Regular User (Standard Access)
**Core Security Features:**
- **Phishing Detection**: Analyze URLs, emails, and messages
- **AI Content Analysis**: Upload and analyze images, videos, audio, documents
- **Personal Dashboard**: View own detection history and statistics
- **Profile Management**: Update account settings and password
- **Educational Access**: Browse security tips and learning resources
- **Data Control**: Export and delete own detection history

### Creating Admin Accounts

#### Method 1: First-Time Setup (Automatic Super Admin)
```bash
# When you first register, you become Super Admin automatically
# Navigate to /admin after registration to access admin features
```

#### Method 2: Manual Role Assignment
```python
# Run this script to promote existing users
from mongodb_config import MongoDBManager
from encryption_utils import decrypt_sensitive_data, encrypt_sensitive_data

db = MongoDBManager()

# Find and promote user
users = db.find_many("users")
for user_data in users:
    try:
        user = decrypt_sensitive_data("user", user_data)
        if user.get("username") == "your_username_here":
            # Set role (super_admin, sub_admin, or user)
            user["role"] = "super_admin"
            user["is_admin"] = True
            
            # Save changes
            encrypted_data = encrypt_sensitive_data("user", user)
            encrypted_data["_id"] = user_data["_id"]
            db.update_one("users", {"_id": user_data["_id"]}, encrypted_data)
            print(f"User {user['username']} promoted to super admin")
            break
    except Exception as e:
        continue
```

## 🛠️ Core Features

### 🛡️ Phishing Detection Engine

#### URL Analysis
- **Link Verification**: Real-time scanning of suspicious URLs
- **Domain Reputation**: Check against known phishing databases
- **Redirect Detection**: Follow and analyze URL redirections
- **SSL Certificate Validation**: Verify website security certificates
- **Confidence Scoring**: 0-100% threat assessment with detailed explanations

#### Email Content Analysis
- **Header Inspection**: Analyze email headers for spoofing indicators
- **Link Extraction**: Identify and verify all embedded links
- **Attachment Scanning**: Security analysis of email attachments
- **Sender Verification**: Check sender reputation and authenticity
- **Social Engineering Detection**: Identify manipulation tactics

#### Message Scanning
- **Text Pattern Analysis**: Detect phishing keywords and phrases
- **Urgency Detection**: Identify high-pressure tactics
- **Contact Information Verification**: Validate phone numbers and addresses
- **Link Analysis**: Check embedded links in messages

### 🤖 AI Content Detection System

#### Image Analysis (Up to 500MB)
- **AI Generation Detection**: Identify AI-created vs authentic photos
- **Metadata Analysis**: EXIF data inspection for authenticity
- **Pixel Pattern Recognition**: Statistical analysis of image characteristics
- **Device Photo Indicators**: Detect real camera vs AI-generated signatures
- **Source Identification**: Identify likely AI generation tools used

#### Video Analysis
- **Deepfake Detection**: Advanced algorithms to identify manipulated videos
- **Frame Consistency**: Analyze temporal consistency across frames
- **Compression Patterns**: Detect AI-specific encoding signatures
- **Motion Analysis**: Identify unnatural movement patterns

#### Audio Analysis
- **Voice Synthesis Detection**: Identify AI-generated speech
- **Spectral Analysis**: Analyze frequency patterns for authenticity
- **Voice Cloning Detection**: Detect artificially cloned voices
- **Audio Artifact Analysis**: Identify AI generation artifacts

#### Document Analysis
- **Writing Pattern Detection**: Identify AI text generation patterns
- **Vocabulary Analysis**: Analyze word choice and sentence structure
- **Content Flow**: Detect unnatural text progression
- **Source Attribution**: Identify likely AI writing tools

### 📊 Admin Dashboard Features

#### User Management
- **User Overview**: Complete user list with registration dates and activity
- **Role Management**: Promote, demote, and assign user roles
- **Account Actions**: Reset passwords, deactivate accounts, delete users
- **Privacy Protection**: View encrypted user data without personal details
- **Bulk Operations**: Perform actions on multiple users simultaneously

#### System Analytics
- **Detection Statistics**: Real-time phishing and AI detection metrics
- **User Activity**: Platform usage patterns and engagement metrics
- **Performance Monitoring**: System response times and accuracy rates
- **Threat Intelligence**: Emerging phishing patterns and trends
- **Resource Usage**: Storage, memory, and processing utilization

#### Content Moderation
- **Reported Content**: Review and moderate user-reported suspicious content
- **Safety Tips Management**: Add, edit, and organize security education content
- **Audit Logs**: Complete system activity and security event logs
- **Data Export**: Generate reports in CSV and JSON formats

#### System Management
- **Database Operations**: Backup, optimize, and maintain data integrity
- **ML Model Training**: Retrain detection models with new data
- **Security Settings**: Configure encryption, session timeouts, file limits
- **API Management**: Rotate keys and manage external service connections

### 📚 Educational Resources

#### Security Awareness
- **39+ Security Tips**: Comprehensive cybersecurity education content
- **Phishing Examples**: Real-world examples with detailed explanations
- **Best Practices**: Guidelines for safe online behavior
- **Current Threats**: Latest phishing trends and attack methods
- **Interactive Learning**: Hands-on security awareness training

#### Safety Guidelines
- **Email Security**: Identify suspicious emails and attachments
- **Password Security**: Create and manage strong passwords
- **Safe Browsing**: Tips for secure web navigation
- **Social Engineering**: Recognize manipulation tactics
- **Mobile Security**: Smartphone and tablet security practices

## 🗄️ Database Configuration

### Automatic Database Setup
The platform uses a hybrid database approach for maximum reliability:
- **Primary**: MongoDB for scalable document storage
- **Fallback**: JSON files for automatic failover when MongoDB is unavailable
- **Security**: All data encrypted using AES-256 field-level encryption
- **Backup**: Automatic data backup and recovery capabilities

### MongoDB Setup (Recommended for Production)

#### Install MongoDB

**Windows:**
1. Download MongoDB Community Server from mongodb.com
2. Install using the MSI installer
3. MongoDB will start automatically as a Windows service

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
# Install MongoDB
sudo apt update
sudo apt install -y mongodb

# Start MongoDB service
sudo systemctl start mongodb
sudo systemctl enable mongodb
```

### Environment Configuration
Create a `.env` file in the project root for custom settings:
```bash
# Security Configuration (Required for production)
USER_ENCRYPTION_SECRET=your-32-character-encryption-key-here
SESSION_SECRET=your-session-secret-key-here

# Database Configuration
DATABASE_URL=mongodb://localhost:27017/phishing_detector

# Application Settings
FLASK_ENV=development
FLASK_DEBUG=True
MAX_CONTENT_LENGTH=524288000  # 500MB file upload limit
```

## 🔒 Security Architecture

### Data Protection
- **AES-256 Encryption**: All sensitive data encrypted at rest and in transit
- **Field-Level Encryption**: Individual encryption of user data fields
- **Zero-Knowledge Architecture**: Admins cannot access encrypted user personal data
- **Secure Sessions**: Encrypted session management with automatic timeout
- **Password Security**: Bcrypt hashing with salt for password storage

### Privacy Protection
- **Data Minimization**: Collect only necessary information
- **User Control**: Users can export and delete their data
- **Audit Logging**: All system actions logged and monitored
- **Secure File Handling**: Temporary file cleanup and secure processing
- **GDPR Compliance**: Privacy-by-design architecture

### Threat Protection
- **Input Validation**: Comprehensive sanitization of all user inputs
- **File Upload Security**: Strict file type and size validation
- **SQL Injection Prevention**: Parameterized queries and ORM protection
- **XSS Protection**: Content Security Policy and output encoding
- **CSRF Protection**: Anti-CSRF tokens on all forms

## 📂 Project Structure

```
ai-phishing-detection-platform/
├── main.py                    # Application entry point
├── app.py                     # Flask application configuration
├── routes.py                  # Main web routes
├── auth_routes.py             # Authentication system
├── admin_routes.py            # Admin dashboard functionality
├── mongodb_config.py          # Database management
├── encryption_utils.py        # AES-256 encryption utilities
├── ml_detector.py             # ML phishing detection
├── ai_content_detector.py     # AI content analysis
├── offline_threat_intel.py    # Threat intelligence database
├── security_tips_updater.py   # Security education content
├── utils.py                   # Utility functions
├── simple_models.py           # ML model definitions
├── threat_intelligence.py     # Threat data management
├── templates/                 # HTML templates
│   ├── base.html              # Base template with Bootstrap
│   ├── index.html             # Homepage with avatar
│   ├── login.html             # User authentication
│   ├── register.html          # User registration
│   ├── check.html             # Phishing detection interface
│   ├── ai_content_check.html  # AI content analysis
│   ├── result.html            # Detection results
│   ├── ai_content_results.html # AI analysis results
│   ├── dashboard.html         # User dashboard
│   ├── admin_dashboard.html   # Admin control panel
│   └── tips.html              # Security education
├── static/                    # Static assets
│   ├── css/
│   │   ├── style.css          # Main styles with avatar animations
│   │   └── loading-animations.css # Loading animations
│   ├── js/
│   │   ├── modules/           # Modular JavaScript
│   │   │   ├── animations.js  # UI animations
│   │   │   ├── auth.js        # Authentication
│   │   │   ├── forms.js       # Form handling
│   │   │   ├── ui.js          # User interface
│   │   │   └── analytics.js   # Analytics
│   │   ├── main.js            # Main application JS
│   │   ├── app.js             # Application initialization
│   │   └── mascot-loader.js   # Loading screen
│   ├── images/
│   │   └── hero-avatar.png    # Homepage avatar image
│   └── uploads/               # Temporary upload storage
├── data/                      # Application data
│   ├── users.json             # Encrypted user database
│   ├── detections.json        # Detection history
│   ├── tips.json              # Security tips
│   ├── reports.json           # Content reports
│   └── ml_models/             # Machine learning models
├── uploads/                   # File upload processing
├── backups/                   # Database backups
└── instance/                  # Instance configuration
```

## 🚀 Advanced Usage

### Machine Learning Model Training

The platform includes real ML model training capabilities:

```python
# Retrain phishing detection model
from admin_routes import retrain_model

# Collect data from database
# Train actual scikit-learn models
# Calculate real accuracy metrics
# Save trained models for production use
```

### System Administration

#### Database Backup and Optimization
```bash
# Access admin dashboard at /admin
# Use "System Management" section
# Click "Backup Database" for full backup
# Click "Optimize Database" for performance tuning
```

#### Performance Monitoring
- Real-time system health checks
- Database performance metrics
- Detection accuracy tracking
- Resource utilization monitoring

#### Security Auditing
- Complete login history tracking
- System action audit logs
- Security event monitoring
- Threat pattern analysis

### API Integration

The platform is designed for easy API integration:
- RESTful endpoints for detection services
- JSON response format for all operations
- Authentication token support
- Rate limiting and security controls

## 🛠️ Troubleshooting

### Common Issues

#### "Port 5000 is already in use"
```bash
# Find and kill process using port 5000
# Windows: netstat -ano | findstr :5000
# macOS/Linux: lsof -ti:5000 | xargs kill -9

# Or use different port
python main.py --port 8080
```

#### "Module not found" errors
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Install missing dependencies
pip install -r requirements.txt
```

#### Database connection issues
```bash
# Check MongoDB status
# Windows: services.msc (look for MongoDB)
# macOS: brew services list | grep mongodb
# Linux: sudo systemctl status mongodb

# Platform automatically falls back to JSON if MongoDB unavailable
```

#### File upload failures
- Check file size (max 500MB)
- Verify file type is supported
- Ensure sufficient disk space
- Check uploads directory permissions

### Performance Optimization

#### For Large Deployments
```bash
# Increase file upload limits
export MAX_CONTENT_LENGTH=1073741824  # 1GB

# Enable MongoDB for better performance
export DATABASE_URL=mongodb://localhost:27017/phishing_detector

# Use production settings
export FLASK_ENV=production
export FLASK_DEBUG=False
```

#### Memory Management
- The AI content detector loads models on-demand
- File uploads are processed and cleaned automatically
- Database connections are pooled and managed efficiently

## 🔮 Current Capabilities

### Fully Functional Features
✅ **User Authentication**: Complete registration, login, and session management  
✅ **Phishing Detection**: Real-time URL, email, and message analysis  
✅ **AI Content Detection**: Image, video, audio, and document analysis  
✅ **Role-based Access**: Super Admin, Sub Admin, and User roles with proper permissions  
✅ **Admin Dashboard**: Complete user management, analytics, and system administration  
✅ **Database Management**: MongoDB with JSON fallback and encryption  
✅ **ML Model Training**: Real scikit-learn model training with accuracy metrics  
✅ **Data Export**: CSV and JSON export functionality  
✅ **Security Education**: 39+ security tips and awareness content  
✅ **File Processing**: Support for multiple file types up to 500MB  
✅ **System Monitoring**: Real-time health checks and performance metrics  
✅ **Content Moderation**: Report management and content review  
✅ **Audit Logging**: Complete system activity tracking  

### Code Quality
✅ **Modular Architecture**: Well-organized, maintainable codebase  
✅ **Comprehensive Documentation**: Detailed comments explaining ML concepts  
✅ **Error Handling**: Robust error management and user feedback  
✅ **Security Best Practices**: Encryption, validation, and secure coding  
✅ **Responsive Design**: Mobile-friendly interface with Bootstrap 5  
✅ **Real Backend Operations**: No placeholder or mock data  

## 📧 Support and Documentation

### Getting Help
1. Check console/terminal output for error messages
2. Review the troubleshooting section above
3. Verify all dependencies are installed correctly
4. Ensure database connectivity (MongoDB or JSON fallback)

### Learning Resources
- **Beginner-Friendly**: Comprehensive comments throughout codebase
- **Educational Focus**: Platform designed for learning cybersecurity concepts
- **Real-World Application**: Practical phishing detection and AI analysis
- **Professional Development**: Industry-standard security practices

### Contributing
The platform is designed as a learning tool with:
- Clean, well-documented code
- Modular architecture for easy extension
- Educational comments explaining complex concepts
- Real-world security applications

---

**Built with ❤️ for cybersecurity education and real-world threat protection**

*This platform demonstrates advanced cybersecurity concepts, machine learning applications, and secure web development practices. Perfect for final semester projects, security research, and practical cybersecurity learning.*