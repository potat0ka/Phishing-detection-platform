# Quick Installation Guide

## Automatic Installation (Recommended)

Run the automated installer:
```bash
python install_dependencies.py
```

This script will:
- Create virtual environment automatically
- Install all required packages
- Verify installation
- Provide next steps

## Manual Installation

### Step 1: Create Virtual Environment
```bash
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### Step 2: Install Required Packages
```bash
pip install flask==2.3.3 pymongo==4.5.0 requests==2.31.0 scikit-learn==1.3.2 nltk==3.8.1 beautifulsoup4==4.12.2 bcrypt==4.0.1 pillow==9.5.0 email-validator==2.1.0 trafilatura==1.6.4 dnspython==2.4.2 passlib==1.7.4 cryptography==41.0.7 werkzeug==2.3.7
```

### Step 3: Run Application
```bash
python main.py
```

## Package List for Reference

Core packages needed:
- flask==2.3.3 (web framework)
- pymongo==4.5.0 (database)
- requests==2.31.0 (HTTP client)
- scikit-learn==1.3.2 (machine learning)
- nltk==3.8.1 (natural language processing)
- beautifulsoup4==4.12.2 (HTML parsing)
- bcrypt==4.0.1 (password hashing)
- pillow==9.5.0 (image processing)
- email-validator==2.1.0 (email validation)
- trafilatura==1.6.4 (text extraction)
- dnspython==2.4.2 (DNS utilities)
- passlib==1.7.4 (password utilities)
- cryptography==41.0.7 (encryption)
- werkzeug==2.3.7 (WSGI utilities)

## Troubleshooting

If installation fails:
1. Ensure Python 3.8+ is installed
2. Update pip: `pip install --upgrade pip`
3. Install packages one by one to identify issues
4. Check virtual environment is activated

## Default Credentials

After installation, use these credentials to test:
- Super Admin: super_admin / SuperAdmin123!
- Sub Admin: potato / potato123
- Regular User: user / user123