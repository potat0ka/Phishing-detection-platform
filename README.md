# 🛡️ AI Phishing Detection Platform

A comprehensive, enterprise-grade phishing detection system that identifies potential phishing content from websites, emails, messages, and links using advanced AI and machine learning algorithms. Built with Flask, Python, HTML, CSS, and JavaScript for a complete web-based security solution.

## 📋 Project Overview

This platform is a full-featured phishing detection system designed to help users identify and avoid phishing attempts across multiple communication channels. The system combines traditional rule-based detection with modern AI/ML techniques to provide accurate threat assessment.

**Key Capabilities:**
- Analyze URLs, emails, and text messages for phishing indicators
- AI-powered content detection for images, videos, audio, and documents
- Real-time threat intelligence and security assessment
- User authentication with role-based access control
- Educational content and security awareness training
- Admin dashboard with comprehensive management tools

**Technologies Used:**
- **Backend**: Python (Flask framework)
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Database**: MongoDB with JSON fallback for reliability
- **Security**: AES-256 encryption, secure session management
- **AI/ML**: Scikit-learn, OpenCV, NLTK for content analysis
- **UI Framework**: Bootstrap 5 with responsive design

## 🚀 Quick Start Guide

### Prerequisites
- **Python**: 3.8 or higher (3.11+ recommended)
- **Operating System**: Windows, macOS, or Linux
- **Memory**: 1GB RAM minimum (2GB recommended)
- **Storage**: 1GB free space
- **Internet**: Required for initial setup

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
pip install flask werkzeug pillow numpy scikit-learn nltk beautifulsoup4 requests trafilatura dnspython email-validator opencv-python-headless cryptography pymongo flask-pymongo psycopg2-binary
```

#### 4. Start the Application
```bash
# Start the Flask development server
python main.py

# Alternative commands if main.py doesn't work:
# python app.py
# flask run
```

#### 5. Access the Platform
1. Open your web browser
2. Navigate to: `http://localhost:5000`
3. Alternative addresses if localhost doesn't work:
   - `http://127.0.0.1:5000`
   - `http://0.0.0.0:5000`

#### 6. Create Your First Account
1. Click "Register" to create a new account
2. Fill in username, email, and secure password
3. Login with your credentials
4. Start using the phishing detection features

## 🗄️ Database Configuration

### Automatic Database Setup
The platform uses a hybrid database approach for maximum reliability:
- **Primary**: MongoDB for scalable document storage
- **Fallback**: JSON files for automatic failover when MongoDB is unavailable
- **Security**: All data is encrypted using AES-256 encryption

### MongoDB Setup (Optional but Recommended)

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

### Environment Configuration (Optional)
Create a `.env` file in the project root for custom settings:
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

## 👥 User Roles and Admin Setup

### User Types

#### Regular Users
**What they can do:**
- Create account and login securely
- Analyze URLs, emails, and messages for phishing threats
- Upload files (images, videos, audio, documents) for AI content analysis
- View their personal detection history
- Access security education content and tips
- Manage their profile and account settings
- Export their detection data

**What they cannot do:**
- Access other users' data or detection history
- View system-wide analytics or statistics
- Manage other users or system settings

#### Admin Users
**Additional capabilities beyond regular users:**
- View system-wide usage statistics and analytics
- Monitor platform performance and security metrics
- Access aggregated detection data (no personal user data)
- Manage system security settings
- View audit logs and security events
- Update security tips and educational content
- Perform system backup and maintenance

**Privacy Protection:**
- Admins cannot view encrypted user personal data
- Zero-knowledge architecture protects user privacy
- All admin actions are logged and audited

### Creating Admin Users

#### Method 1: Create Demo Admin Account
The platform includes a script to create demo accounts:
```bash
# Run the demo account creator
python create_demo_accounts.py

# This creates:
# Admin: username="demo_admin", password="admin123"
# User: username="demo_user", password="user123"
```

#### Method 2: Promote Regular User to Admin
1. Create a regular user account through the web interface
2. Run the following script to promote them:
```python
# Edit and run this script
from mongodb_config import MongoDBManager
from encryption_utils import decrypt_sensitive_data, encrypt_sensitive_data

db = MongoDBManager()

# Find the user you want to promote
users = db.find_many("users")
for user_data in users:
    try:
        user = decrypt_sensitive_data("user", user_data)
        if user.get("username") == "your_username_here":
            # Promote to admin
            user["role"] = "admin"
            user["is_admin"] = True
            
            # Encrypt and save
            encrypted_data = encrypt_sensitive_data("user", user)
            encrypted_data["_id"] = user_data["_id"]
            
            db.update_one("users", {"_id": user_data["_id"]}, encrypted_data)
            print(f"User {user['username']} promoted to admin")
            break
    except Exception as e:
        continue
```

### Accessing Admin Dashboard
1. Login with an admin account
2. Navigate to: `http://localhost:5000/admin`
3. Or click "Admin Dashboard" in the navigation menu (only visible to admins)

## 🛠️ Features Overview

### Core Detection Capabilities

#### 🛡️ Phishing Detection
- **URL Analysis**: Comprehensive scanning of suspicious links and websites
- **Email Content Analysis**: Advanced detection of phishing attempts in emails
- **Message Scanning**: Analysis of text messages and social media content
- **Link Verification**: Real-time assessment of hyperlinks and redirects
- **Confidence Scoring**: Percentage-based threat assessment with detailed explanations
- **Threat Intelligence**: Offline database of known phishing indicators

#### 🤖 AI Content Detection
- **Image Analysis**: Detect AI-generated vs authentic photos (up to 500MB files)
- **Video Analysis**: Identify deepfakes and AI-generated video content
- **Audio Detection**: Recognize synthetic speech and voice cloning attempts
- **Document Scanning**: Analyze text documents for AI writing patterns
- **Device Photo Recognition**: EXIF metadata analysis for authentic device photos
- **Source Identification**: Identify likely AI generation tools used

### User Management Features

#### 👤 Authentication System
- **Secure Registration**: Strong password requirements with visual indicators
- **Encrypted Sessions**: AES-256 encrypted user sessions and data storage
- **Password Security**: Secure hash storage with salt
- **Session Management**: Automatic timeout and secure session handling
- **Privacy Protection**: Zero-knowledge architecture

#### 📊 User Dashboard
- **Detection History**: Complete history of all scans and analysis results
- **Bulk Operations**: Select and delete multiple detection records
- **Profile Management**: Update account settings and preferences
- **Activity Tracking**: Monitor usage patterns and security events
- **Data Export**: Download detection history in CSV/JSON formats

### Educational Features

#### 📚 Security Education
- **39+ Security Tips**: Comprehensive cybersecurity awareness content
- **Current Threat Landscape**: Latest phishing trends and attack methods
- **Interactive Learning**: Real-world examples and prevention techniques
- **Best Practices**: Guidelines for safe online behavior
- **Mobile Optimization**: Educational content optimized for all devices

#### 🎯 Safety Guidelines
- **Phishing Prevention**: Step-by-step guides to avoid threats
- **Email Security**: Identify suspicious emails and attachments
- **Social Engineering**: Recognize manipulation tactics
- **Password Security**: Create and manage strong passwords
- **Safe Browsing**: Tips for secure web navigation

### Administrative Features

#### 🔧 Admin Dashboard
- **User Management**: View registered users (privacy-protected)
- **System Monitoring**: Track platform usage and performance
- **Security Oversight**: Monitor threat detection patterns
- **Content Management**: Update security tips and education
- **Analytics**: Comprehensive system and usage analytics

#### 📈 Analytics and Reporting
- **Detection Statistics**: Track phishing and AI detection rates
- **User Analytics**: Platform usage patterns and trends
- **Threat Intelligence**: Monitor emerging phishing patterns
- **Performance Metrics**: System response times and accuracy

## 📂 Project Structure

```
ai-phishing-detection-platform/
├── main.py                    # Application entry point and server startup
├── app.py                     # Flask application configuration and setup
├── routes.py                  # Main web routes and request handlers
├── auth_routes.py             # Authentication routes (login, register, logout)
├── admin_routes.py            # Admin dashboard routes and functionality
├── mongodb_config.py          # Database connection and management
├── encryption_utils.py        # AES-256 encryption utilities
├── ml_detector.py             # Phishing detection algorithms
├── ai_content_detector.py     # AI content detection system
├── offline_threat_intel.py    # Local threat intelligence database
├── security_tips_updater.py   # Security awareness content management
├── utils.py                   # Utility functions and helpers
├── create_demo_accounts.py    # Demo account creation script
├── templates/                 # HTML templates with Jinja2
│   ├── base.html              # Base template with Bootstrap framework
│   ├── index.html             # Landing page and home
│   ├── auth/                  # Authentication templates
│   │   ├── login.html         # User login form
│   │   └── register.html      # User registration form
│   ├── check.html             # Phishing detection interface
│   ├── ai_content_check.html  # AI content analysis interface
│   ├── result.html            # Analysis results display
│   ├── ai_content_results.html # AI content results display
│   ├── dashboard.html         # User dashboard and history
│   ├── admin_dashboard.html   # Admin control panel
│   └── tips.html              # Security education content
├── static/                    # Static web assets
│   ├── css/                   # Custom stylesheets
│   │   ├── style.css          # Main application styles
│   │   └── loading-animations.css # Loading animations
│   ├── js/                    # JavaScript functionality
│   │   ├── modules/           # Modular JavaScript components
│   │   │   ├── animations.js  # UI animations and effects
│   │   │   ├── auth.js        # Authentication functionality
│   │   │   ├── forms.js       # Form handling and validation
│   │   │   ├── ui.js          # User interface interactions
│   │   │   └── analytics.js   # Analytics and tracking
│   │   ├── main.js            # Main application JavaScript
│   │   ├── app.js             # Application initialization
│   │   └── mascot-loader.js   # Loading screen mascot
│   └── uploads/               # Temporary file upload storage
├── instance/                  # Instance-specific data files
│   ├── users.json             # Encrypted user data (JSON fallback)
│   ├── detections.json        # Encrypted detection history
│   ├── tips.json              # Security tips database
│   └── audit_logs.json        # System activity logs
├── data/                      # Application data files
│   └── threat_intelligence/   # Threat intelligence databases
├── uploads/                   # File upload processing
└── requirements.txt           # Python dependencies list
```

## 🔒 Security Features

### Data Protection
- **AES-256 Encryption**: All sensitive data encrypted at rest
- **Field-Level Encryption**: Individual encryption of user data fields
- **Secure Sessions**: Encrypted session management with automatic timeout
- **Password Security**: Bcrypt hashing with salt for password storage
- **Zero-Knowledge Architecture**: Admins cannot access encrypted user data

### Privacy Protection
- **Data Minimization**: Only collect necessary information
- **User Control**: Users can export and delete their data
- **Audit Logging**: All system actions are logged and monitored
- **Secure File Handling**: Temporary file cleanup and secure processing
- **HTTPS Ready**: SSL/TLS support for production deployment

## 🚀 Production Deployment

### Environment Variables for Production
```bash
# Security (Required for production)
USER_ENCRYPTION_SECRET=your-production-encryption-key-32-chars
SESSION_SECRET=your-production-session-secret-key

# Database (Recommended for production)
DATABASE_URL=mongodb://username:password@host:port/database
# Or MongoDB Atlas
DATABASE_URL=mongodb+srv://username:password@cluster.mongodb.net/database

# Application Settings
FLASK_ENV=production
FLASK_DEBUG=False
```

### Production Checklist
- [ ] Set strong encryption keys in environment variables
- [ ] Use MongoDB for database (not JSON fallback)
- [ ] Configure HTTPS/SSL certificates
- [ ] Set up proper backup procedures
- [ ] Monitor system logs and performance
- [ ] Regular security updates and patches

## 🛠️ Troubleshooting

### Common Issues

#### "Port 5000 is already in use"
```bash
# Try different port
python main.py --port 8080

# Or find and kill process using port 5000
# Windows: netstat -ano | findstr :5000
# macOS/Linux: lsof -ti:5000 | xargs kill
```

#### "Module not found" errors
```bash
# Ensure virtual environment is activated
# Install missing dependencies
pip install -r requirements.txt

# Or install individual packages
pip install flask werkzeug pillow numpy
```

#### Database connection issues
```bash
# Check if MongoDB is running
# Windows: services.msc (look for MongoDB)
# macOS: brew services list | grep mongodb
# Linux: sudo systemctl status mongodb

# Platform will automatically fallback to JSON files if MongoDB unavailable
```

#### File upload issues
```bash
# Check uploads directory permissions
# Ensure sufficient disk space
# Verify file size limits (default: 500MB)
```

### Getting Help
1. Check the console/terminal output for error messages
2. Verify all dependencies are installed correctly
3. Ensure Python version is 3.8 or higher
4. Check file permissions in the project directory
5. Try running with admin/sudo privileges if needed

## 📝 License and Credits

This AI Phishing Detection Platform was developed as a comprehensive security education and threat detection tool. The system incorporates multiple security best practices and modern web development techniques to provide a robust, user-friendly platform for cybersecurity awareness and protection.

**Key Contributors:**
- Advanced phishing detection algorithms
- AI content analysis capabilities
- Responsive web design and user experience
- Enterprise-grade security architecture
- Educational content and security awareness

**Technical Acknowledgments:**
- Flask web framework for robust backend architecture
- Bootstrap 5 for responsive, accessible user interface
- MongoDB for scalable data storage with JSON fallback
- Scikit-learn and OpenCV for machine learning capabilities
- Advanced encryption libraries for data protection

---

🛡️ **Stay Safe Online** - This platform is designed to educate and protect users from evolving cybersecurity threats. Regular updates ensure protection against the latest phishing and social engineering attacks.