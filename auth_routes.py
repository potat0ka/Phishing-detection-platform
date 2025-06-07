"""
Authentication Routes - Professional user management system
Handles registration, login, logout, and session management with MongoDB backend
"""

from flask import Blueprint, request, render_template, redirect, url_for, flash, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from models.mongodb_config import get_mongodb_manager
from utils.encryption_utils import encrypt_sensitive_data, decrypt_sensitive_data
import logging
import re
import secrets
import uuid
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

# Create authentication blueprint
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

def validate_email(email):
    """
    Validate email format using regex pattern
    
    This function ensures email addresses follow standard format:
    - Contains @ symbol with domain
    - Valid characters before and after @
    - Proper domain extension (2+ characters)
    
    Args:
        email (str): Email address to validate
        
    Returns:
        bool: True if email format is valid, False otherwise
    """
    # RFC 5322 compliant email pattern (simplified)
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password):
    """
    Validate password strength according to security best practices
    
    Password requirements:
    - Minimum 8 characters length
    - At least one uppercase letter (A-Z)
    - At least one lowercase letter (a-z)  
    - At least one number (0-9)
    
    This helps protect against brute force attacks and ensures
    users create secure passwords for their accounts.
    
    Args:
        password (str): Password to validate
        
    Returns:
        tuple: (is_valid: bool, message: str)
    """
    # Check minimum length requirement
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    
    # Check for uppercase letter
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    
    # Check for lowercase letter
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    
    # Check for number
    if not re.search(r'\d', password):
        return False, "Password must contain at least one number"
    
    return True, "Password is valid"

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    User registration system - Creates regular user accounts with encrypted data storage
    
    This function handles both GET and POST requests:
    - GET: Shows the registration form
    - POST: Processes user registration and creates new account
    
    Security Features:
    - Password strength validation (8+ chars, upper/lower/numbers)
    - Email format validation with regex
    - Username uniqueness checking
    - Data encryption before database storage
    - Default role assignment as 'user' (regular user, not admin)
    
    For beginners:
    - New users are created as regular users by default
    - Super admin can later promote users to sub-admin or admin roles
    - All user data is encrypted for security
    - Duplicate usernames and emails are prevented
    """
    if request.method == 'GET':
        return render_template('auth/register.html')
    
    try:
        # Extract form data from the registration form
        # .strip() removes extra spaces, .lower() standardizes email format
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        # Input validation - checking all required fields and formats
        if not username or len(username) < 3:
            flash('Username must be at least 3 characters long', 'error')
            return render_template('auth/register.html')
        
        if not validate_email(email):
            flash('Please enter a valid email address', 'error')
            return render_template('auth/register.html')
        
        # Check password strength using our custom validation function
        is_valid_password, password_message = validate_password(password)
        if not is_valid_password:
            flash(password_message, 'error')
            return render_template('auth/register.html')
        
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return render_template('auth/register.html')
        
        # Get MongoDB manager instance
        db_manager = get_mongodb_manager()
        
        # Prevent duplicate accounts - check both username and email
        # This searches the database for existing users with same username
        existing_user = db_manager.find_one('users', {'username': username})
        if existing_user:
            flash('Username already exists. Please choose a different username.', 'error')
            return render_template('auth/register.html')
        
        # Check if email is already registered
        existing_email = db_manager.find_one('users', {'email': email})
        if existing_email:
            flash('Email address already registered. Please use a different email.', 'error')
            return render_template('auth/register.html')
        
        # Create new user data structure with all required fields
        user_data = {
            'username': username,
            'email': email,
            'password_hash': generate_password_hash(password),  # Securely hash the password
            'role': 'user',  # Default role - creates regular user (not admin)
            'created_at': datetime.utcnow().isoformat(),  # When account was created
            'last_login': None,  # No login yet since account is new
            'is_active': True,  # Account is active and can log in
            'login_attempts': 0,  # Track failed login attempts for security
            'locked_until': None,  # Account locking for security (if needed)
            'profile': {
                'full_name': '',
                'phone': '',
                'preferences': {
                    'email_notifications': True,
                    'security_alerts': True
                }
            }
        }
        
        # Encrypt sensitive user data before storing in database
        # This protects user information even if database is compromised
        encrypted_user_data = encrypt_sensitive_data('user', user_data)
        
        # Insert the new user into the database
        # This returns the user ID if successful, None if failed
        user_id = db_manager.insert_one('users', encrypted_user_data)
        
        if user_id:
            # Log successful registration for monitoring
            logger.info(f"New user registered successfully: {username} (ID: {user_id})")
            
            # Show success message and redirect to login page
            flash('Account created successfully! You can now log in with your credentials.', 'success')
            return redirect(url_for('auth.login'))
        else:
            # Database insertion failed
            flash('Failed to create account. Please try again.', 'error')
            return render_template('auth/register.html')
            
    except Exception as e:
        # Handle any unexpected errors during registration
        logger.error(f"Registration error: {e}")
        flash('An error occurred during registration. Please try again.', 'error')
        return render_template('auth/register.html')

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
        
        # Get MongoDB manager and all users, check both encrypted and non-encrypted data
        db_manager = get_mongodb_manager()
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
        locked_until = decrypted_user.get('locked_until')
        if locked_until:
            # Convert string to datetime if needed
            if isinstance(locked_until, str):
                try:
                    locked_until = datetime.fromisoformat(locked_until.replace('Z', '+00:00'))
                except:
                    locked_until = None
            
            if locked_until and datetime.utcnow() < locked_until:
                flash('Account temporarily locked. Please try again later.', 'error')
                return render_template('auth/login.html')
        
        # Check if account is active
        if not decrypted_user.get('is_active', True):
            flash('Account has been deactivated', 'error')
            return render_template('auth/login.html')
        
        # Verify password
        if not check_password_hash(decrypted_user['password_hash'], password):
            # Log failed login attempt
            failed_login_log = {
                'timestamp': datetime.utcnow().isoformat(),
                'username': username,
                'user_id': user.get('_id', user.get('id')),
                'ip_address': request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr),
                'user_agent': request.headers.get('User-Agent', 'Unknown'),
                'success': False,
                'failure_reason': 'Invalid password',
                'login_method': 'password'
            }
            db_manager.insert_one('login_logs', failed_login_log)
            
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
        
        # Log login activity for admin tracking
        login_log = {
            'timestamp': datetime.utcnow().isoformat(),
            'username': decrypted_user['username'],
            'user_id': user.get('_id', user.get('id')),
            'ip_address': request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr),
            'user_agent': request.headers.get('User-Agent', 'Unknown'),
            'success': True,
            'login_method': 'password',
            'session_id': session.get('_permanent_id', 'unknown')
        }
        db_manager.insert_one('login_logs', login_log)
        
        # Create session with proper role handling
        session['user_id'] = user.get('_id', user.get('id'))
        session['username'] = decrypted_user['username']
        session['email'] = decrypted_user['email']
        session['user_role'] = decrypted_user.get('role', 'user')  # Store as user_role for consistency
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
        try:
            logger.error(f"Login error details - Username: {username if 'username' in locals() else 'undefined'}, User found: {user is not None if 'user' in locals() else 'undefined'}")
            if 'user' in locals() and user:
                logger.error(f"User data keys: {list(user.keys())}")
        except:
            logger.error("Error logging additional details")
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

# Profile functionality removed - using login/logout only

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
    """Decorator to require admin role - supports both admin, sub_admin, and super_admin"""
    from functools import wraps
    
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or not session.get('logged_in'):
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({'success': False, 'message': 'Login required'}), 401
            
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('auth.login'))
        
        # Check for admin roles - support all admin role types
        user_role = session.get('user_role', session.get('role', 'user'))
        admin_roles = ['admin', 'sub_admin', 'super_admin']
        
        if user_role not in admin_roles:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({'success': False, 'message': 'Admin access required'}), 403
            
            flash('Admin access required.', 'danger')
            return redirect(url_for('index'))
        
        return f(*args, **kwargs)
    
    return decorated_function

def get_current_user():
    """Get current user data from session with role information"""
    if 'user_id' not in session or not session.get('logged_in'):
        return None
    
    # Get MongoDB manager and try finding by session user_id (handles both _id and id formats)
    db_manager = get_mongodb_manager()
    user_id = session['user_id']
    user = db_manager.find_one('users', {'_id': user_id}) or db_manager.find_one('users', {'id': user_id})
    
    if user:
        try:
            # Try to decrypt user data
            decrypted_user = decrypt_sensitive_data('user', user)
            return decrypted_user
        except:
            # If decryption fails, return original data (for demo accounts)
            return user
    
    # Fallback: create user data from session if user not found in DB
    return {
        'id': session['user_id'],
        'username': session.get('username', 'Unknown'),
        'email': session.get('email', ''),
        'role': session.get('user_role', 'user')
    }