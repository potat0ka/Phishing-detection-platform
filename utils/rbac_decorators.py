"""
Role-Based Access Control Decorators - Fixed Version
===================================================

This module provides decorators for securing routes based on user roles and permissions.
It implements comprehensive access control for the phishing detection platform.

Author: AI Assistant
"""

from functools import wraps
from flask import session, flash, redirect, url_for, request, jsonify
from models.rbac_model import RBACModel
import logging

logger = logging.getLogger(__name__)

def is_ajax_request():
    """Check if the request is an AJAX/JSON request"""
    return (request.headers.get('X-Requested-With') == 'XMLHttpRequest' or 
            request.content_type == 'application/json')

def login_required(f):
    """
    Decorator to require user authentication
    
    This ensures only logged-in users can access protected routes
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            # For API requests, return JSON error (check for AJAX/JSON requests)
            if is_ajax_request():
                return jsonify({'error': 'Authentication required', 'redirect': '/auth/login'}), 401
            
            flash('Please log in to access this page', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def role_required(*allowed_roles):
    """
    Decorator to require specific roles
    
    Args:
        *allowed_roles: Variable number of role names that are allowed to access the route
        
    Example:
        @role_required('admin', 'superadmin')
        def admin_only_route():
            pass
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                # For API requests, return JSON error
                if is_ajax_request():
                    return jsonify({'error': 'Authentication required', 'redirect': '/auth/login'}), 401
                
                flash('Please log in to access this page', 'error')
                return redirect(url_for('auth.login'))
            
            user_role = session.get('role', 'user')
            if user_role not in allowed_roles:
                # For API requests, return JSON error
                if is_ajax_request():
                    return jsonify({'error': 'Insufficient permissions', 'required_roles': list(allowed_roles)}), 403
                
                # Convert allowed_roles to list of strings for proper joining
                allowed_roles_list = [str(role) for role in allowed_roles]
                flash(f'Access denied. Required role: {" or ".join(allowed_roles_list)}', 'error')
                return redirect(url_for('rbac.user_dashboard'))
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def permission_required(*permissions):
    """
    Decorator to require specific permissions
    
    Args:
        *permissions: Variable number of permission names required to access the route
        
    Example:
        @permission_required('manage_users', 'view_system_stats')
        def user_management_route():
            pass
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                if is_ajax_request():
                    return jsonify({'error': 'Authentication required', 'redirect': '/auth/login'}), 401
                
                flash('Please log in to access this page', 'error')
                return redirect(url_for('auth.login'))
            
            user_role = session.get('role', 'user')
            
            # Check if user has all required permissions
            for permission in permissions:
                if not RBACModel.has_permission(user_role, permission):
                    if is_ajax_request():
                        return jsonify({
                            'error': f'Permission denied: {permission}', 
                            'required_permissions': list(permissions)
                        }), 403
                    
                    flash(f'Access denied. Missing permission: {permission}', 'error')
                    return redirect(url_for('admin.user_dashboard'))
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def admin_required(f):
    """
    Decorator to require admin or superadmin role
    
    This is a convenience decorator for admin-only routes
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            if is_ajax_request():
                return jsonify({'error': 'Authentication required', 'redirect': '/auth/login'}), 401
            
            flash('Please log in to access admin area', 'error')
            return redirect(url_for('auth.login'))
        
        user_role = session.get('role', 'user')
        if user_role not in ['admin', 'superadmin']:
            if is_ajax_request():
                return jsonify({'error': 'Admin access required'}), 403
            
            flash('Admin access required for this feature', 'error')
            return redirect(url_for('admin.user_dashboard'))
        
        return f(*args, **kwargs)
    return decorated_function

def superadmin_required(f):
    """
    Decorator to require superadmin role only
    
    This is for the most sensitive operations
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            if is_ajax_request():
                return jsonify({'error': 'Authentication required', 'redirect': '/auth/login'}), 401
            
            flash('Please log in to access this area', 'error')
            return redirect(url_for('auth.login'))
        
        user_role = session.get('role', 'user')
        if user_role != 'superadmin':
            if is_ajax_request():
                return jsonify({'error': 'Superadmin access required'}), 403
            
            flash('Superadmin access required for this feature', 'error')
            return redirect(url_for('admin.user_dashboard'))
        
        return f(*args, **kwargs)
    return decorated_function

def can_manage_user_role(target_user_role):
    """
    Decorator to check if current user can manage a user with target_user_role
    
    Args:
        target_user_role: The role of the user being managed
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                if is_ajax_request():
                    return jsonify({'error': 'Authentication required'}), 401
                
                flash('Please log in', 'error')
                return redirect(url_for('auth.login'))
            
            current_role = session.get('role', 'user')
            
            if not RBACModel.can_manage_user(current_role, target_user_role):
                if is_ajax_request():
                    return jsonify({'error': f'Cannot manage {target_user_role} users'}), 403
                
                flash(f'You cannot manage {target_user_role} users', 'error')
                return redirect(url_for('admin.user_dashboard'))
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def log_admin_action(action_description):
    """
    Decorator to automatically log administrative actions
    
    Args:
        action_description: Description of the action being performed
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Execute the function first
            result = f(*args, **kwargs)
            
            # Log the action if successful (assuming 200 status or no error response)
            try:
                user_id = session.get('user_id')
                if user_id:
                    # Extract target user ID from request if available
                    target_user_id = request.form.get('user_id') or request.form.get('target_user_id')
                    
                    # Extract additional details from request
                    details = {
                        'method': request.method,
                        'endpoint': request.endpoint,
                        'form_data': dict(request.form) if request.form else None,
                        'args': dict(request.args) if request.args else None
                    }
                    
                    RBACModel.log_admin_action(
                        user_id=user_id,
                        action=action_description,
                        target_user_id=target_user_id,
                        details=details
                    )
            except Exception as e:
                logger.error(f"Failed to log admin action: {e}")
            
            return result
        return decorated_function
    return decorator

# Helper functions for templates
def get_current_user_role():
    """Get current user's role from session"""
    return session.get('role', 'user')

def current_user_can(permission):
    """Check if current user has a specific permission"""
    user_role = session.get('role', 'user')
    return RBACModel.has_permission(user_role, permission)

def current_user_can_manage(target_role):
    """Check if current user can manage users with target role"""
    current_role = session.get('role', 'user')
    return RBACModel.can_manage_user(current_role, target_role)

# Make functions available to templates
def init_template_globals(app):
    """Initialize template global functions"""
    app.jinja_env.globals.update(
        get_current_user_role=get_current_user_role,
        current_user_can=current_user_can,
        current_user_can_manage=current_user_can_manage,
        rbac_roles=RBACModel.ROLES
    )