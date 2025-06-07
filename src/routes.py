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
from app import app, allowed_file, ALLOWED_EXTENSIONS, get_current_user
from models.mongodb_config import get_mongodb_manager
from auth_routes import login_required, admin_required
from ml_detector import PhishingDetector
from utils.ai_content_detector import AIContentDetector
from utils.explainable_ai import ExplainableAI

# Initialize components
ai_detector = AIContentDetector()
explainer = ExplainableAI()
db_manager = get_mongodb_manager()
from utils.encryption_utils import encrypt_sensitive_data, decrypt_sensitive_data
# Remove unused import - is_logged_in functionality is handled by login_required decorator
from werkzeug.utils import secure_filename
import json
import os
from datetime import datetime
import re
from urllib.parse import urlparse
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

# Initialize the AI/ML detector when the app starts
# This loads the machine learning model for phishing detection
detector = PhishingDetector()

# Initialize the explainable AI system for educational insights
# This provides detailed explanations of how AI detection works
explainer = ExplainableAI()

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
    """Redirect to enhanced authentication system"""
    return redirect(url_for('auth.register'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Redirect to enhanced authentication system"""
    return redirect(url_for('auth.login'))

@app.route('/logout')
def logout():
    """User logout"""
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    """
    Role-based dashboard routing system
    
    Routes users to appropriate dashboards based on their role:
    - Super Admin & Sub Admin: Admin Dashboard with role-specific permissions
    - Regular User: User Dashboard with personal features only
    """
    current_user = get_current_user()
    user_role = current_user.get('role', 'user') if current_user else 'user'
    
    # Role-based dashboard routing
    if user_role in ['super_admin', 'sub_admin', 'admin']:
        # Admin roles get redirected to admin dashboard
        return redirect(url_for('admin.admin_dashboard'))
    else:
        # Regular users get user dashboard
        return user_dashboard()

@app.route('/user-dashboard')
@login_required
def user_dashboard():
    """
    User Dashboard - Personal features only for regular users
    
    Features available to regular users:
    - View personal scan history
    - Personal activity statistics 
    - Manage own detection records
    - Basic account features
    
    No admin functionality accessible
    """
    current_user = get_current_user()
    user_id = session.get('user_id')
    
    if not current_user:
        return redirect(url_for('auth.login'))
    
    # Ensure only regular users can access this dashboard
    user_role = current_user.get('role', 'user')
    if user_role in ['super_admin', 'sub_admin', 'admin']:
        return redirect(url_for('admin.admin_dashboard'))
    
    # Get MongoDB manager and user's personal scan history
    db_manager = get_mongodb_manager()
    user_detections = db_manager.find_many('detections', {'user_id': user_id})
    
    # Calculate personal statistics
    total_scans = len(user_detections)
    phishing_detected = 0
    safe_results = 0
    
    for detection in user_detections:
        try:
            # Try to decrypt detection data if encrypted
            decrypted_detection = decrypt_sensitive_data('detection', detection)
            result = decrypted_detection.get('result', 'unknown')
        except:
            # Fallback to non-encrypted data
            result = detection.get('result', 'unknown')
        
        if result in ['phishing', 'malicious', 'suspicious', 'dangerous']:
            phishing_detected += 1
        elif result in ['safe', 'legitimate']:
            safe_results += 1
    
    # Get recent detections for activity timeline
    recent_detections = user_detections[-10:] if user_detections else []
    
    # Prepare user statistics
    user_stats = {
        'total_scans': total_scans,
        'phishing_detected': phishing_detected,
        'safe_results': safe_results,
        'accuracy_rate': round((safe_results / total_scans * 100) if total_scans > 0 else 0, 1)
    }
    
    return render_template('dashboard.html', 
                         current_user=current_user,
                         stats=user_stats,
                         detections=recent_detections,
                         is_admin=False,
                         user_role=user_role)

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
            
            # Generate explainable AI insights for educational purposes
            explanation = explainer.explain_phishing_detection(
                url=input_content if input_type == 'url' else '',
                content=input_content if input_type != 'url' else '',
                detection_result=result
            )
            
            # Save detection with encrypted user activity data
            if session.get('user_id'):
                try:
                    user_id = session.get('user_id')
                    user_ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.environ.get('REMOTE_ADDR'))
                    user_agent = request.headers.get('User-Agent')
                    
                    detection_data = {
                        'user_id': user_id,
                        'input_type': input_type,
                        'input_content': input_content,
                        'result': result['classification'],
                        'confidence_score': result['confidence'],
                        'threat_level': result.get('threat_level', 'unknown'),
                        'reasons': result['reasons'],
                        'ai_analysis': result['ai_analysis'],
                        'explanation': explanation,  # Include educational explanation
                        'user_ip': user_ip,
                        'user_agent': user_agent,
                        'timestamp': datetime.utcnow()
                    }
                    
                    # Encrypt sensitive detection data and save to database
                    db_manager = get_mongodb_manager()
                    encrypted_detection = encrypt_sensitive_data('detection', detection_data)
                    db_manager.insert_one('detections', encrypted_detection)
                    logger.info(f"Encrypted detection saved for user: {user_id}")
                except Exception as save_error:
                    app.logger.error(f"Failed to save encrypted detection: {save_error}")
                    # Continue without saving - don't let this block the analysis
            
            return render_template('result.html', 
                                 result=result, 
                                 explanation=explanation,
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
    # Get tips organized by category from database
    all_tips = db_manager.find_many('security_tips')
    email_tips = [tip for tip in all_tips if tip.get('category') == 'email']
    url_tips = [tip for tip in all_tips if tip.get('category') == 'url']
    general_tips = [tip for tip in all_tips if tip.get('category') == 'general']
    
    # Get trending threats information from database
    trending_threats = db_manager.find_many('trending_threats', limit=5)
    
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
        existing_tips = db_manager.find_many('security_tips')
        if existing_tips:
            app.logger.info(f"Tips already initialized: {len(existing_tips)} tips found")
            return
        
        # Initialize with basic security tips from fallback data
        app.logger.info("Initializing security tips from fallback data")
        
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
        
        # Insert basic tips into database
        for tip in basic_tips:
            db_manager.insert_one('security_tips', tip)
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
                allowed_exts = ALLOWED_EXTENSIONS.get(content_type, set())
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
            
            # Generate explainable AI insights for educational purposes
            explanation = explainer.explain_ai_content_detection(
                file_path=file_path,
                content_type=content_type,
                detection_result=analysis_result
            )
            
            # Save analysis result with encrypted user activity data
            user_id = session['user_id']
            user_ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.environ.get('REMOTE_ADDR'))
            user_agent = request.headers.get('User-Agent')
            
            detection_data = {
                'user_id': user_id,
                'input_type': f"ai_{content_type}",
                'input_content': filename,
                'result': analysis_result['classification'],
                'confidence_score': analysis_result['confidence'],
                'timestamp': datetime.utcnow(),
                'reasons': analysis_result['details'],
                'ai_analysis': analysis_result,
                'explanation': explanation,  # Include educational explanation
                'user_ip': user_ip,
                'user_agent': user_agent
            }
            
            # Encrypt and save detection data
            encrypted_detection = encrypt_sensitive_data('detection', detection_data)
            db_manager.insert_one('detections', encrypted_detection)
            
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
                                 result=analysis_result,
                                 explanation=explanation)
                                 
        except Exception as e:
            flash(f'Analysis failed: {str(e)}', 'error')
            return redirect(url_for('ai_content_check'))
    
    # GET request - show upload form
    return render_template('ai_content_check.html')



@app.route('/detection-details/<detection_id>')
@login_required
def detection_details(detection_id):
    """Get detailed information about a specific detection"""
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'success': False, 'error': 'User not authenticated'})
        
        # Find the detection by ID for this user
        detection = db_manager.find_one('detections', {
            'id': detection_id,
            'user_id': user_id
        })
        
        if not detection:
            return jsonify({'success': False, 'error': 'Detection not found'})
        
        # Decrypt sensitive data if needed
        try:
            decrypted_detection = decrypt_sensitive_data('detection', detection)
        except Exception as e:
            logger.warning(f"Failed to decrypt detection data: {e}")
            decrypted_detection = detection
        
        # Format the response with proper field handling
        response_data = {
            'id': decrypted_detection.get('id', detection_id),
            'input_type': decrypted_detection.get('input_type', 'Unknown'),
            'input_content': decrypted_detection.get('input_content', decrypted_detection.get('content', 'No content available')),
            'result': decrypted_detection.get('result', 'Unknown'),
            'confidence_score': decrypted_detection.get('confidence_score', decrypted_detection.get('confidence', 0.0)),
            'created_at': decrypted_detection.get('created_at', decrypted_detection.get('timestamp', 'Unknown')),
            'analysis_details': decrypted_detection.get('analysis_details', ''),
            'threat_indicators': decrypted_detection.get('threat_indicators', []),
            'recommendations': decrypted_detection.get('recommendations', [])
        }
        
        return jsonify({'success': True, 'detection': response_data})
        
    except Exception as e:
        logger.error(f"Error fetching detection details: {e}")
        return jsonify({'success': False, 'error': 'Failed to fetch detection details'})

@app.route('/delete-detection/<detection_id>', methods=['DELETE'])
@login_required
def delete_detection_record(detection_id):
    """Delete a specific detection from user's history"""
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'success': False, 'error': 'User not authenticated'})
        
        # Try to find the detection using both possible ID formats
        detection = None
        
        # First try with 'id' field
        detection = db_manager.find_one('detections', {
            'id': detection_id,
            'user_id': user_id
        })
        
        # If not found, try with '_id' field
        if not detection:
            detection = db_manager.find_one('detections', {
                '_id': detection_id,
                'user_id': user_id
            })
        
        if not detection:
            return jsonify({'success': False, 'error': 'Detection not found or access denied'})
        
        # Delete using the found detection's actual identifier
        delete_query = {'user_id': user_id}
        if detection.get('id'):
            delete_query['id'] = detection['id']
        else:
            delete_query['_id'] = detection['_id']
        
        deleted = db_manager.delete_one('detections', delete_query)
        
        if deleted:
            logger.info(f"User {user_id} deleted detection {detection_id}")
            return jsonify({'success': True, 'message': 'Detection deleted successfully'})
        else:
            return jsonify({'success': False, 'error': 'Failed to delete detection'})
        
    except Exception as e:
        logger.error(f"Error deleting detection {detection_id}: {e}")
        return jsonify({'success': False, 'error': 'Failed to delete detection'})

@app.route('/delete-all-history', methods=['DELETE'])
@login_required
def delete_all_user_history():
    """Delete all detection history for the current user"""
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'success': False, 'error': 'User not authenticated'})
        
        # Get all detections for this user first to count them
        user_detections = db_manager.find_many('detections', {'user_id': user_id})
        deletion_count = 0
        
        # Delete each detection individually (since we don't have delete_many)
        for detection in user_detections:
            deleted = db_manager.delete_one('detections', {
                '_id': detection.get('_id') or detection.get('id'),
                'user_id': user_id
            })
            if deleted:
                deletion_count += 1
        
        if deletion_count > 0:
            logger.info(f"User {user_id} deleted {deletion_count} detection records")
            return jsonify({
                'success': True, 
                'message': f'Successfully deleted {deletion_count} detection records',
                'deleted_count': deletion_count
            })
        else:
            return jsonify({'success': True, 'message': 'No history found to delete'})
        
    except Exception as e:
        logger.error(f"Error deleting all user history: {e}")
        return jsonify({'success': False, 'error': 'Failed to delete history'})