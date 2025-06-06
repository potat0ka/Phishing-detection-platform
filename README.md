# AI Phishing Detection Platform

A comprehensive AI-powered cybersecurity platform that detects phishing attacks and AI-generated threats using machine learning algorithms.

**Author**: Bigendra Shrestha  
**Purpose**: Final Semester Project - Cybersecurity & AI  
**Target**: Educational and Research Use

## Quick Overview

This platform provides:
- Real-time phishing URL detection
- Email threat analysis
- AI-generated content detection
- User-friendly web interface
- Admin dashboard for management
- Educational cybersecurity tips

## 🚀 Quick Start Guide

Follow these simple steps to run the project on your computer:

### Step 1: Install Python

**Windows:**
- Download Python 3.11+ from [python.org](https://python.org)
- During installation, check "Add Python to PATH"

**macOS:**
```bash
# Using Homebrew (recommended)
brew install python@3.11
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install python3.11 python3.11-pip python3.11-venv
```

### Step 2: Clone the Repository

```bash
git clone https://github.com/your-username/ai-phishing-detection-platform.git
cd ai-phishing-detection-platform
```

### Step 3: Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate
```

### Step 4: Install Dependencies

```bash
# Install all required packages
pip install -r requirements-local.txt
```

### Step 5: Run the Application

```bash
python main.py
```

### Step 6: Access the Application

1. Open your web browser
2. Go to: `http://localhost:5000`
3. You should see the AI Phishing Detection Platform homepage

## 🔑 Default Login Credentials

**Admin Account:**
- Username: `admin`
- Password: `admin123`

**Regular User:**
- Username: `user`
- Password: `user123`

**Important:** Change these passwords after first login!

## ⚙️ Configuration (Optional)

The application works out of the box with default settings. For advanced configuration:

### Environment Variables

Create a `.env` file in the project root (optional):

```env
# Database (optional - uses JSON files by default)
MONGODB_URI=mongodb://localhost:27017/phishing_detection

# Security (optional - auto-generated if not provided)
SESSION_SECRET=your-secret-key-here
USER_ENCRYPTION_SECRET=your-encryption-key-here

# External Services (optional)
SENDGRID_API_KEY=your-sendgrid-key
ANTHROPIC_API_KEY=your-anthropic-key
```

### Database Options

**Option 1: JSON Files (Default)**
- No setup required
- Data stored in `data/` folder
- Perfect for development and testing

**Option 2: MongoDB (Advanced)**
```bash
# Install MongoDB
# Windows: Download from mongodb.com
# macOS: brew install mongodb/brew/mongodb-community
# Linux: sudo apt install mongodb

# Start MongoDB service
# Windows: net start MongoDB
# macOS: brew services start mongodb/brew/mongodb-community
# Linux: sudo systemctl start mongod
```

## 🐛 Troubleshooting

### Common Issues and Solutions

**1. Python not found**
```bash
# Check if Python is installed
python --version
# or
python3 --version

# If not installed, download from python.org
```

**2. Permission denied errors**
```bash
# Use --user flag
pip install --user -r requirements-local.txt
```

**3. Virtual environment activation fails**
```bash
# Windows (try these alternatives):
venv\Scripts\activate.bat
venv\Scripts\activate.ps1

# macOS/Linux:
source venv/bin/activate
```

**4. Module not found errors**
```bash
# Ensure virtual environment is activated
# Then reinstall dependencies
pip install -r requirements-local.txt
```

**5. Port 5000 already in use**
```bash
# Find and kill process using port 5000
# Windows:
netstat -ano | findstr :5000
taskkill /PID <PID_NUMBER> /F

# macOS/Linux:
lsof -ti:5000 | xargs kill -9
```

**6. Database connection errors**
- No action needed - application automatically uses JSON files
- Check console for "Database: JSON Fallback" message

### Getting Help

If you encounter other issues:
1. Check the console output for error messages
2. Ensure all dependencies are installed correctly
3. Verify Python version is 3.11 or higher
4. Make sure you're in the project directory
5. Ensure virtual environment is activated

## ✨ Features

### 🔍 Detection Capabilities
- **URL Analysis**: Scan suspicious links for phishing indicators
- **Email Protection**: Analyze email content for threats
- **Message Scanning**: Check text messages for malicious patterns
- **File Analysis**: Upload and scan images, videos, audio, documents
- **AI Content Detection**: Identify AI-generated content

### 👥 User Roles
- **Admin**: Full system access, user management, system configuration
- **User**: Access to all detection tools and personal dashboard

### 🛡️ Security Features
- **Data Encryption**: AES-256 encryption for sensitive information
- **Secure Authentication**: Protected login system
- **Session Management**: Automatic logout for security
- **Input Validation**: Protection against malicious inputs

### 📊 Dashboard Features
- **Detection History**: View all your previous scans
- **Statistics**: Personal usage analytics
- **Safety Tips**: Learn cybersecurity best practices
- **Admin Panel**: System management (admin only)

## 📱 How to Use

### For Regular Users
1. **Register/Login**: Create an account or use demo credentials
2. **Choose Detection Type**: URL, Email, Message, or File
3. **Submit Content**: Enter or upload content to analyze
4. **View Results**: Get detailed threat analysis with explanations
5. **Learn**: Read safety tips to improve your cybersecurity knowledge

### For Administrators
1. **Access Admin Dashboard**: Login with admin credentials
2. **Manage Users**: Create, edit, or remove user accounts
3. **View Analytics**: Monitor system usage and detection statistics
4. **Configure Settings**: Adjust system security and detection parameters

## 🛠 Technology Stack

- **Backend**: Python Flask
- **Database**: MongoDB with JSON fallback
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5
- **AI/ML**: scikit-learn, OpenCV, TensorFlow
- **Security**: AES-256 encryption, secure sessions

## 📁 Project Structure

```
ai-phishing-detection-platform/
├── app.py                 # Main Flask application
├── main.py               # Application entry point
├── routes.py             # Web routes
├── auth_routes.py        # Authentication
├── admin_routes.py       # Admin functions
├── ml_detector.py        # AI detection algorithms
├── models/               # Database models
├── utils/                # Utility functions
├── templates/            # HTML templates
├── static/               # CSS, JS, images
├── data/                 # JSON database files
└── requirements-local.txt # Dependencies
```

## 🚀 Deployment

### Local Development
The application runs on `http://localhost:5000` by default.

### Production Deployment
```bash
# Install production server
pip install gunicorn

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## 🔧 Advanced Configuration

### Custom Port
```bash
# Run on different port
python main.py --port 8080
```

### Environment Variables
```bash
# Set custom database URL
export MONGODB_URI="mongodb://localhost:27017/custom_db"

# Set security keys
export SESSION_SECRET="your-secret-key"
export USER_ENCRYPTION_SECRET="your-encryption-key"
```

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
