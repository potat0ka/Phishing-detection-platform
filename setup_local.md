# Local Setup Guide for AI Phishing Detection Platform

## Quick Setup (Recommended)

1. **Install Dependencies**:
   ```bash
   python install_local.py
   ```

2. **Set up Environment** (optional - MongoDB will fallback to local files):
   ```bash
   # Create .env file with your MongoDB connection
   echo "MONGODB_URI=your_mongodb_connection_string" > .env
   ```

3. **Run the Application**:
   ```bash
   python main.py
   ```

4. **Access the Application**:
   Open your browser to: http://localhost:8080

## Manual Installation (Alternative)

If the automatic installer doesn't work, install dependencies manually:

```bash
# Core Flask dependencies
pip install Flask==2.3.3 Flask-Login Flask-PyMongo pymongo Werkzeug

# Security and validation
pip install bcrypt cryptography passlib email-validator dnspython

# Text processing
pip install beautifulsoup4 trafilatura nltk python-docx pdfplumber

# AI and machine learning
pip install scikit-learn openai

# Image and multimedia
pip install Pillow opencv-python imagehash librosa soundfile pytesseract

# Utilities
pip install requests python-dotenv
```

## Requirements

- **Python**: 3.8 or higher
- **Operating System**: Windows, macOS, or Linux
- **Memory**: 2GB RAM minimum
- **Storage**: 500MB free space

## MongoDB Setup (Optional)

The application works without MongoDB (uses local file storage), but for full functionality:

1. Create a free MongoDB Atlas account
2. Get your connection string
3. Add it to a `.env` file:
   ```
   MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/database
   ```

## Troubleshooting

### Common Issues:

1. **Module not found errors**: Run the installer or install missing packages manually
2. **Port already in use**: The app runs on port 8080 by default
3. **Permission errors**: Use `python -m pip install` instead of `pip install`
4. **MongoDB connection issues**: The app will work with local file storage if MongoDB is unavailable

### Getting Help:

- Check the error logs in the terminal
- Ensure all dependencies are installed
- Verify Python version is 3.8+
- Make sure port 8080 is available

## Features Available Locally

✅ Phishing URL Detection
✅ Email Content Analysis  
✅ Text Analysis for AI-generated content
✅ File Upload Analysis (PDF, DOCX, images)
✅ User Authentication and Registration
✅ Admin Dashboard
✅ Safety Tips and Resources

The platform runs fully offline with all AI-powered detection features!