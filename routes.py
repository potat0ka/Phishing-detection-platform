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
from app import app
from simple_models import User, Detection, PhishingTip  # Our simple database models
from ml_detector import PhishingDetector  # AI/ML detection engine
from ai_content_detector import ai_detector  # AI content detection for images/documents
from utils import is_logged_in, login_required  # Helper functions
from security_tips_updater import security_updater  # Security tips management
from werkzeug.utils import secure_filename  # For secure file uploads
import json
import os
from datetime import datetime, timedelta

# Initialize the AI/ML detector when the app starts
# This loads the machine learning model for phishing detection
detector = PhishingDetector()

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
        user_id = User.create_user(username, email, password)
        
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
        
        try:
            # Perform phishing detection
            result = detector.analyze(input_content, input_type)
            
            # Save detection if user is logged in
            if is_logged_in():
                user_id = session.get('user_id')
                Detection.create_detection(
                    user_id=user_id,
                    input_type=input_type,
                    input_content=input_content,
                    result=result['classification'],
                    confidence_score=result['confidence'],
                    reasons=result['reasons'],
                    ai_analysis=result['ai_analysis']
                )
            
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
            
            # Check if file type is allowed
            from app import allowed_file, ALLOWED_IMAGE_EXTENSIONS, ALLOWED_DOCUMENT_EXTENSIONS
            if not allowed_file(file.filename, content_type):
                allowed_exts = ALLOWED_IMAGE_EXTENSIONS if content_type == 'image' else ALLOWED_DOCUMENT_EXTENSIONS
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
            
            # Save analysis result to database
            user_id = session['user_id']
            Detection.create_detection(
                user_id=user_id,
                input_type=f"ai_{content_type}",
                input_content=filename,
                result=analysis_result['classification'],
                confidence_score=analysis_result['confidence'],
                reasons=analysis_result['details'],
                ai_analysis=analysis_result
            )
            
            # Save analysis result for future reference
            ai_detector.save_analysis_result(file_path, analysis_result)
            
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