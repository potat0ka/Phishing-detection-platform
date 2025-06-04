# AI Phishing Detection Platform

An advanced AI-powered phishing detection web platform designed to educate and protect users through intelligent security technologies and machine learning innovations.

## Features

### Core Security Features
- **AI-Powered Phishing Detection**: Advanced machine learning algorithms to detect phishing URLs, emails, and messages with confidence scoring
- **Comprehensive AI Content Detection**: Analyze images, videos, audio, and documents to detect AI-generated content with source identification
- **Offline Threat Intelligence**: Local threat detection without external API dependencies
- **Real-time Security Assessment**: Domain and URL security evaluation with threat level classification
- **Device Peripheral Integration**: Camera capture and microphone recording for content analysis

### Enhanced User Experience
- **Photo to Text (OCR)**: Extract text from images using Tesseract.js with real-time processing
- **Multiple File Format Support**: Images (JPG, PNG, GIF), videos (MP4, AVI, MOV), audio (MP3, WAV), documents (TXT, PDF)
- **Bulk Management**: Multiple selection and deletion of detection history
- **User Authentication**: Secure registration and login with session management
- **Educational Security Tips**: 39+ comprehensive cybersecurity tips with latest threat intelligence
- **Mobile-Friendly Design**: Touch-optimized interactions with responsive Bootstrap design
- **File Upload Validation**: 500MB maximum file size with comprehensive error handling

## Quick Setup Guide

### Prerequisites

- Python 3.11 or higher
- PostgreSQL database (optional - SQLite will be used as fallback)

#### Check Python installation:
```bash
python --version
# or
python3 --version
```

### Installation

#### Method 1: Quick Setup

1. **Download the project**
   ```bash
   git clone <repository-url>
   cd ai-phishing-detection-platform
   ```

2. **Install all dependencies**
   ```bash
   pip install flask flask-sqlalchemy gunicorn werkzeug pillow numpy scikit-learn nltk beautifulsoup4 requests trafilatura dnspython email-validator anthropic opencv-python tensorflow psycopg2-binary
   ```

3. **Run the application**
   ```bash
   python main.py
   ```
   
   **Alternative with Gunicorn:**
   ```bash
   gunicorn --bind 0.0.0.0:5000 --reuse-port --reload main:app
   ```

4. **Access the application**
   - Open browser: `http://localhost:5000`
   - Register an account and start using the platform

#### Virtual Environment Setup (Recommended for development)

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
   pip install flask flask-sqlalchemy gunicorn werkzeug pillow numpy scikit-learn nltk beautifulsoup4 requests trafilatura dnspython
   ```

3. **Run the application**
   ```bash
   python main.py
   ```

### 🖥️ Platform-Specific Instructions

#### Windows
```cmd
# Install Python 3.11+ from python.org if not installed
# Open Command Prompt or PowerShell as Administrator
git clone <repository-url>
cd ai-phishing-detector
python -m venv venv
venv\Scripts\activate
pip install flask flask-sqlalchemy gunicorn werkzeug pillow numpy scikit-learn nltk beautifulsoup4 requests trafilatura
python main.py
```

#### macOS
```bash
# Install Homebrew if not installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
# Install Python 3.11+
brew install python@3.11
git clone <repository-url>
cd ai-phishing-detector
python3 -m venv venv
source venv/bin/activate
pip install flask flask-sqlalchemy gunicorn werkzeug pillow numpy scikit-learn nltk beautifulsoup4 requests trafilatura
python main.py
```

#### Linux (Ubuntu/Debian)
```bash
# Update package list
sudo apt update
# Install Python 3.11 and dependencies
sudo apt install python3.11 python3.11-pip python3.11-venv git python3.11-dev
# Clone and setup
git clone <repository-url>
cd ai-phishing-detector
python3.11 -m venv venv
source venv/bin/activate
pip install flask flask-sqlalchemy gunicorn werkzeug pillow numpy scikit-learn nltk beautifulsoup4 requests trafilatura
python main.py
```

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
