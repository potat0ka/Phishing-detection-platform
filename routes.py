from flask import render_template, request, redirect, url_for, flash, session, jsonify
from app import app, db
from models import User, Detection, PhishingTip
from ml_detector import PhishingDetector
# Social automation removed - this is a phishing detection platform
from utils import is_logged_in, login_required
import json
from datetime import datetime, timedelta

# Initialize ML detector for phishing detection
detector = PhishingDetector()

@app.route('/')
def index():
    """Home page with phishing check form"""
    tips = PhishingTip.query.filter_by(priority=1).limit(3).all()
    return render_template('index.html', tips=tips)

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        # Validation
        if not username or not email or not password:
            flash('All fields are required.', 'error')
            return render_template('register.html')
        
        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return render_template('register.html')
        
        if len(password) < 6:
            flash('Password must be at least 6 characters long.', 'error')
            return render_template('register.html')
        
        # Check if user exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists.', 'error')
            return render_template('register.html')
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered.', 'error')
            return render_template('register.html')
        
        # Create new user
        user = User()
        user.username = username
        user.email = email
        user.set_password(password)
        
        try:
            db.session.add(user)
            db.session.commit()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash('Registration failed. Please try again.', 'error')
            app.logger.error(f"Registration error: {e}")
    
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
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['username'] = user.username
            flash(f'Welcome back, {user.username}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password.', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """User logout"""
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    """User dashboard with detection history"""
    user_id = session['user_id']
    detections = Detection.query.filter_by(user_id=user_id).order_by(Detection.created_at.desc()).limit(20).all()
    
    # Calculate statistics
    total_checks = Detection.query.filter_by(user_id=user_id).count()
    phishing_detected = Detection.query.filter_by(user_id=user_id, result='phishing').count()
    safe_results = Detection.query.filter_by(user_id=user_id, result='safe').count()
    
    stats = {
        'total_checks': total_checks,
        'phishing_detected': phishing_detected,
        'safe_results': safe_results,
        'accuracy_rate': round((safe_results / total_checks * 100) if total_checks > 0 else 0, 1)
    }
    
    return render_template('dashboard.html', detections=detections, stats=stats)

@app.route('/check', methods=['GET', 'POST'])
def check():
    """Phishing detection interface"""
    if request.method == 'POST':
        input_type = request.form.get('input_type', 'url')
        input_content = request.form.get('input_content', '').strip()
        
        if not input_content:
            flash('Please provide content to check.', 'error')
            return render_template('check.html')
        
        # Perform AI-powered phishing detection
        try:
            result = detector.analyze(input_content, input_type)
            
            # Save to database if user is logged in
            if is_logged_in():
                detection = Detection(
                    user_id=session['user_id'],
                    input_type=input_type,
                    input_content=input_content,
                    result=result['classification'],
                    confidence_score=result['confidence'],
                    reasons=json.dumps(result['reasons']),
                    ai_analysis=json.dumps(result['ai_analysis'])
                )
                db.session.add(detection)
                db.session.commit()
            
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
    """Educational tips about phishing prevention"""
    email_tips = PhishingTip.query.filter_by(category='email').all()
    url_tips = PhishingTip.query.filter_by(category='url').all()
    general_tips = PhishingTip.query.filter_by(category='general').all()
    
    return render_template('tips.html', 
                         email_tips=email_tips,
                         url_tips=url_tips, 
                         general_tips=general_tips)

@app.route('/api/quick-check', methods=['POST'])
def quick_check():
    """Quick API endpoint for checking content"""
    try:
        data = request.get_json()
        if not data or 'content' not in data:
            return jsonify({'error': 'No content provided'}), 400
        
        input_type = data.get('type', 'url')
        content = data['content'].strip()
        
        if not content:
            return jsonify({'error': 'Empty content provided'}), 400
        
        result = detector.analyze(content, input_type)
        return jsonify(result)
    
    except Exception as e:
        app.logger.error(f"Quick check error: {e}")
        return jsonify({'error': 'Analysis failed'}), 500

# Initialize default tips if database is empty
def initialize_tips():
    """Initialize default phishing tips"""
    with app.app_context():
        if PhishingTip.query.count() == 0:
            default_tips = [
                {
                    'title': 'Check the Sender\'s Email Address',
                'content': 'Verify the sender\'s email address carefully. Phishing emails often use addresses that look similar to legitimate ones but contain subtle differences.',
                    'category': 'email',
                    'priority': 1
                },
                {
                    'title': 'Look for Spelling and Grammar Errors',
                    'content': 'Legitimate organizations usually have professional communications. Multiple spelling or grammar errors can be a red flag.',
                    'category': 'email',
                    'priority': 1
                },
                {
                    'title': 'Verify URLs Before Clicking',
                    'content': 'Hover over links to see the actual destination. Be suspicious of shortened URLs or domains that don\'t match the supposed sender.',
                    'category': 'url',
                    'priority': 1
                },
                {
                    'title': 'Check for HTTPS and SSL Certificates',
                    'content': 'Legitimate websites, especially those handling sensitive information, should use HTTPS. Look for the padlock icon in your browser.',
                    'category': 'url',
                    'priority': 1
                },
                {
                    'title': 'Be Wary of Urgent Language',
                    'content': 'Phishing attempts often create false urgency like "Act now!" or "Your account will be closed!" Take time to verify before acting.',
                    'category': 'general',
                    'priority': 1
                },
                {
                    'title': 'Never Share Personal Information',
                    'content': 'Legitimate companies will never ask for passwords, social security numbers, or credit card details via email or suspicious websites.',
                    'category': 'general',
                    'priority': 1
                }
            ]
            
            for tip_data in default_tips:
                tip = PhishingTip(**tip_data)
                db.session.add(tip)
            
            try:
                db.session.commit()
                app.logger.info("Default phishing tips initialized")
            except Exception as e:
                db.session.rollback()
                app.logger.error(f"Failed to initialize tips: {e}")

# Additional security and utility routes can be added here in the future
