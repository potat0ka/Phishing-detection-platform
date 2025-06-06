# AI Phishing Detection Platform

A comprehensive AI-powered cybersecurity platform that protects users from phishing attacks and AI-generated threats through advanced machine learning detection algorithms.

## 🎯 Project Overview

This platform serves as a final semester project demonstrating practical application of cybersecurity concepts, machine learning, and web development. It provides real-time protection against phishing URLs, emails, messages, and AI-generated content across multiple formats.

**Author**: Bigendra Shrestha  
**Purpose**: Final Semester Project - Cybersecurity & AI  
**Target**: Educational and Research Use

## ✨ Key Features

### Security Detection
- **Phishing URL Analysis**: Real-time scanning of suspicious links
- **Email Threat Detection**: Identifies malicious email content
- **AI Content Recognition**: Detects AI-generated images, videos, audio, and text
- **Multi-Format Support**: Analyzes documents, media files, and text content

### User Management
- **Role-Based Access**: Three-tier system (Super Admin, Sub Admin, Regular User)
- **Secure Authentication**: Encrypted sessions and password protection
- **User Analytics**: Track detection history and usage patterns

### Educational Features
- **Explainable AI**: Understand how detection algorithms work
- **Safety Tips**: Learn cybersecurity best practices
- **Interactive Learning**: Hands-on experience with threat detection

### Professional Interface
- **Modern Dashboard**: Bootstrap 5 responsive design
- **Real-time Analytics**: Charts and statistics
- **Dark Theme**: Professional appearance
- **Mobile Friendly**: Works on all devices

## 🛠 Technology Stack

### Backend
- **Python Flask**: Web framework
- **MongoDB**: Primary database with JSON fallback
- **PyMongo**: Database connectivity
- **Werkzeug**: Security and utilities

### Frontend
- **HTML5/CSS3**: Modern web standards
- **JavaScript ES6**: Interactive functionality
- **Bootstrap 5**: Responsive UI framework
- **Font Awesome**: Icon library
- **Chart.js**: Data visualization

### Security & AI
- **AES-256 Encryption**: Data protection
- **Scikit-learn**: Machine learning
- **OpenCV**: Image processing
- **NLTK**: Natural language processing
- **Custom Algorithms**: Threat detection logic

### Development Tools
- **Git**: Version control
- **Replit**: Development environment
- **Chrome DevTools**: Debugging
- **Postman**: API testing

## 📋 Prerequisites

### System Requirements
- **Python**: 3.11 or higher
- **MongoDB**: 4.4+ (or uses JSON fallback)
- **RAM**: 2GB minimum, 4GB recommended
- **Storage**: 500MB free space
- **Browser**: Chrome, Firefox, Safari, or Edge (latest versions)

### Development Tools (Optional)
- **Git**: For version control
- **VS Code**: Recommended code editor
- **MongoDB Compass**: Database management GUI

## 🚀 Installation Guide

### Windows Setup

#### 1. Install Python
```powershell
# Download Python from python.org or use winget
winget install Python.Python.3.11

# Verify installation
python --version
pip --version
```

#### 2. Install MongoDB (Optional)
```powershell
# Download MongoDB Community Server from mongodb.com
# Or use Chocolatey
choco install mongodb

# Start MongoDB service
net start MongoDB
```

#### 3. Clone and Setup Project
```powershell
# Clone the repository
git clone https://github.com/your-username/ai-phishing-detection-platform.git
cd ai-phishing-detection-platform

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -e .

# Run the application
python main.py
```

### macOS Setup

#### 1. Install Python and MongoDB
```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python@3.11

# Install MongoDB
brew tap mongodb/brew
brew install mongodb-community

# Start MongoDB
brew services start mongodb/brew/mongodb-community
```

#### 2. Clone and Setup Project
```bash
# Clone the repository
git clone https://github.com/your-username/ai-phishing-detection-platform.git
cd ai-phishing-detection-platform

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -e .

# Run the application
python main.py
```

### Linux Setup (Arch/Ubuntu/Debian)

#### Arch Linux
```bash
# Update system
sudo pacman -Syu

# Install Python and MongoDB
sudo pacman -S python python-pip mongodb

# Start MongoDB
sudo systemctl start mongodb
sudo systemctl enable mongodb

# Clone and setup project
git clone https://github.com/your-username/ai-phishing-detection-platform.git
cd ai-phishing-detection-platform

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -e .

# Run the application
python main.py
```

#### Ubuntu/Debian
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install python3.11 python3.11-venv python3-pip

# Install MongoDB
wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | sudo apt-key add -
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/6.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list
sudo apt update
sudo apt install mongodb-org

# Start MongoDB
sudo systemctl start mongod
sudo systemctl enable mongod

# Clone and setup project
git clone https://github.com/your-username/ai-phishing-detection-platform.git
cd ai-phishing-detection-platform

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -e .

# Run the application
python main.py
```

### Quick Start (Any Platform)

After completing platform-specific setup:

```bash
# Navigate to project directory
cd ai-phishing-detection-platform

# Activate virtual environment
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate

# Install dependencies
pip install -e .

# Run the application
python main.py
```

Access the application at: `http://localhost:5000`

## 👥 User Management System

### Role Hierarchy

#### Super Admin
- **Full System Access**: Complete control over all platform features
- **User Management**: Create, edit, promote, demote, and delete any user
- **System Configuration**: Modify security settings, API keys, and system parameters
- **Data Management**: Export user data, detection logs, and system reports
- **Model Training**: Access to AI model retraining and optimization features

#### Sub Admin
- **Limited User Management**: Create and manage regular users only
- **Content Moderation**: Review and moderate reported phishing content
- **Analytics Access**: View system statistics and user activity reports
- **Restricted Actions**: Cannot promote users or access system configuration

#### Regular User
- **Phishing Detection**: Access to all detection tools (URL, email, message, content)
- **Personal Dashboard**: View own detection history and statistics
- **Educational Content**: Access to safety tips and learning materials
- **Profile Management**: Update personal information and change password

### Default Accounts

The system creates default accounts on first startup:

```
Super Admin:
Username: admin
Password: admin123
Email: admin@phishingdetector.com

Sub Admin:
Username: subadmin
Password: subadmin123
Email: subadmin@phishingdetector.com

Regular User:
Username: user
Password: user123
Email: user@phishingdetector.com
```

**Important**: Change default passwords immediately after first login for security.

### Creating New Users

#### Via Admin Dashboard
1. Login as Super Admin or Sub Admin
2. Navigate to Admin Dashboard > User Management
3. Click "Create New User"
4. Fill in user details and assign role
5. User receives account credentials

#### Via Registration (Regular Users Only)
1. Visit `/register` page
2. Complete registration form
3. Account created with Regular User role
4. Email verification (if configured)

## 🗄 Database Configuration

### MongoDB Setup (Recommended)

#### Connection String Format
```
mongodb://username:password@host:port/database_name
```

#### Local MongoDB
```python
# Example connection for local MongoDB
MONGODB_URI = "mongodb://localhost:27017/phishing_detection"
```

#### MongoDB Atlas (Cloud)
```python
# Example connection for MongoDB Atlas
MONGODB_URI = "mongodb+srv://username:password@cluster.mongodb.net/phishing_detection"
```

### JSON Fallback (Automatic)

If MongoDB is unavailable, the system automatically uses JSON file storage:

```
data/
├── users.json          # User accounts and profiles
├── detections.json     # Detection history and results
├── reports.json        # Reported content and moderation
├── tips.json           # Safety tips and educational content
└── analytics.json      # System analytics and statistics
```

### Database Collections/Files

#### users.json / users collection
```json
{
  "username": "string",
  "email": "string", 
  "password_hash": "string",
  "role": "admin|sub_admin|user",
  "status": "active|inactive",
  "created_at": "datetime",
  "last_login": "datetime",
  "profile_data": "encrypted_string"
}
```

#### detections.json / detections collection
```json
{
  "user_id": "string",
  "content": "encrypted_string",
  "content_type": "url|email|message|image|video|audio|document",
  "result": "safe|suspicious|dangerous",
  "confidence": "float",
  "ai_analysis": "object",
  "timestamp": "datetime"
}
```

### Environment Variables

Create a `.env` file with the following configuration:

```env
# Database Configuration
MONGODB_URI=mongodb://localhost:27017/phishing_detection

# Security Settings
SESSION_SECRET=your-secure-session-secret-key-here
USER_ENCRYPTION_SECRET=your-encryption-key-for-user-data

# External Services (Optional)
SENDGRID_API_KEY=your-sendgrid-api-key
ANTHROPIC_API_KEY=your-anthropic-api-key

# Application Settings
FLASK_ENV=development
DEBUG=True
UPLOAD_FOLDER=uploads
MAX_CONTENT_LENGTH=16777216
```

## 🚀 Usage Guide

### First Time Setup
1. Start the application with `python main.py`
2. Visit `http://localhost:5000`
3. Use default credentials to login or register new account
4. Change default passwords for security

### Phishing Detection Workflow
1. **URL Analysis**: Paste suspicious URLs for real-time scanning
2. **Email Detection**: Copy email content for threat analysis
3. **Message Scanning**: Analyze text messages for phishing indicators
4. **File Analysis**: Upload images, videos, audio, or documents for AI content detection

### Admin Management
1. Login as Super Admin or Sub Admin
2. Access Admin Dashboard via user menu
3. Manage users, view analytics, moderate content
4. Configure system settings and security parameters

## 📁 Project Structure

```
ai-phishing-detection-platform/
├── models/                 # Database models and configurations
│   ├── __init__.py
│   ├── mongodb_config.py   # MongoDB connection and fallback
│   └── user_models.py      # User data structures
├── utils/                  # Utility functions and helpers
│   ├── __init__.py
│   ├── encryption_utils.py # Data encryption/decryption
│   ├── file_utils.py       # File handling utilities
│   └── validation_utils.py # Input validation functions
├── static/                 # Frontend assets
│   ├── css/               # Stylesheets and animations
│   ├── js/                # Modular JavaScript components
│   └── images/            # Static images and assets
├── templates/             # HTML templates
│   ├── admin/             # Admin dashboard templates
│   ├── auth/              # Authentication templates
│   └── base.html          # Base template with Bootstrap
├── data/                  # JSON fallback storage
├── uploads/               # User uploaded files
├── app.py                 # Flask application configuration
├── main.py                # Application entry point
├── routes.py              # Main application routes
├── auth_routes.py         # Authentication system
├── admin_routes.py        # Admin dashboard functionality
├── ml_detector.py         # AI/ML detection algorithms
├── offline_threat_intel.py # Threat intelligence system
├── security_tips_updater.py # Educational content system
├── pyproject.toml         # Python dependencies and project config
├── DEPENDENCIES.md        # Comprehensive dependency documentation
├── CODEBASE_CLEANUP_SUMMARY.md # Project organization summary
└── README.md             # This documentation
```

## 📦 Dependencies

This project uses modern Python dependency management through `pyproject.toml`. All dependencies are automatically installed with a single command.

### Key Dependencies
- **Flask 3.1.1+**: Web framework
- **PyMongo 4.13.0+**: MongoDB driver with JSON fallback
- **scikit-learn 1.6.1+**: Machine learning algorithms
- **OpenCV-Python 4.11.0+**: Computer vision and image processing
- **TensorFlow 2.14.0+**: Deep learning framework
- **cryptography 45.0.3+**: AES-256 encryption for security

For complete dependency information, see [DEPENDENCIES.md](DEPENDENCIES.md).

## 🧪 Testing

### Manual Testing
1. **Registration**: Create new user accounts
2. **Authentication**: Test login/logout functionality
3. **Role Management**: Verify role-based access control
4. **Detection Features**: Test all detection capabilities
5. **Admin Functions**: Verify admin dashboard features

### Security Testing
1. **Input Validation**: Test with malicious inputs
2. **Authentication**: Verify session management
3. **Authorization**: Test role restrictions
4. **Data Encryption**: Verify sensitive data protection

## 🚀 Deployment

### Local Deployment
The application is ready for local deployment using the installation instructions above.

### Production Deployment
For production deployment:

1. **Set Environment Variables**:
   ```bash
   export FLASK_ENV=production
   export DEBUG=False
   export SESSION_SECRET=secure-production-key
   ```

2. **Use Production Database**:
   Configure MongoDB connection for production environment

3. **Enable HTTPS**:
   Use reverse proxy (nginx) or cloud platform SSL

4. **Security Hardening**:
   - Change all default passwords
   - Configure firewall rules
   - Enable monitoring and logging

### Cloud Deployment Options
- **Heroku**: Ready for Heroku deployment
- **AWS**: Compatible with EC2, Lambda, and RDS
- **Google Cloud**: Works with App Engine and Cloud Run
- **DigitalOcean**: Compatible with Droplets and App Platform

## 📚 Learning Resources

### For Beginners
This project demonstrates key concepts in:
- **Web Development**: Flask framework, HTML/CSS/JavaScript
- **Database Management**: MongoDB operations and data modeling
- **Security**: Authentication, authorization, and data encryption
- **Machine Learning**: AI algorithms for threat detection
- **Software Engineering**: Project structure and best practices

### Code Examples
Every file includes detailed comments explaining:
- What each function does
- How algorithms work
- Why specific approaches were chosen
- How to modify or extend functionality

## 🤝 Contributing

### Development Setup
1. Fork the repository
2. Create feature branch
3. Make changes with proper documentation
4. Test thoroughly
5. Submit pull request

### Code Standards
- Follow PEP 8 for Python code
- Add comments for complex logic
- Include docstrings for functions
- Test all new features

## 📄 License

This project is created for educational purposes as a final semester project.

## 🆘 Support

### Common Issues
- **MongoDB Connection**: Check connection string and service status
- **Python Dependencies**: Ensure all packages are installed correctly
- **File Permissions**: Verify write permissions for data directory
- **Port Conflicts**: Ensure port 5000 is available

### Getting Help
- Check the troubleshooting section below
- Review code comments for implementation details
- Test with provided default accounts

## 🔧 Troubleshooting

### Application Won't Start
```bash
# Check Python version
python --version

# Verify dependencies
pip list

# Check for errors
python main.py
```

### Database Connection Issues
```bash
# Test MongoDB connection
python -c "import pymongo; print('MongoDB available')"

# Check JSON fallback
ls -la data/
```

### Permission Errors
```bash
# Fix permissions
chmod -R 755 .
mkdir -p data uploads
```

---

**Author**: Bigendra Shrestha  
**Project**: Final Semester - AI Phishing Detection Platform  
**Institution**: Saraswati Multiple Campus
**Year**: 2024-2025
