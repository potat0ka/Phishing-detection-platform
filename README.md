# AI Phishing Detection Platform

A comprehensive cybersecurity platform that uses advanced machine learning algorithms to detect phishing attempts in URLs, emails, and text messages. Built with Flask and MongoDB, featuring role-based access control and real-time threat analysis.

## 🎯 Features

### Core Detection Capabilities
- **URL Analysis**: Real-time scanning of suspicious links and websites
- **Email Security**: Advanced phishing email detection with header analysis
- **Text Message Scanning**: SMS and message content analysis for social engineering
- **Multimedia Analysis**: OCR and content extraction from images and documents
- **File Upload Support**: Analysis of PDFs, Word documents, and image files

### Security & Access Control
- **Role-Based Access Control (RBAC)**: Three-tier user system (User/Admin/Superadmin)
- **Secure Authentication**: bcrypt password hashing with session management
- **User Management**: Comprehensive admin panel for user oversight
- **Activity Logging**: Detailed audit trails for all system actions

### Advanced Analytics
- **Real-time Dashboard**: Live statistics and threat monitoring
- **Scan History**: Complete tracking of all detection activities
- **Performance Metrics**: System health and detection accuracy stats
- **Custom Reports**: Exportable analysis reports and trends

### Technical Excellence
- **Modular Architecture**: Clean separation of concerns with Blueprint routing
- **Database Flexibility**: MongoDB Atlas integration with local file fallback
- **Responsive Design**: Mobile-friendly interface with dark theme support
- **API Ready**: RESTful endpoints for integration capabilities

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- MongoDB Atlas account (or local MongoDB)
- 2GB RAM minimum
- Internet connection for initial setup

### Automated Installation

1. **Clone the repository**
   ```bash
   git clone <your-repository-url>
   cd ai-phishing-detection-platform
   ```

2. **Run the automated installer**
   ```bash
   python install_dependencies.py
   ```

3. **Configure environment**
   Edit the `.env` file with your MongoDB connection:
   ```
   MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/phishing_db
   SESSION_SECRET=your-secret-key-here
   ```

4. **Launch the platform**
   ```bash
   python main.py
   ```

5. **Access the application**
   Open your browser to: `http://localhost:8080`

### Manual Installation

If you prefer manual setup:

```bash
# Install Python dependencies
pip install flask pymongo flask-login bcrypt werkzeug
pip install requests beautifulsoup4 scikit-learn nltk
pip install pillow opencv-python librosa soundfile
pip install pytesseract python-docx pdfplumber trafilatura

# Install system dependencies (Ubuntu/Debian)
sudo apt-get update
sudo apt-get install tesseract-ocr tesseract-ocr-eng ffmpeg libsndfile1

# Create required directories
mkdir -p data logs uploads static/uploads models

# Run the application
python main.py
```

## 📖 Usage Guide

### Getting Started
1. **Register an Account**: Create your user account through the registration page
2. **Login**: Access the platform with your credentials
3. **Start Scanning**: Use the detection tools to analyze suspicious content
4. **View Results**: Check your scan history and detailed analysis reports

### Detection Methods

#### URL Scanning
```
1. Navigate to the "Check URL" section
2. Enter the suspicious URL
3. Click "Analyze"
4. Review the detailed threat assessment
```

#### Email Analysis
```
1. Go to "Email Scanner"
2. Paste email content or upload .eml files
3. Submit for analysis
4. Get comprehensive phishing probability score
```

#### Text Message Scanning
```
1. Access "Text Analysis"
2. Input message content
3. Run detection algorithms
4. Receive detailed social engineering assessment
```

### Admin Features
- **User Management**: Create, modify, and deactivate user accounts
- **Safety Tips**: Manage cybersecurity educational content
- **System Monitoring**: Monitor platform performance and usage
- **Content Moderation**: Oversee user-generated content and reports

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
*Last Updated: 2024*