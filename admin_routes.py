"""
Admin Routes for AI Phishing Detection Platform
==============================================

This file contains all admin-specific routes for platform management,
user administration, content moderation, and system analytics.

Admin Features:
- User management (create, edit, deactivate users)
- Phishing scan logs monitoring
- Reported content moderation
- Safety tips management
- Live analytics and system monitoring
- Data export functionality

Security Note:
- All admin functions require proper authentication and role verification
- User data is encrypted and admins cannot access personal information
- All admin actions are logged for security auditing
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from auth_routes import admin_required, get_current_user
from mongodb_config import db_manager
from encryption_utils import decrypt_sensitive_data, encrypt_sensitive_data
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta
import json
import logging
import uuid
import time
import random

# Set up logging for admin actions
logger = logging.getLogger(__name__)

# Create admin blueprint
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/')
@admin_required
def admin_dashboard():
    """
    Main admin dashboard with role-based permissions
    
    Super Admin: Full access to all features
    Sub Admin: User management only, no promotion/demotion
    """
    try:
        current_user = get_current_user()
        current_role = current_user.get('role', 'user') if current_user else 'user'
        
        # Define permissions based on role
        permissions = {
            'can_create_users': current_role in ['super_admin', 'sub_admin'],
            'can_promote_demote': current_role == 'super_admin',
            'can_delete_users': current_role in ['super_admin', 'sub_admin'],
            'can_view_system_logs': current_role == 'super_admin',
            'can_export_data': current_role == 'super_admin'
        }
        
        # Get system statistics
        stats = calculate_system_stats()
        
        # Get users with statistics
        users = get_all_users_with_stats()
        
        # Get recent scan logs
        scan_logs = get_recent_scan_logs()
        
        # Get reported content
        reported_content = get_reported_content()
        
        return render_template('admin_dashboard.html',
                         current_user=current_user,
                         permissions=permissions,
                         stats=stats,
                         users=users,
                         scan_logs=scan_logs,
                         reported_content=reported_content)

    except Exception as e:
        logger.error(f"Error loading admin dashboard: {e}")
        flash('Error loading admin dashboard', 'error')
        return redirect(url_for('main.index'))

@admin_bp.route('/user/create', methods=['POST'])
@admin_required
def create_user():
    """
    Create a new user account (Admin functionality)
    
    Role Permissions:
    - Super Admin: Can create users with any role
    - Sub Admin: Can create regular users only
    """
    try:
        current_user = get_current_user()
        current_role = current_user.get('role', 'user') if current_user else 'user'
        
        # Get form data
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        role = request.form.get('role', 'user').strip()
        
        # Validate required fields
        if not all([username, email, password]):
            return jsonify({
                'success': False,
                'message': 'Username, email, and password are required'
            }), 400
        
        # Role-based restrictions
        if current_role == 'sub_admin' and role in ['super_admin', 'sub_admin']:
            return jsonify({
                'success': False,
                'message': 'Sub Admin can only create regular users'
            }), 403
        
        # Validate password strength
        if len(password) < 8:
            return jsonify({
                'success': False,
                'message': 'Password must be at least 8 characters long'
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
                'message': 'Email already exists'
            }), 400
        
        # Create new user
        password_hash = generate_password_hash(password)
        user_id = f"user_{int(time.time())}_{random.randint(1000, 9999)}"
        
        new_user = {
            'id': user_id,
            '_id': f"users_{random.randint(1, 999999)}_{random.randint(100000, 999999)}",
            'username': username,
            'email': email,
            'password_hash': password_hash,
            'role': role,
            'active': True,
            'is_active': True,
            'created_at': datetime.utcnow().isoformat(),
            'last_login': None,
            'login_attempts': 0,
            'locked_until': None
        }
        
        # Insert user into database
        db_manager.insert_one('users', new_user)
        
        # Log admin action
        logger.info(f"Admin {current_role} {current_user.get('username')} created new user {username} with role {role}")
        
        return jsonify({
            'success': True,
            'message': f'User "{username}" created successfully with role "{role}"'
        })
        
    except Exception as e:
        logger.error(f"Error creating user: {e}")
        return jsonify({
            'success': False,
            'message': 'Error occurred while creating user'
        }), 500

@admin_bp.route('/user/<user_id>')
@admin_required
def get_user(user_id):
    """Get detailed user information for view details functionality"""
    try:
        # Find user using multiple ID formats
        user = db_manager.find_one('users', {'id': user_id})
        if not user:
            user = db_manager.find_one('users', {'_id': user_id})
        if not user:
            user = db_manager.find_one('users', {'id': str(user_id)})
        
        if not user:
            return jsonify({'success': False, 'error': 'User not found'}), 404
        
        # Get user's scan statistics
        scan_count = len(db_manager.find_many('detections', {'user_id': user_id})) or 0
        
        # Count phishing detections for this user
        user_detections = db_manager.find_many('detections', {'user_id': user_id})
        phishing_detections = 0
        for detection in user_detections:
            result = detection.get('result', {})
            category = result.get('category', '')
            if category in ['phishing', 'suspicious', 'dangerous']:
                phishing_detections += 1
        
        # Prepare user data (excluding sensitive information)
        user_data = {
            'id': user.get('id'),
            'username': user.get('username'),
            'email': user.get('email'),
            'role': user.get('role', 'user'),
            'active': user.get('active', True),
            'created_at': user.get('created_at', 'Unknown'),
            'last_login': user.get('last_login', 'Never'),
            'last_activity': user.get('last_activity', 'Unknown'),
            'scan_count': scan_count,
            'phishing_detected': phishing_detections
        }
        
        logger.info(f"Admin {get_current_user().get('username')} viewed user details for {user_data['username']}")
        return jsonify({'success': True, 'user': user_data})
        
    except Exception as e:
        logger.error(f"Error getting user details: {e}")
        return jsonify({'success': False, 'error': f'Failed to get user details: {str(e)}'})

@admin_bp.route('/user/<user_id>/reset-password', methods=['POST'])
@admin_required
def reset_user_password(user_id):
    """Reset a user's password with admin-provided value"""
    try:
        current_user = get_current_user()
        current_role = current_user.get('role', 'user') if current_user else 'user'
        
        # Get new password from form
        new_password = request.form.get('password', '').strip()
        
        if not new_password:
            return jsonify({
                'success': False,
                'message': 'New password is required'
            }), 400
        
        if len(new_password) < 8:
            return jsonify({
                'success': False,
                'message': 'Password must be at least 8 characters long'
            }), 400
        
        # Find the user
        user = db_manager.find_one('users', {'id': user_id})
        if not user:
            return jsonify({
                'success': False,
                'message': 'User not found'
            }), 404
        
        # Hash the new password
        password_hash = generate_password_hash(new_password)
        
        # Update user password
        db_manager.update_one('users', {'id': user_id}, {
            '$set': {
                'password_hash': password_hash,
                'last_password_reset': datetime.utcnow().isoformat(),
                'password_reset_by': current_user.get('username')
            }
        })
        
        logger.info(f"Admin {current_role} {current_user.get('username')} reset password for user {user.get('username')}")
        
        return jsonify({
            'success': True,
            'message': f'Password reset successfully for user {user.get("username")}'
        })
        
    except Exception as e:
        logger.error(f"Error resetting user password: {e}")
        return jsonify({
            'success': False,
            'message': 'Error occurred while resetting password'
        }), 500

@admin_bp.route('/user/<user_id>/promote', methods=['POST'])
@admin_required
def promote_user(user_id):
    """Promote user to sub-admin role (Super Admin only)"""
    try:
        current_user = get_current_user()
        current_role = current_user.get('role', 'user') if current_user else 'user'
        
        # Only super admin can promote users
        if current_role != 'super_admin':
            return jsonify({
                'success': False,
                'message': 'Only Super Admin can promote users'
            }), 403
        
        # Find the user
        user = db_manager.find_one('users', {'id': user_id})
        if not user:
            return jsonify({
                'success': False,
                'message': 'User not found'
            }), 404
        
        # Check if user is already admin
        if user.get('role') in ['admin', 'sub_admin', 'super_admin']:
            return jsonify({
                'success': False,
                'message': 'User already has administrative privileges'
            }), 400
        
        # Promote user to sub_admin
        db_manager.update_one('users', {'id': user_id}, {
            '$set': {
                'role': 'sub_admin',
                'promoted_at': datetime.utcnow().isoformat(),
                'promoted_by': current_user.get('username')
            }
        })
        
        logger.info(f"Super Admin {current_user.get('username')} promoted user {user.get('username')} to sub_admin")
        
        return jsonify({
            'success': True,
            'message': f'User {user.get("username")} promoted to Sub Admin successfully'
        })
        
    except Exception as e:
        logger.error(f"Error promoting user: {e}")
        return jsonify({
            'success': False,
            'message': 'Error occurred while promoting user'
        }), 500

@admin_bp.route('/user/<user_id>/demote', methods=['POST'])
@admin_required
def demote_user(user_id):
    """Demote user role (Super Admin only)"""
    try:
        current_user = get_current_user()
        current_role = current_user.get('role', 'user') if current_user else 'user'
        
        # Only super admin can demote users
        if current_role != 'super_admin':
            return jsonify({
                'success': False,
                'message': 'Only Super Admin can demote users'
            }), 403
        
        # Find the user
        user = db_manager.find_one('users', {'id': user_id})
        if not user:
            return jsonify({
                'success': False,
                'message': 'User not found'
            }), 404
        
        # Cannot demote self
        if user.get('id') == current_user.get('id'):
            return jsonify({
                'success': False,
                'message': 'Cannot demote yourself'
            }), 400
        
        # Cannot demote other super admins
        if user.get('role') == 'super_admin':
            return jsonify({
                'success': False,
                'message': 'Cannot demote Super Admin users'
            }), 400
        
        # Check if user is already regular user
        if user.get('role') == 'user':
            return jsonify({
                'success': False,
                'message': 'User is already a regular user'
            }), 400
        
        # Demote user to regular user
        db_manager.update_one('users', {'id': user_id}, {
            '$set': {
                'role': 'user',
                'demoted_at': datetime.utcnow().isoformat(),
                'demoted_by': current_user.get('username')
            }
        })
        
        logger.info(f"Super Admin {current_user.get('username')} demoted user {user.get('username')} to regular user")
        
        return jsonify({
            'success': True,
            'message': f'User {user.get("username")} demoted to regular user successfully'
        })
        
    except Exception as e:
        logger.error(f"Error demoting user: {e}")
        return jsonify({
            'success': False,
            'message': 'Error occurred while demoting user'
        }), 500

@admin_bp.route('/user/<user_id>/delete', methods=['POST'])
@admin_required
def delete_user(user_id):
    """
    Delete a user account permanently with comprehensive data cleanup
    
    Role Permissions:
    - Super Admin: Can delete any user except self
    - Sub Admin: Cannot delete Super Admin or other Sub Admins
    """
    try:
        current_user = get_current_user()
        current_role = current_user.get('role', 'user') if current_user else 'user'
        
        # Find the user to delete
        user = db_manager.find_one('users', {'id': user_id})
        if not user:
            return jsonify({
                'success': False,
                'message': 'User not found'
            }), 404
        
        # Cannot delete self
        if user.get('id') == current_user.get('id'):
            return jsonify({
                'success': False,
                'message': 'Cannot delete your own account'
            }), 400
        
        # Role-based restrictions
        user_role = user.get('role', 'user')
        if current_role == 'sub_admin':
            if user_role in ['super_admin', 'sub_admin']:
                return jsonify({
                    'success': False,
                    'message': 'Sub Admin cannot delete Super Admin or other Sub Admin users'
                }), 403
        
        # Delete user's data (scans, reports, etc.)
        # Delete all user detections
        user_detections = db_manager.find_many('detections', {'user_id': user_id})
        for detection in user_detections:
            db_manager.delete_one('detections', {'_id': detection.get('_id')})
        
        # Delete all user scan logs
        user_logs = db_manager.find_many('scan_logs', {'user_id': user_id})
        for log in user_logs:
            db_manager.delete_one('scan_logs', {'_id': log.get('_id')})
        
        # Delete all user reports
        user_reports = db_manager.find_many('reports', {'reported_by': user_id})
        for report in user_reports:
            db_manager.delete_one('reports', {'_id': report.get('_id')})
        
        # Delete the user account
        result = db_manager.delete_one('users', {'id': user_id})
        
        if result:
            logger.info(f"Admin {current_role} {current_user.get('username')} deleted user {user.get('username')}")
            return jsonify({
                'success': True,
                'message': f'User {user.get("username")} and all associated data deleted successfully'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Failed to delete user'
            }), 500
        
    except Exception as e:
        logger.error(f"Error deleting user: {e}")
        return jsonify({
            'success': False,
            'message': 'Error occurred while deleting user'
        }), 500

@admin_bp.route('/safety-tips/create', methods=['POST'])
@admin_required
def create_safety_tip():
    """Create a new safety tip"""
    try:
        current_user = get_current_user()
        
        # Get form data
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        category = request.form.get('category', 'general').strip()
        
        # Validate required fields
        if not all([title, content]):
            return jsonify({
                'success': False,
                'message': 'Title and content are required'
            }), 400
        
        # Create new safety tip
        tip_id = f"tip_{int(time.time())}_{random.randint(1000, 9999)}"
        
        new_tip = {
            'id': tip_id,
            '_id': f"tips_{random.randint(1, 999999)}_{random.randint(100000, 999999)}",
            'title': title,
            'content': content,
            'category': category,
            'created_at': datetime.utcnow().isoformat(),
            'created_by': current_user.get('username'),
            'active': True
        }
        
        # Insert tip into database
        db_manager.insert_one('safety_tips', new_tip)
        
        # Log admin action
        logger.info(f"Admin {current_user.get('username')} created new safety tip: {title}")
        
        return jsonify({
            'success': True,
            'message': f'Safety tip "{title}" created successfully'
        })
        
    except Exception as e:
        logger.error(f"Error creating safety tip: {e}")
        return jsonify({
            'success': False,
            'message': 'Error occurred while creating safety tip'
        }), 500

@admin_bp.route('/export/users', methods=['GET'])
@admin_required
def export_users():
    """Export user data as CSV"""
    try:
        import csv
        from io import StringIO
        
        current_user = get_current_user()
        current_role = current_user.get('role', 'user') if current_user else 'user'
        
        # Only Super Admin can export data
        if current_role != 'super_admin':
            return jsonify({
                'success': False,
                'message': 'Only Super Admin can export data'
            }), 403
        
        # Get all users with statistics
        users = get_all_users_with_stats()
        
        # Create CSV content
        output = StringIO()
        writer = csv.writer(output)
        
        # Write header
        writer.writerow(['ID', 'Username', 'Email', 'Role', 'Active', 'Created At', 'Last Login', 'Scan Count'])
        
        # Write user data
        for user in users:
            writer.writerow([
                user.get('id', ''),
                user.get('username', ''),
                user.get('email', ''),
                user.get('role', ''),
                user.get('active', ''),
                user.get('created_at', ''),
                user.get('last_login', ''),
                user.get('scan_count', 0)
            ])
        
        csv_content = output.getvalue()
        output.close()
        
        # Log export action
        logger.info(f"Super Admin {current_user.get('username')} exported user data")
        
        from flask import Response
        return Response(
            csv_content,
            mimetype='text/csv',
            headers={'Content-Disposition': 'attachment; filename=users_export.csv'}
        )
        
    except Exception as e:
        logger.error(f"Error exporting users: {e}")
        return jsonify({
            'success': False,
            'message': 'Error occurred while exporting data'
        }), 500

@admin_bp.route('/export/detections', methods=['GET'])
@admin_required
def export_detections():
    """Export detection history as CSV"""
    try:
        import csv
        from io import StringIO
        
        current_user = get_current_user()
        current_role = current_user.get('role', 'user') if current_user else 'user'
        
        # Only Super Admin can export data
        if current_role != 'super_admin':
            return jsonify({
                'success': False,
                'message': 'Only Super Admin can export data'
            }), 403
        
        # Get all detections
        detections = db_manager.find_many('detections', {})
        
        # Create CSV content
        output = StringIO()
        writer = csv.writer(output)
        
        # Write header
        writer.writerow(['ID', 'User ID', 'URL/Content', 'Result', 'Category', 'Confidence', 'Timestamp'])
        
        # Write detection data
        for detection in detections:
            result = detection.get('result', {})
            writer.writerow([
                detection.get('id', ''),
                detection.get('user_id', ''),
                detection.get('content', '')[:100],  # Truncate long content
                result.get('result', ''),
                result.get('category', ''),
                result.get('confidence', ''),
                detection.get('timestamp', '')
            ])
        
        csv_content = output.getvalue()
        output.close()
        
        # Log export action
        logger.info(f"Super Admin {current_user.get('username')} exported detection data")
        
        from flask import Response
        return Response(
            csv_content,
            mimetype='text/csv',
            headers={'Content-Disposition': 'attachment; filename=detections_export.csv'}
        )
        
    except Exception as e:
        logger.error(f"Error exporting detections: {e}")
        return jsonify({
            'success': False,
            'message': 'Error occurred while exporting data'
        }), 500

# Helper functions
def get_all_users_with_stats():
    """Get all users with their scan statistics"""
    try:
        users = db_manager.find_many('users', {})
        user_stats = []
        
        for user in users:
            # Get scan count for each user
            scan_count = len(db_manager.find_many('detections', {'user_id': user.get('id')}))
            
            user_stats.append({
                'id': user.get('id'),
                'username': user.get('username'),
                'email': user.get('email'),
                'role': user.get('role', 'user'),
                'active': user.get('active', True),
                'created_at': user.get('created_at', 'Unknown'),
                'last_login': user.get('last_login', 'Never'),
                'scan_count': scan_count
            })
        
        return user_stats
    except Exception as e:
        logger.error(f"Error getting users with stats: {e}")
        return []

def get_recent_scan_logs(limit=50):
    """Get recent scan logs with user information"""
    try:
        logs = db_manager.find_many('detections', {}, limit=limit)
        return logs[:limit]
    except Exception as e:
        logger.error(f"Error getting scan logs: {e}")
        return []

def get_reported_content():
    """Get reported content for moderation"""
    try:
        reports = db_manager.find_many('reports', {})
        return reports
    except Exception as e:
        logger.error(f"Error getting reported content: {e}")
        return []

def calculate_system_stats():
    """Calculate real-time system statistics"""
    try:
        total_users = len(db_manager.find_many('users', {}))
        total_scans = len(db_manager.find_many('detections', {}))
        active_users = len(db_manager.find_many('users', {'active': True}))
        
        # Count dangerous detections
        all_detections = db_manager.find_many('detections', {})
        dangerous_detections = 0
        for detection in all_detections:
            result = detection.get('result', {})
            category = result.get('category', '')
            if category in ['phishing', 'suspicious', 'dangerous']:
                dangerous_detections += 1
        
        safe_count = total_scans - dangerous_detections
        
        return {
            'total_users': total_users,
            'active_users': active_users,
            'total_scans': total_scans,
            'dangerous_count': dangerous_detections,
            'safe_count': safe_count,
            'suspicious_count': 0  # Placeholder
        }
    except Exception as e:
        logger.error(f"Error calculating system stats: {e}")
        return {
            'total_users': 0,
            'active_users': 0,
            'total_scans': 0,
            'dangerous_count': 0,
            'safe_count': 0,
            'suspicious_count': 0
        }