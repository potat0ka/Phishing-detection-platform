"""
Role-Based Access Control Routes
===============================

This blueprint handles RBAC-specific routes:
- Password reset requests and approvals
- User role management
- Model uploads
- Admin user management
- Audit logging

Author: AI Assistant
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.utils import secure_filename
from utils.rbac_decorators import (
    login_required, role_required, permission_required, 
    admin_required, superadmin_required, log_admin_action
)
from models.rbac_model import RBACModel
from models.user_model import UserModel
from models.safety_tips_model import SafetyTipsModel
from models.database import db
from datetime import datetime
import logging
import os

logger = logging.getLogger(__name__)

# Create blueprint for RBAC routes
rbac_bp = Blueprint('rbac', __name__, url_prefix='/rbac')

@rbac_bp.route('/password-reset/request', methods=['POST'])
@login_required
def request_password_reset():
    """Request password reset for current user"""
    try:
        user_id = session.get('user_id')
        user_role = session.get('role', 'user')

        # Create password reset request
        request_id = RBACModel.create_password_reset_request(user_id, user_role)

        if request_id:
            flash('Password reset request submitted. An admin will review your request.', 'info')
        else:
            flash('Failed to submit password reset request. Please try again.', 'error')

        return redirect(url_for('rbac.user_dashboard'))

    except Exception as e:
        logger.error(f"Error requesting password reset: {e}")
        flash('Error submitting password reset request', 'error')
        return redirect(url_for('rbac.user_dashboard'))

@rbac_bp.route('/superadmin-dashboard')
@role_required('superadmin')
def superadmin_dashboard():
    """Super Admin dashboard with full platform control"""
    try:
        # Get comprehensive statistics for super admin
        stats = {
            'total_users': UserModel.get_user_count(),
            'total_admins': UserModel.get_admin_count(),
            'total_superadmins': UserModel.get_superadmin_count(),
            'pending_password_resets': len(RBACModel.get_pending_password_reset_requests()),
            'recent_uploads': RBACModel.get_model_uploads()[:5],
            'system_health': 'Operational'
        }

        # Get all users for management
        all_users = UserModel.get_all_users()

        # Add template context functions
        def get_current_user_role():
            return session.get('role', 'user')

        def current_user_can(permission):
            user_role = session.get('role', 'user')
            return RBACModel.has_permission(user_role, permission)

        return render_template('admin/rbac_dashboard.html', 
                             stats=stats, 
                             users=all_users,
                             current_time=datetime.utcnow(),
                             get_current_user_role=get_current_user_role,
                             current_user_can=current_user_can)
    except Exception as e:
        logger.error(f"Error loading superadmin dashboard: {e}")
        flash('Error loading dashboard', 'error')
        return redirect(url_for('main.index'))

@rbac_bp.route('/admin-dashboard')
@role_required('admin', 'superadmin')
def admin_dashboard():
    """Admin dashboard with user management capabilities"""
    try:
        current_role = session.get('role')

        # Get statistics appropriate for admin level
        stats = {
            'total_users': UserModel.get_user_count(),
            'pending_password_resets': len(RBACModel.get_pending_password_reset_requests()),
            'recent_scans': 25,  # Will be implemented with scan history
            'active_models': 3
        }

        # Admins can only see regular users, superadmins see all
        if current_role == 'superadmin':
            manageable_users = UserModel.get_all_users()
        else:
            manageable_users = UserModel.get_users_by_role('user')

        # Add template context functions
        def get_current_user_role():
            return session.get('role', 'user')

        def current_user_can(permission):
            user_role = session.get('role', 'user')
            return RBACModel.has_permission(user_role, permission)

        # Generate navigation URLs for admin dashboard
        nav_urls = {
            'dashboard': url_for('rbac.admin_dashboard'),
            'users': url_for('rbac.manage_users'),
            'phishing': url_for('main.index'),  # Fixed: redirect to main page for now
            'safety_tips': url_for('main.tips'),  # Fixed: redirect to tips page
            'check': url_for('main.check'),
            'analyze': url_for('main.analyze_media')
        }

        return render_template('admin/rbac_dashboard.html', 
                             stats=stats, 
                             users=manageable_users,
                             current_role=current_role,
                             current_time=datetime.utcnow(),
                             get_current_user_role=get_current_user_role,
                             current_user_can=current_user_can,
                             nav_urls=nav_urls)
    except Exception as e:
        logger.error(f"Error loading admin dashboard: {e}")
        flash('Error loading dashboard', 'error')
        return redirect(url_for('main.index'))

@rbac_bp.route('/user-dashboard')
@login_required
def user_dashboard():
    """User dashboard with personal scan history and tools"""
    try:
        user_id = session.get('user_id')
        username = session.get('username')

        # Get user-specific statistics
        stats = {
            'total_scans': 0,  # Will implement with scan history
            'clean_results': 0,
            'phishing_detected': 0,
            'last_scan': 'Never'
        }

        # Get recent scan history for this user
        recent_scans = []  # Will implement with scan history model

        # Add template context functions
        def get_current_user_role():
            return session.get('role', 'user')

        def current_user_can(permission):
            user_role = session.get('role', 'user')
            return RBACModel.has_permission(user_role, permission)

        return render_template('admin/rbac_dashboard.html', 
                             stats=stats, 
                             recent_scans=recent_scans,
                             username=username,
                             current_time=datetime.utcnow(),
                             get_current_user_role=get_current_user_role,
                             current_user_can=current_user_can)
    except Exception as e:
        logger.error(f"Error loading user dashboard: {e}")
        flash('Error loading dashboard', 'error')
        return redirect(url_for('main.index'))

@rbac_bp.route('/password-reset/requests')
@permission_required('reset_user_passwords')
def view_password_reset_requests():
    """View pending password reset requests (admin/superadmin only)"""
    try:
        pending_requests = RBACModel.get_pending_password_reset_requests()

        # Get user details for each request
        requests_with_users = []
        for req in pending_requests:
            user = UserModel.find_user_by_id(req['user_id'])
            if user:
                req['user_info'] = {
                    'username': user.get('username'),
                    'email': user.get('email'),
                    'role': user.get('role')
                }
                requests_with_users.append(req)

        return render_template('admin/password_reset_requests.html', 
                             requests=requests_with_users)

    except Exception as e:
        logger.error(f"Error viewing password reset requests: {e}")
        flash('Error loading password reset requests', 'error')
        return redirect(url_for('main.index'))

@rbac_bp.route('/upload-model', methods=['POST'])
@permission_required('upload_models')
def upload_model_legacy():
    """Upload ML model (admin/superadmin only)"""
    try:
        if 'model_file' not in request.files:
            flash('No file selected', 'error')
            return redirect(request.referrer or url_for('rbac.superadmin_dashboard'))

        file = request.files['model_file']
        if file.filename == '':
            flash('No file selected', 'error')
            return redirect(request.referrer or url_for('rbac.superadmin_dashboard'))

        if file and file.filename and allowed_file(file.filename, ['pkl', 'joblib', 'h5']):
            filename = secure_filename(file.filename)
            upload_path = os.path.join('data/models', filename)

            # Ensure models directory exists
            os.makedirs(os.path.dirname(upload_path), exist_ok=True)

            # Save the file
            file.save(upload_path)

            # Log the upload
            upload_record = {
                'filename': filename,
                'upload_date': datetime.utcnow().isoformat(),
                'uploaded_by': session.get('username'),
                'file_path': upload_path,
                'status': 'active'
            }

            # Store upload record
            if db and db.connected:
                db.insert_document('model_uploads', upload_record)

            flash(f'Model {filename} uploaded successfully', 'success')
            logger.info(f"Model uploaded: {filename} by {session.get('username')}")

        else:
            flash('Invalid file type. Please upload .pkl, .joblib, or .h5 files', 'error')

    except Exception as e:
        logger.error(f"Error uploading model: {e}")
        flash('Error uploading model', 'error')

    return redirect(request.referrer or url_for('rbac.superadmin_dashboard'))

@rbac_bp.route('/update-safety-tips', methods=['POST'])
@permission_required('manage_content')
def update_safety_tips():
    """Update safety tips (admin/superadmin only)"""
    try:
        safety_tip = request.form.get('safety_tip', '').strip()
        tip_category = request.form.get('tip_category', 'general')

        if not safety_tip:
            flash('Safety tip content is required', 'error')
            return redirect(request.referrer or url_for('rbac.superadmin_dashboard'))

        tip_record = {
            'content': safety_tip,
            'category': tip_category,
            'created_date': datetime.utcnow().isoformat(),
            'created_by': session.get('username'),
            'is_active': True
        }

        # Store safety tip
        if db and db.connected:
            db.insert_document('safety_tips', tip_record)
        else:
            # File-based fallback
            import json
            tips_file = 'data/safety_tips.json'
            os.makedirs(os.path.dirname(tips_file), exist_ok=True)

            if os.path.exists(tips_file):
                with open(tips_file, 'r') as f:
                    tips = json.load(f)
            else:
                tips = []

            tip_record['_id'] = len(tips) + 1
            tips.append(tip_record)

            with open(tips_file, 'w') as f:
                json.dump(tips, f, indent=2)

        flash(f'Safety tip added to {tip_category} category', 'success')
        logger.info(f"Safety tip added by {session.get('username')}: {tip_category}")

    except Exception as e:
        logger.error(f"Error updating safety tips: {e}")
        flash('Error adding safety tip', 'error')

    return redirect(request.referrer or url_for('rbac.superadmin_dashboard'))

@rbac_bp.route('/create-user', methods=['POST'])
@permission_required('manage_users')
def create_user_legacy():
    """Create new user (admin/superadmin only)"""
    try:
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        role = request.form.get('role', 'user')

        current_role = session.get('role')

        # Role validation: admins can't create superadmins
        if current_role == 'admin' and role == 'superadmin':
            flash('Admins cannot create super admin accounts', 'error')
            return redirect(request.referrer or url_for('rbac.admin_dashboard'))

        # Validate input
        if not username or not email or not password:
            flash('All fields are required', 'error')
            return redirect(request.referrer or url_for('rbac.superadmin_dashboard'))

        # Create user using existing UserModel
        user_id = UserModel.create_user(username, email, password, role)

        if user_id:
            flash(f'User {username} created successfully as {role}', 'success')
            logger.info(f"User created: {username} ({role}) by {session.get('username')}")
        else:
            flash('Failed to create user. Username or email may already exist.', 'error')

    except Exception as e:
        logger.error(f"Error creating user: {e}")
        flash('Error creating user', 'error')

    return redirect(request.referrer or url_for('rbac.superadmin_dashboard'))

def allowed_file(filename, extensions):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in extensions

@rbac_bp.route('/password-reset/approve', methods=['POST'])
@permission_required('reset_user_passwords')
@log_admin_action('Approved password reset request')
def approve_password_reset():
    """Approve password reset request"""
    try:
        request_id = request.form.get('request_id')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        if not request_id or not new_password:
            flash('Request ID and new password are required', 'error')
            return redirect(url_for('rbac.view_password_reset_requests'))

        if new_password != confirm_password:
            flash('Passwords do not match', 'error')
            return redirect(url_for('rbac.view_password_reset_requests'))

        if len(new_password) < 8:
            flash('Password must be at least 8 characters long', 'error')
            return redirect(url_for('rbac.view_password_reset_requests'))

        approved_by = session.get('user_id')
        success = RBACModel.approve_password_reset(request_id, approved_by, new_password)

        if success:
            flash('Password reset approved successfully', 'success')
        else:
            flash('Failed to approve password reset', 'error')

        return redirect(url_for('rbac.view_password_reset_requests'))

    except Exception as e:
        logger.error(f"Error approving password reset: {e}")
        flash('Error approving password reset', 'error')
        return redirect(url_for('rbac.view_password_reset_requests'))

@rbac_bp.route('/password-reset/decline', methods=['POST'])
@permission_required('reset_user_passwords')
@log_admin_action('Declined password reset request')
def decline_password_reset():
    """Decline a password reset request"""
    try:
        request_id = request.form.get('request_id')

        if not request_id:
            flash('Request ID is required', 'error')
            return redirect(url_for('rbac.view_password_reset_requests'))

        # Update request status to declined
        success = RBACModel.decline_password_reset(request_id, session.get('user_id'))

        if success:
            flash('Password reset request declined successfully', 'success')
        else:
            flash('Failed to decline password reset request', 'error')

        return redirect(url_for('rbac.view_password_reset_requests'))

    except Exception as e:
        logger.error(f"Error declining password reset: {e}")
        flash('Error processing password reset decline', 'error')
        return redirect(url_for('rbac.view_password_reset_requests'))

@rbac_bp.route('/users/manage')
@permission_required('manage_users')
def manage_users():
    """User management interface"""
    try:
        users = UserModel.get_all_users()
        current_role = session.get('role', 'user')

        # Filter users based on current user's permissions
        manageable_users = []
        for user in users:
            if RBACModel.can_manage_user(current_role, user.get('role', 'user')):
                manageable_users.append(user)

        return render_template('admin/manage_users.html', 
                             users=manageable_users,
                             current_role=current_role)

    except Exception as e:
        logger.error(f"Error loading user management: {e}")
        flash('Error loading user management', 'error')
        return render_template('admin/manage_users.html', users=[], current_role='user')

@rbac_bp.route('/users/create', methods=['POST'])
@permission_required('manage_users')
@log_admin_action('Created new user')
def create_user():
    """Create new user (admin/superadmin only)"""
    try:
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        role = request.form.get('role', 'user')

        current_role = session.get('role', 'user')

        # Validate that current user can create users with this role
        if not RBACModel.can_manage_user(current_role, role):
            flash(f'You cannot create {role} users', 'error')
            return redirect(url_for('rbac.manage_users'))

        # Validate input
        if not username or not email or not password:
            flash('All fields are required', 'error')
            return redirect(url_for('rbac.manage_users'))

        # Check if user already exists
        if UserModel.find_user_by_email(email):
            flash('Email already exists', 'error')
            return redirect(url_for('rbac.manage_users'))

        if UserModel.find_user_by_username(username):
            flash('Username already exists', 'error')
            return redirect(url_for('rbac.manage_users'))

        # Create user
        user_id = UserModel.create_user(username, email, password, role)

        if user_id:
            flash(f'User {username} created successfully with role {role}', 'success')
        else:
            flash('Failed to create user', 'error')

        return redirect(url_for('rbac.manage_users'))

    except Exception as e:
        logger.error(f"Error creating user: {e}")
        flash('Error creating user', 'error')
        return redirect(url_for('rbac.manage_users'))

@rbac_bp.route('/users/update-role', methods=['POST'])
@permission_required('manage_users')
@log_admin_action('Updated user role')
def update_user_role():
    """Update user role"""
    try:
        user_id = request.form.get('user_id')
        new_role = request.form.get('new_role')

        current_role = session.get('role', 'user')

        if not user_id or not new_role:
            flash('User ID and new role are required', 'error')
            return redirect(url_for('rbac.manage_users'))

        # Get target user
        target_user = UserModel.find_user_by_id(user_id)
        if not target_user:
            flash('User not found', 'error')
            return redirect(url_for('rbac.manage_users'))

        current_target_role = target_user.get('role', 'user')

        # Check permissions
        if not RBACModel.can_manage_user(current_role, current_target_role):
            flash(f'You cannot manage {current_target_role} users', 'error')
            return redirect(url_for('rbac.manage_users'))

        if not RBACModel.can_manage_user(current_role, new_role):
            flash(f'You cannot assign {new_role} role', 'error')
            return redirect(url_for('rbac.manage_users'))

        # Update role
        success = UserModel.update_user_role(user_id, new_role)

        if success:
            flash(f'User role updated to {new_role}', 'success')
        else:
            flash('Failed to update user role', 'error')

        return redirect(url_for('rbac.manage_users'))

    except Exception as e:
        logger.error(f"Error updating user role: {e}")
        flash('Error updating user role', 'error')
        return redirect(url_for('rbac.manage_users'))

@rbac_bp.route('/users/deactivate', methods=['POST'])
@permission_required('manage_users')
@log_admin_action('Deactivated user')
def deactivate_user():
    """Deactivate user account"""
    try:
        user_id = request.form.get('user_id')
        current_role = session.get('role', 'user')

        if not user_id:
            flash('User ID is required', 'error')
            return redirect(url_for('rbac.manage_users'))

        # Get target user
        target_user = UserModel.find_user_by_id(user_id)
        if not target_user:
            flash('User not found', 'error')
            return redirect(url_for('rbac.manage_users'))

        target_role = target_user.get('role', 'user')

        # Check permissions
        if not RBACModel.can_manage_user(current_role, target_role):
            flash(f'You cannot deactivate {target_role} users', 'error')
            return redirect(url_for('rbac.manage_users'))

        # Deactivate user
        success = UserModel.deactivate_user(user_id)

        if success:
            flash('User deactivated successfully', 'success')
        else:
            flash('Failed to deactivate user', 'error')

        return redirect(url_for('rbac.manage_users'))

    except Exception as e:
        logger.error(f"Error deactivating user: {e}")
        flash('Error deactivating user', 'error')
        return redirect(url_for('rbac.manage_users'))

@rbac_bp.route('/models/upload')
@permission_required('upload_models')
def model_upload_page():
    """Model upload interface"""
    try:
        uploaded_models = RBACModel.get_model_uploads()
        return render_template('admin/model_upload.html', models=uploaded_models)

    except Exception as e:
        logger.error(f"Error loading model upload page: {e}")
        flash('Error loading model upload page', 'error')
        return render_template('admin/model_upload.html', models=[])

@rbac_bp.route('/models/upload', methods=['POST'])
@permission_required('upload_models')
@log_admin_action('Uploaded ML model')
def upload_model():
    """Upload ML model file"""
    try:
        if 'model_file' not in request.files:
            flash('No file selected', 'error')
            return redirect(url_for('rbac.model_upload_page'))

        file = request.files['model_file']
        model_type = request.form.get('model_type', '').strip()

        if file.filename == '':
            flash('No file selected', 'error')
            return redirect(url_for('rbac.model_upload_page'))

        if not model_type:
            flash('Model type is required', 'error')
            return redirect(url_for('rbac.model_upload_page'))

        uploaded_by = session.get('user_id')
        result = RBACModel.save_uploaded_model(file, model_type, uploaded_by)

        if result:
            flash(f'Model {file.filename} uploaded successfully', 'success')
        else:
            flash('Failed to upload model', 'error')

        return redirect(url_for('rbac.model_upload_page'))

    except Exception as e:
        logger.error(f"Error uploading model: {e}")
        flash('Error uploading model', 'error')
        return redirect(url_for('rbac.model_upload_page'))

@rbac_bp.route('/models/activate', methods=['POST'])
@permission_required('upload_models')
@log_admin_action('Activated ML model')
def activate_model():
    """Activate uploaded model"""
    try:
        upload_id = request.form.get('upload_id')

        if not upload_id:
            flash('Upload ID is required', 'error')
            return redirect(url_for('rbac.model_upload_page'))

        activated_by = session.get('user_id')
        success = RBACModel.activate_model(upload_id, activated_by)

        if success:
            flash('Model activated successfully', 'success')
        else:
            flash('Failed to activate model', 'error')

        return redirect(url_for('rbac.model_upload_page'))

    except Exception as e:
        logger.error(f"Error activating model: {e}")
        flash('Error activating model', 'error')
        return redirect(url_for('rbac.model_upload_page'))

# Safety Tips Management Routes
@rbac_bp.route('/safety-tips/manage')
@permission_required('manage_content')
def manage_safety_tips():
    """Safety tips management interface"""
    try:
        # Get all tips organized by category
        url_tips = SafetyTipsModel.get_tips_by_category('url')
        email_tips = SafetyTipsModel.get_tips_by_category('email')
        general_tips = SafetyTipsModel.get_tips_by_category('general')

        return render_template('admin/manage_safety_tips.html', 
                             url_tips=url_tips,
                             email_tips=email_tips,
                             general_tips=general_tips,
                             categories=SafetyTipsModel.CATEGORIES)

    except Exception as e:
        logger.error(f"Error loading safety tips management: {e}")
        flash('Error loading safety tips', 'error')
        return render_template('admin/manage_safety_tips.html', 
                             url_tips=[], email_tips=[], general_tips=[],
                             categories=SafetyTipsModel.CATEGORIES)

@rbac_bp.route('/safety-tips/add', methods=['POST'])
@permission_required('manage_content')
@log_admin_action('Added safety tip')
def add_safety_tip():
    """Add new safety tip"""
    try:
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        category = request.form.get('category', '').strip()

        if not title or not content or not category:
            flash('Title, content, and category are required', 'error')
            return redirect(url_for('rbac.manage_safety_tips'))

        if category not in SafetyTipsModel.CATEGORIES:
            flash('Invalid category selected', 'error')
            return redirect(url_for('rbac.manage_safety_tips'))

        created_by = session.get('username', 'admin')
        result = SafetyTipsModel.add_tip(title, content, category, created_by)

        if result:
            flash(f'Safety tip added to {category} category successfully', 'success')
        else:
            flash('Failed to add safety tip', 'error')

        return redirect(url_for('rbac.manage_safety_tips'))

    except Exception as e:
        logger.error(f"Error adding safety tip: {e}")
        flash('Error adding safety tip', 'error')
        return redirect(url_for('rbac.manage_safety_tips'))

@rbac_bp.route('/safety-tips/edit/<tip_id>', methods=['GET', 'POST'])
@permission_required('manage_content')
def edit_safety_tip(tip_id):
    """Edit existing safety tip"""
    if request.method == 'GET':
        try:
            tip = SafetyTipsModel.get_tip_by_id(tip_id)
            if not tip:
                flash('Safety tip not found', 'error')
                return redirect(url_for('rbac.manage_safety_tips'))

            return render_template('admin/edit_safety_tip.html', 
                                 tip=tip, 
                                 categories=SafetyTipsModel.CATEGORIES)
        except Exception as e:
            logger.error(f"Error loading tip for editing: {e}")
            flash('Error loading safety tip', 'error')
            return redirect(url_for('rbac.manage_safety_tips'))

    # POST request - update tip
    try:
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        category = request.form.get('category', '').strip()

        if not title or not content or not category:
            flash('Title, content, and category are required', 'error')
            return redirect(url_for('rbac.edit_safety_tip', tip_id=tip_id))

        if category not in SafetyTipsModel.CATEGORIES:
            flash('Invalid category selected', 'error')
            return redirect(url_for('rbac.edit_safety_tip', tip_id=tip_id))

        success = SafetyTipsModel.update_tip(tip_id, title, content, category)

        if success:
            flash('Safety tip updated successfully', 'success')
        else:
            flash('Failed to update safety tip', 'error')

        return redirect(url_for('rbac.manage_safety_tips'))

    except Exception as e:
        logger.error(f"Error updating safety tip: {e}")
        flash('Error updating safety tip', 'error')
        return redirect(url_for('rbac.manage_safety_tips'))

@rbac_bp.route('/safety-tips/delete', methods=['POST'])
@permission_required('manage_content')
@log_admin_action('Deleted safety tip')
def delete_safety_tip():
    """Delete safety tip"""
    try:
        tip_id = request.form.get('tip_id')

        if not tip_id:
            flash('Tip ID is required', 'error')
            return redirect(url_for('rbac.manage_safety_tips'))

        success = SafetyTipsModel.delete_tip(tip_id)

        if success:
            flash('Safety tip deleted successfully', 'success')
        else:
            flash('Failed to delete safety tip', 'error')

        return redirect(url_for('rbac.manage_safety_tips'))

    except Exception as e:
        logger.error(f"Error deleting safety tip: {e}")
        flash('Error deleting safety tip', 'error')
        return redirect(url_for('rbac.manage_safety_tips'))

@rbac_bp.route('/api/user-permissions')
@login_required
def api_user_permissions():
    """API endpoint to get current user's permissions"""
    try:
        user_role = session.get('role', 'user')
        permissions = RBACModel.ROLES.get(user_role, {}).get('permissions', [])

        return jsonify({
            'role': user_role,
            'permissions': permissions,
            'can_manage_users': RBACModel.has_permission(user_role, 'manage_users'),
            'can_upload_models': RBACModel.has_permission(user_role, 'upload_models'),
            'can_reset_passwords': RBACModel.has_permission(user_role, 'reset_user_passwords')
        })

    except Exception as e:
        logger.error(f"Error getting user permissions: {e}")
        return jsonify({'error': 'Failed to get permissions'}), 500

# Initialize superadmin account if it doesn't exist
@rbac_bp.route('/initialize-superadmin', methods=['GET', 'POST'])
def initialize_superadmin():
    """One-time initialization of superadmin account"""
    # Check if any superadmin already exists
    users = UserModel.get_all_users()
    superadmin_exists = any(user.get('role') == 'superadmin' for user in users)

    if request.method == 'GET':
        if superadmin_exists:
            flash('Superadmin account already exists', 'info')
            return redirect(url_for('auth.login'))
        return render_template('auth/init_superadmin.html')

    # POST request - create superadmin
    try:
        if superadmin_exists:
            flash('Superadmin account already exists', 'error')
            return redirect(url_for('auth.login'))

        # Create default superadmin
        username = request.form.get('username', 'superadmin')
        email = request.form.get('email', 'admin@phishingdetector.com')
        password = request.form.get('password', 'SuperAdmin123!')

        user_id = UserModel.create_user(username, email, password, 'superadmin')

        if user_id:
            flash('Superadmin account created successfully', 'success')
            logger.info(f"Superadmin account created: {username}")
        else:
            flash('Failed to create superadmin account', 'error')

        return redirect(url_for('auth.login'))

    except Exception as e:
        logger.error(f"Error initializing superadmin: {e}")
        flash('Error creating superadmin account', 'error')
        return redirect(url_for('main.index'))