# AI Phishing Detection Platform

An advanced AI-powered phishing detection platform that combines cutting-edge machine learning technologies with user-friendly security analysis and educational insights.

## Features

### Core Detection Capabilities
- **URL Analysis**: Real-time phishing URL detection with threat intelligence
- **Email Content Analysis**: Advanced email phishing detection with pattern recognition
- **Message Analysis**: General text message phishing detection
- **AI Content Detection**: Identify AI-generated content and deepfakes
- **Explainable AI**: Detailed explanations of detection results

### User Management
- **Role-Based Access Control**: Super Admin, Sub Admin, and Regular User roles
- **Secure Authentication**: Encrypted user data and session management
- **User Dashboard**: Personalized detection history and statistics

### Admin Features
- **User Management**: Create, edit, and manage user accounts
- **Analytics Dashboard**: Real-time system statistics and monitoring
- **ML Model Management**: Train and optimize detection models
- **Security Tips Management**: Educational content administration
- **Data Export**: CSV export functionality for users and detections

## Technology Stack

- **Backend**: Python Flask web framework
- **Database**: MongoDB Atlas with local JSON fallback
- **AI/ML**: TensorFlow, scikit-learn, NLTK
- **Frontend**: Bootstrap 5 with responsive design
- **Charts**: Chart.js for data visualization
- **Security**: Advanced encryption and secure session management

## Installation

### Prerequisites
- Python 3.8 or higher
- MongoDB Atlas account (optional - JSON fallback available)

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ai-phishing-detection-platform
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements-local.txt
   ```

3. **Environment Configuration**
   ```bash
   # Copy the example environment file
   cp .env.example .env
   
   # Edit .env with your configuration
   # Set MONGO_URI for MongoDB Atlas connection
   # Set USER_ENCRYPTION_SECRET for data encryption
   ```

4. **Run the application**
   ```bash
   python main.py
   ```

5. **Access the platform**
   - Open your browser to `http://localhost:8080`
   - Register a new account or use admin credentials

## Usage

### For Regular Users
1. **Registration**: Create an account with secure password
2. **Detection Tools**: Analyze URLs, emails, and messages for phishing
3. **Dashboard**: View detection history and personal statistics
4. **Security Tips**: Learn about phishing prevention

### For Administrators
1. **Admin Dashboard**: Access comprehensive system management
2. **User Management**: Create and manage user accounts
3. **ML Model Training**: Train and optimize detection algorithms
4. **Analytics**: Monitor platform usage and security metrics

## Configuration

### Database Configuration
- **MongoDB Atlas**: Set `MONGO_URI` in environment variables
- **Local Fallback**: Automatic JSON file storage if MongoDB unavailable

### Security Settings
- **Encryption**: Set `USER_ENCRYPTION_SECRET` for data protection
- **Session Management**: Automatic secure session handling
- **Password Policy**: Enforced strong password requirements

## API Endpoints

### Public Endpoints
- `GET /` - Home page
- `POST /auth/register` - User registration
- `POST /auth/login` - User login
- `GET /tips` - Security tips and education

### Protected Endpoints
- `GET /dashboard` - User dashboard
- `POST /check` - Phishing detection
- `GET /history` - Detection history

### Admin Endpoints
- `GET /admin` - Admin dashboard
- `POST /admin/users` - User management
- `POST /admin/train-model` - ML model training

## Security Features

- **Data Encryption**: All sensitive user data encrypted at rest
- **Secure Sessions**: Flask session management with CSRF protection
- **Role-Based Access**: Granular permission system
- **Input Validation**: Comprehensive input sanitization
- **Rate Limiting**: Protection against abuse and attacks

## ML Model Information

The platform uses ensemble learning combining:
- **Pattern Recognition**: Rule-based phishing indicators
- **Machine Learning**: TensorFlow neural networks
- **Natural Language Processing**: NLTK text analysis
- **Threat Intelligence**: Offline threat database

## Contributing

This project was developed by Bigendra Shrestha as a final semester project at Saraswati Multiple Campus (8th semester).

## License

Educational project - All rights reserved.

## Support

For technical support or questions, please contact the development team.

---

**Note**: This platform is designed for educational and research purposes. Always use multiple verification methods for critical security decisions.