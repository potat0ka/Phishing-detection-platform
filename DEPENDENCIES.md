# Dependencies Documentation

## Python Dependencies

This project uses `pyproject.toml` for dependency management. All required packages are automatically installed when you run the setup command.

### Core Dependencies

#### Web Framework
- **Flask 3.1.1+**: Main web framework for the application
- **Werkzeug 3.1.3+**: WSGI utilities and security functions
- **Gunicorn 23.0.0+**: Production WSGI HTTP server

#### Database & Storage
- **PyMongo 4.13.0+**: MongoDB driver for Python
- **Motor 3.7.1+**: Asynchronous MongoDB driver
- **Flask-PyMongo 3.0.1+**: Flask extension for MongoDB
- **Flask-SQLAlchemy 3.1.1+**: SQL toolkit and ORM
- **SQLAlchemy 2.0.41+**: Python SQL toolkit
- **psycopg2-binary 2.9.10+**: PostgreSQL adapter
- **dnspython 2.7.0+**: DNS toolkit for MongoDB connections
- **bson 0.5.10+**: BSON encoding and decoding

#### Machine Learning & AI
- **scikit-learn 1.6.1+**: Machine learning library
- **NumPy 2.2.6+**: Numerical computing
- **NLTK 3.9.1+**: Natural language processing
- **TensorFlow 2.14.0+**: Deep learning framework
- **OpenCV-Python 4.11.0+**: Computer vision library
- **Pillow 11.2.1+**: Image processing library

#### Security & Authentication
- **cryptography 45.0.3+**: Cryptographic recipes and primitives
- **PyJWT 2.10.1+**: JSON Web Token implementation
- **Flask-Login 0.6.3+**: User session management
- **Flask-Dance 7.1.0+**: OAuth integration
- **oauthlib 3.2.2+**: OAuth request-signing logic

#### External Services
- **SendGrid 6.12.3+**: Email delivery service
- **Anthropic 0.52.2+**: AI API client
- **requests 2.32.3+**: HTTP library

#### Content Processing
- **BeautifulSoup4 4.13.4+**: HTML/XML parsing
- **trafilatura 2.0.0+**: Web content extraction
- **email-validator 2.2.0+**: Email address validation

## Installation Methods

### Method 1: Using pyproject.toml (Recommended)
```bash
# Install in development mode
pip install -e .

# Or install normally
pip install .
```

### Method 2: Direct pip install
```bash
# Install specific packages if needed
pip install flask pymongo scikit-learn opencv-python
```

### Method 3: Using requirements.txt equivalent
If you need a traditional requirements.txt file, you can generate one:
```bash
# Generate requirements from pyproject.toml
pip freeze > requirements.txt
```

## Development Dependencies

For development and testing, you may also want:
```bash
pip install pytest black flake8 mypy
```

## System Requirements

- **Python**: 3.11 or higher
- **Operating System**: Windows, macOS, or Linux
- **Memory**: 2GB RAM minimum, 4GB recommended
- **Storage**: 500MB free space
- **Network**: Internet connection for external API services

## Optional Dependencies

### MongoDB (Recommended)
```bash
# Ubuntu/Debian
sudo apt install mongodb

# macOS
brew install mongodb/brew/mongodb-community

# Windows
# Download from mongodb.com
```

### PostgreSQL (Alternative Database)
```bash
# Ubuntu/Debian
sudo apt install postgresql postgresql-contrib

# macOS
brew install postgresql

# Windows
# Download from postgresql.org
```

## Dependency Management

### Adding New Dependencies
To add a new dependency, edit `pyproject.toml`:
```toml
[project]
dependencies = [
    "new-package>=1.0.0",
    # ... existing dependencies
]
```

### Version Pinning
Dependencies use minimum version constraints (>=) to ensure compatibility while allowing updates for security patches.

### Security Updates
Regularly update dependencies for security:
```bash
pip install --upgrade -e .
```

## Platform-Specific Notes

### Windows
- Some packages may require Visual Studio Build Tools
- Use `pip install --user` if permission issues occur

### macOS
- May require Xcode Command Line Tools
- Use Homebrew for system dependencies

### Linux
- Install system packages before Python packages
- Use virtual environments to avoid conflicts

## Troubleshooting

### Common Issues

1. **Import Errors**
   ```bash
   pip install --force-reinstall -e .
   ```

2. **Version Conflicts**
   ```bash
   pip install --upgrade pip setuptools wheel
   ```

3. **Permission Denied**
   ```bash
   pip install --user -e .
   ```

4. **MongoDB Connection Issues**
   - Ensure MongoDB service is running
   - Check connection string in environment variables
   - Application will fallback to JSON storage automatically

### Environment Isolation
Always use virtual environments:
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
pip install -e .
```

## Production Considerations

### Performance
- Use `gunicorn` for production deployment
- Configure worker processes based on CPU cores
- Enable gzip compression for static files

### Security
- Pin exact versions for production: `pip freeze > requirements-prod.txt`
- Regularly scan for vulnerabilities: `pip audit`
- Use environment variables for sensitive configuration

### Monitoring
Consider adding monitoring dependencies:
- `prometheus-client`: Metrics collection
- `sentry-sdk`: Error tracking
- `APScheduler`: Task scheduling

This dependency management ensures a robust, secure, and maintainable application suitable for both educational and production use.