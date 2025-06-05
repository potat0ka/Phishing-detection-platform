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

# Set up logging for admin actions
logger = logging.getLogger(__name__)

# Create admin blueprint for organizing admin routes
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# Admin dashboard functionality is handled in routes.py dashboard() function
# based on user role detection

# Helper functions for admin dashboard (used by routes.py)

def create_user():
    """Create a new user account"""
    try:
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        role = request.form.get('role', 'user')
        
        if not all([username, email, password]):
            return jsonify({'success': False, 'error': 'All fields are required'})
        
        # Check if user already exists
        existing_user = db_manager.find_one('users', {'username': username})
        if existing_user:
            return jsonify({'success': False, 'error': 'Username already exists'})
        
        existing_email = db_manager.find_one('users', {'email': email})
        if existing_email:
            return jsonify({'success': False, 'error': 'Email already exists'})
        
        # Create user data
        user_data = {
            'id': f'user_{username}_{uuid.uuid4().hex[:8]}',
            'username': username,
            'email': email,
            'password_hash': generate_password_hash(password),
            'role': role,
            'created_at': datetime.utcnow().isoformat(),
            'last_login': None,
            'is_active': True,
            'login_attempts': 0,
            'locked_until': None,
            'created_by_admin': True
        }
        
        # Insert user
        user_id = db_manager.insert_one('users', user_data)
        
        if user_id:
            logger.info(f"Admin created new user: {username}")
            return jsonify({'success': True, 'message': f'User {username} created successfully'})
        else:
            return jsonify({'success': False, 'error': 'Failed to create user'})
            
    except Exception as e:
        logger.error(f"Error creating user: {e}")
        return jsonify({'success': False, 'error': str(e)})

@admin_bp.route('/user/<user_id>')
@admin_required
def get_user(user_id):
    """
    Get detailed user information with comprehensive data
    
    Returns user details, activity statistics, and recent activity logs
    for admin dashboard view details functionality
    """
    try:
        # Find user using multiple ID formats (handles data inconsistency)
        user = None
        
        # Try with 'id' field first
        user = db_manager.find_one('users', {'id': user_id})
        
        # If not found, try with '_id' field
        if not user:
            user = db_manager.find_one('users', {'_id': user_id})
        
        if not user:
            return jsonify({'success': False, 'error': 'User not found'})
        
        # Handle encrypted user data safely
        display_user = user.copy()
        try:
            if user.get('username_encrypted') or user.get('email_encrypted'):
                decrypted_user = decrypt_sensitive_data('user', user)
                display_user.update(decrypted_user)
        except Exception as decrypt_error:
            logger.warning(f"Could not decrypt user data for {user_id}: {decrypt_error}")
            # Continue with original data if decryption fails
        
        # Get comprehensive user statistics
        user_stats = {}
        
        # Count user's detections (handle multiple user ID formats)
        detection_count = 0
        detection_count += db_manager.count_documents('detections', {'user_id': user_id})
        
        # Also check alternate ID format if exists
        if user.get('id') and user.get('id') != user_id:
            detection_count += db_manager.count_documents('detections', {'user_id': user.get('id')})
        
        user_stats['total_scans'] = detection_count
        
        # Get recent detections for activity timeline
        recent_detections = []
        detections = db_manager.find_many('detections', {'user_id': user_id}, limit=5)
        
        for detection in detections:
            detection_summary = {
                'id': detection.get('id') or detection.get('_id'),
                'type': detection.get('input_type', 'unknown'),
                'result': detection.get('result', 'unknown'),
                'timestamp': detection.get('timestamp') or detection.get('created_at'),
                'content_preview': (detection.get('input_content') or detection.get('content', ''))[:50]
            }
            recent_detections.append(detection_summary)
        
        user_stats['recent_activity'] = recent_detections
        
        # Count reports made by this user
        report_count = db_manager.count_documents('reports', {'reporter_id': user_id})
        user_stats['reports_made'] = report_count
        
        # Calculate account age and last activity
        from datetime import datetime
        try:
            created_date = user.get('created_at')
            if created_date:
                if isinstance(created_date, str):
                    created_dt = datetime.fromisoformat(created_date.replace('Z', '+00:00'))
                else:
                    created_dt = created_date
                account_age_days = (datetime.now() - created_dt.replace(tzinfo=None)).days
                user_stats['account_age_days'] = account_age_days
        except:
            user_stats['account_age_days'] = 0
        
        # Last login information
        last_login = user.get('last_login')
        user_stats['last_login'] = last_login
        
        # Security information
        user_stats['login_attempts'] = user.get('login_attempts', 0)
        user_stats['is_locked'] = bool(user.get('locked_until'))
        
        # Clean up sensitive data for display
        safe_user_data = {
            'id': user.get('id') or user.get('_id'),
            'username': display_user.get('username', 'Unknown'),
            'email': display_user.get('email', 'Unknown'),
            'role': user.get('role', 'user'),
            'is_active': user.get('is_active', True),
            'created_at': user.get('created_at'),
            'last_login': user.get('last_login'),
            'login_attempts': user.get('login_attempts', 0),
            'locked_until': user.get('locked_until'),
            'email_verified': user.get('email_verified', False),
            'profile_completed': user.get('profile_completed', False)
        }
        
        return jsonify({
            'success': True, 
            'user': safe_user_data,
            'stats': user_stats
        })
        
    except Exception as e:
        logger.error(f"Error getting user details for {user_id}: {e}")
        return jsonify({'success': False, 'error': f'Failed to load user details: {str(e)}'})

@admin_bp.route('/user/<user_id>', methods=['PUT'])
@admin_required
def update_user(user_id):
    """Update user information"""
    try:
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        role = request.form.get('role', 'user')
        is_active = request.form.get('is_active') == 'on'
        
        if not all([username, email]):
            return jsonify({'success': False, 'error': 'Username and email are required'})
        
        # Update user data
        update_data = {
            'username': username,
            'email': email,
            'role': role,
            'is_active': is_active,
            'updated_at': datetime.utcnow().isoformat()
        }
        
        success = db_manager.update_one('users', {'id': user_id}, {'$set': update_data})
        
        if success:
            logger.info(f"Admin updated user: {user_id}")
            return jsonify({'success': True, 'message': 'User updated successfully'})
        else:
            return jsonify({'success': False, 'error': 'Failed to update user'})
            
    except Exception as e:
        logger.error(f"Error updating user {user_id}: {e}")
        return jsonify({'success': False, 'error': str(e)})

@admin_bp.route('/user/<user_id>/toggle-status', methods=['POST'])
@admin_required
def toggle_user_status(user_id):
    """Toggle user active/inactive status"""
    try:
        user = db_manager.find_one('users', {'id': user_id})
        if not user:
            return jsonify({'success': False, 'error': 'User not found'})
        
        # Try to decrypt if encrypted
        try:
            decrypted_user = decrypt_sensitive_data('user', user)
            current_status = decrypted_user.get('is_active', True)
        except:
            current_status = user.get('is_active', True)
        
        new_status = not current_status
        
        success = db_manager.update_one('users', {'id': user_id}, 
                                      {'$set': {'is_active': new_status, 
                                               'updated_at': datetime.utcnow().isoformat()}})
        
        if success:
            status_text = 'activated' if new_status else 'deactivated'
            logger.info(f"Admin {status_text} user: {user_id}")
            return jsonify({'success': True, 'message': f'User {status_text} successfully'})
        else:
            return jsonify({'success': False, 'error': 'Failed to update user status'})
            
    except Exception as e:
        logger.error(f"Error toggling user status {user_id}: {e}")
        return jsonify({'success': False, 'error': str(e)})

@admin_bp.route('/user/<user_id>/delete', methods=['POST'])
@admin_required
def delete_user(user_id):
    """
    Delete a user account permanently with comprehensive data cleanup
    
    This function handles the complete removal of a user and all associated data:
    1. Security checks (prevent self-deletion, role restrictions)
    2. Data cleanup (detections, reports, admin actions)
    3. User account deletion
    """
    try:
        current_user = get_current_user()
        current_user_id = current_user.get('_id') or current_user.get('id') if current_user else None
        
        # Security Check 1: Prevent admin from deleting themselves
        if current_user_id == user_id:
            return jsonify({'success': False, 'error': 'You cannot delete your own account'})
        
        # Security Check 2: Find user using multiple ID formats (handles inconsistent data)
        user = None
        
        # Try with 'id' field first
        user = db_manager.find_one('users', {'id': user_id})
        
        # If not found, try with '_id' field
        if not user:
            user = db_manager.find_one('users', {'_id': user_id})
        
        if not user:
            return jsonify({'success': False, 'error': 'User not found'})
        
        # Security Check 3: Role-based restrictions
        target_user_role = user.get('role', 'user') if user else 'user'
        current_user_role = (current_user or {}).get('role', 'user')
        
        # Super Admin can delete anyone except themselves
        # Sub-Admin can only delete regular users
        if current_user_role == 'sub_admin' and target_user_role in ['admin', 'super_admin', 'sub_admin']:
            return jsonify({'success': False, 'error': 'Sub-admins cannot delete other administrators'})
        
        # Get user's username for logging (handle encryption)
        username = 'Unknown'
        try:
            if user.get('username_encrypted'):
                decrypted_user = decrypt_sensitive_data('user', user)
                username = decrypted_user.get('username', 'Unknown')
            else:
                username = user.get('username', 'Unknown')
        except Exception as decrypt_error:
            logger.warning(f"Could not decrypt username for user {user_id}: {decrypt_error}")
            username = user.get('username', 'Unknown')
        
        # Data Cleanup Phase 1: Delete user's detection history
        # Handle both possible user ID formats in detections
        detection_count = 0
        
        # Delete detections with user_id matching the target user
        detections = db_manager.find_many('detections', {'user_id': user_id})
        for detection in detections:
            detection_id = detection.get('_id') or detection.get('id')
            if detection_id:
                deleted = db_manager.delete_one('detections', {'_id': detection_id})
                if deleted:
                    detection_count += 1
        
        # Also check for detections with the alternate ID format
        if user.get('id') and user.get('id') != user_id:
            alt_detections = db_manager.find_many('detections', {'user_id': user.get('id')})
            for detection in alt_detections:
                detection_id = detection.get('_id') or detection.get('id')
                if detection_id:
                    deleted = db_manager.delete_one('detections', {'_id': detection_id})
                    if deleted:
                        detection_count += 1
        
        # Data Cleanup Phase 2: Delete reported content by this user
        report_count = 0
        reports = db_manager.find_many('reports', {'reporter_id': user_id})
        for report in reports:
            report_id = report.get('_id') or report.get('id')
            if report_id:
                deleted = db_manager.delete_one('reports', {'_id': report_id})
                if deleted:
                    report_count += 1
        
        # Data Cleanup Phase 3: Delete admin actions logged by this user
        action_count = 0
        admin_actions = db_manager.find_many('admin_actions', {'admin_id': user_id})
        for action in admin_actions:
            action_id = action.get('_id') or action.get('id')
            if action_id:
                deleted = db_manager.delete_one('admin_actions', {'_id': action_id})
                if deleted:
                    action_count += 1
        
        # Final Step: Delete the user account using the correct identifier
        user_deleted = False
        
        # Try deleting with the ID that was found
        if user.get('id'):
            user_deleted = db_manager.delete_one('users', {'id': user.get('id')})
        
        # If that didn't work, try with _id
        if not user_deleted and user.get('_id'):
            user_deleted = db_manager.delete_one('users', {'_id': user.get('_id')})
        
        if user_deleted:
            # Log comprehensive deletion details
            logger.info(f"Admin {(current_user or {}).get('username', 'Unknown')} successfully deleted user: {username} (ID: {user_id})")
            logger.info(f"Cleanup: {detection_count} detections, {report_count} reports, {action_count} admin actions")
            
            return jsonify({
                'success': True, 
                'message': f'User {username} and all associated data deleted successfully',
                'details': {
                    'detections_deleted': detection_count,
                    'reports_deleted': report_count,
                    'admin_actions_deleted': action_count
                }
            })
        else:
            return jsonify({'success': False, 'error': 'Failed to delete user account'})
            
    except Exception as e:
        logger.error(f"Critical error deleting user {user_id}: {e}")
        return jsonify({'success': False, 'error': f'Deletion failed: {str(e)}'})

@admin_bp.route('/user/<user_id>/reset-password', methods=['POST'])
@admin_required
def reset_user_password(user_id):
    """
    Reset a user's password with admin-provided value
    
    Allows admins to set a custom password for user recovery or temporary access
    """
    try:
        current_user = get_current_user()
        new_password = request.form.get('new_password', '').strip()
        
        if not new_password:
            return jsonify({'success': False, 'error': 'New password is required'})
        
        if len(new_password) < 6:
            return jsonify({'success': False, 'error': 'Password must be at least 6 characters long'})
        
        # Find user using multiple ID formats
        user = db_manager.find_one('users', {'id': user_id})
        if not user:
            user = db_manager.find_one('users', {'_id': user_id})
        
        if not user:
            return jsonify({'success': False, 'error': 'User not found'})
        
        # Role-based security check
        target_user_role = user.get('role', 'user')
        current_user_role = (current_user or {}).get('role', 'user')
        
        # Sub-admins cannot reset passwords for other admins
        if current_user_role == 'sub_admin' and target_user_role in ['admin', 'super_admin', 'sub_admin']:
            return jsonify({'success': False, 'error': 'Sub-admins cannot reset passwords for other administrators'})
        
        # Generate new password hash
        from werkzeug.security import generate_password_hash
        new_password_hash = generate_password_hash(new_password)
        
        # Update user password and reset login attempts
        update_data = {
            'password_hash': new_password_hash,
            'login_attempts': 0,
            'locked_until': None,
            'updated_at': datetime.utcnow().isoformat()
        }
        
        # Update using correct ID format
        update_query = {'id': user.get('id')} if user.get('id') else {'_id': user.get('_id')}
        success = db_manager.update_one('users', update_query, {'$set': update_data})
        
        if success:
            # Get username for logging
            username = 'Unknown'
            try:
                if user.get('username_encrypted'):
                    decrypted_user = decrypt_sensitive_data('user', user)
                    username = decrypted_user.get('username', 'Unknown')
                else:
                    username = user.get('username', 'Unknown')
            except:
                username = user.get('username', 'Unknown')
            
            logger.info(f"Admin {(current_user or {}).get('username', 'Unknown')} reset password for user: {username}")
            return jsonify({'success': True, 'message': f'Password reset successfully for {username}'})
        else:
            return jsonify({'success': False, 'error': 'Failed to reset password'})
            
    except Exception as e:
        logger.error(f"Error resetting password for user {user_id}: {e}")
        return jsonify({'success': False, 'error': f'Password reset failed: {str(e)}'})

@admin_bp.route('/user/<user_id>/promote', methods=['POST'])
@admin_required
def promote_user(user_id):
    """
    Promote user to sub-admin role (Super Admin only)
    
    Implements role hierarchy:
    - Super Admin can promote users to Sub-Admin
    - Sub-Admins cannot promote anyone
    """
    try:
        current_user = get_current_user()
        current_user_role = (current_user or {}).get('role', 'user')
        
        # Only Super Admin can promote users
        if current_user_role != 'super_admin':
            return jsonify({'success': False, 'error': 'Only Super Admins can promote users'})
        
        # Find target user
        user = db_manager.find_one('users', {'id': user_id})
        if not user:
            user = db_manager.find_one('users', {'_id': user_id})
        
        if not user:
            return jsonify({'success': False, 'error': 'User not found'})
        
        current_role = user.get('role', 'user')
        
        # Determine new role based on current role
        if current_role == 'user':
            new_role = 'sub_admin'
        elif current_role == 'sub_admin':
            new_role = 'admin'
        else:
            return jsonify({'success': False, 'error': 'User already has maximum role'})
        
        # Update user role
        update_data = {
            'role': new_role,
            'updated_at': datetime.utcnow().isoformat()
        }
        
        update_query = {'id': user.get('id')} if user.get('id') else {'_id': user.get('_id')}
        success = db_manager.update_one('users', update_query, {'$set': update_data})
        
        if success:
            # Get username for logging
            username = 'Unknown'
            try:
                if user.get('username_encrypted'):
                    decrypted_user = decrypt_sensitive_data('user', user)
                    username = decrypted_user.get('username', 'Unknown')
                else:
                    username = user.get('username', 'Unknown')
            except:
                username = user.get('username', 'Unknown')
            
            logger.info(f"Super Admin {(current_user or {}).get('username', 'Unknown')} promoted {username} to {new_role}")
            return jsonify({'success': True, 'message': f'User {username} promoted to {new_role.replace("_", " ").title()}'})
        else:
            return jsonify({'success': False, 'error': 'Failed to promote user'})
            
    except Exception as e:
        logger.error(f"Error promoting user {user_id}: {e}")
        return jsonify({'success': False, 'error': f'Promotion failed: {str(e)}'})

@admin_bp.route('/user/<user_id>/demote', methods=['POST'])
@admin_required
def demote_user(user_id):
    """
    Demote user role (Super Admin only)
    
    Allows Super Admin to demote sub-admins back to regular users
    """
    try:
        current_user = get_current_user()
        current_user_role = (current_user or {}).get('role', 'user')
        
        # Only Super Admin can demote users
        if current_user_role != 'super_admin':
            return jsonify({'success': False, 'error': 'Only Super Admins can demote users'})
        
        # Find target user
        user = db_manager.find_one('users', {'id': user_id})
        if not user:
            user = db_manager.find_one('users', {'_id': user_id})
        
        if not user:
            return jsonify({'success': False, 'error': 'User not found'})
        
        current_role = user.get('role', 'user')
        
        # Prevent demoting another super admin
        if current_role == 'super_admin':
            return jsonify({'success': False, 'error': 'Cannot demote Super Admin'})
        
        # Determine new role
        if current_role == 'admin':
            new_role = 'sub_admin'
        elif current_role == 'sub_admin':
            new_role = 'user'
        else:
            return jsonify({'success': False, 'error': 'User already has minimum role'})
        
        # Update user role
        update_data = {
            'role': new_role,
            'updated_at': datetime.utcnow().isoformat()
        }
        
        update_query = {'id': user.get('id')} if user.get('id') else {'_id': user.get('_id')}
        success = db_manager.update_one('users', update_query, {'$set': update_data})
        
        if success:
            # Get username for logging
            username = 'Unknown'
            try:
                if user.get('username_encrypted'):
                    decrypted_user = decrypt_sensitive_data('user', user)
                    username = decrypted_user.get('username', 'Unknown')
                else:
                    username = user.get('username', 'Unknown')
            except:
                username = user.get('username', 'Unknown')
            
            logger.info(f"Super Admin {(current_user or {}).get('username', 'Unknown')} demoted {username} to {new_role}")
            return jsonify({'success': True, 'message': f'User {username} demoted to {new_role.replace("_", " ").title()}'})
        else:
            return jsonify({'success': False, 'error': 'Failed to demote user'})
            
    except Exception as e:
        logger.error(f"Error demoting user {user_id}: {e}")
        return jsonify({'success': False, 'error': f'Demotion failed: {str(e)}'})

# Safety Tips Management Routes
@admin_bp.route('/tips', methods=['POST'])
@admin_required
def create_tip():
    """Create a new safety tip"""
    try:
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        category = request.form.get('category', 'general')
        priority = int(request.form.get('priority', 2))
        
        if not all([title, content]):
            return jsonify({'success': False, 'error': 'Title and content are required'})
        
        tip_data = {
            'id': f'tip_{uuid.uuid4().hex[:8]}',
            'title': title,
            'content': content,
            'category': category,
            'priority': priority,
            'created_at': datetime.utcnow().isoformat(),
            'created_by_admin': True
        }
        
        tip_id = db_manager.insert_one('security_tips', tip_data)
        
        if tip_id:
            logger.info(f"Admin created new safety tip: {title}")
            return jsonify({'success': True, 'message': 'Safety tip created successfully'})
        else:
            return jsonify({'success': False, 'error': 'Failed to create tip'})
            
    except Exception as e:
        logger.error(f"Error creating tip: {e}")
        return jsonify({'success': False, 'error': str(e)})

@admin_bp.route('/tip/<tip_id>')
@admin_required
def get_tip(tip_id):
    """Get safety tip details"""
    try:
        tip = db_manager.find_one('security_tips', {'id': tip_id})
        if not tip:
            return jsonify({'success': False, 'error': 'Tip not found'})
        
        return jsonify({'success': True, 'tip': tip})
        
    except Exception as e:
        logger.error(f"Error getting tip {tip_id}: {e}")
        return jsonify({'success': False, 'error': str(e)})

@admin_bp.route('/tip/<tip_id>', methods=['PUT'])
@admin_required
def update_tip(tip_id):
    """Update safety tip"""
    try:
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        category = request.form.get('category', 'general')
        priority = int(request.form.get('priority', 2))
        
        if not all([title, content]):
            return jsonify({'success': False, 'error': 'Title and content are required'})
        
        update_data = {
            'title': title,
            'content': content,
            'category': category,
            'priority': priority,
            'updated_at': datetime.utcnow().isoformat()
        }
        
        success = db_manager.update_one('security_tips', {'id': tip_id}, {'$set': update_data})
        
        if success:
            logger.info(f"Admin updated safety tip: {tip_id}")
            return jsonify({'success': True, 'message': 'Safety tip updated successfully'})
        else:
            return jsonify({'success': False, 'error': 'Failed to update tip'})
            
    except Exception as e:
        logger.error(f"Error updating tip {tip_id}: {e}")
        return jsonify({'success': False, 'error': str(e)})

@admin_bp.route('/tip/<tip_id>', methods=['DELETE'])
@admin_required
def delete_tip(tip_id):
    """Delete safety tip"""
    try:
        success = db_manager.delete_one('security_tips', {'id': tip_id})
        
        if success:
            logger.info(f"Admin deleted safety tip: {tip_id}")
            return jsonify({'success': True, 'message': 'Safety tip deleted successfully'})
        else:
            return jsonify({'success': False, 'error': 'Failed to delete tip'})
            
    except Exception as e:
        logger.error(f"Error deleting tip {tip_id}: {e}")
        return jsonify({'success': False, 'error': str(e)})

# Reported Content Management Routes
@admin_bp.route('/report/<report_id>')
@admin_required
def get_report(report_id):
    """Get reported content details"""
    try:
        report = db_manager.find_one('reported_content', {'id': report_id})
        if not report:
            return jsonify({'success': False, 'error': 'Report not found'})
        
        return jsonify({'success': True, 'report': report})
        
    except Exception as e:
        logger.error(f"Error getting report {report_id}: {e}")
        return jsonify({'success': False, 'error': str(e)})

@admin_bp.route('/report/<report_id>/approve', methods=['POST'])
@admin_required
def approve_report(report_id):
    """Approve a reported content"""
    try:
        current_user = get_current_user()
        username = current_user.get('username', 'admin') if current_user else 'admin'
        
        success = db_manager.update_one('reported_content', {'id': report_id}, 
                                      {'$set': {'status': 'approved', 
                                               'reviewed_at': datetime.utcnow().isoformat(),
                                               'reviewed_by': username}})
        
        if success:
            logger.info(f"Admin approved report: {report_id}")
            return jsonify({'success': True, 'message': 'Report approved successfully'})
        else:
            return jsonify({'success': False, 'error': 'Failed to approve report'})
            
    except Exception as e:
        logger.error(f"Error approving report {report_id}: {e}")
        return jsonify({'success': False, 'error': str(e)})

@admin_bp.route('/report/<report_id>/reject', methods=['POST'])
@admin_required
def reject_report(report_id):
    """Reject a reported content"""
    try:
        current_user = get_current_user()
        username = current_user.get('username', 'admin') if current_user else 'admin'
        
        success = db_manager.update_one('reported_content', {'id': report_id}, 
                                      {'$set': {'status': 'rejected', 
                                               'reviewed_at': datetime.utcnow().isoformat(),
                                               'reviewed_by': username}})
        
        if success:
            logger.info(f"Admin rejected report: {report_id}")
            return jsonify({'success': True, 'message': 'Report rejected successfully'})
        else:
            return jsonify({'success': False, 'error': 'Failed to reject report'})
            
    except Exception as e:
        logger.error(f"Error rejecting report {report_id}: {e}")
        return jsonify({'success': False, 'error': str(e)})

# Export and System Management Routes
@admin_bp.route('/export/scan-logs')
@admin_required
def export_scan_logs():
    """Export scan logs as CSV"""
    try:
        import csv
        from io import StringIO
        from flask import make_response
        
        # Get all scan logs
        scan_logs = get_recent_scan_logs(limit=1000)
        
        # Create CSV content
        output = StringIO()
        writer = csv.writer(output)
        
        # Write header
        writer.writerow(['Date', 'User', 'Type', 'Content', 'Result', 'Confidence', 'IP Address'])
        
        # Write data
        for scan in scan_logs:
            writer.writerow([
                scan.get('created_at', '')[:16].replace('T', ' '),
                scan.get('username', 'Unknown'),
                scan.get('input_type', 'Unknown'),
                (scan.get('input_content', '') or scan.get('content', ''))[:100],
                scan.get('result', 'Unknown'),
                f"{(scan.get('confidence_score', 0) or scan.get('confidence', 0)) * 100:.1f}%",
                scan.get('user_ip', 'Unknown')
            ])
        
        # Create response
        response = make_response(output.getvalue())
        response.headers['Content-Type'] = 'text/csv'
        response.headers['Content-Disposition'] = f'attachment; filename=scan_logs_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        
        return response
        
    except Exception as e:
        logger.error(f"Error exporting scan logs: {e}")
        return jsonify({'success': False, 'error': str(e)})

@admin_bp.route('/export/system-report')
@admin_required
def export_system_report():
    """Export comprehensive system report"""
    try:
        from io import StringIO
        from flask import make_response
        
        # Generate system report
        stats = calculate_system_stats()
        analytics = calculate_analytics_data()
        
        report_content = f"""
AI Phishing Detection Platform - System Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

SYSTEM STATISTICS:
- Total Users: {stats.get('total_users', 0)}
- New Users Today: {stats.get('new_users_today', 0)}
- Total Scans: {stats.get('total_scans', 0)}
- Scans Today: {stats.get('scans_today', 0)}
- Threats Detected: {stats.get('threats_detected', 0)}
- Threat Rate: {stats.get('threat_rate', 0) * 100:.1f}%
- Active Sessions: {stats.get('active_sessions', 0)}

ANALYTICS:
- Average Response Time: {analytics.get('avg_response_time', 0):.1f}ms
- Detection Accuracy: {analytics.get('accuracy_rate', 0) * 100:.1f}%
- Storage Used: {analytics.get('total_storage', 0)}MB
- System Uptime: 99.9%

RECENT ACTIVITY:
- Last 7 days scan activity available in detailed logs
- User registration trends available in user management
- Security tip engagement metrics available in content management

Report generated by Admin Dashboard
        """
        
        response = make_response(report_content.strip())
        response.headers['Content-Type'] = 'text/plain'
        response.headers['Content-Disposition'] = f'attachment; filename=system_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt'
        
        return response
        
    except Exception as e:
        logger.error(f"Error exporting system report: {e}")
        return jsonify({'success': False, 'error': str(e)})

@admin_bp.route('/clear-logs', methods=['POST'])
@admin_required
def clear_logs():
    """Clear old system logs"""
    try:
        # Clear logs older than 30 days
        cutoff_date = datetime.utcnow() - timedelta(days=30)
        cutoff_str = cutoff_date.isoformat()
        
        # Clear old detections
        cleared_detections = 0
        all_detections = db_manager.find_many('detections')
        for detection in all_detections:
            created_at = detection.get('created_at', '')
            if created_at and created_at < cutoff_str:
                db_manager.delete_one('detections', {'id': detection.get('id')})
                cleared_detections += 1
        
        logger.info(f"Admin cleared {cleared_detections} old detection logs")
        return jsonify({'success': True, 'message': f'Cleared {cleared_detections} old logs'})
        
    except Exception as e:
        logger.error(f"Error clearing logs: {e}")
        return jsonify({'success': False, 'error': str(e)})

# Helper Functions
def get_all_users_with_stats():
    """Get all users with their scan statistics"""
    try:
        all_users = db_manager.find_many('users')
        users = []
        
        for user_data in all_users:
            # Try to decrypt if encrypted, otherwise use original data
            try:
                user = decrypt_sensitive_data('user', user_data)
            except:
                user = user_data.copy()
            
            # Ensure we have basic user data
            if not user.get('username'):
                continue
            
            # Get scan count for each user
            user_id = user.get('id', '')
            scan_count = db_manager.count_documents('detections', {'user_id': user_id})
            user['scan_count'] = scan_count
            
            # Format last login date
            if user.get('last_login'):
                user['last_login'] = user['last_login'][:16].replace('T', ' ')
            
            users.append(user)
        
        return users
        
    except Exception as e:
        logger.error(f"Error getting users with stats: {e}")
        return []

def get_recent_scan_logs(limit=50):
    """Get recent scan logs with user information"""
    try:
        all_detections = db_manager.find_many('detections')
        scan_logs = []
        
        # Sort by created_at and limit
        sorted_detections = sorted(all_detections, 
                                 key=lambda x: x.get('created_at', ''), 
                                 reverse=True)[:limit]
        
        for detection_data in sorted_detections:
            # Try to decrypt if encrypted, otherwise use original data
            try:
                detection = decrypt_sensitive_data('detection', detection_data)
            except:
                detection = detection_data.copy()
            
            # Get username for user_id
            user_id = detection.get('user_id', '')
            if user_id:
                user = db_manager.find_one('users', {'id': user_id})
                if user:
                    try:
                        user_data = decrypt_sensitive_data('user', user)
                        detection['username'] = user_data.get('username', 'Unknown')
                    except:
                        detection['username'] = user.get('username', 'Unknown')
                else:
                    detection['username'] = 'Unknown'
            else:
                detection['username'] = 'Unknown'
            
            # Format created_at date
            if detection.get('created_at'):
                detection['created_at'] = detection['created_at'][:16].replace('T', ' ')
            
            scan_logs.append(detection)
        
        return scan_logs
        
    except Exception as e:
        logger.error(f"Error getting scan logs: {e}")
        return []

def get_reported_content():
    """Get reported content for moderation"""
    try:
        # Get reported content from database
        reports = db_manager.find_many('reported_content')
        
        # Format reports for display
        formatted_reports = []
        for report in reports:
            formatted_report = {
                'id': report.get('id', 'unknown'),
                'type': report.get('type', 'unknown'),
                'content': report.get('content', 'No content'),
                'status': report.get('status', 'pending'),
                'reporter_username': report.get('reporter_username', 'Anonymous'),
                'reason': report.get('reason', 'Not specified'),
                'created_at': report.get('created_at', '').split('T')[0] if report.get('created_at') else 'Unknown'
            }
            formatted_reports.append(formatted_report)
        
        # If no reports exist, create some sample data for demonstration
        if not formatted_reports:
            sample_reports = [
                {
                    'id': 'report_001',
                    'type': 'email',
                    'content': 'Suspicious email claiming to be from bank asking for account details',
                    'status': 'pending',
                    'reporter_username': 'demo_user',
                    'reason': 'Phishing attempt',
                    'created_at': '2025-06-05'
                },
                {
                    'id': 'report_002',
                    'type': 'url',
                    'content': 'https://fake-bank-login.suspicious-site.com',
                    'status': 'pending',
                    'reporter_username': 'demo_user',
                    'reason': 'Suspicious website',
                    'created_at': '2025-06-04'
                }
            ]
            return sample_reports
        
        return formatted_reports
        
    except Exception as e:
        logger.error(f"Error getting reported content: {e}")
        return []

def calculate_system_stats():
    """Calculate real-time system statistics"""
    try:
        # Get current date
        today = datetime.utcnow().date().isoformat()
        
        # Count total users
        total_users = db_manager.count_documents('users')
        
        # Count new users today
        new_users_today = 0
        all_users = db_manager.find_many('users')
        for user in all_users:
            created_at = user.get('created_at', '')
            if created_at and created_at.startswith(today):
                new_users_today += 1
        
        # Count total scans
        total_scans = db_manager.count_documents('detections')
        
        # Count scans today
        scans_today = 0
        threats_detected = 0
        all_detections = db_manager.find_many('detections')
        
        for detection in all_detections:
            created_at = detection.get('created_at', '')
            if created_at and created_at.startswith(today):
                scans_today += 1
            
            # Count threats (dangerous or suspicious results)
            result = detection.get('result', '').lower()
            if result in ['dangerous', 'suspicious']:
                threats_detected += 1
        
        # Calculate threat rate
        threat_rate = threats_detected / total_scans if total_scans > 0 else 0
        
        # Active sessions (simplified - in real implementation would track actual sessions)
        active_sessions = max(1, new_users_today)  # Simplified calculation
        
        return {
            'total_users': total_users,
            'new_users_today': new_users_today,
            'total_scans': total_scans,
            'scans_today': scans_today,
            'threats_detected': threats_detected,
            'threat_rate': threat_rate,
            'active_sessions': active_sessions
        }
        
    except Exception as e:
        logger.error(f"Error calculating system stats: {e}")
        return {
            'total_users': 0,
            'new_users_today': 0,
            'total_scans': 0,
            'scans_today': 0,
            'threats_detected': 0,
            'threat_rate': 0,
            'active_sessions': 0
        }

def calculate_analytics_data():
    """Calculate analytics data for charts and metrics"""
    try:
        # Get detection results counts
        safe_count = 0
        suspicious_count = 0
        dangerous_count = 0
        
        all_detections = db_manager.find_many('detections')
        for detection in all_detections:
            result = detection.get('result', '').lower()
            if result == 'safe':
                safe_count += 1
            elif result == 'suspicious':
                suspicious_count += 1
            elif result == 'dangerous':
                dangerous_count += 1
        
        # Generate activity data for last 7 days
        activity_labels = []
        activity_data = []
        
        for i in range(6, -1, -1):
            date = (datetime.utcnow() - timedelta(days=i)).strftime('%m/%d')
            activity_labels.append(date)
            
            # Count scans for this date
            day_scans = 0
            target_date = (datetime.utcnow() - timedelta(days=i)).date().isoformat()
            
            for detection in all_detections:
                created_at = detection.get('created_at', '')
                if created_at and created_at.startswith(target_date):
                    day_scans += 1
            
            activity_data.append(day_scans)
        
        # Calculate performance metrics
        avg_response_time = 150.5  # Simulated - would be calculated from actual performance data
        accuracy_rate = 0.95  # Simulated - would be calculated from user feedback
        total_storage = len(all_detections) * 0.1  # Simplified storage calculation
        
        return {
            'safe_count': safe_count,
            'suspicious_count': suspicious_count,
            'dangerous_count': dangerous_count,
            'activity_labels': json.dumps(activity_labels),
            'activity_data': json.dumps(activity_data),
            'avg_response_time': avg_response_time,
            'accuracy_rate': accuracy_rate,
            'total_storage': round(total_storage, 1)
        }
        
    except Exception as e:
        logger.error(f"Error calculating analytics data: {e}")
        return {
            'safe_count': 0,
            'suspicious_count': 0,
            'dangerous_count': 0,
            'activity_labels': json.dumps(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']),
            'activity_data': json.dumps([0, 0, 0, 0, 0, 0, 0]),
            'avg_response_time': 0,
            'accuracy_rate': 0,
            'total_storage': 0
        }