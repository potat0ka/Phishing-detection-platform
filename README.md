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
```

### 2. Install Dependencies (Choose One Method)

**Method A: Automatic Installation (Recommended)**
```bash
python install_dependencies.py
```
This script automatically creates virtual environment and installs all dependencies.

**Method B: Manual Installation**
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install core packages
pip install scikit-learn
pip install numpy

# Install all required packages
pip install flask==2.3.3 pymongo==4.5.0 requests==2.31.0 scikit-learn==1.3.2 nltk==3.8.1 beautifulsoup4==4.12.2 bcrypt==4.0.1 pillow==9.5.0 email-validator==2.1.0 trafilatura==1.6.4 dnspython==2.4.2 passlib==1.7.4 cryptography==41.0.7
```

**Alternative Installation (Arch Linux/Package Managers):**
```bash
# For Arch Linux users
sudo pacman -S python-scikit-learn
sudo pacman -S python-numpy

# Then install remaining packages with pip
pip install flask==2.3.3 pymongo==4.5.0 requests==2.31.0 nltk==3.8.1 beautifulsoup4==4.12.2 bcrypt==4.0.1 pillow==9.5.0 email-validator==2.1.0 trafilatura==1.6.4 dnspython==2.4.2 passlib==1.7.4 cryptography==41.0.7
```

### 3. Configure Environment (Optional)

```bash
# Copy environment template
cp .env.example .env

# Edit .env file with your database settings if needed
```

### 4. Run the Application

```bash
python main.py
```

### 5. Access the Platform

Open your web browser and go to: `http://localhost:8080`

### 6. Default Login Credentials

**Super Admin:**
- Username: `super_admin`
- Password: `SuperAdmin123!`

**Sub Admin:**
- Username: `potato`
- Password: `potato123`

**Regular User:**
- Username: `potato1`
- Password: `123456789`

*Note: Change these default passwords immediately after first login for security.*

## 🔧 Detailed Installation Guide

### Windows Installation

1. **Install Python**:
   - Download Python 3.8+ from [python.org](https://python.org)
   - During installation, check "Add Python to PATH"

2. **Open Command Prompt** and verify installation:
   ```cmd
   python --version
   pip --version
   ```

3. **Navigate to project directory**:
   ```cmd
   cd ai-phishing-detection-platform
   ```

4. **Install dependencies**:
   ```cmd
   # Option 1: Automatic installation
   python install_dependencies.py
   
   # Option 2: Manual installation
   python -m venv venv
   venv\Scripts\activate
   pip install flask==2.3.3 pymongo==4.5.0 requests==2.31.0 scikit-learn==1.3.2 nltk==3.8.1 beautifulsoup4==4.12.2 bcrypt==4.0.1 pillow==9.5.0 email-validator==2.1.0 trafilatura==1.6.4 dnspython==2.4.2 passlib==1.7.4 cryptography==41.0.7
   ```

6. **Run the application**:
   ```cmd
   python main.py
   ```

7. **Deactivate virtual environment when done**:
   ```cmd
   deactivate
   ```

### macOS Installation

1. **Install Python** (if not already installed):
   ```bash
   # Using Homebrew
   brew install python

   # Or download from python.org
   ```

2. **Navigate to project directory**:
   ```bash
   cd ai-phishing-detection-platform
   ```

3. **Create and activate virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the application**:
   ```bash
   python3 main.py
   ```

6. **Deactivate virtual environment when done**:
   ```bash
   deactivate
   ```

### Linux (Ubuntu/Debian) Installation

1. **Update system and install Python**:
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip python3-venv
   ```

2. **Navigate to project directory**:
   ```bash
   cd ai-phishing-detection-platform
   ```

3. **Create and activate virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the application**:
   ```bash
   python3 main.py
   ```

6. **Deactivate virtual environment when done**:
   ```bash
   deactivate
   ```

### Arch Linux Installation

1. **Install Python and pip**:
   ```bash
   sudo pacman -S python python-pip
   ```

2. **Navigate to project directory**:
   ```bash
   cd ai-phishing-detection-platform
   ```

3. **Create and activate virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the application**:
   ```bash
   python main.py
   ```

6. **Deactivate virtual environment when done**:
   ```bash
   deactivate
   ```

## 🗄️ Database Configuration

### Option 1: Local Storage (Default)
The application works out-of-the-box with local JSON file storage. No additional setup required.

### Option 2: Local MongoDB Setup (Recommended)

**Step 1: Install MongoDB Community Edition**

**For Windows:**
1. Download MongoDB from [https://www.mongodb.com/try/download/community](https://www.mongodb.com/try/download/community)
2. During installation, select "Install MongoDB as a Service"
3. Start MongoDB server from Services app or using `mongod` command

**For macOS (using Homebrew):**
```bash
brew tap mongodb/brew
brew install mongodb-community@7.0
brew services start mongodb-community@7.0
```

**For Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install -y mongodb
sudo systemctl start mongodb
sudo systemctl enable mongodb
```

**For Arch Linux:**
```bash
sudo pacman -S mongodb
sudo systemctl start mongodb
sudo systemctl enable mongodb
```

**Step 2: Verify MongoDB Is Running**
```bash
mongo
```
If the MongoDB shell opens without errors, you're ready to proceed!

**Step 3: Configure Project to Use Local MongoDB**
In your `.env` file, set:
```env
MONGODB_URI=mongodb://localhost:27017/phishing_detector
```

**Step 4: Troubleshooting Local MongoDB**
If connection fails, check:
- MongoDB service is running: `sudo systemctl status mongodb`
- Port 27017 is open: `netstat -tlnp | grep 27017`
- MONGODB_URI points to localhost correctly
- No firewall blocking port 27017

### Option 3: MongoDB Atlas (Cloud Database)

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
├── main.py                    # Main application entry point
├── install_dependencies.py   # Automated dependency installer
├── requirements-manual.txt   # Manual dependency reference
├── INSTALL.md                # Quick installation guide
├── MONGODB_SETUP.md          # MongoDB configuration guide
├── DEPLOYMENT.md             # Production deployment guide
├── src/                      # Source code directory
│   ├── app.py               # Flask application setup
│   ├── routes.py            # Main application routes
│   ├── auth_routes.py       # Authentication routes
│   ├── admin_routes.py      # Admin panel routes
│   ├── ml_detector.py       # AI detection algorithms
│   ├── models/              # Database models
│   └── utils/               # Utility functions
├── templates/               # HTML templates
├── static/                 # CSS, JavaScript, images
├── data/                   # Local data storage
├── .env.example            # Environment template
└── README.md              # This file
```

## 📋 Installation Files

- **install_dependencies.py** - Automated installer that creates virtual environment and installs all packages
- **requirements-manual.txt** - Complete list of required packages with versions
- **INSTALL.md** - Quick installation guide with troubleshooting
- **MONGODB_SETUP.md** - Comprehensive MongoDB setup for all platforms

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
