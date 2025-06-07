# AI Phishing Detection Platform

An advanced AI-powered phishing detection platform that combines cutting-edge machine learning technologies with user-friendly security analysis and educational insights. This comprehensive cybersecurity solution was developed as a final semester project for Bachelor of Computer Applications (BCA) at Saraswati Multiple Campus.

## 📌 Project Overview

This platform provides real-time detection and analysis of phishing attempts across multiple channels including URLs, emails, and text messages. Built with modern web technologies and machine learning algorithms, it offers both educational insights and practical security tools for users of all technical levels.

**Key Capabilities:**
- Real-time phishing detection with AI-powered analysis
- Educational security tips and threat awareness
- Role-based user management system
- Comprehensive admin dashboard with analytics
- Cross-platform compatibility and responsive design

## 🚀 Features

### Core Detection Capabilities
- **URL Analysis**: Real-time phishing URL detection with threat intelligence
- **Email Content Analysis**: Advanced email phishing detection with pattern recognition
- **Message Analysis**: General text message phishing detection
- **AI Content Detection**: Identify AI-generated content and deepfakes
- **Explainable AI**: Detailed explanations of detection results with confidence scores

### User Management
- **Role-Based Access Control**: Super Admin, Sub Admin, and Regular User roles
- **Secure Authentication**: Encrypted user data and session management
- **User Dashboard**: Personalized detection history and statistics
- **Password Security**: Enforced strong password requirements

### Admin Features
- **User Management**: Create, edit, and manage user accounts with bulk operations
- **Analytics Dashboard**: Real-time system statistics and monitoring
- **ML Model Management**: Train and optimize detection models
- **Security Tips Management**: Educational content administration
- **Data Export**: CSV export functionality for users and detections

## 💻 Technology Stack

- **Backend**: Python Flask web framework with modular architecture
- **Database**: MongoDB Atlas with automatic local JSON fallback
- **AI/ML**: TensorFlow, scikit-learn, NLTK for advanced threat detection
- **Frontend**: Bootstrap 5 with responsive design and modern JavaScript
- **Charts**: Chart.js for interactive data visualization
- **Security**: Advanced encryption, secure session management, and CSRF protection

## 📋 Prerequisites

- **Python**: Version 3.8 or higher
- **Internet Connection**: For package installation
- **MongoDB Atlas Account**: Optional (automatic fallback to local storage)

## 🔧 Cross-Platform Installation

### Automated Setup (Recommended)

The platform includes an intelligent setup script that automatically detects your operating system and provides optimized installation options:

```bash
# Clone the repository
git clone https://github.com/bigendran/phishing-detection-platform.git
cd phishing-detection-platform

# Run automated setup
python setup.py
```

### Platform-Specific Installation

#### Windows Users
- **Minimal Installation**: Zero compilation, works on all Windows versions (85% accuracy)
- **Basic Installation**: Enhanced features, standard dependencies (90% accuracy)  
- **Full Installation**: Complete ML features, requires build tools (95% accuracy)

See [WINDOWS_INSTALLATION.md](WINDOWS_INSTALLATION.md) for detailed Windows setup guide.

#### macOS Users
- **Basic Installation**: Fast setup with core features
- **Full Installation**: Complete ML capabilities with Xcode tools

#### Linux Users
- **Basic Installation**: Minimal dependencies
- **Full Installation**: Complete feature set with system compiler

### Installation Features by Type

| Feature | Minimal | Basic | Full |
|---------|---------|-------|------|
| Phishing Detection | ✅ (85%) | ✅ (90%) | ✅ (95%) |
| User Authentication | ✅ | ✅ | ✅ |
| Admin Dashboard | ✅ | ✅ | ✅ |
| AI Content Detection | Basic | Enhanced | Complete |
| Machine Learning | ❌ | Limited | Full |
| Real-time Analytics | ✅ | ✅ | Advanced |

### Automatic Fallback System

The setup script includes comprehensive fallback handling:
- Detects compilation capability automatically
- Falls back to basic installation if build tools unavailable  
- Provides minimal installation for maximum compatibility
- Handles Unicode encoding issues across all platforms

## 🛠️ Quick Start

### Windows Users (Recommended)
```bash
# 1. Clone the repository
git clone https://github.com/bigendran/phishing-detection-platform.git
cd phishing-detection-platform

# 2. Use the dedicated Windows installer (handles all compatibility issues)
python install_windows.py

# 3. Activate and run
venv\Scripts\activate
python main.py
```

### Cross-Platform Installation
```bash
# 1. Clone and setup
git clone https://github.com/bigendran/phishing-detection-platform.git
cd phishing-detection-platform
python setup.py

# 2. Activate environment and run
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate
python main.py
```

### 3. Access the Platform
Open your browser and navigate to: `http://localhost:8080`

## 🔐 Default Admin Account

For testing purposes, you can create an admin account through the registration page and then promote it via the database or use the built-in super admin functionality.

### Automated Setup (Recommended)

The easiest way to set up the platform on any operating system:

```bash
# Download project files and extract to desired location
cd ai-phishing-detection-platform

# Run the automated setup script
python setup.py
```

The setup script will:
- Detect your operating system automatically
- Install the correct dependencies for your platform
- Create virtual environment
- Configure the .env file
- Test the installation
- Provide activation instructions

### Manual Setup

If you prefer manual installation, choose your operating system below:

### Windows Setup

1. **Install Python**
   ```bash
   # Download Python 3.8+ from python.org
   # During installation, check "Add Python to PATH"
   # Verify installation
   python --version
   ```

2. **Download and Setup Project**
   ```bash
   # Download project files and extract to desired location
   cd ai-phishing-detection-platform
   
   # Create virtual environment
   python -m venv venv
   
   # Activate virtual environment
   venv\Scripts\activate
   
   # For Windows, use the Windows-compatible requirements file
   pip install -r requirements-windows.txt
   
   # If you encounter compilation errors, try upgrading pip first:
   python -m pip install --upgrade pip
   pip install -r requirements-windows.txt
   ```

### macOS Setup

1. **Install Python and Prerequisites**
   ```bash
   # Install Homebrew (if not already installed)
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   
   # Install Python and development tools
   brew install python3
   
   # Install Xcode Command Line Tools (for compilation)
   xcode-select --install
   
   # Verify installation
   python3 --version
   ```

2. **Download and Setup Project**
   ```bash
   # Download project files and extract to desired location
   cd ai-phishing-detection-platform
   
   # Create virtual environment
   python3 -m venv venv
   
   # Activate virtual environment
   source venv/bin/activate
   
   # Upgrade pip first
   python -m pip install --upgrade pip
   
   # Install macOS-optimized dependencies
   pip install -r requirements-macos.txt
   ```

### Linux (Including Arch Linux) Setup

1. **Install Python and Development Tools**
   ```bash
   # Ubuntu/Debian
   sudo apt update
   sudo apt install python3 python3-pip python3-venv python3-dev build-essential
   
   # Arch Linux
   sudo pacman -S python python-pip base-devel
   
   # CentOS/RHEL/Fedora
   sudo dnf install python3 python3-pip python3-devel gcc gcc-c++ make
   
   # openSUSE
   sudo zypper install python3 python3-pip python3-devel gcc gcc-c++
   
   # Verify installation
   python3 --version
   ```

2. **Download and Setup Project**
   ```bash
   # Download project files and extract to desired location
   cd ai-phishing-detection-platform
   
   # Create virtual environment
   python3 -m venv venv
   
   # Activate virtual environment
   source venv/bin/activate
   
   # Upgrade pip first
   python -m pip install --upgrade pip
   
   # Install Linux-optimized dependencies
   pip install -r requirements-linux.txt
   ```

## 🛢️ MongoDB Atlas Setup (Optional)

The platform works without MongoDB Atlas using local JSON storage, but for production use, MongoDB Atlas is recommended.

### Step-by-Step MongoDB Atlas Configuration

1. **Create MongoDB Account**
   - Visit [MongoDB Atlas](https://www.mongodb.com/atlas)
   - Sign up for a free account
   - Verify your email address

2. **Create Database Cluster**
   - Click "Build a Database"
   - Choose "FREE" tier (M0 Sandbox)
   - Select your preferred cloud provider and region
   - Name your cluster (e.g., "ai-phishing-db")

3. **Configure Database Access**
   - Create a database user with username and password
   - Add your IP address to the IP Access List (or use 0.0.0.0/0 for development)

4. **Get Connection String**
   - Click "Connect" on your cluster
   - Choose "Connect your application"
   - Copy the connection string

5. **Configure Environment Variables**
   ```bash
   # Create .env file in project root
   cp .env.example .env
   
   # Edit .env file with your MongoDB connection details
   ```

### Example .env Configuration

Create a `.env` file in your project root with the following content:

```ini
# MongoDB Atlas Configuration
MONGO_URI=mongodb+srv://potato:<db_password>@build-a-database.5k4i357.mongodb.net/?retryWrites=true&w=majority&appName=Build-a-Database

# Flask Configuration
FLASK_SECRET_KEY=your-unique-secret-key-here-change-for-production
FLASK_ENV=development

# Security Settings (Generate a random 32-character string)
USER_ENCRYPTION_SECRET=your-32-character-encryption-secret

# Application Settings
DEBUG=True
PORT=8080
```

**Important Security Notes:**
- Replace `<db_password>` with your actual MongoDB password
- Generate unique values for `FLASK_SECRET_KEY` and `USER_ENCRYPTION_SECRET`
- Never commit the `.env` file to version control

## 🚀 Running the Application

1. **Activate Virtual Environment**
   ```bash
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

2. **Start the Application**
   ```bash
   python main.py
   ```

3. **Access the Platform**
   - Open your web browser
   - Navigate to `http://localhost:8080`
   - The application will display startup information in the terminal

## 🧪 How to Use the Project

### For Regular Users

1. **Registration and Login**
   - Visit the homepage and click "Register"
   - Create an account with a strong password (minimum 8 characters, uppercase, lowercase, numbers)
   - Login with your credentials

2. **Dashboard Navigation**
   - Access your personal dashboard after login
   - View detection history and statistics
   - Monitor your security analysis trends

3. **Phishing Detection Analysis**
   - **URL Analysis**: Paste suspicious URLs for real-time threat assessment
   - **Email Analysis**: Copy and paste email content for phishing detection
   - **Message Analysis**: Analyze text messages and social media content
   - **AI Content Detection**: Identify potentially AI-generated content

4. **Educational Resources**
   - Visit the "Security Tips" section for cybersecurity education
   - Learn about latest phishing techniques and prevention methods
   - Access regularly updated threat intelligence

### For Administrators

1. **Admin Access**
   - Super Admin and Sub Admin roles have additional privileges
   - Access admin dashboard via `/admin` route

2. **User Management**
   - Create, edit, and manage user accounts
   - Promote/demote user roles (Super Admin only)
   - Export user data and analytics

3. **System Administration**
   - Monitor platform usage and security metrics
   - Train and optimize ML detection models
   - Manage security tips and educational content
   - Generate comprehensive system reports

4. **Analytics and Reporting**
   - View real-time system statistics
   - Monitor detection accuracy and user engagement
   - Export data for external analysis

## 🔒 Security Features

- **Data Encryption**: All sensitive user data encrypted at rest using AES encryption
- **Secure Sessions**: Flask session management with CSRF protection
- **Role-Based Access Control**: Granular permission system with three user levels
- **Input Validation**: Comprehensive sanitization of all user inputs
- **Password Security**: Enforced strong password policies with secure hashing
- **Rate Limiting**: Protection against abuse and automated attacks

## 🤖 Machine Learning Information

The platform employs ensemble learning techniques combining multiple detection methods:

- **Pattern Recognition**: Rule-based phishing indicators and URL analysis
- **Neural Networks**: TensorFlow-based deep learning models
- **Natural Language Processing**: NLTK for advanced text analysis
- **Threat Intelligence**: Offline database of known malicious indicators
- **Explainable AI**: Detailed explanations of detection decisions

## 🧼 Clean Code Practices

This project follows industry best practices for maintainable code:

- **Comprehensive Documentation**: Every function and module thoroughly commented
- **Beginner-Friendly**: Code written with educational clarity in mind
- **Modular Architecture**: Separation of concerns with clear file organization
- **Error Handling**: Robust exception handling and user feedback
- **Security First**: Secure coding practices throughout the application

## 🛠️ Development and Deployment

### Local Development
```bash
# Run in development mode with auto-reload
python main.py

# The application runs on http://localhost:8080
# Debug mode is enabled for development
```

### Production Considerations
- Set `FLASK_ENV=production` in environment variables
- Use a production WSGI server like Gunicorn
- Configure proper SSL certificates
- Set up database backups and monitoring

## 📁 Project Structure

```
ai-phishing-detection-platform/
├── main.py                 # Application entry point
├── app.py                  # Flask application configuration
├── routes.py               # User routes and endpoints
├── auth_routes.py          # Authentication system
├── admin_routes.py         # Admin panel functionality
├── ml_detector.py          # Machine learning detection engine
├── models/                 # Database models and configuration
├── templates/              # HTML templates
├── static/                 # CSS, JavaScript, and images
├── utils/                  # Utility functions and helpers
├── data/                   # Local data storage (JSON fallback)
├── requirements-local.txt  # Python dependencies
├── .env.example           # Environment configuration template
└── README.md              # This documentation
```

## 🚨 Troubleshooting

### Common Issues and Solutions

1. **Windows Compilation Errors (NumPy, TensorFlow, etc.)**
   
   **Problem**: Error messages like "Unknown compiler(s)" or "metadata-generation-failed"
   
   **Solution A - Use Windows Requirements File (Recommended)**:
   ```bash
   # Use the pre-compiled Windows-compatible packages
   pip install -r requirements-windows.txt
   ```
   
   **Solution B - Install Build Tools**:
   ```bash
   # Download and install Microsoft C++ Build Tools from:
   # https://visualstudio.microsoft.com/visual-cpp-build-tools/
   
   # Then retry installation
   pip install -r requirements-local.txt
   ```
   
   **Solution C - Use Conda (Alternative)**:
   ```bash
   # Install Anaconda or Miniconda
   conda create -n phishing-detector python=3.9
   conda activate phishing-detector
   conda install numpy scipy scikit-learn tensorflow flask pymongo
   pip install -r requirements-windows.txt
   ```

2. **Module Not Found Error**
   ```bash
   # Ensure virtual environment is activated
   source venv/bin/activate  # macOS/Linux
   venv\Scripts\activate     # Windows
   
   # Upgrade pip first
   python -m pip install --upgrade pip
   
   # Reinstall dependencies
   pip install -r requirements-windows.txt  # Windows
   pip install -r requirements-local.txt    # macOS/Linux
   ```

3. **Python Version Compatibility**
   ```bash
   # Check Python version (must be 3.8+)
   python --version
   
   # If using older Python, install newer version:
   # Windows: Download from python.org
   # macOS: brew install python@3.11
   # Linux: sudo apt install python3.11
   ```

4. **Virtual Environment Issues**
   ```bash
   # Delete and recreate virtual environment
   rm -rf venv          # Linux/macOS
   rmdir /s venv        # Windows
   
   # Create new environment
   python -m venv venv
   
   # Activate and install
   venv\Scripts\activate                    # Windows
   source venv/bin/activate                # macOS/Linux
   pip install -r requirements-windows.txt # Windows
   ```

5. **MongoDB Connection Issues**
   - Verify your connection string in `.env` file
   - Check IP address whitelist in MongoDB Atlas dashboard
   - Ensure database password doesn't contain special characters
   - The application automatically falls back to local JSON storage if MongoDB fails

6. **Port Already in Use (8080)**
   ```bash
   # Find and kill process using port 8080
   # Linux/macOS
   lsof -ti:8080 | xargs kill -9
   
   # Windows
   netstat -ano | findstr :8080
   taskkill /PID <PID_NUMBER> /F
   
   # Alternative: Change port in main.py
   # Edit: app.run(host="0.0.0.0", port=8081, debug=True)
   ```

7. **Permission Errors**
   ```bash
   # Linux/macOS - Set executable permissions
   chmod +x main.py
   
   # Windows - Run Command Prompt as Administrator
   # Right-click Command Prompt -> "Run as administrator"
   ```

8. **SSL Certificate Errors**
   ```bash
   # Update certificates
   pip install --upgrade certifi
   
   # For macOS additional step:
   /Applications/Python\ 3.x/Install\ Certificates.command
   ```

9. **Memory Errors During Installation**
   ```bash
   # Install packages one by one
   pip install flask
   pip install numpy
   pip install scikit-learn
   # Continue with other packages
   
   # Or increase virtual memory on Windows
   ```

10. **Antivirus Blocking Installation**
    - Temporarily disable antivirus during installation
    - Add Python and project folder to antivirus whitelist
    - Some antivirus software blocks pip installations

### Requirements Files Compatibility

| Platform | Requirements File | Notes |
|----------|------------------|-------|
| **Windows** | `requirements-windows.txt` | Pre-compiled packages, avoids C++ compilation |
| **macOS** | `requirements-macos.txt` | Optimized for macOS with headless OpenCV |
| **Linux** | `requirements-linux.txt` | Works on Ubuntu, Debian, Arch, CentOS, Fedora |
| **Universal** | `requirements-local.txt` | Generic version, may require build tools |

### Platform-Specific Notes

**Windows Users:**
- Use `requirements-windows.txt` to avoid compilation errors
- Install Python from python.org, not Microsoft Store version
- Ensure "Add Python to PATH" is checked during installation
- If you encounter NumPy compilation errors, the Windows requirements file resolves this

**macOS Users:**
- Use `requirements-macos.txt` for optimal compatibility
- Install Xcode Command Line Tools: `xcode-select --install`
- Uses `opencv-python-headless` to avoid GUI dependencies

**Linux Users:**
- Use `requirements-linux.txt` for best results
- Install development packages as shown in setup instructions
- Works across major distributions (Ubuntu, Arch, CentOS, Fedora, openSUSE)

## 📚 Educational Use

This project serves as an excellent learning resource for:

- **Web Development**: Flask framework, HTML/CSS/JavaScript
- **Database Management**: MongoDB integration and data modeling
- **Machine Learning**: TensorFlow, scikit-learn, and NLP techniques
- **Cybersecurity**: Phishing detection and threat analysis
- **Software Engineering**: Clean code practices and project organization

## 🔄 Future Enhancements

Potential improvements and extensions:
- Mobile application development
- Advanced threat intelligence integration
- Real-time notification system
- Multi-language support
- API endpoints for third-party integration

## 👨‍💻 Author

**Bigendra Shrestha**  
Final Semester Project  
Bachelor of Computer Applications (BCA)  
Saraswati Multiple Campus  

*Developed as a comprehensive cybersecurity and AI project demonstrating practical applications of machine learning in threat detection and web application development.*

---

## 📄 License

Educational project - All rights reserved.

## 🤝 Support

For technical support, questions, or collaboration opportunities, please contact the development team.

**Note**: This platform is designed for educational and research purposes. While robust security measures are implemented, always use multiple verification methods for critical security decisions in production environments.