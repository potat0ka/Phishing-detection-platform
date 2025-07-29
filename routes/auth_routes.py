"""
Authentication Routes
====================

This blueprint handles user authentication with MongoDB and bcrypt:
- User registration with bcrypt password hashing
- Login with MongoDB queries and bcrypt verification
- Role-based dashboard redirects
- Session management

Author: Bigendra Shrestha
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.user_model import UserModel
from utils.validation import validate_email, validate_password
from models.user_model import hash_password, verify_password
import logging
import bcrypt

logger = logging.getLogger(__name__)

# Create blueprint for authentication routes
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """User registration with bcrypt password hashing"""
    if request.method == 'GET':
        return render_template('auth/register.html')

    try:
        # Get form data
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')

        # Validate input
        if not username or not email or not password:
            flash('All fields are required', 'error')
            return render_template('auth/register.html')

        if not validate_email(email):
            flash('Please enter a valid email address', 'error')
            return render_template('auth/register.html')

        if not validate_password(password):
            flash('Password must be at least 8 characters long and contain letters and numbers', 'error')
            return render_template('auth/register.html')

        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return render_template('auth/register.html')

        # Check if user already exists using UserModel
        existing_user = UserModel.find_user_by_email(email)
        if existing_user:
            flash('Email address already registered', 'error')
            return render_template('auth/register.html')

        existing_username = UserModel.find_user_by_username(username)
        if existing_username:
            flash('Username already taken', 'error')
            return render_template('auth/register.html')

        # Create new user with bcrypt hashed password
        user_id = UserModel.create_user(username, email, password)

        if user_id:
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('Registration failed. Please try again.', 'error')
            return render_template('auth/register.html')

    except Exception as e:
        logger.error(f"Registration error: {e}")
        flash('Registration error. Please try again.', 'error')
        return render_template('auth/register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """MongoDB authentication with bcrypt password verification"""
    if request.method == 'GET':
        return render_template('auth/login.html')

    try:
        # Get form data
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')

        print("Login attempt for:", email)

        # Validate input
        if not email or not password:
            flash('Email and password are required', 'error')
            return render_template('auth/login.html')

        # Find user using UserModel (handles MongoDB and file fallback)
        user = UserModel.find_user_by_email(email)
        if not user:
            # Also try username as fallback for flexibility
            user = UserModel.find_user_by_username(email)

        if not user:
            flash('Invalid email/username or password', 'error')
            return render_template('auth/login.html')

        # Debug logging
        print(f"Login attempt for: {email}")
        print(f"User from DB: {user}")
        
        # Get password hash from user document
        stored_password_hash = user.get('password_hash') or user.get('password', '')
        
        if not stored_password_hash:
            print(f"Login failed for: {email} - No password hash found")
            flash('Invalid email/username or password', 'error')
            return render_template('auth/login.html')

        # Verify password with bcrypt
        try:
            # Ensure we have the password as bytes for bcrypt
            password_bytes = password.encode('utf-8')
            
            # Handle both 'password' and 'password_hash' fields
            if isinstance(stored_password_hash, str):
                stored_hash_bytes = stored_password_hash.encode('utf-8')
            else:
                stored_hash_bytes = stored_password_hash

            # Verify password using bcrypt
            if not bcrypt.checkpw(password_bytes, stored_hash_bytes):
                print(f"Login failed for: {email} - Password verification failed")
                print(f"Expected hash format: {stored_password_hash[:20]}...")
                flash('Invalid email/username or password', 'error')
                return render_template('auth/login.html')
                
            print(f"Login successful for: {email}")

        except Exception as bcrypt_error:
            print(f"Bcrypt verification error for {email}: {bcrypt_error}")
            print(f"Stored hash: {stored_password_hash}")
            flash('Invalid email/username or password', 'error')
            return render_template('auth/login.html')

        # Check if user is active
        if not user.get('is_active', True):
            flash('Account has been deactivated', 'error')
            return render_template('auth/login.html')

        # Create session with email and role as specified
        session['email'] = user['email']
        session['role'] = user.get('role', 'user')
        session['user_id'] = str(user.get('_id', ''))
        session['username'] = user.get('username', email.split('@')[0])
        session.permanent = True

        # Update last login time if possible
        try:
            UserModel.update_last_login(user.get('_id'))
        except Exception:
            pass  # Don't fail login if update fails

        # Flask-Login integration
        try:
            from flask_login import login_user
            from app import User
            flask_user = User(
                user_id=user['_id'],
                username=user['username'],
                email=user['email'],
                role=user.get('role', 'user')
            )
            login_user(flask_user, remember=True)
        except ImportError:
            logger.warning("Flask-Login integration failed - using session-only authentication")

        flash(f'Welcome back, {user.get("username", "User")}!', 'success')

        # Handle next parameter for redirects after login
        next_page = request.args.get('next')
        if next_page:
            return redirect(next_page)

        # Role-based redirect as specified: /rbac/{role}-dashboard
        user_role = user.get('role', 'user')
        print(f"Redirecting {email} with role {user_role} to /rbac/{user_role}-dashboard")
        
        if user_role == 'superadmin':
            return redirect('/rbac/superadmin-dashboard')
        elif user_role == 'admin':
            return redirect('/rbac/admin-dashboard')
        else:
            return redirect('/rbac/user-dashboard')

    except Exception as e:
        logger.error(f"Login error: {e}")
        flash('An error occurred during login. Please try again.', 'error')
        return render_template('auth/login.html')

@auth_bp.route('/logout')
def logout():
    """User logout - clears session and Flask-Login"""
    username = session.get('username', 'User')
    
    # Flask-Login logout
    try:
        from flask_login import logout_user
        logout_user()
    except ImportError:
        pass
    
    session.clear()
    flash(f'Goodbye, {username}! You have been logged out.', 'info')
    return redirect(url_for('main.index'))

@auth_bp.route('/profile')
def profile():
    """User profile page"""
    if 'user_id' not in session:
        flash('Please log in to view your profile', 'error')
        return redirect(url_for('auth.login'))

    return render_template('auth/profile.html')

@auth_bp.route('/change-password', methods=['GET', 'POST'])
def change_password():
    """Change user password with bcrypt"""
    if 'user_id' not in session:
        flash('Please log in to change your password', 'error')
        return redirect(url_for('auth.login'))

    if request.method == 'GET':
        return render_template('auth/change_password.html')

    try:
        current_password = request.form.get('current_password', '').strip()
        new_password = request.form.get('new_password', '').strip()
        confirm_password = request.form.get('confirm_password', '').strip()

        if not all([current_password, new_password, confirm_password]):
            flash('All fields are required', 'error')
            return render_template('auth/change_password.html')

        if new_password != confirm_password:
            flash('New passwords do not match', 'error')
            return render_template('auth/change_password.html')

        if len(new_password) < 8:
            flash('Password must be at least 8 characters long', 'error')
            return render_template('auth/change_password.html')

        # Get current user
        user_id = session['user_id']
        current_user = UserModel.get_user_by_id(user_id)

        if not current_user:
            flash('User not found', 'error')
            return redirect(url_for('auth.logout'))

        # Verify current password with bcrypt
        stored_password = current_user.get('password_hash', '').encode('utf-8')
        current_password_bytes = current_password.encode('utf-8')

        if not bcrypt.checkpw(current_password_bytes, stored_password):
            flash('Current password is incorrect', 'error')
            return render_template('auth/change_password.html')

        # Update password
        success = UserModel.update_user_password(user_id, new_password)

        if success:
            flash('Password changed successfully!', 'success')
            return redirect(url_for('auth.profile'))
        else:
            flash('Failed to change password. Please try again.', 'error')
            return render_template('auth/change_password.html')

    except Exception as e:
        logger.error(f"Change password error: {e}")
        flash('An error occurred. Please try again.', 'error')
        return render_template('auth/change_password.html')

@auth_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    """Forgot password page - placeholder for now"""
    if request.method == 'GET':
        return render_template('auth/forgot_password.html')

    # For now, just redirect to login with message
    flash('Password reset functionality will be available soon. Please contact admin.', 'info')
    return redirect(url_for('auth.login'))

@auth_bp.route('/dashboard')
def dashboard_redirect():
    """Redirect to proper role-based dashboard"""
    if 'user_id' not in session:
        flash('Please log in to view your dashboard', 'warning')
        return redirect(url_for('auth.login'))

    user_role = session.get('role', 'user')

    if user_role == 'superadmin':
        return redirect(url_for('rbac.superadmin_dashboard'))
    elif user_role == 'admin':
        return redirect(url_for('rbac.admin_dashboard'))
    else:
        return redirect(url_for('rbac.user_dashboard'))

# Helper functions for templates
@auth_bp.app_template_global()
def is_authenticated():
    """Check if user is logged in"""
    return 'user_id' in session

@auth_bp.app_template_global()
def current_user():
    """Get current user info from session"""
    if 'user_id' in session:
        return {
            'id': session['user_id'],
            'username': session['username'],
            'email': session['email'],
            'role': session.get('role', 'user')
        }
    return None

@auth_bp.app_template_global()
def is_admin():
    """Check if current user is admin"""
    return session.get('role') == 'admin'