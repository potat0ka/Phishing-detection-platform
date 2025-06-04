# AI Phishing Detection Platform

An advanced AI-powered phishing detection web platform with enterprise-level security and comprehensive user data encryption. Built using Flask, MongoDB, and machine learning technologies to protect users from digital threats.

## 🔒 Security Features

### Enterprise-Level Data Protection
- **AES-256 Encryption**: All user data, activity logs, and sensitive information encrypted at rest
- **MongoDB with JSON Fallback**: Hybrid database architecture ensuring reliability and data integrity
- **Field-Level Encryption**: Usernames, emails, IP addresses, and user activity individually encrypted
- **Zero-Knowledge Architecture**: Platform administrators cannot access user personal information
- **Professional Logging**: Comprehensive audit trails with encrypted activity monitoring

### AI-Powered Detection Systems
- **Phishing Detection**: Advanced machine learning algorithms for URLs, emails, and messages
- **AI Content Detection**: Analyze images, videos, audio, and documents for AI-generated content
- **Device Photo Recognition**: EXIF metadata analysis to identify authentic device photos
- **Conservative Thresholds**: 85% confidence for AI-generated, 65% for possibly AI content
- **Source Identification**: Detect likely AI generation tools and editing software

### Comprehensive Security Infrastructure
- **Offline Threat Intelligence**: Local threat detection without external dependencies
- **Real-time Domain Analysis**: URL security evaluation with threat level classification
- **Multi-Modal Analysis**: Support for images, videos, audio, and document content
- **Bulk Operations**: Multiple selection and encrypted deletion of detection history

## 🚀 Platform Features

### User Experience
- **Responsive Design**: Mobile-optimized with Bootstrap and touch-friendly interactions
- **File Upload Support**: 500MB maximum with comprehensive validation and security scanning
- **OCR Integration**: Extract and analyze text from images with real-time processing
- **Educational Content**: 39+ cybersecurity tips with latest threat intelligence updates
- **Session Management**: Secure authentication with encrypted user sessions

### Technical Architecture
- **Flask Backend**: Professional web framework with production-ready configuration
- **MongoDB Primary**: NoSQL database with automatic JSON fallback for reliability
- **Encryption Layer**: Transparent data encryption/decryption with key management
- **Modular Design**: Clean separation of concerns with comprehensive error handling
- **Production Ready**: Professional logging, error handling, and security best practices

## 🛠️ Quick Setup Guide

### Prerequisites
- Python 3.11 or higher
- MongoDB (optional - JSON fallback available)
- PostgreSQL (optional - for additional data storage)

#### Check Python installation:
```bash
python --version
# Should show Python 3.11 or higher
```

### Installation

#### Method 1: Quick Setup (Recommended)

1. **Download the project**
   ```bash
   git clone <repository-url>
   cd ai-phishing-detection-platform
   ```

2. **Install all dependencies**
   ```bash
   pip install flask gunicorn werkzeug pillow numpy scikit-learn nltk beautifulsoup4 requests trafilatura dnspython email-validator anthropic opencv-python tensorflow psycopg2-binary cryptography pymongo flask-pymongo motor bson
   ```

3. **Set up environment variables (optional)**
   ```bash
   export USER_ENCRYPTION_SECRET="your-secure-encryption-key"
   export SESSION_SECRET="your-session-secret"
   export DATABASE_URL="your-mongodb-connection-string"
   ```

4. **Run the application**
   ```bash
   gunicorn --bind 0.0.0.0:5000 --reuse-port --reload main:app
   ```

5. **Access the platform**
   - Open your browser to `http://localhost:5000`
   - The platform will automatically use JSON fallback if MongoDB is not available
   - All user data will be encrypted with AES-256 encryption
   - Register an account to start using the phishing detection and AI content analysis features

#### Alternative: Virtual Environment Setup

1. **Create virtual environment**
   ```bash
   # On Windows
   python -m venv venv
   venv\Scripts\activate
   
   # On Mac/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

2. **Install dependencies**
   ```bash
   pip install flask gunicorn werkzeug pillow numpy scikit-learn nltk beautifulsoup4 requests trafilatura dnspython email-validator anthropic opencv-python tensorflow psycopg2-binary cryptography pymongo flask-pymongo motor bson
   ```

3. **Run the application**
   ```bash
   gunicorn --bind 0.0.0.0:5000 --reuse-port --reload main:app
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

## 🎯 Usage Guide

### Core Features

1. **Phishing Detection**
   - Analyze URLs, emails, and messages for phishing indicators
   - Get confidence scores and detailed explanations
   - View threat intelligence and security recommendations

2. **AI Content Analysis**
   - Upload images, videos, audio, or documents (up to 500MB)
   - Detect AI-generated content with source identification
   - Analyze device photos vs AI-generated images
   - OCR text extraction from images

3. **User Dashboard**
   - View encrypted detection history
   - Bulk delete selected detections
   - Monitor account statistics and activity

4. **Security Education**
   - Access 39+ cybersecurity tips with latest threat intelligence
   - Learn about phishing prevention techniques
   - Stay updated on emerging threats

### API Endpoints

- `POST /api/quick-check` - Quick phishing analysis
- `GET /tips` - Security education content
- `POST /ai-content-check` - AI content analysis
- `DELETE /delete-detection/<id>` - Remove detection history

## 🚀 Deployment

### Production Considerations

1. **Set encryption keys** in environment variables
2. **Configure MongoDB** for production database
3. **Set up SSL/TLS** for HTTPS encryption
4. **Configure reverse proxy** (nginx/Apache) if needed
5. **Set up backup strategy** for encrypted user data

### Replit Deployment

This platform is optimized for Replit deployment with automatic configuration detection and JSON fallback for reliable operation in cloud environments.

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
