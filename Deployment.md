# AI Phishing Detection Platform - Deployment Guide

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [System Requirements](#system-requirements)
3. [Installation Methods](#installation-methods)
4. [Local Development Deployment](#local-development-deployment)
5. [Production Deployment](#production-deployment)
6. [Docker Deployment](#docker-deployment)
7. [Cloud Deployment](#cloud-deployment)
8. [Configuration](#configuration)
9. [Database Setup](#database-setup)
10. [Security Configuration](#security-configuration)
11. [Monitoring and Logging](#monitoring-and-logging)
12. [Troubleshooting](#troubleshooting)
13. [Maintenance](#maintenance)

---

## Prerequisites

Before deploying the AI Phishing Detection Platform, ensure you have the following prerequisites installed on your target system:

### Required Software

- **Python 3.8+** (Recommended: Python 3.9 or 3.10)
- **MongoDB 4.4+** (Community or Enterprise Edition)
- **Git** (for cloning the repository)
- **pip** (Python package installer)
- **uv** (Fast Python package installer - optional but recommended)

### Optional Software

- **Docker** and **Docker Compose** (for containerized deployment)
- **Nginx** (for production reverse proxy)
- **Redis** (for session storage and caching)
- **Supervisor** or **systemd** (for process management)

---

## System Requirements

### Minimum Requirements

- **CPU:** 2 cores, 2.0 GHz
- **RAM:** 4 GB
- **Storage:** 10 GB free space
- **Network:** Stable internet connection
- **OS:** Windows 10+, macOS 10.15+, Ubuntu 18.04+, CentOS 7+

### Recommended Requirements

- **CPU:** 4+ cores, 2.5+ GHz
- **RAM:** 8+ GB
- **Storage:** 50+ GB SSD
- **Network:** High-speed internet connection
- **OS:** Latest stable versions

### Production Requirements

- **CPU:** 8+ cores, 3.0+ GHz
- **RAM:** 16+ GB
- **Storage:** 100+ GB SSD with backup
- **Network:** Redundant internet connections
- **Load Balancer:** For high availability

---

## Installation Methods

### Method 1: Automated Installation (Recommended)

```bash
# Clone the repository
git clone https://github.com/your-username/phishing-detection-platform.git
cd phishing-detection-platform

# Run automated installation
python install_minimal.py
```

### Method 2: Manual Installation

Follow the detailed steps in the [Local Development Deployment](#local-development-deployment) section.

### Method 3: Docker Installation

See the [Docker Deployment](#docker-deployment) section for containerized deployment.

---

## Local Development Deployment

### Step 1: Clone the Repository

```bash
# Clone the project repository
git clone https://github.com/your-username/phishing-detection-platform.git
cd phishing-detection-platform
```

### Step 2: Set Up Python Environment

#### Using venv (Standard)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

#### Using conda (Alternative)

```bash
# Create conda environment
conda create -n phishing-detection python=3.9
conda activate phishing-detection
```

### Step 3: Install Dependencies

#### Using uv (Recommended - Faster)

```bash
# Install uv if not already installed
pip install uv

# Install dependencies
uv pip install -r requirements.txt
```

#### Using pip (Standard)

```bash
# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt
```

#### Using pyproject.toml

```bash
# Install project in development mode
pip install -e .
```

### Step 4: Set Up Environment Variables

```bash
# Copy environment template
cp .env.example .env

# Edit environment variables
# On Windows:
notepad .env
# On macOS/Linux:
nano .env
```

**Required Environment Variables:**

```env
# Flask Configuration
SECRET_KEY=your-secret-key-here
FLASK_ENV=development
DEBUG=True

# Database Configuration
MONGO_URI=mongodb://localhost:27017/phishing_detection

# Security Settings
WTF_CSRF_ENABLED=True
SESSION_COOKIE_SECURE=False
SESSION_COOKIE_HTTPONLY=True

# File Upload Settings
MAX_CONTENT_LENGTH=16777216
UPLOAD_FOLDER=uploads

# ML Model Settings
MODEL_UPDATE_INTERVAL=3600
THREAT_SCORE_THRESHOLD=0.7
```

### Step 5: Set Up MongoDB

#### Local MongoDB Installation

**Windows:**

```bash
# Download and install MongoDB Community Server
# From: https://www.mongodb.com/try/download/community

# Start MongoDB service
net start MongoDB
```

**macOS:**

```bash
# Install using Homebrew
brew tap mongodb/brew
brew install mongodb-community

# Start MongoDB service
brew services start mongodb/brew/mongodb-community
```

**Ubuntu/Debian:**

```bash
# Import MongoDB public GPG key
wget -qO - https://www.mongodb.org/static/pgp/server-5.0.asc | sudo apt-key add -

# Add MongoDB repository
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/5.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-5.0.list

# Update package database
sudo apt-get update

# Install MongoDB
sudo apt-get install -y mongodb-org

# Start MongoDB service
sudo systemctl start mongod
sudo systemctl enable mongod
```

#### MongoDB Atlas (Cloud Alternative)

1. Create account at [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Create a new cluster
3. Get connection string
4. Update `MONGO_URI` in `.env` file

### Step 6: Initialize Database

```bash
# Run database initialization script
python -c "from app import app; from models.phishing_model import PhishingModel; app.app_context().push(); PhishingModel().initialize_database()"
```

### Step 7: Download ML Models and Data

```bash
# Create necessary directories
mkdir -p data/models
mkdir -p data/datasets

# Download NLTK data
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('vader_lexicon')"
```

### Step 8: Run the Application

```bash
# Start the Flask application
python app.py
```

The application will be available at `http://localhost:5000`

### Step 9: Create Admin User

```bash
# Run user management script
python debug_manage_users.py
```

Or create manually:

```bash
python -c "
from app import app
from models.user_model import UserModel
app.app_context().push()
user_model = UserModel()
user_model.create_user('admin', 'admin@example.com', 'secure_password', 'admin')
print('Admin user created successfully')
"
```

---

## Production Deployment

### Step 1: Server Preparation

#### Update System

```bash
# Ubuntu/Debian
sudo apt update && sudo apt upgrade -y

# CentOS/RHEL
sudo yum update -y
```

#### Install Required Packages

```bash
# Ubuntu/Debian
sudo apt install -y python3 python3-pip python3-venv nginx supervisor git

# CentOS/RHEL
sudo yum install -y python3 python3-pip git nginx supervisor
```

### Step 2: Create Application User

```bash
# Create dedicated user for the application
sudo useradd -m -s /bin/bash phishing-app
sudo usermod -aG sudo phishing-app

# Switch to application user
sudo su - phishing-app
```

### Step 3: Deploy Application

```bash
# Clone repository
git clone https://github.com/your-username/phishing-detection-platform.git
cd phishing-detection-platform

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Install production WSGI server
pip install gunicorn
```

### Step 4: Production Environment Configuration

```bash
# Create production environment file
cp .env.example .env.production
```

**Production Environment Variables:**

```env
# Flask Configuration
SECRET_KEY=your-very-secure-secret-key
FLASK_ENV=production
DEBUG=False

# Database Configuration
MONGO_URI=mongodb://username:password@localhost:27017/phishing_detection_prod

# Security Settings
WTF_CSRF_ENABLED=True
SESSION_COOKIE_SECURE=True
SESSION_COOKIE_HTTPONLY=True
SESSION_COOKIE_SAMESITE=Strict

# Performance Settings
MAX_CONTENT_LENGTH=16777216
UPLOAD_FOLDER=/var/uploads/phishing-detection

# Logging
LOG_LEVEL=INFO
LOG_FILE=/var/log/phishing-detection/app.log
```

### Step 5: Configure Gunicorn

Create `gunicorn.conf.py`:

```python
# Gunicorn configuration file
bind = "127.0.0.1:8000"
workers = 4
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2
max_requests = 1000
max_requests_jitter = 100
preload_app = True

# Logging
accesslog = "/var/log/phishing-detection/gunicorn-access.log"
errorlog = "/var/log/phishing-detection/gunicorn-error.log"
loglevel = "info"

# Process naming
proc_name = "phishing-detection"

# Server mechanics
daemon = False
pidfile = "/var/run/phishing-detection/gunicorn.pid"
user = "phishing-app"
group = "phishing-app"
tmp_upload_dir = None

# SSL (if using HTTPS directly)
# keyfile = "/path/to/keyfile"
# certfile = "/path/to/certfile"
```

### Step 6: Configure Supervisor

Create `/etc/supervisor/conf.d/phishing-detection.conf`:

```ini
[program:phishing-detection]
command=/home/phishing-app/phishing-detection-platform/venv/bin/gunicorn -c gunicorn.conf.py app:app
directory=/home/phishing-app/phishing-detection-platform
user=phishing-app
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/phishing-detection/supervisor.log
stdout_logfile_maxbytes=10MB
stdout_logfile_backups=5
environment=PATH="/home/phishing-app/phishing-detection-platform/venv/bin"
```

### Step 7: Configure Nginx

Create `/etc/nginx/sites-available/phishing-detection`:

```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;
    
    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com www.your-domain.com;
    
    # SSL Configuration
    ssl_certificate /path/to/your/certificate.crt;
    ssl_certificate_key /path/to/your/private.key;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;
    
    # Security Headers
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection "1; mode=block";
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; font-src 'self';";
    
    # File Upload Limit
    client_max_body_size 16M;
    
    # Static Files
    location /static {
        alias /home/phishing-app/phishing-detection-platform/static;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
    
    # Main Application
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_connect_timeout 30s;
        proxy_send_timeout 30s;
        proxy_read_timeout 30s;
    }
    
    # Health Check Endpoint
    location /health {
        access_log off;
        proxy_pass http://127.0.0.1:8000/health;
    }
}
```

Enable the site:

```bash
sudo ln -s /etc/nginx/sites-available/phishing-detection /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### Step 8: Start Services

```bash
# Create log directories
sudo mkdir -p /var/log/phishing-detection
sudo chown phishing-app:phishing-app /var/log/phishing-detection

# Create run directory
sudo mkdir -p /var/run/phishing-detection
sudo chown phishing-app:phishing-app /var/run/phishing-detection

# Start supervisor
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start phishing-detection

# Start nginx
sudo systemctl start nginx
sudo systemctl enable nginx
```

---

## Docker Deployment

### Step 1: Create Dockerfile

Create `Dockerfile`:

```dockerfile
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY pyproject.toml .
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Download NLTK data
RUN python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('vader_lexicon')"

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Start application
CMD ["gunicorn", "-c", "gunicorn.conf.py", "app:app"]
```

### Step 2: Create Docker Compose

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
      - MONGO_URI=mongodb://mongo:27017/phishing_detection
      - SECRET_KEY=${SECRET_KEY}
    depends_on:
      - mongo
      - redis
    volumes:
      - ./uploads:/app/uploads
      - ./logs:/app/logs
    restart: unless-stopped
    networks:
      - phishing-network

  mongo:
    image: mongo:5.0
    ports:
      - "27017:27017"
    environment:
      - MONGO_INITDB_ROOT_USERNAME=${MONGO_ROOT_USERNAME}
      - MONGO_INITDB_ROOT_PASSWORD=${MONGO_ROOT_PASSWORD}
      - MONGO_INITDB_DATABASE=phishing_detection
    volumes:
      - mongo_data:/data/db
      - ./mongo-init:/docker-entrypoint-initdb.d
    restart: unless-stopped
    networks:
      - phishing-network

  redis:
    image: redis:6-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    restart: unless-stopped
    networks:
      - phishing-network

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - app
    restart: unless-stopped
    networks:
      - phishing-network

volumes:
  mongo_data:
  redis_data:

networks:
  phishing-network:
    driver: bridge
```

### Step 3: Create Environment File

Create `.env.docker`:

```env
SECRET_KEY=your-docker-secret-key
MONGO_ROOT_USERNAME=admin
MONGO_ROOT_PASSWORD=secure_password
FLASK_ENV=production
```

### Step 4: Deploy with Docker Compose

```bash
# Build and start services
docker-compose --env-file .env.docker up -d

# View logs
docker-compose logs -f

# Scale application
docker-compose up -d --scale app=3

# Stop services
docker-compose down
```

---

## Cloud Deployment

### AWS Deployment

#### Using AWS Elastic Beanstalk

1. **Install EB CLI:**

```bash
pip install awsebcli
```

2. **Initialize EB Application:**

```bash
eb init phishing-detection-platform
```

3. **Create Environment:**

```bash
eb create production
```

4. **Deploy:**

```bash
eb deploy
```

#### Using AWS ECS

1. **Create Task Definition**
2. **Create ECS Cluster**
3. **Create Service**
4. **Configure Load Balancer**

### Google Cloud Platform

#### Using Google App Engine

Create `app.yaml`:

```yaml
runtime: python39

env_variables:
  SECRET_KEY: "your-secret-key"
  MONGO_URI: "your-mongodb-uri"
  FLASK_ENV: "production"

automatic_scaling:
  min_instances: 1
  max_instances: 10
  target_cpu_utilization: 0.6

resources:
  cpu: 1
  memory_gb: 2
  disk_size_gb: 10
```

Deploy:

```bash
gcloud app deploy
```

### Microsoft Azure

#### Using Azure App Service

```bash
# Create resource group
az group create --name phishing-detection-rg --location eastus

# Create app service plan
az appservice plan create --name phishing-detection-plan --resource-group phishing-detection-rg --sku B1 --is-linux

# Create web app
az webapp create --resource-group phishing-detection-rg --plan phishing-detection-plan --name phishing-detection-app --runtime "PYTHON|3.9"

# Deploy code
az webapp deployment source config-zip --resource-group phishing-detection-rg --name phishing-detection-app --src app.zip
```

---

## Configuration

### Environment Variables Reference

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `SECRET_KEY` | Flask secret key for sessions | None | Yes |
| `FLASK_ENV` | Flask environment | development | No |
| `DEBUG` | Enable debug mode | False | No |
| `MONGO_URI` | MongoDB connection string | mongodb://localhost:27017/phishing_detection | Yes |
| `REDIS_URL` | Redis connection string | redis://localhost:6379/0 | No |
| `MAX_CONTENT_LENGTH` | Maximum file upload size | 16777216 | No |
| `UPLOAD_FOLDER` | File upload directory | uploads | No |
| `LOG_LEVEL` | Logging level | INFO | No |
| `LOG_FILE` | Log file path | None | No |
| `MODEL_UPDATE_INTERVAL` | ML model update interval (seconds) | 3600 | No |
| `THREAT_SCORE_THRESHOLD` | Threat detection threshold | 0.7 | No |

### Security Configuration

#### SSL/TLS Setup

1. **Obtain SSL Certificate:**

```bash
# Using Let's Encrypt
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

2. **Configure SSL in Nginx:**

See the Nginx configuration in the Production Deployment section.

#### Firewall Configuration

```bash
# Ubuntu/Debian (UFW)
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable

# CentOS/RHEL (firewalld)
sudo firewall-cmd --permanent --add-service=ssh
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --add-service=https
sudo firewall-cmd --reload
```

---

## Database Setup

### MongoDB Configuration

#### Replica Set Setup (Production)

1. **Configure Replica Set:**

```javascript
// Connect to MongoDB
mongo

// Initialize replica set
rs.initiate({
  _id: "rs0",
  members: [
    { _id: 0, host: "mongo1:27017" },
    { _id: 1, host: "mongo2:27017" },
    { _id: 2, host: "mongo3:27017" }
  ]
})
```

2. **Create Database User:**

```javascript
use phishing_detection
db.createUser({
  user: "phishing_app",
  pwd: "secure_password",
  roles: [
    { role: "readWrite", db: "phishing_detection" }
  ]
})
```

#### Database Indexing

```javascript
// Create indexes for better performance
db.urls.createIndex({ "url": 1 })
db.urls.createIndex({ "threat_score": -1 })
db.urls.createIndex({ "created_at": -1 })
db.users.createIndex({ "email": 1 }, { unique: true })
db.users.createIndex({ "username": 1 }, { unique: true })
```

### Backup and Restore

#### Backup

```bash
# Create backup
mongodump --uri="mongodb://username:password@localhost:27017/phishing_detection" --out=/backup/$(date +%Y%m%d_%H%M%S)

# Automated backup script
#!/bin/bash
BACKUP_DIR="/backup/mongodb"
DATE=$(date +%Y%m%d_%H%M%S)
mkdir -p $BACKUP_DIR
mongodump --uri="$MONGO_URI" --out="$BACKUP_DIR/$DATE"
find $BACKUP_DIR -type d -mtime +7 -exec rm -rf {} +
```

#### Restore

```bash
# Restore from backup
mongorestore --uri="mongodb://username:password@localhost:27017/phishing_detection" /backup/20241201_120000/phishing_detection
```

---

## Security Configuration

### Application Security

#### Rate Limiting

Install Flask-Limiter:

```bash
pip install Flask-Limiter
```

Configure in `app.py`:

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/api/scan')
@limiter.limit("10 per minute")
def scan_endpoint():
    # Your code here
    pass
```

#### Input Validation

Ensure all user inputs are properly validated and sanitized.

#### CSRF Protection

CSRF protection is enabled by default in the application.

### Infrastructure Security

#### Server Hardening

```bash
# Disable root login
sudo sed -i 's/PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config

# Change default SSH port
sudo sed -i 's/#Port 22/Port 2222/' /etc/ssh/sshd_config

# Restart SSH service
sudo systemctl restart sshd

# Install fail2ban
sudo apt install fail2ban
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
```

#### Database Security

```bash
# Enable MongoDB authentication
sudo nano /etc/mongod.conf

# Add to configuration:
security:
  authorization: enabled

# Restart MongoDB
sudo systemctl restart mongod
```

---

## Monitoring and Logging

### Application Monitoring

#### Health Check Endpoint

Add to `app.py`:

```python
@app.route('/health')
def health_check():
    try:
        # Check database connection
        mongo.db.command('ping')
        return {'status': 'healthy', 'timestamp': datetime.utcnow().isoformat()}
    except Exception as e:
        return {'status': 'unhealthy', 'error': str(e)}, 500
```

#### Logging Configuration

Configure logging in `app.py`:

```python
import logging
from logging.handlers import RotatingFileHandler

if not app.debug:
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/phishing_detection.log', maxBytes=10240000, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('Phishing Detection Platform startup')
```

### System Monitoring

#### Using Prometheus and Grafana

1. **Install Prometheus:**

```bash
# Download and install Prometheus
wget https://github.com/prometheus/prometheus/releases/download/v2.40.0/prometheus-2.40.0.linux-amd64.tar.gz
tar xvfz prometheus-*.tar.gz
cd prometheus-*
./prometheus --config.file=prometheus.yml
```

2. **Configure Grafana:**

```bash
# Install Grafana
sudo apt-get install -y software-properties-common
sudo add-apt-repository "deb https://packages.grafana.com/oss/deb stable main"
wget -q -O - https://packages.grafana.com/gpg.key | sudo apt-key add -
sudo apt-get update
sudo apt-get install grafana

# Start Grafana
sudo systemctl start grafana-server
sudo systemctl enable grafana-server
```

---

## Troubleshooting

### Common Issues

#### Application Won't Start

1. **Check Python version:**

```bash
python --version
# Should be 3.8 or higher
```

2. **Check dependencies:**

```bash
pip list
# Verify all required packages are installed
```

3. **Check environment variables:**

```bash
echo $SECRET_KEY
echo $MONGO_URI
```

4. **Check logs:**

```bash
tail -f logs/phishing_detection.log
```

#### Database Connection Issues

1. **Check MongoDB status:**

```bash
sudo systemctl status mongod
```

2. **Test connection:**

```bash
mongo --eval "db.adminCommand('ismaster')"
```

3. **Check firewall:**

```bash
sudo ufw status
```

#### Performance Issues

1. **Check system resources:**

```bash
top
df -h
free -m
```

2. **Check application metrics:**

```bash
curl http://localhost:5000/health
```

3. **Optimize database:**

```javascript
// MongoDB optimization
db.runCommand({"profile": 2})
db.system.profile.find().limit(5).sort({ts: -1}).pretty()
```

### Log Analysis

#### Application Logs

```bash
# View recent logs
tail -f /var/log/phishing-detection/app.log

# Search for errors
grep -i error /var/log/phishing-detection/app.log

# View access logs
tail -f /var/log/nginx/access.log
```

#### System Logs

```bash
# View system logs
journalctl -u phishing-detection -f

# View MongoDB logs
journalctl -u mongod -f

# View Nginx logs
journalctl -u nginx -f
```

---

## Maintenance

### Regular Maintenance Tasks

#### Daily Tasks

1. **Check application health:**

```bash
curl -f http://localhost:5000/health || echo "Application unhealthy"
```

2. **Monitor disk space:**

```bash
df -h | grep -E '(8[0-9]|9[0-9])%' && echo "Disk space warning"
```

3. **Check logs for errors:**

```bash
grep -i error /var/log/phishing-detection/app.log | tail -10
```

#### Weekly Tasks

1. **Update ML models:**

```bash
python -c "from utils.ml_detector import MLPhishingDetector; detector = MLPhishingDetector(); detector.update_models()"
```

2. **Database maintenance:**

```javascript
// Compact database
db.runCommand({"compact": "urls"})
db.runCommand({"compact": "users"})
```

3. **Log rotation:**

```bash
logrotate /etc/logrotate.d/phishing-detection
```

#### Monthly Tasks

1. **Security updates:**

```bash
sudo apt update && sudo apt upgrade -y
```

2. **Backup verification:**

```bash
# Test restore from backup
mongorestore --dry-run /backup/latest
```

3. **Performance review:**

```bash
# Analyze slow queries
db.setProfilingLevel(2, {slowms: 100})
```

### Update Procedures

#### Application Updates

```bash
# Backup current version
cp -r /home/phishing-app/phishing-detection-platform /home/phishing-app/phishing-detection-platform.backup

# Pull latest changes
cd /home/phishing-app/phishing-detection-platform
git pull origin main

# Update dependencies
source venv/bin/activate
pip install -r requirements.txt

# Run database migrations (if any)
python migrate.py

# Restart application
sudo supervisorctl restart phishing-detection
```

#### System Updates

```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Update Python packages
pip list --outdated
pip install --upgrade package_name

# Restart services
sudo systemctl restart mongod
sudo supervisorctl restart phishing-detection
sudo systemctl restart nginx
```

---

## Support and Resources

### Documentation

- [Flask Documentation](https://flask.palletsprojects.com/)
- [MongoDB Documentation](https://docs.mongodb.com/)
- [Nginx Documentation](https://nginx.org/en/docs/)
- [Supervisor Documentation](http://supervisord.org/)

### Community Support

- **GitHub Issues:** Report bugs and request features
- **Stack Overflow:** Tag questions with `phishing-detection`
- **Discord/Slack:** Join our community chat

### Professional Support

For enterprise deployments and professional support, contact:
- Email: support@phishing-detection.com
- Phone: +1-555-PHISH-HELP

---

**Last Updated:** December 2024  
**Version:** 1.0  
**Maintainer:** AI Phishing Detection Platform Team