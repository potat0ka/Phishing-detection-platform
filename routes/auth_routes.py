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

from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify, current_app
from models.user_model import UserModel
from utils.validation import validate_email, validate_password
from models.user_model import hash_password, verify_password
import logging
import bcrypt
import os
from werkzeug.utils import secure_filename
from PIL import Image

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

        logger.info(f"Login attempt for: {email}")

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

        # Authentication logging
        logger.debug(f"User lookup result: {bool(user)}")
        logger.debug(f"Authentication attempt for: {email}")
        
        # Get password hash from user document
        stored_password_hash = user.get('password_hash') or user.get('password', '')
        
        if not stored_password_hash:
            logger.warning(f"Login failed for: {email} - No password hash found")
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
                logger.warning(f"Login failed for: {email} - Password verification failed")
                flash('Invalid email/username or password', 'error')
                return render_template('auth/login.html')
                
            logger.info(f"Login successful for: {email}")

        except Exception as bcrypt_error:
            logger.error(f"Bcrypt verification error for {email}: {bcrypt_error}")
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
        session['profile_photo'] = user.get('profile_photo', None)
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
        logger.info(f"Redirecting {email} with role {user_role} to dashboard")
        
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

    # Get user data including profile photo
    user = UserModel.find_user_by_id(session['user_id'])
    return render_template('auth/profile.html', user=user)

@auth_bp.route('/upload-profile-photo', methods=['POST'])
def upload_profile_photo():
    """Upload and update user profile photo"""
    if 'user_id' not in session:
        logger.warning("Upload attempt without authentication")
        return jsonify({'success': False, 'error': 'Not authenticated'}), 401
    
    user_id = session['user_id']
    logger.info(f"Profile photo upload started for user {user_id}")
    
    try:
        if 'profile_photo' not in request.files:
            logger.warning(f"No file in request for user {user_id}")
            return jsonify({'success': False, 'error': 'No file selected'}), 400
        
        file = request.files['profile_photo']
        if file.filename == '':
            logger.warning(f"Empty filename for user {user_id}")
            return jsonify({'success': False, 'error': 'No file selected'}), 400
        
        logger.info(f"Processing file: {file.filename} for user {user_id}")
        
        # Check file type
        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
        if not ('.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in allowed_extensions):
            logger.warning(f"Invalid file type {file.filename} for user {user_id}")
            return jsonify({'success': False, 'error': 'Invalid file type. Please use PNG, JPG, JPEG, or GIF'}), 400
        
        # Create secure filename (always save as JPEG since we convert)
        filename = secure_filename(file.filename)
        user_id = session['user_id']
        new_filename = f"profile_{user_id}.jpg"
        
        # Create upload directory if it doesn't exist
        upload_dir = os.path.join('static', 'uploads', 'profile_photos')
        os.makedirs(upload_dir, exist_ok=True)
        
        file_path = os.path.join(upload_dir, new_filename)
        
        # Remove old profile photo if it exists
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                logger.info(f"Removed old profile photo: {file_path}")
            except Exception as e:
                logger.warning(f"Could not remove old profile photo {file_path}: {e}")
        
        # Save the uploaded file (already cropped from frontend)
        file.save(file_path)
        
        # The image is already cropped to 300x300 from frontend
        # Just optimize it for web display
        with Image.open(file_path) as img:
            # Convert to RGB if necessary (for JPEG compatibility)
            if img.mode in ('RGBA', 'LA', 'P'):
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = background
            
            # Save optimized image
            img.save(file_path, 'JPEG', optimize=True, quality=90)
        
        # Update user profile photo in database
        photo_url = f"/static/uploads/profile_photos/{new_filename}"
        logger.info(f"Updating database with photo URL: {photo_url} for user {user_id}")
        
        success = UserModel.update_profile_photo(user_id, photo_url)
        
        if success:
            # Update session with new photo
            session['profile_photo'] = photo_url
            logger.info(f"Profile photo successfully updated for user {user_id}")
            return jsonify({
                'success': True, 
                'message': 'Profile photo updated successfully',
                'photo_url': photo_url
            })
        else:
            logger.error(f"Database update failed for user {user_id}")
            return jsonify({'success': False, 'error': 'Failed to update profile photo in database'}), 500
            
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        logger.error(f"Error uploading profile photo: {e}")
        logger.error(f"Full traceback: {error_details}")
        return jsonify({'success': False, 'error': f'Upload error: {str(e)}'}), 500

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
        current_user = UserModel.find_user_by_id(user_id)

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

# Dashboard redirect removed - handled by rbac_routes.py
# All dashboard functionality is now centralized in RBAC routes

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