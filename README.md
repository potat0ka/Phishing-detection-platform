# AI Phishing Detection Platform 🛡️

A comprehensive phishing detection web application powered by AI and machine learning. Perfect for learning backend development with a simple JSON-based database system!

## 🌟 Features

- **AI-Powered Detection**: Advanced machine learning algorithms to detect phishing URLs, emails, and messages
- **User Authentication**: Secure user registration and login system
- **Detection History**: Track your security scans and results
- **Educational Security Tips**: 45+ comprehensive cybersecurity tips with animated carousel
- **Real-time Threat Intelligence**: Latest phishing trends and awareness content
- **Simple JSON Database**: Easy-to-understand data storage perfect for learning
- **Responsive Design**: Works on desktop, tablet, and mobile devices

## 🚀 Quick Setup Guide

### Prerequisites

You need Python 3.7 or higher installed on your system.

#### Check if Python is installed:
```bash
python --version
# or
python3 --version
```

If Python is not installed, download it from [python.org](https://www.python.org/downloads/)

### 📥 Installation

#### Option 1: Quick Setup (Recommended for beginners)

1. **Download the project**
   ```bash
   git clone <repository-url>
   cd ai-phishing-detector
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Open your browser**
   - Go to: `http://localhost:5000`
   - Start using the application!

#### Option 2: Virtual Environment Setup (Recommended for development)

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
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

### 🖥️ Platform-Specific Instructions

#### Windows
```cmd
# Install Python from python.org if not installed
# Open Command Prompt or PowerShell
git clone <repository-url>
cd ai-phishing-detector
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

#### macOS
```bash
# Install Homebrew if not installed: /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
# Install Python: brew install python3
git clone <repository-url>
cd ai-phishing-detector
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

#### Linux (Ubuntu/Debian)
```bash
# Update package list
sudo apt update
# Install Python and pip if not installed
sudo apt install python3 python3-pip python3-venv git
# Clone and setup
git clone <repository-url>
cd ai-phishing-detector
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
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

### Common Issues

#### "Module not found" error
```bash
# Make sure virtual environment is activated
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

#### "Permission denied" error
```bash
# On Mac/Linux, use python3 instead of python
python3 app.py
```

#### Port already in use
```bash
# Kill process using port 5000
# On Mac/Linux:
lsof -ti:5000 | xargs kill -9

# On Windows:
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

#### Database files not created
- Check if you have write permissions in the project directory
- The `database/` folder should be created automatically
- If issues persist, create the folder manually: `mkdir database`

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