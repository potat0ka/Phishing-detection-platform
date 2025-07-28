"""
Admin Routes - Dashboard and Management
======================================

This blueprint handles admin-only routes:
- Admin dashboard
- Phishing data management
- Security tips management
- User management

Author: Bigendra Shrestha
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from functools import wraps
from models import PhishingModel, SecurityTipsModel, UserModel, AnalyticsModel
from utils.validation import validate_url
import logging

logger = logging.getLogger(__name__)

# Create blueprint for admin routes
admin_bp = Blueprint('admin', __name__)

def login_required(f):
    """
    Decorator to require user authentication
    
    This ensures only logged-in users can access protected routes
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """
    Decorator to require admin authentication
    
    This ensures only users with admin or superadmin role can access admin routes
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access admin area', 'error')
            return redirect(url_for('auth.login'))
        
        user_role = session.get('role', 'user')
        if user_role not in ['admin', 'superadmin']:
            flash('Admin access required for this feature', 'error')
            return redirect(url_for('rbac.user_dashboard'))
        
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/dashboard')
@login_required
def dashboard_redirect():
    """
    Redirect old dashboard route to proper RBAC dashboard based on user role
    """
    user_role = session.get('role', 'user')
    
    if user_role == 'superadmin':
        return redirect(url_for('rbac.superadmin_dashboard'))
    elif user_role == 'admin':
        return redirect(url_for('rbac.admin_dashboard'))
    else:
        return redirect(url_for('rbac.user_dashboard'))

@admin_bp.route('/admin-panel')
@admin_required
def admin_panel():
    """
    Admin panel - redirect to RBAC dashboard based on user role
    """
    user_role = session.get('role', 'user')
    
    if user_role == 'superadmin':
        return redirect(url_for('rbac.superadmin_dashboard'))
    elif user_role == 'admin':
        return redirect(url_for('rbac.admin_dashboard'))
    else:
        return redirect(url_for('rbac.user_dashboard'))

@admin_bp.route('/phishing/add', methods=['POST'])
@admin_required
def add_phishing_url():
    """
    Add new phishing URL to database
    
    Receives form data and adds new phishing threat to MongoDB
    """
    try:
        url = request.form.get('url', '').strip()
        category = request.form.get('category', 'phishing')
        status = request.form.get('status', 'active')
        description = request.form.get('description', '')
        confidence_score = float(request.form.get('confidence_score', 0.8))
        
        if not url or not validate_url(url):
            flash('Please enter a valid URL', 'error')
            return redirect(url_for('admin.admin_panel'))
        
        # Add to database
        result = PhishingModel.add_phishing_url(
            url=url,
            category=category,
            status=status,
            description=description,
            confidence_score=confidence_score
        )
        
        if result:
            flash('Phishing URL added successfully', 'success')
        else:
            flash('Failed to add phishing URL', 'error')
            
    except Exception as e:
        logger.error(f"Error adding phishing URL: {e}")
        flash('Error adding phishing URL', 'error')
    
    return redirect(url_for('admin.admin_panel'))

@admin_bp.route('/phishing/edit/<data_id>')
@admin_required
def edit_phishing_data(data_id):
    """
    Edit phishing data entry
    """
    try:
        # Get phishing data entry
        phishing_data = PhishingModel.get_all_phishing_data()
        current_entry = None
        
        for entry in phishing_data:
            if str(entry.get('_id')) == str(data_id):
                current_entry = entry
                break
        
        if not current_entry:
            flash('Phishing data entry not found', 'error')
            return redirect(url_for('admin.admin_panel'))
        
        return render_template('admin/edit_phishing.html', entry=current_entry)
        
    except Exception as e:
        logger.error(f"Error loading phishing data for edit: {e}")
        flash('Error loading phishing data', 'error')
        return redirect(url_for('admin.admin_panel'))

@admin_bp.route('/phishing/update/<data_id>', methods=['POST'])
@admin_required
def update_phishing_data(data_id):
    """
    Update phishing data entry
    """
    try:
        url = request.form.get('url', '').strip()
        category = request.form.get('category', 'phishing')
        status = request.form.get('status', 'active')
        description = request.form.get('description', '')
        confidence_score = float(request.form.get('confidence_score', 0.8))
        
        if not url or not validate_url(url):
            flash('Please enter a valid URL', 'error')
            return redirect(url_for('admin.edit_phishing_data', data_id=data_id))
        
        # Update in database
        result = PhishingModel.update_phishing_url(
            data_id=data_id,
            url=url,
            category=category,
            status=status,
            description=description,
            confidence_score=confidence_score
        )
        
        if result:
            flash('Phishing URL updated successfully', 'success')
            return redirect(url_for('admin.admin_panel'))
        else:
            flash('Failed to update phishing URL', 'error')
            return redirect(url_for('admin.edit_phishing_data', data_id=data_id))
            
    except Exception as e:
        logger.error(f"Error updating phishing URL: {e}")
        flash('Error updating phishing URL', 'error')
        return redirect(url_for('admin.edit_phishing_data', data_id=data_id))

@admin_bp.route('/phishing/delete', methods=['POST'])
@admin_required
def delete_phishing_url():
    """
    Delete phishing URL from database
    """
    try:
        url = request.form.get('url', '').strip()
        
        if not url:
            flash('URL is required', 'error')
            return redirect(url_for('admin.admin_panel'))
        
        result = PhishingModel.delete_phishing_url(url)
        
        if result > 0:
            flash('Phishing URL deleted successfully', 'success')
        else:
            flash('Failed to delete phishing URL', 'error')
            
    except Exception as e:
        logger.error(f"Error deleting phishing URL: {e}")
        flash('Error deleting phishing URL', 'error')
    
    return redirect(url_for('admin.admin_panel'))

@admin_bp.route('/tips/add', methods=['POST'])
@admin_required
def add_security_tip():
    """
    Add new security tip to database
    """
    try:
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        category = request.form.get('category', 'general')
        difficulty = request.form.get('difficulty', 'beginner')
        
        if not title or not content:
            flash('Title and content are required', 'error')
            return redirect(url_for('admin.admin_panel'))
        
        result = SecurityTipsModel.add_tip(title, content, category, difficulty)
        
        if result:
            flash('Security tip added successfully', 'success')
        else:
            flash('Failed to add security tip', 'error')
            
    except Exception as e:
        logger.error(f"Error adding security tip: {e}")
        flash('Error adding security tip', 'error')
    
    return redirect(url_for('admin.admin_panel'))

@admin_bp.route('/tips/edit/<tip_id>', methods=['POST'])
@admin_required
def edit_security_tip(tip_id):
    """Edit existing security tip"""
    try:
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        category = request.form.get('category', 'general')
        difficulty = request.form.get('difficulty', 'beginner')
        
        if not title or not content:
            flash('Title and content are required', 'error')
            return redirect(url_for('admin.admin_panel'))
        
        result = SecurityTipsModel.update_tip(tip_id, title, content, category, difficulty)
        
        if result:
            flash('Security tip updated successfully', 'success')
        else:
            flash('Failed to update security tip', 'error')
            
    except Exception as e:
        logger.error(f"Error updating security tip: {e}")
        flash('Error updating security tip', 'error')
    
    return redirect(url_for('admin.admin_panel'))

@admin_bp.route('/tips/delete/<tip_id>', methods=['POST'])
@admin_required
def delete_security_tip(tip_id):
    """Delete security tip"""
    try:
        result = SecurityTipsModel.delete_tip(tip_id)
        
        if result:
            flash('Security tip deleted successfully', 'success')
        else:
            flash('Failed to delete security tip', 'error')
            
    except Exception as e:
        logger.error(f"Error deleting security tip: {e}")
        flash('Error deleting security tip', 'error')
    
    return redirect(url_for('admin.admin_panel'))

@admin_bp.route('/users')
@admin_required
def manage_users():
    """
    User management page
    """
    try:
        users = UserModel.get_all_users()
        return render_template('admin/users.html', users=users)
        
    except Exception as e:
        logger.error(f"Error loading users: {e}")
        flash('Error loading user data', 'error')
        return render_template('admin/users.html', users=[])

@admin_bp.route('/users/role', methods=['POST'])
@admin_required
def update_user_role():
    """
    Update user role
    """
    try:
        user_id = request.form.get('user_id')
        new_role = request.form.get('role')
        
        if not user_id or not new_role:
            flash('User ID and role are required', 'error')
            return redirect(url_for('admin.admin_panel'))
        
        result = UserModel.update_user_role(user_id, new_role)
        
        if result > 0:
            flash('User role updated successfully', 'success')
        else:
            flash('Failed to update user role', 'error')
            
    except Exception as e:
        logger.error(f"Error updating user role: {e}")
        flash('Error updating user role', 'error')
    
    return redirect(url_for('admin.admin_panel'))

@admin_bp.route('/api/stats')
@admin_required
def api_get_stats():
    """
    API endpoint to get real-time statistics for dashboard
    """
    try:
        stats = AnalyticsModel.get_system_stats()
        detection_stats = AnalyticsModel.get_detection_stats()
        
        return jsonify({
            'system_stats': stats,
            'detection_stats': detection_stats,
            'status': 'success'
        })
        
    except Exception as e:
        logger.error(f"API stats error: {e}")
        return jsonify({'error': 'Failed to fetch statistics'}), 500