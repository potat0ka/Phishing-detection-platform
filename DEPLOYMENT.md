# Production Deployment Guide

## Overview

This guide provides instructions for deploying the AI Phishing Detection Platform to production environments including cloud platforms, VPS servers, and containerized deployments.

## Pre-Deployment Checklist

### Security Configuration
- [ ] Set strong `FLASK_SECRET_KEY` environment variable
- [ ] Configure `USER_ENCRYPTION_SECRET` for data encryption
- [ ] Set up MongoDB Atlas with proper authentication
- [ ] Enable HTTPS/SSL certificates
- [ ] Configure firewall rules
- [ ] Set `DEBUG=False` in production

### Performance Optimization
- [ ] Use production WSGI server (Gunicorn/uWSGI)
- [ ] Configure reverse proxy (Nginx/Apache)
- [ ] Set up database connection pooling
- [ ] Enable gzip compression
- [ ] Configure static file serving

## Deployment Options

### 1. Replit Deployment (Recommended for Testing)

```bash
# The application is already configured for Replit
# Simply click the "Run" button or use:
python main.py
```

**Environment Variables in Replit:**
```env
FLASK_SECRET_KEY=your_production_secret_key
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/database
USER_ENCRYPTION_SECRET=your_encryption_key
DEBUG=False
```

### 2. Heroku Deployment

1. **Create Heroku App:**
```bash
heroku create your-app-name
```

2. **Set Environment Variables:**
```bash
heroku config:set FLASK_SECRET_KEY=your_secret_key
heroku config:set MONGODB_URI=mongodb+srv://user:pass@cluster.mongodb.net/db
heroku config:set USER_ENCRYPTION_SECRET=your_encryption_key
heroku config:set DEBUG=False
```

3. **Create Procfile:**
```
web: gunicorn -w 4 -b 0.0.0.0:$PORT main:app
```

4. **Deploy:**
```bash
git add .
git commit -m "Production deployment"
git push heroku main
```

### 3. VPS/Cloud Server Deployment

#### Prerequisites
- Ubuntu 20.04+ or CentOS 8+
- Python 3.8+
- Nginx
- MongoDB (local or Atlas)

#### Installation Steps

1. **Server Setup:**
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install python3 python3-pip python3-venv nginx -y

# Create application user
sudo useradd -m -s /bin/bash phishing-detector
sudo su - phishing-detector
```

2. **Application Setup:**
```bash
# Clone repository
git clone <your-repository-url>
cd ai-phishing-detection-platform

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install gunicorn
```

3. **Environment Configuration:**
```bash
# Create production environment file
cat > .env << EOF
FLASK_SECRET_KEY=your_very_secure_secret_key_here
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/phishing_detector
USER_ENCRYPTION_SECRET=your_encryption_key_here
DEBUG=False
PORT=5000
HOST=127.0.0.1
EOF
```

4. **Systemd Service:**
```bash
# Create service file
sudo tee /etc/systemd/system/phishing-detector.service << EOF
[Unit]
Description=AI Phishing Detection Platform
After=network.target

[Service]
User=phishing-detector
Group=phishing-detector
WorkingDirectory=/home/phishing-detector/ai-phishing-detection-platform
Environment=PATH=/home/phishing-detector/ai-phishing-detection-platform/venv/bin
ExecStart=/home/phishing-detector/ai-phishing-detection-platform/venv/bin/gunicorn -w 4 -b 127.0.0.1:5000 main:app
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable phishing-detector
sudo systemctl start phishing-detector
```

5. **Nginx Configuration:**
```bash
# Create Nginx config
sudo tee /etc/nginx/sites-available/phishing-detector << EOF
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }

    location /static {
        alias /home/phishing-detector/ai-phishing-detection-platform/static;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
EOF

# Enable site
sudo ln -s /etc/nginx/sites-available/phishing-detector /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 4. Docker Deployment

1. **Create Dockerfile:**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 5000

# Run application
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "main:app"]
```

2. **Create docker-compose.yml:**
```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "80:5000"
    environment:
      - FLASK_SECRET_KEY=your_secret_key
      - MONGODB_URI=mongodb://mongo:27017/phishing_detector
      - USER_ENCRYPTION_SECRET=your_encryption_key
      - DEBUG=False
    depends_on:
      - mongo
    volumes:
      - ./data:/app/data

  mongo:
    image: mongo:5.0
    ports:
      - "27017:27017"
    volumes:
      - mongo_data:/data/db
    environment:
      - MONGO_INITDB_ROOT_USERNAME=admin
      - MONGO_INITDB_ROOT_PASSWORD=password

volumes:
  mongo_data:
```

3. **Deploy with Docker:**
```bash
# Build and run
docker-compose up -d

# View logs
docker-compose logs -f web
```

## Database Setup

### MongoDB Atlas (Recommended)

1. **Create Cluster:**
   - Sign up at [mongodb.com/atlas](https://mongodb.com/atlas)
   - Create free tier cluster
   - Configure database user and IP whitelist

2. **Connection String:**
   ```
   mongodb+srv://username:password@cluster.mongodb.net/phishing_detector
   ```

### Local MongoDB

1. **Install MongoDB:**
```bash
# Ubuntu
sudo apt install mongodb

# CentOS
sudo yum install mongodb-org

# Start service
sudo systemctl start mongod
sudo systemctl enable mongod
```

2. **Create Database:**
```bash
mongo
use phishing_detector
db.createUser({
  user: "phishing_user",
  pwd: "secure_password",
  roles: [{ role: "readWrite", db: "phishing_detector" }]
})
```

## SSL/HTTPS Configuration

### Using Certbot (Let's Encrypt)

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Obtain certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

## Monitoring and Logging

### Application Logs
```bash
# View systemd logs
sudo journalctl -u phishing-detector -f

# View Nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### Health Checks
```bash
# Application health endpoint
curl http://your-domain.com/health

# Expected response:
# {"status": "healthy", "database": "connected", "version": "2.0.0"}
```

## Performance Tuning

### Gunicorn Configuration
```python
# gunicorn.conf.py
bind = "127.0.0.1:5000"
workers = 4
worker_class = "sync"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 100
timeout = 30
keepalive = 2
```

### Nginx Optimization
```nginx
# Add to nginx.conf
worker_processes auto;
worker_connections 1024;

gzip on;
gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;

# Rate limiting
limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
limit_req zone=api burst=20 nodelay;
```

## Security Hardening

### Firewall Configuration
```bash
# UFW (Ubuntu)
sudo ufw allow ssh
sudo ufw allow 'Nginx Full'
sudo ufw enable

# Fail2ban for SSH protection
sudo apt install fail2ban
```

### Application Security
- Use strong secret keys (minimum 32 characters)
- Enable HTTPS only
- Set secure cookie flags
- Implement rate limiting
- Regular security updates

## Backup Strategy

### Database Backup
```bash
# MongoDB Atlas: Use Atlas backup features
# Local MongoDB:
mongodump --db phishing_detector --out /backup/$(date +%Y%m%d)

# Automated backup script
#!/bin/bash
BACKUP_DIR="/backup/mongodb/$(date +%Y%m%d)"
mkdir -p $BACKUP_DIR
mongodump --db phishing_detector --out $BACKUP_DIR
tar -czf $BACKUP_DIR.tar.gz $BACKUP_DIR
rm -rf $BACKUP_DIR
```

### Application Backup
```bash
# Backup application data
tar -czf phishing_detector_$(date +%Y%m%d).tar.gz \
    /home/phishing-detector/ai-phishing-detection-platform/data
```

## Scaling Considerations

### Horizontal Scaling
- Use load balancer (Nginx, HAProxy)
- Deploy multiple application instances
- Shared database (MongoDB Atlas)
- Session store (Redis)

### Vertical Scaling
- Increase server resources (CPU, RAM)
- Optimize database queries
- Use caching (Redis, Memcached)
- CDN for static files

## Troubleshooting

### Common Issues

**Application Won't Start:**
```bash
# Check logs
sudo journalctl -u phishing-detector
# Check Python path and dependencies
source venv/bin/activate && python -c "import flask; print('OK')"
```

**Database Connection Failed:**
```bash
# Test MongoDB connection
python -c "
import pymongo
client = pymongo.MongoClient('your_connection_string')
print(client.admin.command('hello'))
"
```

**High Memory Usage:**
```bash
# Monitor processes
htop
# Adjust Gunicorn workers
# Check for memory leaks in application logs
```

## Maintenance

### Regular Tasks
- [ ] Update system packages monthly
- [ ] Update Python dependencies quarterly
- [ ] Monitor disk space and logs
- [ ] Test backup restoration
- [ ] Security audit
- [ ] Performance monitoring

### Update Procedure
```bash
# 1. Backup current version
sudo systemctl stop phishing-detector
cp -r /home/phishing-detector/ai-phishing-detection-platform /backup/

# 2. Update code
cd /home/phishing-detector/ai-phishing-detection-platform
git pull origin main

# 3. Update dependencies
source venv/bin/activate
pip install -r requirements.txt

# 4. Restart service
sudo systemctl start phishing-detector
sudo systemctl status phishing-detector
```

---

For additional support or questions about deployment, refer to the main README.md or contact the development team.