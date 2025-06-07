# AI Phishing Detection Platform

A comprehensive cybersecurity platform that uses artificial intelligence and machine learning to detect phishing URLs, emails, and malicious content. Built as a final semester project for cybersecurity education.

## 🚀 Features

- **AI-Powered Detection**: Advanced machine learning algorithms to identify phishing attempts
- **Multi-Modal Analysis**: Detects phishing in URLs, emails, and AI-generated content
- **User Management**: Role-based authentication system (Admin, Sub-Admin, Regular User)
- **Educational Resources**: Interactive safety tips and learning materials
- **Real-Time Monitoring**: Live dashboard with detection statistics
- **Cross-Platform Support**: Runs on Windows, macOS, and Linux

## 🛠️ Technology Stack

- **Backend**: Python 3.11, Flask web framework
- **Database**: MongoDB Atlas (cloud) with local JSON fallback
- **Frontend**: Bootstrap 5, Chart.js for visualizations
- **AI/ML**: scikit-learn, NLTK for natural language processing
- **Security**: bcrypt for password hashing, custom encryption utilities

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- MongoDB Atlas account (optional - local storage available)
- Internet connection for package installation

## ⚡ Quick Start

### 1. Download and Setup

```bash
# Clone or download this project
git clone <your-repository-url>
cd ai-phishing-detection-platform

# Install required packages
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env file with your settings (optional for basic usage)
```

### 3. Run the Application

```bash
# Start the web server
python main.py
```

### 4. Access the Platform

Open your web browser and go to: `http://localhost:8080`

## 🔧 Detailed Installation Guide

### Windows Installation

1. **Install Python**:
   - Download Python 3.8+ from [python.org](https://python.org)
   - During installation, check "Add Python to PATH"

2. **Open Command Prompt** and run:
   ```cmd
   python --version
   pip --version
   ```

3. **Install dependencies**:
   ```cmd
   pip install flask pymongo requests scikit-learn nltk beautifulsoup4 bcrypt
   ```

4. **Run the application**:
   ```cmd
   python main.py
   ```

### macOS Installation

1. **Install Python** (if not already installed):
   ```bash
   # Using Homebrew
   brew install python

   # Or download from python.org
   ```

2. **Install dependencies**:
   ```bash
   pip3 install flask pymongo requests scikit-learn nltk beautifulsoup4 bcrypt
   ```

3. **Run the application**:
   ```bash
   python3 main.py
   ```

### Linux (Ubuntu/Debian) Installation

1. **Update system and install Python**:
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip
   ```

2. **Install dependencies**:
   ```bash
   pip3 install flask pymongo requests scikit-learn nltk beautifulsoup4 bcrypt
   ```

3. **Run the application**:
   ```bash
   python3 main.py
   ```

### Arch Linux Installation

1. **Install Python and pip**:
   ```bash
   sudo pacman -S python python-pip
   ```

2. **Install dependencies**:
   ```bash
   pip install flask pymongo requests scikit-learn nltk beautifulsoup4 bcrypt
   ```

3. **Run the application**:
   ```bash
   python main.py
   ```

## 🗄️ Database Configuration

### Option 1: Local Storage (Default)
The application works out-of-the-box with local JSON file storage. No additional setup required.

### Option 2: MongoDB Atlas (Cloud Database)

1. **Create MongoDB Atlas Account**:
   - Go to [mongodb.com/atlas](https://mongodb.com/atlas)
   - Create a free account and cluster

2. **Get Connection String**:
   - In Atlas dashboard, click "Connect"
   - Choose "Connect your application"
   - Copy the connection string

3. **Configure Environment**:
   ```bash
   # Edit .env file
   MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/phishing_detector
   ```

### Option 3: Local MongoDB

1. **Install MongoDB locally**:
   - Windows: Download from [mongodb.com](https://mongodb.com)
   - macOS: `brew install mongodb/brew/mongodb-community`
   - Linux: Follow [official guide](https://docs.mongodb.com/manual/administration/install-on-linux/)

2. **Configure Environment**:
   ```bash
   # Edit .env file
   MONGODB_URI=mongodb://localhost:27017/phishing_detector
   ```

## 🔐 Environment Configuration

Create a `.env` file in the project root:

```env
# Flask Settings
FLASK_SECRET_KEY=your_secret_key_here

# Database (optional - defaults to local storage)
MONGODB_URI=mongodb://localhost:27017/phishing_detector

# Encryption (optional - auto-generated if not set)
USER_ENCRYPTION_SECRET=your_encryption_key_here

# Application Settings
DEBUG=True
PORT=8080
HOST=0.0.0.0
```

## 🚀 Usage

### For Regular Users
1. **Register Account**: Create a new user account
2. **Check URLs**: Paste suspicious URLs for AI analysis
3. **Scan Emails**: Copy email content for phishing detection
4. **Learn Security**: Browse educational safety tips

### For Administrators
1. **Login with Admin Account**: Use admin credentials
2. **User Management**: Create, edit, and manage user accounts
3. **Monitor Activity**: View detection logs and system statistics
4. **Train AI Models**: Retrain machine learning models with new data

## 🔧 Troubleshooting

### Common Issues

**Port Already in Use**:
```bash
# Change port in main.py or kill existing process
lsof -ti:8080 | xargs kill -9  # macOS/Linux
netstat -ano | findstr :8080   # Windows
```

**Module Not Found**:
```bash
# Reinstall dependencies
pip install --force-reinstall -r requirements.txt
```

**Database Connection Failed**:
- Application will automatically use local storage
- Check MongoDB connection string in .env file
- Ensure MongoDB service is running (if using local)

### Platform-Specific Notes

**Windows**:
- Use `python` command (not `python3`)
- Use Command Prompt or PowerShell
- Ensure Python is in PATH

**macOS**:
- May need to use `python3` instead of `python`
- Install Xcode Command Line Tools if needed

**Linux**:
- Use `python3` command
- May need to install `python3-dev` package
- Use `sudo` for system-wide installations

## 📁 Project Structure

```
ai-phishing-detection-platform/
├── main.py                 # Main application entry point
├── src/                    # Source code directory
│   ├── app.py             # Flask application setup
│   ├── routes.py          # Main application routes
│   ├── auth_routes.py     # Authentication routes
│   ├── admin_routes.py    # Admin panel routes
│   ├── ml_detector.py     # AI detection algorithms
│   ├── models/            # Database models
│   └── utils/             # Utility functions
├── templates/             # HTML templates
├── static/               # CSS, JavaScript, images
├── data/                 # Local data storage
├── .env.example          # Environment template
└── README.md            # This file
```

## 🤝 Contributing

This is an educational project. Feel free to:
- Report bugs and issues
- Suggest improvements
- Submit educational enhancements
- Share security insights

## 📄 License

This project is created for educational purposes as part of a cybersecurity curriculum.

## 👨‍💻 Author

**Bigendra Shrestha**  
Final Semester Student - Cybersecurity & AI  
Saraswati Multiple Campus (8th Semester)

---

**⚠️ Educational Notice**: This platform is designed for learning cybersecurity concepts. Always verify results with additional security tools in production environments.