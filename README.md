# AI Phishing Detection Platform

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://python.org)
[![Flask Version](https://img.shields.io/badge/flask-2.3%2B-green.svg)](https://flask.palletsprojects.com/)
[![MongoDB](https://img.shields.io/badge/database-MongoDB-green.svg)](https://mongodb.com)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)](#)
[![Security](https://img.shields.io/badge/security-OWASP%20compliant-orange.svg)](#)

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Security](#security)
- [Testing](#testing)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [Support](#support)
- [License](#license)

## 🎯 Overview

The **AI Phishing Detection Platform** is a comprehensive cybersecurity solution that leverages advanced machine learning algorithms and natural language processing to detect phishing attempts across multiple communication channels. Built with modern web technologies and designed for scalability, this platform provides real-time threat analysis for URLs, emails, text messages, and multimedia content.

### 🚀 Key Highlights

- **Multi-Vector Detection**: Comprehensive analysis across URLs, emails, SMS, and multimedia
- **Advanced ML Algorithms**: Scikit-learn and NLTK-powered detection engines
- **Real-Time Analysis**: Instant threat assessment with detailed scoring
- **Enterprise-Ready**: Role-based access control and audit logging
- **Scalable Architecture**: Modular design with MongoDB and Flask
- **User-Friendly Interface**: Responsive design with intuitive navigation

## 🎯 Features

### 🔍 Core Detection Capabilities

#### URL Analysis Engine
- **Real-time URL Scanning**: Instant analysis of suspicious links and websites
- **Domain Reputation Checking**: Cross-reference with known threat databases
- **Pattern Recognition**: Advanced regex and ML-based URL structure analysis
- **Redirect Chain Analysis**: Deep inspection of URL redirections
- **SSL Certificate Validation**: Security certificate verification

#### Email Security Suite
- **Header Analysis**: Comprehensive email header inspection
- **Content Scanning**: Natural language processing for phishing indicators
- **Attachment Analysis**: Safe scanning of email attachments
- **Sender Reputation**: Domain and IP reputation verification
- **Social Engineering Detection**: Advanced behavioral pattern recognition

#### Text Message Analysis
- **SMS Content Scanning**: Real-time analysis of text messages
- **Social Engineering Detection**: Identification of manipulation tactics
- **Urgency Pattern Recognition**: Detection of pressure tactics
- **Link Extraction**: Automatic URL extraction and analysis
- **Multi-language Support**: Detection across multiple languages

#### Multimedia Content Analysis
- **OCR Technology**: Text extraction from images using Tesseract
- **Document Processing**: Analysis of PDFs, Word documents, and presentations
- **Image Analysis**: Computer vision-based threat detection
- **Audio Processing**: Voice message and audio file analysis
- **Metadata Extraction**: Hidden data analysis for forensic purposes

### 🔐 Security & Access Control

#### Role-Based Access Control (RBAC)
- **Three-Tier System**: User, Admin, and Superadmin roles
- **Granular Permissions**: Fine-grained access control
- **Dynamic Role Assignment**: Flexible role management
- **Session Management**: Secure session handling with timeout
- **Activity Monitoring**: Comprehensive audit trails

#### Authentication & Authorization
- **Secure Password Hashing**: bcrypt with configurable rounds
- **Multi-Factor Authentication**: Optional 2FA support
- **Session Security**: HTTP-only cookies with CSRF protection
- **Password Policies**: Configurable complexity requirements
- **Account Lockout**: Brute force protection

### 📊 Advanced Analytics & Reporting

#### Real-Time Dashboard
- **Live Threat Monitoring**: Real-time threat landscape visualization
- **Performance Metrics**: System health and response time tracking
- **Detection Statistics**: Accuracy and false positive rates
- **User Activity**: Comprehensive usage analytics
- **Trend Analysis**: Historical data visualization

#### Comprehensive Reporting
- **Scan History**: Complete tracking of all detection activities
- **Custom Reports**: Exportable analysis reports in multiple formats
- **Threat Intelligence**: Aggregated threat data and trends
- **Performance Reports**: System efficiency and optimization insights
- **Compliance Reports**: Regulatory compliance documentation

### 🏗️ Technical Excellence

#### Modern Architecture
- **Modular Design**: Clean separation of concerns with Flask Blueprints
- **Microservices Ready**: Easily decomposable into microservices
- **Database Flexibility**: MongoDB with optional Redis caching
- **API-First Design**: RESTful endpoints for seamless integration
- **Containerization**: Docker support for easy deployment

#### Performance & Scalability
- **Asynchronous Processing**: Background task processing
- **Caching Layer**: Redis-based caching for improved performance
- **Load Balancing**: Support for horizontal scaling
- **Database Optimization**: Indexed queries and connection pooling
- **CDN Integration**: Static asset optimization

## 🚀 Installation

### System Requirements

#### Minimum Requirements
- **Operating System**: Windows 10+, macOS 10.15+, Ubuntu 18.04+, CentOS 7+
- **Python**: 3.8 or higher (3.9+ recommended)
- **Memory**: 4GB RAM minimum
- **Storage**: 10GB free space
- **Network**: Stable internet connection

#### Recommended Requirements
- **Memory**: 8GB RAM or higher
- **Storage**: 50GB SSD storage
- **CPU**: Multi-core processor (4+ cores)
- **Network**: High-speed internet connection

### Prerequisites

Before installation, ensure you have the following installed:

```bash
# Check Python version
python --version  # Should be 3.8+

# Check pip
pip --version

# Install Git (if not already installed)
# Windows: Download from https://git-scm.com/
# macOS: brew install git
# Ubuntu/Debian: sudo apt install git
```

### Quick Start (Automated Installation)

#### Option 1: Using the Automated Installer (Recommended)

```bash
# 1. Clone the repository
git clone https://github.com/your-username/phishing-detection-platform.git
cd phishing-detection-platform

# 2. Run the automated installer
python install_minimal.py

# 3. Configure environment variables
cp .env.example .env
# Edit .env file with your configuration

# 4. Start the application
python app.py
```

#### Option 2: Using UV Package Manager (Fastest)

```bash
# 1. Install UV (if not already installed)
pip install uv

# 2. Clone and setup
git clone https://github.com/your-username/phishing-detection-platform.git
cd phishing-detection-platform

# 3. Install dependencies with UV
uv pip install -r requirements.txt

# 4. Setup environment
cp .env.example .env

# 5. Run the application
python app.py
```

### Manual Installation

#### Step 1: Clone the Repository

```bash
git clone https://github.com/your-username/phishing-detection-platform.git
cd phishing-detection-platform
```

#### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

#### Step 3: Install Python Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install core dependencies
pip install flask flask-login flask-pymongo
pip install pymongo dnspython bcrypt
pip install werkzeug requests beautifulsoup4
pip install scikit-learn nltk trafilatura

# Install multimedia processing
pip install pillow opencv-python librosa soundfile
pip install pytesseract python-docx pdfplumber
pip install imagehash email-validator

# Install development dependencies (optional)
pip install pytest black flake8 mypy
```

#### Step 4: Install System Dependencies

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr tesseract-ocr-eng
sudo apt-get install ffmpeg libsndfile1
```

**macOS:**
```bash
brew install tesseract
brew install ffmpeg
```

**Windows:**
- Download Tesseract from: https://github.com/UB-Mannheim/tesseract/wiki
- Download FFmpeg from: https://ffmpeg.org/download.html
- Add both to your system PATH

#### Step 5: Setup Database

**Option A: MongoDB Atlas (Recommended)**
1. Create account at [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Create a new cluster
3. Get connection string
4. Add to `.env` file

**Option B: Local MongoDB**
```bash
# Ubuntu/Debian
sudo apt-get install mongodb
sudo systemctl start mongodb

# macOS
brew install mongodb-community
brew services start mongodb/brew/mongodb-community

# Windows
# Download from https://www.mongodb.com/try/download/community
```

#### Step 6: Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit configuration (use your preferred editor)
nano .env  # or vim .env or code .env
```

**Required Environment Variables:**
```env
# Flask Configuration
SECRET_KEY=your-very-secure-secret-key-here
FLASK_ENV=development
DEBUG=True

# Database Configuration
MONGO_URI=mongodb://localhost:27017/phishing_detection
# OR for MongoDB Atlas:
# MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/phishing_detection

# Security Settings
WTF_CSRF_ENABLED=True
SESSION_COOKIE_SECURE=False  # Set to True in production with HTTPS
SESSION_COOKIE_HTTPONLY=True

# File Upload Settings
MAX_CONTENT_LENGTH=16777216  # 16MB
UPLOAD_FOLDER=uploads
```

#### Step 7: Initialize Application

```bash
# Create required directories
mkdir -p data logs uploads static/uploads models

# Download NLTK data
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('vader_lexicon')"

# Initialize database (optional - will be created automatically)
python -c "from app import app; app.app_context().push(); print('Database initialized')"
```

#### Step 8: Run the Application

```bash
# Start the Flask application
python app.py
```

The application will be available at: `http://localhost:5000`

### Docker Installation

For containerized deployment:

```bash
# Build and run with Docker Compose
docker-compose up -d

# Or build manually
docker build -t phishing-detection .
docker run -p 5000:5000 phishing-detection
```

### Verification

After installation, verify everything is working:

1. **Check Application Health:**
   ```bash
   curl http://localhost:5000/health
   ```

2. **Run Tests:**
   ```bash
   python -m pytest tests/
   ```

3. **Check Database Connection:**
   ```bash
   python test_route.py
   ```

### Default Accounts

The application creates default test accounts:
- **Admin**: `admin@example.com` / `admin123`
- **User**: `user@example.com` / `user123`

**⚠️ Important**: Change these credentials immediately in production!

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root (copy from `.env.example`):

```bash
# Application Configuration
FLASK_ENV=development                    # development/production
FLASK_DEBUG=True                        # Enable debug mode
SECRET_KEY=your-secret-key-here         # Change in production!
PORT=5000                               # Application port

# Database Configuration
MONGO_URI=mongodb://localhost:27017/phishing_detection
# For MongoDB Atlas:
# MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/phishing_detection

# Security Configuration
PASSWORD_SALT_ROUNDS=12                 # bcrypt salt rounds
SESSION_TIMEOUT=3600                    # Session timeout in seconds
MAX_LOGIN_ATTEMPTS=5                    # Maximum login attempts
LOCKOUT_DURATION=900                    # Account lockout duration (seconds)

# File Upload Configuration
MAX_FILE_SIZE=10485760                  # 10MB in bytes
UPLOAD_FOLDER=static/uploads            # Upload directory
ALLOWED_EXTENSIONS=pdf,docx,txt,png,jpg,gif

# External API Configuration (Optional)
VIRUSTOTAL_API_KEY=your-virustotal-key  # VirusTotal integration
GOOGLE_SAFE_BROWSING_KEY=your-gsb-key   # Google Safe Browsing

# Email Configuration (Optional)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password

# Logging Configuration
LOG_LEVEL=INFO                          # DEBUG/INFO/WARNING/ERROR
LOG_FILE=data/logs/app.log              # Log file path
LOG_MAX_SIZE=10485760                   # 10MB log rotation
LOG_BACKUP_COUNT=5                      # Number of backup logs

# Performance Configuration
CACHE_TYPE=simple                       # simple/redis/memcached
CACHE_DEFAULT_TIMEOUT=300               # Cache timeout in seconds
REDIS_URL=redis://localhost:6379/0     # Redis connection (if using)

# Rate Limiting
RATELIMIT_STORAGE_URL=memory://         # Rate limit storage
RATELIMIT_DEFAULT=100 per hour          # Default rate limit
```

### Database Setup

#### MongoDB Atlas (Recommended for Production)

1. **Create MongoDB Atlas Account**:
   - Visit [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
   - Create a free cluster
   - Note your connection string

2. **Configure Database Access**:
   ```bash
   # Add to .env file
   MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/phishing_detection?retryWrites=true&w=majority
   ```

3. **Set Network Access**:
   - Add your IP address to the whitelist
   - For development: Add `0.0.0.0/0` (not recommended for production)

#### Local MongoDB Installation

**Windows:**
```powershell
# Download and install MongoDB Community Server
# https://www.mongodb.com/try/download/community

# Start MongoDB service
net start MongoDB

# Verify installation
mongo --version
```

**Linux (Ubuntu/Debian):**
```bash
# Import MongoDB public key
wget -qO - https://www.mongodb.org/static/pgp/server-4.4.asc | sudo apt-key add -

# Add MongoDB repository
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/4.4 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.4.list

# Install MongoDB
sudo apt-get update
sudo apt-get install -y mongodb-org

# Start MongoDB service
sudo systemctl start mongod
sudo systemctl enable mongod
```

**macOS:**
```bash
# Using Homebrew
brew tap mongodb/brew
brew install mongodb-community@4.4

# Start MongoDB service
brew services start mongodb/brew/mongodb-community
```

### Application Configuration

#### Production Settings

```python
# config.py modifications for production
class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    
    # Security headers
    SECURITY_HEADERS = {
        'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
        'X-Content-Type-Options': 'nosniff',
        'X-Frame-Options': 'DENY',
        'X-XSS-Protection': '1; mode=block',
        'Content-Security-Policy': "default-src 'self'"
    }
    
    # Session configuration
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Database connection pooling
    MONGO_CONNECT_TIMEOUT = 5000
    MONGO_SERVER_SELECTION_TIMEOUT = 5000
    MONGO_MAX_POOL_SIZE = 50
```

#### Development Settings

```python
# config.py for development
class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False
    
    # Relaxed security for development
    SESSION_COOKIE_SECURE = False
    
    # Enhanced logging
    LOG_LEVEL = 'DEBUG'
    
    # Development database
    MONGO_URI = 'mongodb://localhost:27017/phishing_detection_dev'
```

## 🔒 Security Features

### Authentication & Authorization

#### Multi-Factor Authentication (MFA)
- **TOTP Support**: Time-based One-Time Password integration
- **Backup Codes**: Emergency access codes
- **Device Trust**: Remember trusted devices
- **Session Management**: Secure session handling

#### Role-Based Access Control (RBAC)

```python
# User Roles and Permissions
ROLES = {
    'superadmin': {
        'permissions': ['*'],  # All permissions
        'description': 'Full system access'
    },
    'admin': {
        'permissions': [
            'user.create', 'user.read', 'user.update', 'user.delete',
            'scan.read', 'scan.delete', 'system.monitor',
            'content.manage', 'reports.generate'
        ],
        'description': 'Administrative access'
    },
    'analyst': {
        'permissions': [
            'scan.create', 'scan.read', 'scan.update',
            'reports.read', 'dashboard.access'
        ],
        'description': 'Security analyst access'
    },
    'user': {
        'permissions': [
            'scan.create', 'scan.read.own', 'dashboard.basic'
        ],
        'description': 'Standard user access'
    }
}
```

#### Password Security
- **bcrypt Hashing**: Industry-standard password hashing
- **Salt Rounds**: Configurable computational cost
- **Password Policies**: Minimum length, complexity requirements
- **Password History**: Prevent password reuse
- **Account Lockout**: Protection against brute force attacks

### Data Protection

#### Encryption
- **Data at Rest**: MongoDB encryption
- **Data in Transit**: TLS/SSL encryption
- **Sensitive Data**: Field-level encryption for PII
- **API Keys**: Secure storage and rotation

#### Input Validation & Sanitization
- **XSS Prevention**: Content Security Policy, input sanitization
- **SQL Injection**: Parameterized queries (NoSQL injection prevention)
- **File Upload Security**: Type validation, virus scanning
- **Rate Limiting**: API and form submission protection

#### Privacy Compliance
- **Data Minimization**: Collect only necessary data
- **Data Retention**: Configurable retention policies
- **User Consent**: Clear privacy policies
- **Data Export**: User data download capability
- **Right to Deletion**: Account and data removal

## 📊 Performance & Monitoring

### System Requirements

#### Minimum Requirements
- **CPU**: 2 cores, 2.0 GHz
- **RAM**: 4 GB
- **Storage**: 10 GB available space
- **Network**: Broadband internet connection
- **OS**: Windows 10+, macOS 10.14+, Ubuntu 18.04+

#### Recommended Requirements
- **CPU**: 4+ cores, 3.0+ GHz
- **RAM**: 8+ GB
- **Storage**: 50+ GB SSD
- **Network**: High-speed internet
- **OS**: Latest stable versions

#### Production Requirements
- **CPU**: 8+ cores, 3.5+ GHz
- **RAM**: 16+ GB
- **Storage**: 100+ GB SSD with backup
- **Network**: Redundant internet connections
- **Load Balancer**: Nginx or similar
- **Database**: MongoDB replica set

### Performance Optimization

#### Database Optimization
```javascript
// MongoDB Indexes for optimal performance
db.users.createIndex({ "email": 1 }, { unique: true })
db.users.createIndex({ "created_at": 1 })
db.scan_history.createIndex({ "user_id": 1, "timestamp": -1 })
db.scan_history.createIndex({ "url_hash": 1 })
db.phishing_data.createIndex({ "domain": 1 })
db.phishing_data.createIndex({ "threat_score": -1 })

// Compound indexes for complex queries
db.scan_history.createIndex({ 
    "user_id": 1, 
    "scan_type": 1, 
    "timestamp": -1 
})
```

#### Caching Strategy
- **Application Cache**: Flask-Caching with Redis backend
- **Database Query Cache**: MongoDB query result caching
- **Static Asset Cache**: CDN integration for static files
- **API Response Cache**: Cached responses for repeated requests

#### Monitoring & Alerting

**Health Checks:**
```python
# Health check endpoint
@app.route('/health')
def health_check():
    checks = {
        'database': check_database_connection(),
        'cache': check_cache_connection(),
        'disk_space': check_disk_space(),
        'memory': check_memory_usage()
    }
    
    status = 'healthy' if all(checks.values()) else 'unhealthy'
    return jsonify({'status': status, 'checks': checks})
```

**Metrics Collection:**
- **Response Times**: API and page load times
- **Error Rates**: 4xx and 5xx error tracking
- **Resource Usage**: CPU, memory, disk utilization
- **User Activity**: Login patterns, feature usage
- **Security Events**: Failed logins, suspicious activity

**Logging Configuration:**
```python
# Structured logging setup
import logging
from logging.handlers import RotatingFileHandler

# Configure application logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(name)s %(message)s',
    handlers=[
        RotatingFileHandler(
            'data/logs/app.log',
            maxBytes=10485760,  # 10MB
            backupCount=5
        ),
        logging.StreamHandler()
    ]
)

# Security event logging
security_logger = logging.getLogger('security')
security_handler = RotatingFileHandler(
    'data/logs/security.log',
    maxBytes=10485760,
    backupCount=10
)
security_logger.addHandler(security_handler)
 ```

## 🤝 Contributing

### Development Setup

#### Prerequisites for Contributors
- **Python 3.8+** with pip or UV package manager
- **Git** for version control
- **MongoDB** (local or Atlas) for database
- **Code Editor** (VS Code recommended)
- **Node.js** (optional, for frontend tooling)

#### Setting Up Development Environment

1. **Fork and Clone Repository**:
   ```bash
   git clone https://github.com/yourusername/phishing-detection-platform.git
   cd phishing-detection-platform
   ```

2. **Create Development Branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Install Development Dependencies**:
   ```bash
   # Using UV (recommended)
   uv sync --dev
   
   # Or using pip
   pip install -e ".[dev]"
   ```

4. **Set Up Pre-commit Hooks**:
   ```bash
   pre-commit install
   ```

5. **Configure Development Environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your development settings
   ```

### Code Style & Standards

#### Python Code Style
- **Formatter**: Black with line length 88
- **Linter**: Flake8 with custom configuration
- **Type Checker**: MyPy for static type analysis
- **Import Sorting**: isort for consistent imports

```bash
# Format code
black .

# Check linting
flake8 .

# Type checking
mypy .

# Sort imports
isort .
```

#### Frontend Code Style
- **JavaScript**: ES6+ with Prettier formatting
- **CSS**: BEM methodology for class naming
- **HTML**: Semantic markup with accessibility considerations

#### Documentation Standards
- **Docstrings**: Google-style docstrings for all functions
- **Comments**: Clear, concise explanations for complex logic
- **README**: Keep documentation up-to-date
- **API Docs**: Document all API endpoints

### Testing Guidelines

#### Running Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_models.py

# Run tests with verbose output
pytest -v
```

#### Test Categories
- **Unit Tests**: Test individual functions and methods
- **Integration Tests**: Test component interactions
- **API Tests**: Test REST API endpoints
- **Security Tests**: Test authentication and authorization
- **Performance Tests**: Test system performance under load

#### Writing Tests
```python
# Example test structure
import pytest
from app import create_app
from models.user_model import User

class TestUserModel:
    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
    
    def teardown_method(self):
        """Clean up after each test method."""
        self.app_context.pop()
    
    def test_user_creation(self):
        """Test user creation with valid data."""
        user_data = {
            'email': 'test@example.com',
            'password': 'securepassword123',
            'role': 'user'
        }
        user = User.create_user(user_data)
        assert user is not None
        assert user['email'] == 'test@example.com'
```

### Contribution Workflow

#### Pull Request Process
1. **Create Feature Branch**: Branch from `main` for new features
2. **Implement Changes**: Follow coding standards and write tests
3. **Run Tests**: Ensure all tests pass locally
4. **Update Documentation**: Update relevant documentation
5. **Submit PR**: Create pull request with detailed description
6. **Code Review**: Address feedback from maintainers
7. **Merge**: PR will be merged after approval

#### Commit Message Format
```
type(scope): brief description

Detailed explanation of changes (if needed)

Closes #issue-number
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

#### Issue Reporting
When reporting issues, please include:
- **Environment**: OS, Python version, browser
- **Steps to Reproduce**: Clear reproduction steps
- **Expected Behavior**: What should happen
- **Actual Behavior**: What actually happens
- **Screenshots**: If applicable
- **Logs**: Relevant error messages

## 🐛 Troubleshooting

### Common Issues

#### Installation Problems

**Issue**: `ModuleNotFoundError` during installation
```bash
# Solution: Ensure virtual environment is activated
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

**Issue**: MongoDB connection errors
```bash
# Check MongoDB service status
# Windows:
net start MongoDB

# Linux:
sudo systemctl status mongod

# macOS:
brew services list | grep mongodb
```

**Issue**: Port already in use
```bash
# Find process using port 5000
netstat -ano | findstr :5000  # Windows
lsof -i :5000                 # Linux/macOS

# Kill process or change port in .env
PORT=5001
```

#### Runtime Errors

**Issue**: Template not found errors
- Verify template files exist in `templates/` directory
- Check template path in route handlers
- Ensure Flask app can find template directory

**Issue**: Static files not loading
- Check `static/` directory structure
- Verify file paths in templates
- Clear browser cache

**Issue**: Database connection timeouts
- Check MongoDB service status
- Verify connection string in `.env`
- Check network connectivity
- Increase timeout values in configuration

#### Performance Issues

**Issue**: Slow page load times
- Enable caching (Redis recommended)
- Optimize database queries
- Add database indexes
- Compress static assets

**Issue**: High memory usage
- Monitor for memory leaks
- Optimize image processing
- Implement pagination for large datasets
- Use database connection pooling

### Debug Mode

Enable debug mode for development:
```bash
# In .env file
FLASK_ENV=development
FLASK_DEBUG=True

# Or set environment variables
export FLASK_ENV=development
export FLASK_DEBUG=True
```

### Logging and Monitoring

#### Application Logs
```bash
# View application logs
tail -f data/logs/app.log

# View security logs
tail -f data/logs/security.log

# Search for specific errors
grep "ERROR" data/logs/app.log
```

#### Database Monitoring
```javascript
// MongoDB performance monitoring
db.runCommand({serverStatus: 1})
db.stats()
db.collection.stats()
```

## 📞 Support

### Getting Help

#### Documentation Resources
- **[Technical Documentation](Documentation.md)**: Comprehensive technical guide
- **[Deployment Guide](Deployment.md)**: Step-by-step deployment instructions
- **[API Documentation](docs/API.md)**: REST API reference
- **[Contributing Guide](docs/CONTRIBUTING.md)**: Contribution guidelines

#### Community Support
- **GitHub Issues**: Report bugs and request features
- **Discussions**: Ask questions and share ideas
- **Wiki**: Community-maintained documentation
- **Stack Overflow**: Tag questions with `phishing-detection-platform`

#### Professional Support
For enterprise deployments and professional support:
- **Email**: support@phishing-detection-platform.com
- **Documentation**: Enterprise deployment guides
- **Training**: Custom training sessions available
- **Consulting**: Architecture and security consulting

### Frequently Asked Questions

**Q: Can I use this platform commercially?**
A: Yes, the platform is released under MIT license, allowing commercial use.

**Q: How accurate is the phishing detection?**
A: Accuracy depends on training data and configuration. Typical accuracy ranges from 85-95%.

**Q: Can I integrate with existing security tools?**
A: Yes, the platform provides REST APIs for integration with SIEM and other security tools.

**Q: What's the maximum file size for analysis?**
A: Default limit is 10MB, configurable via `MAX_FILE_SIZE` environment variable.

**Q: Is the platform GDPR compliant?**
A: The platform includes privacy features, but GDPR compliance depends on your implementation and usage.

## 📄 License

### MIT License

```
MIT License

Copyright (c) 2024 AI Phishing Detection Platform

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

### Third-Party Licenses

This project uses several open-source libraries. See individual package licenses for details:
- **Flask**: BSD-3-Clause License
- **MongoDB**: Server Side Public License (SSPL)
- **Scikit-learn**: BSD-3-Clause License
- **NLTK**: Apache License 2.0
- **OpenCV**: Apache License 2.0
- **Bootstrap**: MIT License

## 🚀 Roadmap

### Version 2.0 (Planned)
- **Enhanced AI Models**: Improved detection accuracy with deep learning
- **Real-time Monitoring**: Live threat detection and alerting
- **Mobile App**: Native mobile applications for iOS and Android
- **Advanced Analytics**: Machine learning-powered insights and trends
- **API Gateway**: Enhanced API management and rate limiting

### Version 2.1 (Future)
- **Multi-language Support**: Internationalization and localization
- **Threat Intelligence**: Integration with external threat feeds
- **Automated Response**: Automated threat mitigation capabilities
- **Compliance Reporting**: GDPR, SOX, and other compliance reports
- **Cloud-native**: Kubernetes deployment and microservices architecture

### Long-term Vision
- **AI-powered Security**: Advanced machine learning for zero-day threat detection
- **Global Threat Network**: Collaborative threat intelligence sharing
- **Behavioral Analysis**: User behavior analytics for insider threat detection
- **Quantum-safe Security**: Post-quantum cryptography implementation

---

## 📊 Project Statistics

![GitHub stars](https://img.shields.io/github/stars/username/phishing-detection-platform?style=social)
![GitHub forks](https://img.shields.io/github/forks/username/phishing-detection-platform?style=social)
![GitHub issues](https://img.shields.io/github/issues/username/phishing-detection-platform)
![GitHub pull requests](https://img.shields.io/github/issues-pr/username/phishing-detection-platform)
![GitHub license](https://img.shields.io/github/license/username/phishing-detection-platform)

**Built with ❤️ by the AI Phishing Detection Platform Team**

*Making the internet safer, one detection at a time.*

### Technology Stack

#### Backend Technologies
- **Framework**: Flask 2.3+ with Python 3.8+
- **Database**: MongoDB 4.4+ with PyMongo driver
- **Authentication**: Flask-Login with bcrypt password hashing
- **Session Management**: Flask sessions with secure cookie handling
- **Caching**: Redis (optional) for improved performance
- **Task Queue**: Celery (optional) for background processing

#### Machine Learning & AI
- **ML Framework**: Scikit-learn for classification algorithms
- **NLP Processing**: NLTK for natural language processing
- **Text Extraction**: Trafilatura for web content extraction
- **Computer Vision**: OpenCV and Pillow for image processing
- **OCR**: Tesseract for text extraction from images
- **Audio Processing**: Librosa for audio file analysis

#### Frontend Technologies
- **Template Engine**: Jinja2 with Flask
- **CSS Framework**: Bootstrap 5 with custom styling
- **JavaScript**: Vanilla JS with modern ES6+ features
- **Icons**: Font Awesome and custom SVG icons
- **Charts**: Chart.js for data visualization

#### Development & Deployment
- **Package Management**: UV (recommended) or pip with virtual environments
- **Code Quality**: Black (formatting), Flake8 (linting), MyPy (type checking)
- **Testing**: Pytest with coverage reporting
- **Containerization**: Docker and Docker Compose
- **Web Server**: Gunicorn (production) with Nginx reverse proxy
- **Process Management**: Supervisor for service management

### Data Flow Architecture

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   User      │───▶│   Flask     │───▶│  Detection  │───▶│  Database   │
│  Interface  │    │  Routes     │    │  Services   │    │  Storage    │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
       ▲                   │                   │                   │
       │                   ▼                   ▼                   ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  Response   │◀───│  Template   │◀───│   ML/AI     │◀───│   Models    │
│  Rendering  │    │  Engine     │    │ Processing  │    │ & Utilities │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
```

## 📖 Usage Guide

### Getting Started

#### First-Time Setup
1. **Access the Application**: Navigate to `http://localhost:5000` in your web browser
2. **Create Account**: Click "Register" to create a new user account
3. **Verify Installation**: Check that all features are working correctly
4. **Explore Interface**: Familiarize yourself with the dashboard and navigation

#### User Registration and Authentication
```bash
# Default test accounts (change in production!)
Admin Account:
  Email: admin@example.com
  Password: admin123
  
User Account:
  Email: user@example.com
  Password: user123
```

### Core Detection Features

#### 🔗 URL Analysis

**Quick URL Check:**
1. Navigate to the homepage
2. Enter suspicious URL in the "Quick Check" field
3. Click "Analyze Now" for instant results
4. Review threat score and detailed analysis

**Comprehensive URL Analysis:**
1. Go to "URL Scanner" from the main menu
2. Enter the target URL
3. Select analysis depth (Quick/Standard/Deep)
4. Click "Analyze URL"
5. Review detailed report including:
   - Domain reputation score
   - SSL certificate analysis
   - Redirect chain inspection
   - Content analysis results
   - Historical threat data

#### 📧 Email Security Analysis

**Email Content Scanning:**
1. Access "Email Scanner" from the dashboard
2. Choose input method:
   - Paste email content directly
   - Upload .eml or .msg files
   - Forward emails to analysis address
3. Click "Analyze Email"
4. Review comprehensive results:
   - Header analysis
   - Sender reputation
   - Content threat assessment
   - Attachment safety check
   - Social engineering indicators

**Bulk Email Analysis:**
1. Navigate to "Bulk Analysis" (Admin only)
2. Upload multiple email files
3. Configure analysis parameters
4. Start batch processing
5. Download results report

#### 💬 Text Message Analysis

**SMS/Message Scanning:**
1. Go to "Text Analysis" section
2. Input message content
3. Select message type (SMS, WhatsApp, etc.)
4. Click "Analyze Text"
5. Review social engineering assessment:
   - Urgency indicators
   - Manipulation tactics
   - Suspicious patterns
   - Link extraction and analysis

#### 📁 File and Multimedia Analysis

**Document Analysis:**
1. Access "File Scanner"
2. Upload supported files:
   - PDF documents
   - Word documents (.docx, .doc)
   - PowerPoint presentations
   - Text files
   - Image files (PNG, JPG, GIF)
3. Select analysis options
4. Review extracted content and threat assessment

**Image OCR Analysis:**
1. Upload image files containing text
2. System automatically extracts text using OCR
3. Analyzes extracted content for phishing indicators
4. Provides confidence scores and recommendations

### Dashboard and Analytics

#### User Dashboard
- **Recent Scans**: View your latest analysis results
- **Threat Summary**: Overview of detected threats
- **Scan Statistics**: Personal usage analytics
- **Quick Actions**: Fast access to common tasks

#### Admin Dashboard (Admin/Superadmin only)
- **System Overview**: Platform health and performance
- **User Management**: Account administration
- **Threat Intelligence**: Aggregated threat data
- **System Configuration**: Platform settings

### Advanced Features

#### API Integration

**REST API Endpoints:**
```bash
# Quick URL check
POST /api/quick-check
Content-Type: application/json
{
  "url": "https://suspicious-site.com"
}

# Comprehensive scan
POST /api/scan
Content-Type: application/json
{
  "type": "url",
  "content": "https://example.com",
  "options": {
    "deep_analysis": true,
    "check_redirects": true
  }
}

# Get scan history
GET /api/history?limit=10&offset=0
```

#### Batch Processing
1. Access "Batch Analysis" (Premium feature)
2. Upload CSV file with URLs/content
3. Configure analysis parameters
4. Monitor processing progress
5. Download comprehensive results

### Administrative Functions

#### User Management
- **Create Users**: Add new user accounts
- **Modify Permissions**: Assign roles and permissions
- **Monitor Activity**: Track user actions and usage
- **Account Management**: Enable/disable accounts

#### System Configuration
- **Detection Settings**: Configure ML model parameters
- **Security Policies**: Set password and session policies
- **Integration Settings**: Configure external API connections
- **Monitoring Setup**: Configure alerts and notifications

#### Content Management
- **Safety Tips**: Manage educational content
- **Threat Database**: Update known threat indicators
- **Whitelist Management**: Manage trusted domains/IPs
- **Report Generation**: Create custom analysis reports

## 🏗️ Architecture

### Project Structure
```
ai-phishing-detection-platform/
├── app.py                 # Flask application entry point
├── main.py               # Application launcher
├── config.py             # Configuration management
├── install_dependencies.py # Automated installer
├── models/               # Database models and data access
│   ├── user_model.py     # User authentication and management
│   ├── phishing_model.py # Threat detection data
│   ├── safety_tips_model.py # Educational content
│   └── scan_history_model.py # Analysis tracking
├── routes/               # Blueprint route handlers
│   ├── main_routes.py    # Public pages and detection
│   ├── auth_routes.py    # Authentication flows
│   ├── admin_routes.py   # Administrative functions
│   └── rbac_routes.py    # Role-based access control
├── services/             # Business logic and external APIs
│   ├── mongo_service.py  # Database connection management
│   └── text_analysis.py # Content analysis algorithms
├── utils/                # Utility functions and helpers
│   ├── phishing_detector.py # Core detection engine
│   ├── ml_detector.py    # Machine learning models
│   ├── multimedia_analyzer.py # File processing
│   └── validation.py     # Input validation
├── templates/            # Jinja2 HTML templates
├── static/               # CSS, JavaScript, and assets
└── data/                 # Application data and logs
```

### Technology Stack
- **Backend**: Flask 2.3+ with Python 3.8+
- **Database**: MongoDB Atlas with PyMongo
- **Authentication**: Flask-Login with bcrypt hashing
- **Frontend**: Bootstrap 5 with responsive design
- **ML Libraries**: Scikit-learn, NLTK for detection algorithms
- **File Processing**: OpenCV, Pillow, PyTesseract for multimedia
- **Audio Analysis**: Librosa for sound file processing

## 🔧 Configuration

### Environment Variables
Create a `.env` file with the following variables:

```env
# Database Configuration
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/phishing_db

# Security Settings
SESSION_SECRET=your-unique-secret-key-here
FLASK_ENV=production

# Application Settings
APP_NAME=AI Phishing Detection Platform
VERSION=2.0.0
AUTHOR=Bigendra Shrestha

# Upload Limits
MAX_CONTENT_LENGTH=16777216  # 16MB
UPLOAD_FOLDER=uploads

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/application.log
```

### Database Setup
1. Create a MongoDB Atlas cluster
2. Add your IP address to the network access list
3. Create a database user with read/write permissions
4. Copy the connection string to your `.env` file

### Default User Accounts
The platform creates default accounts for testing:
- **Admin**: testadmin@example.com / password123
- **User**: testuser@example.com / password123

**Important**: Change these credentials in production!

## 🔒 Security Features

### Authentication & Authorization
- **Secure Password Storage**: bcrypt hashing with salt
- **Session Management**: HTTP-only cookies with CSRF protection
- **Role-Based Access**: Granular permissions for different user levels
- **Input Validation**: Server-side validation for all user inputs

### Data Protection
- **Encrypted Communications**: HTTPS enforcement in production
- **Database Security**: Connection string encryption
- **File Upload Security**: Type validation and size limits
- **XSS Prevention**: Template auto-escaping and content sanitization

## 📊 Performance & Monitoring

### System Requirements
- **Minimum**: 2GB RAM, 1 CPU core, 5GB storage
- **Recommended**: 4GB RAM, 2 CPU cores, 20GB storage
- **Production**: 8GB RAM, 4 CPU cores, 50GB storage

### Monitoring Features
- Real-time system health dashboard
- Performance metrics and response time tracking
- User activity monitoring and audit logs
- Database connection status and query performance

## 🤝 Contributing

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Install development dependencies
4. Make your changes with tests
5. Submit a pull request

### Code Style
- Follow PEP 8 Python style guidelines
- Use meaningful variable and function names
- Add docstrings for all public functions
- Include type hints where appropriate

### Testing
```bash
# Run unit tests
python -m pytest tests/

# Run integration tests
python test_all_features.py

# Check code coverage
coverage run -m pytest && coverage report
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

### Documentation
- **User Guide**: Detailed usage instructions in `/docs/user-guide.md`
- **API Documentation**: REST API reference in `/docs/api.md`
- **Developer Guide**: Technical documentation in `/docs/developer.md`

### Getting Help
- **Issues**: Report bugs and feature requests through GitHub Issues
- **Discussions**: Join community discussions for questions and ideas
- **Security**: Report security vulnerabilities through responsible disclosure

### System Requirements Troubleshooting
If you encounter installation issues:
1. Verify Python 3.8+ is installed: `python --version`
2. Update pip: `pip install --upgrade pip`
3. Install build tools for your OS
4. Check MongoDB connection with provided test script

## 🎯 Roadmap

### Version 2.1 (Planned)
- [ ] Advanced ML model training interface
- [ ] Real-time threat intelligence feeds
- [ ] API rate limiting and authentication
- [ ] Advanced analytics and reporting dashboard

### Version 2.2 (Future)
- [ ] Mobile application companion
- [ ] Browser extension for real-time protection
- [ ] Machine learning model marketplace
- [ ] Enterprise SSO integration

---

**Built with passion for cybersecurity education and protection.**

*Author: Bigendra Shrestha*  
*Version: 2.0.0*  
*Last Updated: 2025*
