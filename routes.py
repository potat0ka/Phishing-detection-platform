"""
Web Routes for AI Phishing Detection Platform
============================================

This file contains all the web routes (URLs) that users can visit.
Each function below handles a specific page or action on the website.

Routes included:
- / (home page)
- /register (user registration)
- /login (user login)
- /logout (user logout)
- /dashboard (user dashboard)
- /check (phishing detection)
- /tips (security tips)
- /api/quick-check (API endpoint)

Perfect for learning web development concepts!
"""

from flask import render_template, request, redirect, url_for, flash, session, jsonify
from app import app, allowed_file, ALLOWED_EXTENSIONS
from simple_models import User, Detection, PhishingTip
from ml_detector import PhishingDetector
from ai_content_detector import ai_detector
from utils import is_logged_in, login_required
from security_tips_updater import security_updater
from werkzeug.utils import secure_filename
import json
import os
import re
from urllib.parse import urlparse
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

# Initialize the AI/ML detector when the app starts
# This loads the machine learning model for phishing detection
detector = PhishingDetector()

def validate_input_content(content, input_type):
    """
    Validate input content based on type and provide helpful error messages
    
    Args:
        content (str): The content to validate
        input_type (str): Type of content ('url', 'email', 'message')
    
    Returns:
        str: Error message if validation fails, None if valid
    """
    content = content.strip()
    
    # Check minimum length
    if len(content) < 3:
        return "Please enter at least 3 characters to analyze."
    
    # Check maximum length (reasonable limits)
    if len(content) > 10000:
        return "Content is too long. Please enter less than 10,000 characters."
    
    if input_type == 'url':
        # Basic URL validation
        if not content.startswith(('http://', 'https://', 'www.', 'ftp://')):
            # Check if it looks like a domain without protocol
            if '.' in content and ' ' not in content:
                return None  # Allow domain-like strings
            return "Please enter a valid URL (e.g., https://example.com, www.example.com, or example.com)"
        
        # Check for valid URL structure
        try:
            parsed = urlparse(content if content.startswith(('http://', 'https://')) else 'http://' + content)
            if not parsed.netloc:
                return "Please enter a valid URL with a domain name."
        except:
            return "Please enter a valid URL format."
    
    elif input_type == 'email':
        # Basic email content validation (can be email text or headers)
        if '@' not in content and 'from:' not in content.lower() and 'subject:' not in content.lower():
            return "Please enter email content, headers, or at least include an email address with @ symbol."
        
        # Check for extremely short email content
        if len(content) < 10:
            return "Please enter more email content for better analysis (at least 10 characters)."
    
    elif input_type == 'message':
        # Basic message validation
        if len(content) < 5:
            return "Please enter at least 5 characters for message analysis."
        
        # Check if it's just numbers or special characters
        if content.replace(' ', '').isdigit():
            return "Please enter a text message rather than just numbers."
    
    # Check for suspicious test inputs
    test_patterns = ['test', 'asdf', 'qwerty', '123', 'aaa', 'bbb']
    if content.lower().strip() in test_patterns:
        return "Please enter real content for analysis rather than test text."
    
    return None  # No validation errors

@app.route('/')
def index():
    """Home page with phishing check form"""
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        if not all([username, email, password, confirm_password]):
            flash('All fields are required.', 'error')
            return render_template('register.html')
        
        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return render_template('register.html')
        
        if len(password) < 6:
            flash('Password must be at least 6 characters long.', 'error')
            return render_template('register.html')
        
        # Create new user
        user = User.create(username, email, password)
        
        if user_id:
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Username or email already exists.', 'error')
            return render_template('register.html')
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        if not username or not password:
            flash('Username and password are required.', 'error')
            return render_template('login.html')
        
        user = User.authenticate(username, password)
        
        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password.', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """User logout"""
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    """User dashboard with detection history"""
    user_id = session.get('user_id')
    
    # Get user's recent detections
    recent_detections = Detection.find_by_user(user_id, limit=10)
    
    # Get user statistics
    stats = Detection.get_user_stats(user_id)
    
    return render_template('dashboard.html', 
                         detections=recent_detections, 
                         stats=stats)

@app.route('/check', methods=['GET', 'POST'])
def check():
    """Phishing detection interface"""
    if request.method == 'POST':
        input_content = request.form.get('input_content', '').strip()
        input_type = request.form.get('input_type', 'url')
        
        if not input_content:
            flash('Please enter content to analyze.', 'error')
            return render_template('check.html')
        
        # Validate input based on type
        validation_error = validate_input_content(input_content, input_type)
        if validation_error:
            flash(validation_error, 'error')
            return render_template('check.html')
        
        try:
            # Perform phishing detection
            result = detector.analyze(input_content, input_type)
            
            # Save detection with encrypted user activity data
            if is_logged_in():
                try:
                    user_id = session.get('user_id')
                    user_ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.environ.get('REMOTE_ADDR'))
                    user_agent = request.headers.get('User-Agent')
                    
                    Detection.create_detection(
                        user_id=user_id,
                        input_type=input_type,
                        input_content=input_content,
                        result=result['classification'],
                        confidence_score=result['confidence'],
                        reasons=result['reasons'],
                        ai_analysis=result['ai_analysis'],
                        user_ip=user_ip,
                        user_agent=user_agent
                    )
                    logger.info(f"Encrypted detection saved for user: {user_id}")
                except Exception as save_error:
                    app.logger.error(f"Failed to save encrypted detection: {save_error}")
                    # Continue without saving - don't let this block the analysis
            
            return render_template('result.html', 
                                 result=result, 
                                 input_content=input_content,
                                 input_type=input_type)
        
        except Exception as e:
            app.logger.error(f"Detection error: {e}")
            flash('An error occurred during analysis. Please try again.', 'error')
            return render_template('check.html')
    
    return render_template('check.html')

@app.route('/tips')
def tips():
    """Educational tips about phishing prevention with latest threat intelligence"""
    # Update security tips with comprehensive content
    try:
        update_results = security_updater.update_security_tips_database()
        app.logger.info(f"Security tips updated: {update_results}")
    except Exception as e:
        app.logger.error(f"Error updating security tips: {e}")
    
    # Get tips organized by category
    email_tips = PhishingTip.find_by_category('email')
    url_tips = PhishingTip.find_by_category('url')
    general_tips = PhishingTip.find_by_category('general')
    
    # Get trending threats information
    trending_threats = security_updater.get_trending_threats()
    
    # Calculate statistics
    total_tips = len(email_tips) + len(url_tips) + len(general_tips)
    
    stats = {
        'total_tips': total_tips,
        'email_count': len(email_tips),
        'url_count': len(url_tips),
        'general_count': len(general_tips),
        'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M')
    }
    
    return render_template('tips.html', 
                         email_tips=email_tips,
                         url_tips=url_tips, 
                         general_tips=general_tips,
                         trending_threats=trending_threats,
                         stats=stats)

@app.route('/delete-detection/<detection_id>', methods=['DELETE'])
@login_required
def delete_detection(detection_id):
    """Delete a detection from user's history"""
    try:
        user_id = session.get('user_id')
        success = Detection.delete_detection(detection_id, user_id)
        
        if success:
            return jsonify({'success': True, 'message': 'Detection deleted successfully'})
        else:
            return jsonify({'success': False, 'error': 'Detection not found or access denied'}), 404
            
    except Exception as e:
        app.logger.error(f"Delete detection error: {e}")
        return jsonify({'success': False, 'error': 'Failed to delete detection'}), 500

@app.route('/api/quick-check', methods=['POST'])
def quick_check():
    """Quick API endpoint for checking content"""
    try:
        data = request.get_json()
        if not data or 'content' not in data:
            return jsonify({'error': 'No content provided'}), 400
        
        content = data['content']
        input_type = data.get('type', 'url')
        
        # Perform detection
        result = detector.analyze(content, input_type)
        
        return jsonify({
            'classification': result['classification'],
            'confidence': result['confidence'],
            'reasons': result['reasons'][:3],  # Limit reasons for API
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        app.logger.error(f"API error: {e}")
        return jsonify({'error': 'Analysis failed'}), 500

def initialize_tips():
    """Initialize default phishing tips"""
    try:
        # Check if tips already exist
        existing_tips = PhishingTip.find_all()
        if existing_tips:
            app.logger.info(f"Tips already initialized: {len(existing_tips)} tips found")
            return
        
        # Initialize with comprehensive security tips
        security_updater.update_security_tips_database()
        app.logger.info("Security tips initialized successfully")
        
    except Exception as e:
        app.logger.error(f"Error initializing tips: {e}")
        
        # Fallback: Add basic tips
        basic_tips = [
            {
                'id': 'tip-1',
                'title': 'Check Email Sender',
                'content': 'Always verify the sender\'s email address and be suspicious of unexpected emails.',
                'category': 'email',
                'priority': 1,
                'created_at': datetime.now().isoformat()
            },
            {
                'id': 'tip-2',
                'title': 'Hover Over Links',
                'content': 'Hover over links to see the actual destination before clicking.',
                'category': 'url',
                'priority': 1,
                'created_at': datetime.now().isoformat()
            },
            {
                'id': 'tip-3',
                'title': 'Use Strong Passwords',
                'content': 'Create unique, strong passwords and enable two-factor authentication.',
                'category': 'general',
                'priority': 1,
                'created_at': datetime.now().isoformat()
            }
        ]
        
        PhishingTip.bulk_insert(basic_tips)
        app.logger.info("Basic security tips added as fallback")

@app.route('/ai-content-check', methods=['GET', 'POST'])
@login_required
def ai_content_check():
    """AI Content Detection Interface for analyzing images and documents"""
    if request.method == 'POST':
        try:
            # Check if file was uploaded
            if 'file' not in request.files:
                flash('No file selected. Please choose an image or document to analyze.', 'error')
                return redirect(url_for('ai_content_check'))
            
            file = request.files['file']
            content_type = request.form.get('content_type', 'image')
            
            if file.filename == '':
                flash('No file selected. Please choose a file to analyze.', 'error')
                return redirect(url_for('ai_content_check'))
            
            # Check file size (limit to 500MB to prevent timeouts)
            MAX_FILE_SIZE = 500 * 1024 * 1024  # 500MB in bytes
            file.seek(0, 2)  # Seek to end of file
            file_size = file.tell()
            file.seek(0)  # Reset to beginning
            
            if file_size > MAX_FILE_SIZE:
                flash(f'File too large! Please upload a file smaller than 500MB. Your file is {file_size / (1024*1024):.1f}MB.', 'error')
                return redirect(url_for('ai_content_check'))
            
            # Check if file type is allowed
            if not allowed_file(file.filename or '', content_type):
                allowed_exts = APP_CONFIG.ALLOWED_EXTENSIONS.get(content_type, set())
                flash(f'Invalid file type. Please upload a {content_type} file with extension: {", ".join(allowed_exts)}', 'error')
                return redirect(url_for('ai_content_check'))
            
            # Save the uploaded file
            if file.filename:
                filename = secure_filename(file.filename)
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                unique_filename = f"{timestamp}_{filename}"
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
                file.save(file_path)
            else:
                flash('Invalid filename. Please try again.', 'error')
                return redirect(url_for('ai_content_check'))
            
            # Analyze the file for AI content
            analysis_result = ai_detector.analyze_content(file_path, content_type)
            
            # Save analysis result with encrypted user activity data
            user_id = session['user_id']
            user_ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.environ.get('REMOTE_ADDR'))
            user_agent = request.headers.get('User-Agent')
            
            Detection.create_detection(
                user_id=user_id,
                input_type=f"ai_{content_type}",
                input_content=filename,
                result=analysis_result['classification'],
                confidence_score=analysis_result['confidence'],
                reasons=analysis_result['details'],
                ai_analysis=analysis_result,
                user_ip=user_ip,
                user_agent=user_agent
            )
            
            # Save encrypted analysis result for future reference
            ai_detector.save_analysis_result(file_path, analysis_result, user_id, user_ip)
            logger.info(f"Encrypted AI content analysis saved for user: {user_id}")
            
            # Clean up uploaded file for security
            try:
                os.remove(file_path)
            except OSError:
                pass
            
            flash(f'AI Content Analysis Complete! Confidence: {analysis_result["confidence"]:.1%}', 'success')
            
            return render_template('ai_content_results.html', 
                                 filename=filename,
                                 content_type=content_type,
                                 result=analysis_result)
                                 
        except Exception as e:
            flash(f'Analysis failed: {str(e)}', 'error')
            return redirect(url_for('ai_content_check'))
    
    # GET request - show upload form
    return render_template('ai_content_check.html')