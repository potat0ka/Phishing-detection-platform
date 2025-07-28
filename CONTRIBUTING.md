# Contributing to AI Phishing Detection Platform

Thank you for your interest in contributing to the AI Phishing Detection Platform! This document provides guidelines for contributing to the project.

## Code of Conduct

This project follows a simple code of conduct:
- Be respectful and professional in all interactions
- Focus on constructive feedback and collaboration
- Maintain the security-first approach of the platform

## How to Contribute

### 1. Setting Up Development Environment

1. **Fork and Clone**
   ```bash
   git clone https://github.com/your-username/ai-phishing-detection-platform.git
   cd ai-phishing-detection-platform
   ```

2. **Install Dependencies**
   ```bash
   python install_dependencies.py
   # OR manually:
   source venv/bin/activate  # Unix/macOS
   # venv\Scripts\activate   # Windows
   ```

3. **Configure Environment**
   ```bash
   cp .env.template .env
   # Edit .env with your settings
   ```

### 2. Making Changes

1. **Create Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Follow Code Standards**
   - Python: PEP 8 compliance
   - JavaScript: ES6+ modules
   - HTML: Semantic HTML5
   - CSS: BEM methodology preferred

3. **Test Your Changes**
   ```bash
   python main.py
   # Verify functionality at http://localhost:8080
   ```

### 3. Code Style Guidelines

#### Python Code
```python
# Use descriptive function names
def validate_phishing_url(url: str) -> dict:
    """
    Validate if a URL is potentially malicious.
    
    Args:
        url (str): The URL to analyze
        
    Returns:
        dict: Analysis results with confidence score
    """
    pass

# Use type hints where possible
# Follow PEP 8 formatting
# Add comprehensive docstrings
```

#### JavaScript Code
```javascript
// Use ES6+ features
class PhishingAnalyzer {
    constructor(options = {}) {
        this.options = { ...defaults, ...options };
    }
    
    async analyzeContent(content) {
        // Use async/await for promises
        try {
            const result = await this.processContent(content);
            return result;
        } catch (error) {
            console.error('Analysis failed:', error);
            throw error;
        }
    }
}

// Export modules properly
export { PhishingAnalyzer };
```

### 4. Security Considerations

- **Never commit API keys or secrets**
- **Validate all user inputs**
- **Use parameterized queries for database operations**
- **Follow OWASP security guidelines**
- **Test security features thoroughly**

### 5. Submission Process

1. **Commit Changes**
   ```bash
   git add .
   git commit -m "feat: add new phishing detection algorithm
   
   - Implemented advanced URL pattern recognition
   - Added support for internationalized domain names
   - Improved detection accuracy by 15%
   - Updated documentation and tests"
   ```

2. **Push to Fork**
   ```bash
   git push origin feature/your-feature-name
   ```

3. **Create Pull Request**
   - Provide clear description of changes
   - Link any related issues
   - Include screenshots if UI changes
   - Ensure all tests pass

## Types of Contributions

### 🐛 Bug Fixes
- Fix existing functionality issues
- Improve error handling
- Security vulnerability patches

### ✨ New Features
- AI/ML algorithm improvements
- New detection methods
- UI/UX enhancements
- API endpoints

### 📚 Documentation
- README updates
- Code comments
- API documentation
- User guides

### 🧪 Testing
- Unit tests
- Integration tests
- Security tests
- Performance tests

## Project Structure

```
├── app.py                 # Main Flask application
├── routes/                # Blueprint route handlers
├── models/                # Database models
├── utils/                 # Utility functions
├── templates/             # Jinja2 templates
├── static/                # CSS, JS, images
├── data/                  # Local database fallback
├── tests/                 # Test files
└── docs/                  # Documentation
```

## Reporting Issues

### Bug Reports
Include:
- Python version and OS
- Steps to reproduce
- Expected vs actual behavior
- Error messages/screenshots
- Browser information (if web-related)

### Feature Requests
Include:
- Clear description of feature
- Use case/problem it solves
- Implementation suggestions
- Compatibility considerations

## Review Process

1. **Automated Checks**
   - Code style validation
   - Security scanning
   - Test execution

2. **Manual Review**
   - Code quality assessment
   - Security review
   - Documentation check
   - Testing verification

3. **Approval and Merge**
   - Maintainer approval required
   - Squash and merge preferred
   - Update changelog

## Development Tips

### Database Development
- Use the local JSON fallback for development
- Test with both MongoDB and fallback systems
- Maintain data consistency

### Frontend Development
- Test on multiple browsers
- Ensure mobile responsiveness
- Maintain accessibility standards

### AI/ML Development
- Document algorithm changes
- Test with various input types
- Consider performance impact

## Getting Help

- **Documentation**: Check README.md and code comments
- **Issues**: Search existing issues before creating new ones
- **Security**: Report security issues privately

## Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes for significant contributions
- Project documentation

---

By contributing to this project, you agree that your contributions will be licensed under the same license as the project (MIT License).

Thank you for helping make the internet safer! 🛡️