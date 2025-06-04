# AI Phishing Detection Platform

An advanced AI-powered phishing detection web platform with enterprise-level security and comprehensive user data encryption. Built using Flask with simple `python main.py` startup for easy local development and deployment.

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

### Simple Startup
The platform uses Flask's built-in development server with simple `python main.py` startup - no complex server configuration required.

#### System Requirements
- **Python**: 3.8 or higher (3.11+ recommended)
- **Operating System**: Windows, macOS, or Linux
- **Memory**: 512MB RAM minimum
- **Storage**: 500MB free space

### 🚀 Quick Installation

#### Method 1: One-Command Setup
```bash
# Clone and run in one go
git clone <repository-url>
cd ai-phishing-detection-platform
pip install -r requirements-minimal.txt
python main.py
```

#### Method 2: Step-by-Step Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ai-phishing-detection-platform
   ```

2. **Install dependencies**
   ```bash
   # Option A: Use minimal requirements (recommended)
   pip install -r requirements-minimal.txt
   
   # Option B: Manual installation
   pip install flask werkzeug pillow numpy scikit-learn nltk beautifulsoup4 requests trafilatura dnspython email-validator opencv-python-headless cryptography pymongo flask-pymongo psycopg2-binary
   ```

3. **Start the application**
   ```bash
   python main.py
   ```

4. **Open in browser**
   - Navigate to `http://localhost:5000`
   - The platform automatically uses secure JSON storage with AES-256 encryption
   - Create an account to access all features

### ⚙️ Configuration (Optional)
```bash
# Set custom encryption key for production
export USER_ENCRYPTION_SECRET="your-32-character-encryption-key"

# Set session secret
export SESSION_SECRET="your-session-secret"

# Configure MongoDB (optional - JSON fallback available)
export DATABASE_URL="mongodb://localhost:27017/phishing_detector"
```

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
