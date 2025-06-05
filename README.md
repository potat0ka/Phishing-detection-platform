# AI Phishing Detection Platform

A comprehensive AI-powered phishing detection platform that leverages cutting-edge machine learning technologies to provide digital threat protection and security analysis.

## 🚀 Features

- **Multi-Modal Detection**: Analyzes URLs, emails, messages, images, videos, audio, and documents
- **AI Content Detection**: Identifies AI-generated content across multiple formats
- **Real-Time Threat Intelligence**: Updates phishing databases automatically
- **Role-Based Access Control**: Super Admin, Sub Admin, and Regular User roles
- **Interactive Learning**: Educational features to understand AI detection
- **Professional Dashboard**: Comprehensive admin interface with analytics
- **Security First**: End-to-end encryption for sensitive user data
- **Responsive Design**: Modern UI/UX with Bootstrap 5 dark theme

## 🛠 Technology Stack

- **Backend**: Python Flask with SQLAlchemy
- **Database**: PostgreSQL with JSON fallback
- **Frontend**: Bootstrap 5, Chart.js, Font Awesome
- **Security**: AES-256 encryption, secure session management
- **AI/ML**: Custom detection algorithms with explainable AI features
- **Deployment**: Replit-ready with Docker support

## 📋 Prerequisites

- Python 3.11 or higher
- PostgreSQL (optional - uses JSON fallback)
- 2GB RAM minimum
- Modern web browser

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd ai-phishing-detection-platform
```

### 2. Install Dependencies

```bash
# Install Python dependencies
pip install -r requirements.txt
```

### 3. Environment Setup

Create a `.env` file based on `.env.example`:

```bash
cp .env.example .env
```

Configure your environment variables:

```env
# Required
SESSION_SECRET=your-session-secret-key-here
USER_ENCRYPTION_SECRET=your-encryption-key-here

# Optional - PostgreSQL (uses JSON fallback if not provided)
DATABASE_URL=postgresql://username:password@localhost:5432/phishing_db

# Optional - External Services
SENDGRID_API_KEY=your-sendgrid-key
ANTHROPIC_API_KEY=your-anthropic-key
```

### 4. Database Setup

#### Option A: PostgreSQL (Recommended)
```bash
# Create database
createdb phishing_db

# The application will automatically create tables on first run
```

#### Option B: JSON Fallback (Default)
No additional setup required. The application will create JSON files automatically.

### 5. Run the Application

```bash
python main.py
```

The application will be available at `http://localhost:5000`

## 👥 User Management

### Initial Admin Setup

1. Register the first user through the web interface
2. Manually promote to Super Admin by editing `data/users.json`:

```json
{
  "role": "super_admin",
  "username": "your-username"
}
```

### Role Hierarchy

- **Super Admin**: Full system access, can manage all users and settings
- **Sub Admin**: User management only, cannot promote/demote other admins
- **Regular User**: Basic phishing detection features

### Admin Functions

- User creation and management
- System analytics and monitoring
- Safety tips management
- Phishing database updates
- Security settings configuration

## 🔧 Configuration

### Security Settings

The platform uses AES-256 encryption for sensitive data. Configure encryption keys in your environment:

```env
USER_ENCRYPTION_SECRET=your-32-character-encryption-key
```

### Database Configuration

#### PostgreSQL Setup
```bash
# Install PostgreSQL
sudo apt-get install postgresql postgresql-contrib

# Create user and database
sudo -u postgres psql
CREATE USER phishing_user WITH PASSWORD 'your_password';
CREATE DATABASE phishing_db OWNER phishing_user;
GRANT ALL PRIVILEGES ON DATABASE phishing_db TO phishing_user;
```

#### JSON Fallback
The system automatically falls back to JSON file storage if PostgreSQL is unavailable. Data is stored in the `data/` directory.

## 📁 Project Structure

```
├── app.py                     # Flask application configuration
├── main.py                    # Application entry point
├── routes.py                  # Main application routes
├── admin_routes.py            # Admin-specific routes
├── auth_routes.py             # Authentication routes
├── models/
│   ├── simple_models.py       # Data models
│   └── mongodb_config.py      # Database configuration
├── utils/
│   ├── encryption_utils.py    # Data encryption utilities
│   ├── threat_intelligence.py # Threat detection logic
│   └── ai_content_detector.py # AI content analysis
├── templates/                 # HTML templates
├── static/                    # CSS, JS, and images
├── data/                      # JSON database files (fallback)
└── requirements.txt           # Python dependencies
```

## 🔒 Security Features

### Data Protection
- AES-256 encryption for sensitive user data
- Secure session management
- Password hashing with Werkzeug
- Input validation and sanitization

### Access Control
- Role-based permissions
- Session timeout management
- Admin action logging
- Secure file upload handling

## 🎯 Usage Guide

### For Regular Users

1. **Register/Login**: Create account or sign in
2. **Check Content**: Upload files or enter URLs/text for analysis
3. **View Results**: Get detailed threat analysis with explanations
4. **Safety Tips**: Learn about phishing protection
5. **History**: Track your detection history

### For Administrators

1. **Dashboard**: Monitor system statistics and user activity
2. **User Management**: Create, edit, and manage user accounts
3. **Content Moderation**: Review reported content
4. **System Settings**: Configure security and detection parameters
5. **Data Export**: Export user data and detection logs

## 🚀 Deployment

### Replit Deployment (Recommended)

1. Import project to Replit
2. Configure environment variables in Secrets
3. Click "Run" to start the application
4. Use Replit's deployment feature for production

### Manual Deployment

```bash
# Install production server
pip install gunicorn

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Docker Deployment

```bash
# Build image
docker build -t phishing-detector .

# Run container
docker run -p 5000:5000 phishing-detector
```

## 🔍 API Endpoints

### Authentication
- `POST /register` - User registration
- `POST /login` - User login
- `GET /logout` - User logout

### Detection
- `POST /check` - Analyze content for threats
- `GET /detection-details/<id>` - Get detection details
- `DELETE /delete-detection/<id>` - Delete detection record

### Admin
- `GET /admin/` - Admin dashboard
- `POST /admin/create-user` - Create new user
- `GET /admin/export-users` - Export user data

## 🐛 Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Check PostgreSQL is running
   - Verify DATABASE_URL in environment
   - Application will fallback to JSON storage

2. **Permission Denied**
   - Ensure proper file permissions
   - Check user roles are configured correctly

3. **Import Errors**
   - Install all requirements: `pip install -r requirements.txt`
   - Check Python version compatibility

4. **Session Issues**
   - Set SESSION_SECRET in environment
   - Clear browser cookies and restart

### Debug Mode

Enable debug mode for development:

```python
# In main.py
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
```

## 📚 Learning Resources

### For Beginners

This platform is designed as an educational tool. Key learning areas:

1. **Web Development**: Flask framework, HTML/CSS/JavaScript
2. **Database Management**: PostgreSQL, SQLAlchemy ORM
3. **Security**: Encryption, authentication, secure coding
4. **Machine Learning**: AI detection algorithms, data analysis
5. **DevOps**: Deployment, monitoring, maintenance

### Code Comments

The codebase includes extensive comments explaining:
- Function purposes and parameters
- Security considerations
- Algorithm explanations
- Database relationships
- Frontend interactions

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/new-feature`
3. Commit changes: `git commit -am 'Add new feature'`
4. Push branch: `git push origin feature/new-feature`
5. Submit pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author

**Bigendra Shrestha**
- Final Semester Project
- AI Phishing Detection Platform
- Educational Purpose

## 🆘 Support

For support and questions:
1. Check the troubleshooting section
2. Review code comments for implementation details
3. Create an issue in the repository
4. Contact project maintainer

---

**Note**: This platform is designed for educational purposes and security research. Always follow responsible disclosure practices when dealing with security vulnerabilities.