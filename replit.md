# AI Phishing Detection Platform

## Overview

This is a comprehensive cybersecurity platform built with Flask and MongoDB that uses artificial intelligence and machine learning to detect phishing URLs, emails, and malicious content. The system includes user authentication, role-based access control, real-time threat detection, and educational resources for cybersecurity learning.

**Latest Update (July 27, 2025):** **PRODUCTION-READY INSTALLATION & DOCUMENTATION SYSTEM COMPLETED** - Successfully created comprehensive installation ecosystem including automated install_dependencies.py with cross-platform support, virtual environment management, and dependency verification. Added requirements-manual.txt, INSTALL.md quick setup guide, detailed .env.template with API configuration, setup.py for advanced installation, CONTRIBUTING.md development guidelines, and GIT_SETUP.md for repository management. Enhanced README.md with professional documentation, architecture diagrams, and deployment guides. Created security-focused .gitignore and resolved git repository conflicts. Application now fully production-ready with multiple installation methods and complete documentation for developers and users.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Backend Architecture
- **Framework**: Flask web framework with clean modular Blueprint structure
- **Organization**: Structured folders (app.py, routes/, models/, templates/, static/, utils/, config.py)
- **Routing**: Blueprint pattern with main_routes, auth_routes, and admin_routes for separation of concerns
- **Database**: MongoDB with PyMongo/Flask-PyMongo through dedicated model classes (intelligent PostgreSQL fallback)
- **Authentication**: Session-based authentication with bcrypt password hashing
- **Security**: AES-256 encryption for sensitive user data, CSRF protection, secure file uploads

### Frontend Architecture
- **UI Framework**: Bootstrap 5 with dark theme support (Replit theme)
- **JavaScript**: Modular ES6+ architecture with separate managers for different concerns
- **Icons**: Font Awesome 6.4.0 and Bootstrap Icons for comprehensive iconography
- **Animations**: Custom CSS animations with mascot loading system for enhanced UX
- **Charts**: Chart.js for analytics visualizations

### AI/ML Components
- **Detection Engine**: Custom PhishingDetector class using scikit-learn and NLTK
- **Content Analysis**: AI content detection for images and documents
- **Explainable AI**: Educational system that explains detection decisions
- **Threat Intelligence**: Offline threat intelligence system with pattern matching

## Key Components

### 1. Authentication System (`auth_routes.py`)
- User registration with email validation and password strength requirements
- Secure login/logout with session management
- Role-based access control (Super Admin, Sub Admin, Regular User)
- Password recovery functionality
- Account lockout protection against brute force attacks

### 2. AI Detection Engine (`ml_detector.py`)
- Multi-layered phishing detection using ML algorithms
- URL pattern analysis with suspicious keyword detection
- Email content analysis with natural language processing
- Real-time threat scoring with confidence metrics
- Integration with offline threat intelligence databases

### 3. Admin Dashboard (`admin_routes.py`)
- Comprehensive user management (create, edit, deactivate users)
- System monitoring with live analytics and statistics
- Content moderation for reported phishing attempts
- Security tips management with categorization
- ML model configuration and training history

### 4. Data Encryption (`encryption_utils.py`)
- AES-256 encryption for sensitive user data
- Secure key derivation using PBKDF2
- Graceful fallback to basic encryption if cryptography package unavailable
- Comprehensive data protection for privacy compliance

### 5. MongoDB Data Management (`mongodb_manager.py` & `data_sync_models.py`) - **NEW July 25, 2025**
- Complete MongoDB integration with PyMongo/Flask-PyMongo
- Real-time data synchronization between admin dashboard and all website pages
- Collections: phishing_data, security_tips, scan_logs, system_stats, users
- Intelligent fallback system with sample data when MongoDB connection fails
- Dashboard write operations immediately reflect across landing page, analytics, reports, and tips

### 6. Admin Dashboard (`admin_dashboard_routes.py`) - **NEW July 25, 2025**
- Comprehensive admin interface for managing phishing data and security tips
- Add/Edit/Delete operations for phishing URLs, categories, status, descriptions
- All dashboard changes instantly appear across website pages via MongoDB
- Real-time statistics and system monitoring
- API endpoints for dynamic dashboard updates

### 7. Role-Based Access Control System (`rbac_routes.py`, `rbac_decorators.py`, `rbac_model.py`) - **NEW July 26, 2025**
- Complete RBAC implementation with three-tier user hierarchy (User, Admin, Superadmin)
- Comprehensive permission system with 15+ granular permissions (run_scans, manage_users, upload_models, etc.)
- Role-based route protection using Flask decorators (@login_required, @role_required, @permission_required)
- Password reset approval workflow where admins can approve user password reset requests
- Secure model upload system with role restrictions and activation controls
- Hierarchical user management where superadmins manage all, admins manage users only
- Template controls that dynamically show/hide features based on current user's role and permissions
- MongoDB integration with intelligent file storage fallback for maximum reliability
- Flask compatibility fixes and comprehensive error handling
- Complete test suite validating all permissions and user management scenarios

### 8. Enhanced Authentication System (`auth_routes.py`, `user_model.py`) - **UPDATED July 26, 2025**
- Session-based authentication with comprehensive role management
- User registration, login, logout with role assignment (user, admin, superadmin)
- RBAC decorators protecting all sensitive routes and admin functionality
- Session management with secure user tracking and role-based redirects
- Login attempt logging and advanced security features with role-based access controls

## Data Flow

### 1. User Authentication Flow
1. User submits credentials via login form
2. Server validates against encrypted user database
3. Session created with secure token generation
4. Role-based permissions applied for route access
5. Activity logged for security auditing

### 2. Phishing Detection Flow
1. User submits URL/email/message for analysis
2. Content preprocessed and normalized
3. Multiple AI models analyze different aspects
4. Threat intelligence databases consulted
5. Confidence score calculated and result returned
6. Educational explanation generated for user learning

### 3. Admin Management Flow
1. Admin accesses protected dashboard routes
2. Real-time statistics pulled from database
3. User management operations encrypted and logged
4. Content moderation updates threat databases
5. System changes propagated to all users

## External Dependencies

### Required Python Packages
- **Flask**: Web framework and routing
- **PyMongo**: MongoDB database driver for real-time data synchronization
- **Flask-PyMongo**: Flask extension for MongoDB integration
- **Werkzeug**: Security utilities for password hashing
- **scikit-learn**: Machine learning algorithms
- **NLTK**: Natural language processing
- **Pillow**: Image processing for AI content detection
- **cryptography**: Advanced encryption utilities
- **requests**: HTTP client for threat intelligence APIs

### Optional Integrations
- **MongoDB Atlas**: Cloud database for production (configured with MONGO_URI)
- **Threat Intelligence APIs**: VirusTotal, URLVoid, PhishTank (optional)
- **SMTP Server**: Email notifications (configurable)

### Frontend Dependencies
- **Bootstrap 5**: UI framework with dark theme
- **Font Awesome 6.4.0**: Icon library
- **Chart.js**: Data visualization
- **Animate.css**: CSS animations

## Deployment Strategy

### Development Environment
- Local development server on port 8080
- JSON file storage for immediate functionality
- Debug mode enabled with detailed error messages
- Hot reloading for rapid development iteration

### Production Deployment Options
1. **Replit Deployment** (Recommended for testing)
   - One-click deployment with environment variables
   - Automatic HTTPS and domain configuration
   - Integrated database and file storage

2. **Cloud Platform Deployment** (Heroku, AWS, Google Cloud)
   - MongoDB Atlas for production database
   - Environment-based configuration
   - Gunicorn WSGI server with Nginx reverse proxy
   - SSL/TLS termination and security headers

3. **VPS/Self-Hosted Deployment**
   - Docker containerization support
   - systemd service configuration
   - Backup and monitoring setup
   - Firewall and security hardening

### Security Configuration
- Strong secret keys for session management
- HTTPS enforcement in production
- Database authentication and encryption
- File upload restrictions and validation
- Rate limiting and DDoS protection
- Comprehensive audit logging

### Performance Optimization
- Database connection pooling
- Static file caching with CDN support
- Gzip compression for responses
- Lazy loading for large datasets
- Background processing for intensive AI operations