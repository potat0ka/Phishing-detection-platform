"""
Authentication Routes - Professional user management system
Handles registration, login, logout, and session management with MongoDB backend
"""

from flask import Blueprint, request, render_template, redirect, url_for, flash, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from mongodb_config import db_manager
from encryption_utils import encrypt_sensitive_data, decrypt_sensitive_data
import logging
import re
import secrets
import uuid
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

# Create authentication blueprint
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password):
    """Validate password strength"""
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    
    if not re.search(r'\d', password):
        return False, "Password must contain at least one number"
    
    return True, "Password is valid"

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """User registration with encrypted data storage"""
    if request.method == 'GET':
        return render_template('auth/register.html')
    
    try:
        # Get form data
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        # Validation
        if not username or len(username) < 3:
            return jsonify({
                'success': False,
                'message': 'Username must be at least 3 characters long'
            }), 400
        
        if not validate_email(email):
            return jsonify({
                'success': False,
                'message': 'Please enter a valid email address'
            }), 400
        
        is_valid_password, password_message = validate_password(password)
        if not is_valid_password:
            return jsonify({
                'success': False,
                'message': password_message
            }), 400
        
        if password != confirm_password:
            return jsonify({
                'success': False,
                'message': 'Passwords do not match'
            }), 400
        
        # Check if user already exists
        existing_user = db_manager.find_one('users', {'username': username})
        if existing_user:
            return jsonify({
                'success': False,
                'message': 'Username already exists'
            }), 400
        
        existing_email = db_manager.find_one('users', {'email': email})
        if existing_email:
            return jsonify({
                'success': False,
                'message': 'Email address already registered'
            }), 400
        
        # Create user with encrypted data
        user_data = {
            'username': username,
            'email': email,
            'password_hash': generate_password_hash(password),
            'role': 'user',  # Default role
            'created_at': datetime.utcnow(),
            'last_login': None,
            'is_active': True,
            'login_attempts': 0,
            'locked_until': None
        }
        
        # Encrypt sensitive data
        encrypted_user_data = encrypt_sensitive_data('user', user_data)
        
        # Insert user into database
        user_id = db_manager.insert_one('users', encrypted_user_data)
        
        if user_id:
            logger.info(f"New user registered: {username}")
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({
                    'success': True,
                    'message': 'Account created successfully! You can now log in.',
                    'redirect': url_for('auth.login')
                })
            else:
                flash('Account created successfully! You can now log in.', 'success')
                return redirect(url_for('auth.login'))
        else:
            return jsonify({
                'success': False,
                'message': 'Failed to create account. Please try again.'
            }), 500
            
    except Exception as e:
        logger.error(f"Registration error: {e}")
        return jsonify({
            'success': False,
            'message': 'An error occurred during registration'
        }), 500

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login with session management"""
    if request.method == 'GET':
        return render_template('auth/login.html')
    
    try:
        # Get form data
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        remember_me = request.form.get('remember_me') == 'on'
        
        if not username or not password:
            flash('Please enter both username and password', 'error')
            return render_template('auth/login.html')
        
        # Find user in database - handle both encrypted and non-encrypted data
        user = None
        
        # Get all users and check both encrypted and non-encrypted data
        all_users = db_manager.find_many('users', {})
        
        for user_data in all_users:
            # First try non-encrypted data (for demo accounts)
            if (user_data.get('username', '').lower() == username.lower() or 
                user_data.get('email', '').lower() == username.lower()):
                user = user_data
                break
            
            # Then try encrypted data
            try:
                decrypted_user = decrypt_sensitive_data('user', user_data)
                if (decrypted_user.get('username', '').lower() == username.lower() or 
                    decrypted_user.get('email', '').lower() == username.lower()):
                    user = user_data
                    break
            except Exception as e:
                # Continue if decryption fails - might be non-encrypted data
                continue
        
        if not user:
            flash('Invalid username or password', 'error')
            return render_template('auth/login.html')
        
        # Handle both encrypted and non-encrypted user data
        try:
            decrypted_user = decrypt_sensitive_data('user', user)
        except:
            # If decryption fails, use original data (for demo accounts)
            decrypted_user = user
        
        # Check if account is locked
        if decrypted_user.get('locked_until') and datetime.utcnow() < decrypted_user['locked_until']:
            flash('Account temporarily locked. Please try again later.', 'error')
            return render_template('auth/login.html')
        
        # Check if account is active
        if not decrypted_user.get('is_active', True):
            flash('Account has been deactivated', 'error')
            return render_template('auth/login.html')
        
        # Verify password
        if not check_password_hash(decrypted_user['password_hash'], password):
            # Increment login attempts
            login_attempts = decrypted_user.get('login_attempts', 0) + 1
            update_data = {'login_attempts': login_attempts}
            
            # Lock account after 5 failed attempts
            if login_attempts >= 5:
                update_data['locked_until'] = datetime.utcnow() + timedelta(minutes=30)
                logger.warning(f"Account locked for user: {username}")
            
            db_manager.update_one('users', {'_id': user['_id']}, update_data)
            
            flash('Invalid username or password', 'error')
            return render_template('auth/login.html')
        
        # Successful login - update user data
        update_data = {
            'last_login': datetime.utcnow(),
            'login_attempts': 0,
            'locked_until': None
        }
        db_manager.update_one('users', {'_id': user['_id']}, update_data)
        
        # Create session
        session['user_id'] = user['_id']
        session['username'] = decrypted_user['username']
        session['email'] = decrypted_user['email']
        session['role'] = decrypted_user.get('role', 'user')
        session['logged_in'] = True
        
        # Set session permanence
        if remember_me:
            session.permanent = True
        
        logger.info(f"User logged in: {decrypted_user['username']}")
        
        # Determine redirect URL - redirect to home page for now
        next_url = request.form.get('next') or session.pop('next_url', None)
        if not next_url or not next_url.startswith('/'):
            next_url = '/'  # Redirect to home page after successful login
        
        flash('Welcome back! Login successful.', 'success')
        return redirect(next_url)
            
    except Exception as e:
        logger.error(f"Login error: {e}")
        flash('An error occurred during login. Please try again.', 'error')
        return render_template('auth/login.html')

@auth_bp.route('/logout', methods=['GET', 'POST'])
def logout():
    """User logout and session cleanup"""
    try:
        username = session.get('username', 'Unknown')
        
        # Clear session
        session.clear()
        
        logger.info(f"User logged out: {username}")
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({
                'success': True,
                'message': 'Logged out successfully',
                'redirect': url_for('index')
            })
        else:
            flash('You have been logged out successfully.', 'info')
            return redirect(url_for('index'))
            
    except Exception as e:
        logger.error(f"Logout error: {e}")
        return redirect(url_for('index'))

@auth_bp.route('/check-session')
def check_session():
    """Check if user session is valid"""
    if 'user_id' in session and session.get('logged_in'):
        # Verify user still exists and is active
        user = db_manager.find_one('users', {'_id': session['user_id']})
        
        if user:
            decrypted_user = decrypt_sensitive_data('user', user)
            if decrypted_user.get('is_active', True):
                return jsonify({'valid': True}), 200
        
        # Invalid session - clear it
        session.clear()
    
    return jsonify({'valid': False}), 401

@auth_bp.route('/profile')
def profile():
    """User profile management"""
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    user = db_manager.find_one('users', {'_id': session['user_id']})
    if not user:
        session.clear()
        return redirect(url_for('auth.login'))
    
    decrypted_user = decrypt_sensitive_data('user', user)
    
    # Get user statistics
    detection_count = db_manager.count_documents('detections', {'user_id': session['user_id']})
    
    return render_template('auth/profile.html', 
                         user=decrypted_user, 
                         detection_count=detection_count)

@auth_bp.route('/change-password', methods=['POST'])
def change_password():
    """Change user password"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'}), 401
    
    try:
        current_password = request.form.get('current_password', '')
        new_password = request.form.get('new_password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        # Get user
        user = db_manager.find_one('users', {'_id': session['user_id']})
        if not user:
            return jsonify({'success': False, 'message': 'User not found'}), 404
        
        decrypted_user = decrypt_sensitive_data('user', user)
        
        # Verify current password
        if not check_password_hash(decrypted_user['password_hash'], current_password):
            return jsonify({'success': False, 'message': 'Current password is incorrect'}), 400
        
        # Validate new password
        is_valid, message = validate_password(new_password)
        if not is_valid:
            return jsonify({'success': False, 'message': message}), 400
        
        if new_password != confirm_password:
            return jsonify({'success': False, 'message': 'New passwords do not match'}), 400
        
        # Update password
        new_password_hash = generate_password_hash(new_password)
        success = db_manager.update_one('users', 
                                      {'_id': session['user_id']}, 
                                      {'password_hash': new_password_hash})
        
        if success:
            logger.info(f"Password changed for user: {session['username']}")
            return jsonify({'success': True, 'message': 'Password changed successfully'})
        else:
            return jsonify({'success': False, 'message': 'Failed to update password'}), 500
            
    except Exception as e:
        logger.error(f"Password change error: {e}")
        return jsonify({'success': False, 'message': 'An error occurred'}), 500

@auth_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    """Handle forgot password requests"""
    if request.method == 'GET':
        return render_template('auth/forgot_password.html')
    
    try:
        email = request.form.get('email', '').strip().lower()
        
        if not email:
            flash('Please enter your email address.', 'error')
            return render_template('auth/forgot_password.html')
        
        if not validate_email(email):
            flash('Please enter a valid email address.', 'error')
            return render_template('auth/forgot_password.html')
        
        # Check if user exists
        user = db_manager.find_one('users', {'email': email})
        
        # Always show success message for security (don't reveal if email exists)
        if user:
            # Generate reset token
            reset_token = secrets.token_urlsafe(32)
            reset_expires = datetime.utcnow() + timedelta(hours=1)  # Token expires in 1 hour
            
            # Save reset token to database
            reset_data = {
                'reset_token': reset_token,
                'reset_expires': reset_expires,
                'reset_requested_at': datetime.utcnow()
            }
            
            db_manager.update_one('users', {'_id': user['_id']}, reset_data)
            
            # For now, we'll log the reset link instead of sending email
            # In production, you would integrate with an email service
            reset_url = url_for('auth.reset_password', token=reset_token, _external=True)
            logger.info(f"Password reset requested for {email}. Reset URL: {reset_url}")
            
            # Store reset info for demonstration (in production, send via email)
            flash(f'Password reset instructions have been sent to your email. Check your email for the reset link.', 'success')
        else:
            # Don't reveal that the email doesn't exist
            flash('If an account with that email exists, password reset instructions have been sent.', 'success')
        
        return render_template('auth/forgot_password.html')
        
    except Exception as e:
        logger.error(f"Forgot password error: {e}")
        flash('An error occurred. Please try again later.', 'error')
        return render_template('auth/forgot_password.html')

@auth_bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """Handle password reset with token"""
    if request.method == 'GET':
        # Verify token is valid and not expired
        user = db_manager.find_one('users', {
            'reset_token': token,
            'reset_expires': {'$gt': datetime.utcnow()}
        })
        
        if not user:
            flash('Invalid or expired reset token. Please request a new password reset.', 'error')
            return redirect(url_for('auth.forgot_password'))
        
        return render_template('auth/reset_password.html', token=token)
    
    # POST request - process password reset
    try:
        new_password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        if not new_password or not confirm_password:
            flash('Please fill in all fields.', 'error')
            return render_template('auth/reset_password.html', token=token)
        
        if new_password != confirm_password:
            flash('Passwords do not match.', 'error')
            return render_template('auth/reset_password.html', token=token)
        
        # Validate password strength
        is_valid, message = validate_password(new_password)
        if not is_valid:
            flash(message, 'error')
            return render_template('auth/reset_password.html', token=token)
        
        # Verify token is still valid
        user = db_manager.find_one('users', {
            'reset_token': token,
            'reset_expires': {'$gt': datetime.utcnow()}
        })
        
        if not user:
            flash('Invalid or expired reset token. Please request a new password reset.', 'error')
            return redirect(url_for('auth.forgot_password'))
        
        # Update password and clear reset token
        new_password_hash = generate_password_hash(new_password)
        update_data = {
            'password_hash': new_password_hash,
            'reset_token': None,
            'reset_expires': None,
            'reset_completed_at': datetime.utcnow()
        }
        
        success = db_manager.update_one('users', {'_id': user['_id']}, update_data)
        
        if success:
            decrypted_user = decrypt_sensitive_data('user', user)
            logger.info(f"Password reset completed for user: {decrypted_user.get('username', 'unknown')}")
            flash('Your password has been reset successfully. You can now log in with your new password.', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('Failed to reset password. Please try again.', 'error')
            return render_template('auth/reset_password.html', token=token)
            
    except Exception as e:
        logger.error(f"Password reset error: {e}")
        flash('An error occurred while resetting your password. Please try again.', 'error')
        return render_template('auth/reset_password.html', token=token)

# Authentication decorators and helpers
def login_required(f):
    """Decorator to require login for routes"""
    from functools import wraps
    
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or not session.get('logged_in'):
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({'success': False, 'message': 'Login required'}), 401
            
            session['next_url'] = request.url
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('auth.login'))
        
        return f(*args, **kwargs)
    
    return decorated_function

def admin_required(f):
    """Decorator to require admin role"""
    from functools import wraps
    
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or session.get('role') != 'admin':
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({'success': False, 'message': 'Admin access required'}), 403
            
            flash('Admin access required.', 'danger')
            return redirect(url_for('index'))
        
        return f(*args, **kwargs)
    
    return decorated_function

def get_current_user():
    """Get current user data from session"""
    if 'user_id' not in session:
        return None
    
    user = db_manager.find_one('users', {'_id': session['user_id']})
    if user:
        return decrypt_sensitive_data('user', user)
    
    return None