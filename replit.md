# replit.md

## Overview

This is an AI-powered phishing detection platform built with Flask and MongoDB. The application provides real-time phishing detection for URLs, emails, and text messages using machine learning algorithms. It features a comprehensive role-based access control system with three user levels (user, admin, superadmin) and includes advanced text analysis capabilities for detecting AI-generated content and plagiarism.

## User Preferences

Preferred communication style: Simple, everyday language.
Platform positioning: Custom-built cybersecurity platform by Bigendra Shrestha without external development assistance.

## Recent System Updates

### July 28, 2025 - File Upload Feature Restored
- Fixed text authenticity analysis file upload functionality 
- Resolved backend import error that was preventing file processing
- Enhanced JavaScript file handling with better user feedback
- Added console logging for debugging file upload issues
- File upload now fully operational for .txt, .pdf, .docx, and image files
- Users can click upload area or drag files for analysis

### July 29, 2025 - Complete Codebase Cleanup and Optimization
- Successfully completed comprehensive codebase cleanup and optimization removing 115+ LSP errors
- Eliminated all duplicate database modules by consolidating MongoDB operations into services/mongo_service.py
- Fixed all import dependencies and removed references to deleted database.py module throughout the application
- Performed extensive file cleanup removing unused backup files, duplicates, and cache directories
- Consolidated all model database operations to use unified mongo_service instead of duplicate db references
- Resolved JavaScript const redeclaration errors and variable naming conflicts across all frontend modules
- Optimized project structure maintaining clean organization: /routes (6 files), /services (2 files), /models (6 files), /templates (24 files), /static/js (9 files)
- Enhanced error handling and logging consistency across all Python modules
- Application now runs without any LSP diagnostics or import errors
- Text Analysis properly implemented as default tab in analyze-media page focusing on AI detection and plagiarism analysis
- Homepage maintains Quick Phishing Check form with navigation buttons to advanced analysis features
- All MongoDB connection fallbacks properly implemented using mongo_service.is_connected() method
- Removed redundant database connection methods and unified all database operations

### July 28, 2025 - Interactive Upload Progress System
- Implemented colorful, animated progress bar with real-time status updates
- Added encouraging progress messages with dynamic icons and color changes
- Created smooth animations for upload states (progress, success, error)
- Enhanced user experience with file size formatting and type detection
- Added visual feedback with border color changes and background animations
- Progress bar changes colors from blue → info → warning → success during upload

## System Architecture

### Backend Architecture
- **Framework**: Flask web framework with Blueprint-based modular routing
- **Database**: MongoDB Atlas with PyMongo for database operations
- **Authentication**: Flask-Login with bcrypt password hashing
- **Session Management**: Flask sessions with configurable timeout
- **File Storage**: Local file system with configurable upload limits

### Frontend Architecture
- **Template Engine**: Jinja2 templates with Bootstrap 5 for UI components
- **Styling**: Custom CSS with dark theme support and animated components
- **JavaScript**: Modular ES6 architecture with separate modules for different features
- **Icons**: Font Awesome and Bootstrap Icons for consistent iconography

### Security Architecture
- **RBAC System**: Three-tier role system (user/admin/superadmin) with granular permissions
- **Password Security**: bcrypt hashing with salt for all user passwords
- **Session Security**: HTTP-only cookies with CSRF protection
- **Input Validation**: Server-side validation for all user inputs

## Key Components

### Models Layer
- **UserModel**: Handles user authentication, registration, and account management
- **PhishingModel**: Manages phishing threat data and detection results
- **SafetyTipsModel**: Stores and manages cybersecurity educational content
- **ScanHistoryModel**: Tracks user scan history and analytics
- **RBACModel**: Implements role-based access control and permission management
- **AnalyticsModel**: Provides system statistics and usage metrics

### Route Blueprints
- **main_routes**: Public routes (homepage, detection, tips)
- **auth_routes**: Authentication routes (login, register, logout)
- **admin_routes**: Admin dashboard and management functions
- **rbac_routes**: Role-based access control and user management
- **dashboard_routes**: User-specific dashboard functionality

### Utility Services
- **PhishingDetector**: Core ML detection engine for threat analysis
- **TextAnalysisService**: AI content detection and plagiarism checking
- **MultimediaAnalyzer**: Analysis for images, videos, and audio files
- **ValidationUtils**: Input validation and sanitization functions

## Data Flow

### Detection Process
1. User submits content (URL, email, or text) through web interface
2. Content validation and sanitization performed
3. ML detection engine analyzes content using trained models
4. Threat level and confidence score calculated
5. Results stored in scan history (if user authenticated)
6. Formatted results returned to user with explanations

### User Management Flow
1. User registration with bcrypt password hashing
2. Role assignment (default: user, admin/superadmin via creation)
3. Session management with automatic timeout
4. Password reset requests require admin approval
5. Activity logging for admin actions

### Content Management Flow
1. Admins can manage safety tips categorized by type
2. Superadmins can upload ML models and manage all users
3. System maintains audit logs for all administrative actions
4. Content versioning for safety tips and system updates

## External Dependencies

### Required Python Packages
- **Flask**: Web framework and routing
- **PyMongo**: MongoDB database connectivity
- **Flask-Login**: User session management
- **bcrypt**: Password hashing and verification
- **scikit-learn**: Machine learning models (optional)
- **NLTK**: Natural language processing (optional)
- **Werkzeug**: File handling and security utilities

### Frontend Dependencies
- **Bootstrap 5**: UI framework and responsive design
- **Font Awesome**: Icon library for consistent UI
- **Chart.js**: Data visualization for analytics dashboard
- **Animate.css**: CSS animations for enhanced UX

### External Services
- **MongoDB Atlas**: Cloud database hosting with connection string
- **Text Analysis APIs**: External services for advanced content analysis (optional)

## Deployment Strategy

### Environment Configuration
- Configuration managed through environment variables
- Support for development, staging, and production environments
- Database connection strings configurable via MONGO_URI
- Secret keys and sensitive data stored in environment variables

### Database Setup
- MongoDB collections created automatically on first run
- Default test users initialized with proper role assignments
- Safety tips and system data seeded from JSON files
- Database connection fallback to file-based storage if MongoDB unavailable

### Production Considerations
- Debug mode disabled in production environment
- HTTPS required for secure cookie transmission
- File upload limits enforced (16MB default)
- Session timeout configured for security
- Comprehensive error logging and monitoring

### Scalability Features
- Modular architecture supports horizontal scaling
- Database operations optimized with proper indexing
- Static file serving can be offloaded to CDN
- Caching strategies implemented for frequent queries
- Role-based access control supports large user bases

The application is designed to be easily deployable on cloud platforms like Replit, Heroku, or AWS with minimal configuration changes. The modular architecture ensures maintainability and allows for easy feature additions or modifications.