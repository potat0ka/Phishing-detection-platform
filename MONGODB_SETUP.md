# MongoDB Setup Guide for AI Phishing Detection Platform

This guide provides detailed instructions for setting up MongoDB to work with the AI Phishing Detection Platform across all operating systems.

## Database Options Overview

The platform supports three database configurations:

1. **Local JSON Storage** (Default) - Works immediately, no setup required
2. **Local MongoDB** (Recommended for Development) - Better performance and features
3. **MongoDB Atlas** (Recommended for Production) - Cloud-hosted, scalable

## Option 1: Local JSON Storage (Default)

**No setup required** - The application automatically uses local JSON files if MongoDB is not available.

- Data stored in `data/` directory
- Compatible with MongoDB structure
- Automatic fallback if MongoDB connection fails

## Option 2: Local MongoDB Setup

### Windows Installation

1. **Download MongoDB Community Edition**:
   - Go to [https://www.mongodb.com/try/download/community](https://www.mongodb.com/try/download/community)
   - Select "Windows" and "MSI" package
   - Download the installer

2. **Install MongoDB**:
   - Run the downloaded `.msi` file
   - Choose "Complete" installation
   - **Important**: Check "Install MongoDB as a Service"
   - Check "Install MongoDB Compass" (optional GUI tool)

3. **Verify Installation**:
   ```cmd
   # Open Command Prompt as Administrator
   net start MongoDB
   
   # Test connection
   mongo
   ```

4. **Configure Windows Service**:
   - Open "Services" app (services.msc)
   - Find "MongoDB Server" service
   - Set startup type to "Automatic"
   - Start the service if not running

5. **Configure Firewall** (if needed):
   ```cmd
   # Allow MongoDB through Windows Firewall
   netsh advfirewall firewall add rule name="MongoDB" dir=in action=allow protocol=TCP localport=27017
   ```

### macOS Installation

1. **Using Homebrew** (Recommended):
   ```bash
   # Install Homebrew if not already installed
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   
   # Add MongoDB tap
   brew tap mongodb/brew
   
   # Install MongoDB Community Edition
   brew install mongodb-community@7.0
   ```

2. **Start MongoDB Service**:
   ```bash
   # Start MongoDB service
   brew services start mongodb-community@7.0
   
   # Verify it's running
   brew services list | grep mongodb
   ```

3. **Manual Installation** (Alternative):
   - Download from [MongoDB Download Center](https://www.mongodb.com/try/download/community)
   - Extract to `/usr/local/mongodb`
   - Create data directory: `sudo mkdir -p /usr/local/var/mongodb`
   - Create log directory: `sudo mkdir -p /usr/local/var/log/mongodb`
   - Start manually: `/usr/local/mongodb/bin/mongod --dbpath /usr/local/var/mongodb`

4. **Test Connection**:
   ```bash
   # Connect to MongoDB shell
   mongosh
   # or older versions:
   mongo
   ```

### Ubuntu/Debian Installation

1. **Import MongoDB Public Key**:
   ```bash
   curl -fsSL https://pgp.mongodb.com/server-7.0.asc | sudo gpg -o /usr/share/keyrings/mongodb-server-7.0.gpg --dearmor
   ```

2. **Add MongoDB Repository**:
   ```bash
   # Ubuntu 22.04 (Jammy)
   echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-7.0.gpg ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/7.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list
   
   # Ubuntu 20.04 (Focal)
   echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-7.0.gpg ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/7.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list
   ```

3. **Install MongoDB**:
   ```bash
   sudo apt update
   sudo apt install -y mongodb-org
   ```

4. **Start and Enable MongoDB**:
   ```bash
   sudo systemctl start mongod
   sudo systemctl enable mongod
   sudo systemctl status mongod
   ```

5. **Test Connection**:
   ```bash
   mongosh
   ```

### Arch Linux Installation

1. **Install from Official Repository**:
   ```bash
   sudo pacman -S mongodb-bin mongodb-tools
   ```

2. **Alternative - AUR Installation**:
   ```bash
   # Using yay AUR helper
   yay -S mongodb-bin
   
   # Using paru AUR helper
   paru -S mongodb-bin
   ```

3. **Start MongoDB Service**:
   ```bash
   sudo systemctl start mongodb
   sudo systemctl enable mongodb
   sudo systemctl status mongodb
   ```

4. **Test Connection**:
   ```bash
   mongosh
   ```

### CentOS/RHEL Installation

1. **Create Repository File**:
   ```bash
   sudo tee /etc/yum.repos.d/mongodb-org-7.0.repo << EOF
   [mongodb-org-7.0]
   name=MongoDB Repository
   baseurl=https://repo.mongodb.org/yum/redhat/\$releasever/mongodb-org/7.0/x86_64/
   gpgcheck=1
   enabled=1
   gpgkey=https://pgp.mongodb.com/server-7.0.asc
   EOF
   ```

2. **Install MongoDB**:
   ```bash
   sudo yum install -y mongodb-org
   ```

3. **Start and Enable Service**:
   ```bash
   sudo systemctl start mongod
   sudo systemctl enable mongod
   sudo systemctl status mongod
   ```

## Option 3: MongoDB Atlas (Cloud Database)

### Step 1: Create Account

1. Go to [https://www.mongodb.com/atlas](https://www.mongodb.com/atlas)
2. Click "Try Free"
3. Sign up with email or Google/GitHub account
4. Verify your email address

### Step 2: Create Cluster

1. Choose "Build a Database"
2. Select "M0 Sandbox" (Free tier)
3. Choose a cloud provider and region
4. Name your cluster (e.g., "phishing-detector")
5. Click "Create"

### Step 3: Configure Access

1. **Database User**:
   - Username: `phishing_user`
   - Password: Generate secure password
   - Database User Privileges: "Read and write to any database"

2. **Network Access**:
   - Add IP Address: `0.0.0.0/0` (for development)
   - For production: Add specific IP addresses

### Step 4: Get Connection String

1. Click "Connect" on your cluster
2. Choose "Connect your application"
3. Select "Python" and version "3.6 or later"
4. Copy the connection string
5. Replace `<password>` with your database user password

## Configuration

### Environment Setup

Create or edit your `.env` file:

```env
# For Local MongoDB
MONGODB_URI=mongodb://localhost:27017/phishing_detector

# For MongoDB Atlas
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/phishing_detector

# Other settings
FLASK_SECRET_KEY=your_secret_key_here
USER_ENCRYPTION_SECRET=your_encryption_key_here
```

### Testing Your Setup

1. **Test MongoDB Connection**:
   ```python
   # Run this Python script to test
   import pymongo
   
   # For local MongoDB
   client = pymongo.MongoClient("mongodb://localhost:27017/")
   
   # For MongoDB Atlas
   # client = pymongo.MongoClient("your_atlas_connection_string")
   
   try:
       client.admin.command('ping')
       print("MongoDB connection successful!")
   except Exception as e:
       print(f"Connection failed: {e}")
   ```

2. **Test Application**:
   ```bash
   python main.py
   ```
   
   Check the startup logs for database connection status:
   - "Connected to MongoDB Atlas" - Atlas working
   - "Connected to local MongoDB" - Local MongoDB working
   - "Using local JSON storage" - Fallback mode

## Troubleshooting

### Common Issues

**Connection Refused (Local MongoDB)**:
```bash
# Check if MongoDB is running
sudo systemctl status mongod   # Linux
brew services list | grep mongodb   # macOS
net start MongoDB   # Windows

# Check port 27017
netstat -tlnp | grep 27017   # Linux/macOS
netstat -an | findstr 27017   # Windows
```

**Authentication Failed (MongoDB Atlas)**:
- Verify username and password
- Check network access whitelist
- Ensure connection string is correct

**Permission Denied**:
```bash
# Fix data directory permissions (Linux/macOS)
sudo chown -R mongodb:mongodb /var/lib/mongodb
sudo chown -R mongodb:mongodb /var/log/mongodb
```

**Port Already in Use**:
```bash
# Find process using port 27017
sudo lsof -i :27017   # Linux/macOS
netstat -ano | findstr :27017   # Windows

# Kill process if needed
sudo kill -9 <PID>   # Linux/macOS
```

### MongoDB Commands

**Basic Operations**:
```javascript
// Connect to database
use phishing_detector

// Show collections
show collections

// Find documents
db.users.find()
db.detection_logs.find().limit(5)

// Database stats
db.stats()

// Exit
exit
```

**Maintenance**:
```bash
# Backup database
mongodump --db phishing_detector --out /backup/

# Restore database
mongorestore --db phishing_detector /backup/phishing_detector/

# Check database size
du -sh /var/lib/mongodb   # Linux
```

## Security Best Practices

### Local MongoDB

1. **Enable Authentication**:
   ```javascript
   // In mongo shell
   use admin
   db.createUser({
     user: "admin",
     pwd: "securePassword",
     roles: ["userAdminAnyDatabase"]
   })
   ```

2. **Configure mongod.conf**:
   ```yaml
   # /etc/mongod.conf
   security:
     authorization: enabled
   
   net:
     bindIp: 127.0.0.1
     port: 27017
   ```

3. **Restart MongoDB**:
   ```bash
   sudo systemctl restart mongod
   ```

### MongoDB Atlas

- Use strong passwords
- Limit IP access to specific addresses
- Enable database auditing
- Regular backup verification
- Monitor access logs

## Performance Optimization

### Local MongoDB

1. **Configure Memory**:
   ```yaml
   # mongod.conf
   storage:
     wiredTiger:
       engineConfig:
         cacheSizeGB: 2
   ```

2. **Enable Journaling**:
   ```yaml
   storage:
     journal:
       enabled: true
   ```

### Application Level

1. **Connection Pooling** (already configured):
   ```python
   client = MongoClient(
       uri,
       maxPoolSize=50,
       minPoolSize=5
   )
   ```

2. **Index Creation** (automatic):
   ```python
   # Indexes created automatically by the application
   collection.create_index("user_id")
   collection.create_index("timestamp")
   ```

## Switching Between Database Types

The application automatically detects and uses the best available option:

1. **Disable MongoDB**: Comment out `MONGODB_URI` in `.env`
2. **Enable Local MongoDB**: Set `MONGODB_URI=mongodb://localhost:27017/phishing_detector`
3. **Enable Atlas**: Set `MONGODB_URI=mongodb+srv://...` with your Atlas string

No code changes required - the application handles all switching automatically.

---

For additional support, refer to:
- [MongoDB Official Documentation](https://docs.mongodb.com/)
- [MongoDB Atlas Documentation](https://docs.atlas.mongodb.com/)
- [PyMongo Documentation](https://pymongo.readthedocs.io/)