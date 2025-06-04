# AI Phishing Detection Platform 🛡️

A comprehensive phishing detection web application powered by AI and machine learning. Perfect for learning backend development with a simple JSON-based database system!

## 🌟 Features

- **AI-Powered Detection**: Advanced machine learning algorithms to detect phishing URLs, emails, and messages
- **AI Content Detection**: Analyze images and documents to detect if they're AI-generated
- **User Authentication**: Secure user registration and login system
- **Detection History**: Track your security scans and results
- **Educational Security Tips**: 45+ comprehensive cybersecurity tips with animated carousel
- **Real-time Threat Intelligence**: Latest phishing trends and awareness content
- **Simple JSON Database**: Easy-to-understand data storage perfect for learning
- **Responsive Design**: Works on desktop, tablet, and mobile devices

## 🚀 Quick Setup Guide

### Prerequisites

You need Python 3.11 or higher installed on your system.

#### Check if Python is installed:
```bash
python --version
# or
python3 --version
```

If Python is not installed, download it from [python.org](https://www.python.org/downloads/)

### 📥 Installation

#### Quick Setup (Recommended)

1. **Download the project**
   ```bash
   git clone <repository-url>
   cd Phishing-detection-website
   ```

2. **Install dependencies using pip**
   ```bash
   pip install flask flask-sqlalchemy gunicorn werkzeug pillow numpy scikit-learn nltk beautifulsoup4 requests trafilatura
   ```

3. **Run the application**
   ```bash
   python main.py
   ```
   
   **OR using Gunicorn (recommended):**
   ```bash
   gunicorn --bind 0.0.0.0:5000 --reuse-port --reload main:app
   ```

4. **Open your browser**
   - Go to: `http://localhost:5000`
   - Start using the application!

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
   pip install flask flask-sqlalchemy gunicorn werkzeug pillow numpy scikit-learn nltk beautifulsoup4 requests trafilatura
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

## 📁 Project Structure

```
ai-phishing-detector/
├── app.py                      # Main application file (START HERE!)
├── routes.py                   # Web routes and page handlers
├── simple_models.py            # Database models (JSON-based)
├── ml_detector.py              # AI/ML phishing detection engine
├── security_tips_updater.py    # Security tips management
├── utils.py                    # Helper functions
├── main.py                     # Application entry point
├── requirements.txt            # Python dependencies
├── README.md                   # This file!
├── database/                   # JSON database files (auto-created)
│   ├── users.json             # User accounts
│   ├── detections.json        # Detection history
│   └── tips.json              # Security tips
├── templates/                  # HTML templates
│   ├── base.html              # Base template
│   ├── index.html             # Home page
│   ├── check.html             # Detection interface
│   ├── result.html            # Detection results
│   ├── tips.html              # Security tips page
│   ├── dashboard.html         # User dashboard
│   ├── login.html             # Login page
│   └── register.html          # Registration page
└── static/                     # Static files (CSS, JS, images)
    ├── css/
    │   └── style.css          # Custom styles
    └── js/
        └── main.js            # JavaScript functionality
```

## 🗄️ Database System (Perfect for Learning!)

This project uses a **simple JSON-based database** instead of complex systems like PostgreSQL or MongoDB. Here's why it's perfect for beginners:

### Why JSON Database?
- ✅ **Easy to understand**: Data is stored in readable JSON files
- ✅ **No setup required**: No database server installation needed
- ✅ **Portable**: Works on any system without configuration
- ✅ **Transparent**: You can see exactly what data is stored
- ✅ **Great for learning**: Understand data storage concepts

### Database Files
- `database/users.json` - User accounts and authentication
- `database/detections.json` - Phishing detection results
- `database/tips.json` - Security tips and educational content

### Example Data Structure
```json
// users.json
[
  {
    "id": "unique-user-id",
    "username": "john_doe",
    "email": "john@example.com",
    "password_hash": "hashed-password",
    "created_at": "2024-01-01T12:00:00"
  }
]

// detections.json
[
  {
    "id": "detection-id",
    "user_id": "user-id",
    "input_type": "url",
    "input_content": "suspicious-website.com",
    "result": "phishing",
    "confidence_score": 0.85,
    "created_at": "2024-01-01T12:00:00"
  }
]
```

## 🤖 AI & Machine Learning Features

### Detection Capabilities
- **URL Analysis**: Checks suspicious domains, URL patterns, and redirects
- **Email Content Analysis**: Detects phishing emails using NLP
- **Message Analysis**: Analyzes suspicious text messages
- **Threat Intelligence**: Real-time threat data integration

### ML Techniques Used
- **TF-IDF Vectorization**: Text feature extraction
- **Naive Bayes Classification**: Machine learning model
- **Pattern Matching**: Rule-based detection
- **Confidence Scoring**: Reliability assessment

## 🎓 Learning Opportunities

This project is designed for educational purposes and includes:

### Backend Development Concepts
- **Web Framework**: Flask (Python)
- **Database Operations**: CRUD operations with JSON
- **User Authentication**: Session management and password hashing
- **API Development**: RESTful endpoints
- **File I/O**: Reading and writing JSON data

### Frontend Development
- **Responsive Design**: Bootstrap CSS framework
- **Interactive UI**: JavaScript and animations
- **Form Handling**: User input validation
- **AJAX Requests**: Asynchronous data fetching

### Security Concepts
- **Password Hashing**: Secure password storage
- **Session Management**: User authentication
- **Input Validation**: Preventing injection attacks
- **CSRF Protection**: Cross-site request forgery prevention

## 🔧 Configuration

### Environment Variables (Optional)
Create a `.env` file for custom configuration:
```env
SESSION_SECRET=your-secret-key-here
DEBUG=True
PORT=5000
```

### Customization
- **Modify security tips**: Edit `security_tips_updater.py`
- **Adjust ML model**: Update `ml_detector.py`
- **Change styling**: Edit `static/css/style.css`
- **Add new pages**: Create templates and routes

## 🚨 Troubleshooting

### Common Issues and Solutions

#### 1. "Module not found" error
```bash
# Solution 1: Install missing dependencies
pip install flask flask-sqlalchemy gunicorn werkzeug pillow numpy scikit-learn nltk beautifulsoup4 requests trafilatura

# Solution 2: Make sure you're in the right directory
cd path/to/your/project

# Solution 3: If using virtual environment, activate it first
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows
```

#### 2. "Cannot import name 'app' from 'main'" error
```bash
# Make sure you run with correct entry point
python main.py

# NOT python app.py (this is an old instruction)
```

#### 3. "Permission denied" or "Access denied" error
```bash
# On Mac/Linux, use python3 and add sudo if needed
sudo python3 main.py

# On Windows, run Command Prompt as Administrator
```

#### 4. Port 5000 already in use
```bash
# On Mac/Linux:
lsof -ti:5000 | xargs kill -9

# On Windows:
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Alternative: Use different port
python main.py --port 8080
```

#### 5. Database files not created
```bash
# Create database directory manually
mkdir database

# Ensure write permissions
chmod 755 database/  # Mac/Linux
```

#### 6. AI Content Detection issues (PIL/OpenCV errors)
```bash
# Install image processing dependencies
pip install Pillow==11.2.1

# On Linux, you might need additional system packages
sudo apt install python3-dev python3-pip libjpeg-dev zlib1g-dev
```

#### 7. NLTK download errors
```python
# Run this in Python console first
import nltk
nltk.download('punkt')
nltk.download('stopwords')
```

### Step-by-Step Debug Process

If you're still having issues, follow these steps:

1. **Check Python version**
   ```bash
   python --version
   # Should be 3.11 or higher
   ```

2. **Verify you're in the correct directory**
   ```bash
   ls -la
   # You should see main.py, app.py, routes.py, etc.
   ```

3. **Install dependencies one by one**
   ```bash
   pip install flask
   pip install flask-sqlalchemy
   pip install werkzeug
   pip install pillow
   pip install numpy
   pip install scikit-learn
   pip install nltk
   pip install beautifulsoup4
   pip install requests
   pip install trafilatura
   ```

4. **Test basic Flask installation**
   ```python
   # Create test.py
   from flask import Flask
   app = Flask(__name__)
   
   @app.route('/')
   def hello():
       return "Flask is working!"
   
   if __name__ == '__main__':
       app.run(debug=True)
   ```

5. **Run the actual application**
   ```bash
   python main.py
   ```

### Platform-Specific Issues

#### Windows Issues
- Use `python` instead of `python3`
- Run Command Prompt as Administrator
- Install Microsoft Visual C++ Build Tools if compilation errors occur

#### macOS Issues
- Use `python3` instead of `python`
- Install Xcode Command Line Tools: `xcode-select --install`
- Use Homebrew for Python: `brew install python@3.11`

#### Linux Issues
- Install development packages: `sudo apt install python3-dev build-essential`
- Use `python3.11` specifically if multiple versions installed

## 🤝 Contributing

This is an educational project! Feel free to:
- Add new features
- Improve the ML model
- Enhance the UI/UX
- Add more security tips
- Fix bugs

## 📚 Learning Resources

### Recommended Reading
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Python JSON Module](https://docs.python.org/3/library/json.html)
- [Bootstrap CSS](https://getbootstrap.com/docs/)
- [Cybersecurity Basics](https://www.cisa.gov/cybersecurity)

### Next Steps for Learning
1. Add more ML models for better detection
2. Implement email integration
3. Add real-time notifications
4. Create mobile app version
5. Deploy to cloud platforms

## 📄 License

This project is for educational purposes. Feel free to use and modify for learning!

## 💬 Support

If you encounter any issues:
1. Check the troubleshooting section above
2. Ensure all dependencies are installed
3. Verify Python version compatibility
4. Check the console output for error messages

---

**Happy Learning! 🎉**

This project demonstrates real-world web development concepts in a beginner-friendly way. Take time to explore the code, understand how each component works, and experiment with modifications!
