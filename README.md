# AI-Powered Phishing Detection Platform

An advanced phishing detection web application that combines machine learning, real-time threat intelligence, and user-friendly security analysis. Built as a comprehensive cybersecurity solution for detecting phishing URLs, emails, and messages.

## Features

### Core Detection Capabilities
- **AI-Powered Analysis**: Advanced machine learning using TF-IDF vectorization and Naive Bayes classification
- **Real-time Threat Intelligence**: Comprehensive offline threat analysis with local threat database
- **Multi-layered Detection**: Combines pattern matching, AI analysis, and threat intelligence
- **User-Friendly Explanations**: Clear, non-technical explanations of security threats

### Detection Types
- **URL Analysis**: Detects malicious URLs, typosquatting, and suspicious domains
- **Email Analysis**: Identifies phishing emails, urgent language, and credential harvesting
- **Message Analysis**: Analyzes text messages and social media content for threats

### Advanced Features
- **Typosquatting Detection**: Identifies domains that mimic legitimate brands
- **DNS Analysis**: Performs comprehensive DNS lookups and reputation checking
- **Pattern Recognition**: Advanced regex patterns for suspicious content
- **Threat Classification**: 5-level threat scoring (CRITICAL, HIGH, MEDIUM, LOW, MINIMAL)

### User Interface
- **Responsive Design**: Works seamlessly on desktop and mobile devices
- **Dark Theme**: Professional dark mode interface with Bootstrap styling
- **Interactive Dashboard**: User authentication and detection history
- **Educational Content**: Security tips and phishing awareness resources

## Technology Stack

- **Backend**: Python 3.11, Flask
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Machine Learning**: scikit-learn, NLTK, NumPy
- **Frontend**: Bootstrap 5, JavaScript, HTML5
- **Security**: DNS analysis, IP reputation, threat intelligence
- **Deployment**: Gunicorn WSGI server

## Local Installation

### Prerequisites
- Python 3.11 or higher
- PostgreSQL 12 or higher
- Git

### Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone <your-repository-url>
   cd phishing-detection-platform
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up PostgreSQL Database**
   ```bash
   # Create database
   createdb phishing_detector
   
   # Or using PostgreSQL command line
   psql -c "CREATE DATABASE phishing_detector;"
   ```

5. **Configure Environment Variables**
   Create a `.env` file in the project root:
   ```env
   DATABASE_URL=postgresql://username:password@localhost:5432/phishing_detector
   SESSION_SECRET=your-secret-key-here
   FLASK_ENV=development
   
   # Optional: External API Keys for enhanced threat intelligence
   VIRUSTOTAL_API_KEY=your-virustotal-key
   ABUSEIPDB_API_KEY=your-abuseipdb-key
   SHODAN_API_KEY=your-shodan-key
   URLSCAN_API_KEY=your-urlscan-key
   ```

6. **Initialize Database**
   ```bash
   python -c "from app import app, db; app.app_context().push(); db.create_all()"
   ```

7. **Run the Application**
   ```bash
   # Development server
   python main.py
   
   # Or with Gunicorn (production-like)
   gunicorn --bind 0.0.0.0:5000 --reload main:app
   ```

8. **Access the Application**
   Open your browser and navigate to `http://localhost:5000`

## Requirements File

Create a `requirements.txt` file with these dependencies:

```txt
Flask==3.0.0
Flask-SQLAlchemy==3.1.1
psycopg2-binary==2.9.9
Werkzeug==3.0.1
SQLAlchemy==2.0.23
nltk==3.8.1
numpy==1.26.2
scikit-learn==1.3.2
requests==2.32.3
dnspython==2.4.2
gunicorn==21.2.0
python-dotenv==1.0.0
```

## Project Structure

```
phishing-detection-platform/
├── main.py                 # Application entry point
├── app.py                  # Flask application setup
├── routes.py               # URL routes and views
├── models.py               # Database models
├── ml_detector.py          # Machine learning detection engine
├── threat_intelligence.py  # Basic threat intelligence
├── offline_threat_intel.py # Advanced offline threat analysis
├── advanced_threat_intel.py # API-based threat intelligence
├── utils.py                # Utility functions
├── social_automation.py    # Social media automation features
├── static/                 # Static files (CSS, JS, images)
│   ├── css/
│   ├── js/
│   └── images/
├── templates/              # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── check.html
│   ├── result.html
│   ├── dashboard.html
│   └── tips.html
├── instance/               # Instance-specific files
├── .env                    # Environment variables
├── requirements.txt        # Python dependencies
├── README.md              # This file
└── .replit                # Replit configuration
```

## Usage

### Basic Phishing Detection
1. Navigate to the "Check Content" page
2. Select content type (URL, Email, or Message)
3. Paste the suspicious content
4. Click "Analyze with AI"
5. Review the detailed security analysis

### User Registration
1. Click "Register" to create an account
2. Access your personal dashboard
3. View detection history and statistics
4. Get personalized security recommendations

### Educational Resources
- Visit the "Tips" section for security awareness
- Learn about different types of phishing attacks
- Understand how to identify suspicious content

## Deployment Options

### Replit Deployment
1. Import project to Replit
2. Configure environment variables in Secrets
3. Run using the integrated workflows
4. Deploy using Replit's hosting service

### Cloud Deployment (Heroku, AWS, etc.)
1. Set up PostgreSQL database
2. Configure environment variables
3. Deploy using Git or container
4. Set up domain and SSL certificate

### Docker Deployment
Create a `Dockerfile`:
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "main:app"]
```

## Security Features

- **Input Validation**: All user inputs are sanitized and validated
- **SQL Injection Protection**: Using SQLAlchemy ORM with parameterized queries
- **Session Security**: Secure session management with secret keys
- **Password Hashing**: Werkzeug secure password hashing
- **HTTPS Ready**: Configured for SSL/TLS deployment

## API Integration (Optional)

The platform supports integration with external threat intelligence APIs:

- **VirusTotal**: URL and file scanning
- **AbuseIPDB**: IP reputation checking
- **Shodan**: Infrastructure analysis
- **URLScan.io**: Website behavior analysis

Register for free API keys at these services to enhance detection accuracy.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- Create an issue in the GitHub repository
- Review the documentation and examples
- Check the troubleshooting section below

## Troubleshooting

### Common Issues

**Database Connection Error**
- Verify PostgreSQL is running
- Check DATABASE_URL in environment variables
- Ensure database exists and user has permissions

**Missing Dependencies**
- Run `pip install -r requirements.txt`
- Check Python version compatibility
- Verify virtual environment is activated

**NLTK Data Error**
- Run `python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet')"`

**Port Already in Use**
- Change port in command: `gunicorn --bind 0.0.0.0:8000 main:app`
- Kill existing process: `lsof -ti:5000 | xargs kill -9`

## Future Enhancements

- Real-time API threat intelligence integration
- Machine learning model improvements
- Mobile application development
- Enterprise security features
- Advanced reporting and analytics
- Multi-language support

---

Built with ❤️ for cybersecurity education and protection.