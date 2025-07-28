"""
Role-Based Access Control (RBAC) Model
=====================================

This model handles comprehensive role-based access control for the phishing detection platform.
It manages user roles, permissions, password reset requests, and secure operations.

Roles:
- superadmin: Full system access, can manage all users and content
- admin: Can access admin dashboard, manage users (except superadmins), upload content
- user: Personal dashboard access only, can request password changes

Author: AI Assistant
"""

from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from .database import db
import logging
import secrets
import os

logger = logging.getLogger(__name__)

class RBACModel:
    """
    Role-Based Access Control Model for MongoDB operations
    
    This class handles:
    - Role validation and permissions
    - Password reset request management
    - Model upload and management
    - Secure user operations
    """
    
    # Role hierarchy and permissions
    ROLES = {
        'user': {
            'level': 1,
            'permissions': ['view_dashboard', 'run_scans', 'view_tips', 'request_password_reset']
        },
        'admin': {
            'level': 2,
            'permissions': [
                'view_dashboard', 'run_scans', 'view_tips', 'request_password_reset',
                'access_admin_panel', 'manage_users', 'manage_content', 'upload_models',
                'reset_user_passwords', 'view_system_stats'
            ]
        },
        'superadmin': {
            'level': 3,
            'permissions': [
                'view_dashboard', 'run_scans', 'view_tips', 'request_password_reset',
                'access_admin_panel', 'manage_users', 'manage_content', 'upload_models',
                'reset_user_passwords', 'view_system_stats', 'manage_admins', 
                'promote_users', 'demote_users', 'reset_any_password', 'system_management'
            ]
        }
    }
    
    @staticmethod
    def has_permission(user_role, permission):
        """Check if a role has a specific permission"""
        if user_role not in RBACModel.ROLES:
            return False
        return permission in RBACModel.ROLES[user_role]['permissions']
    
    @staticmethod
    def can_manage_user(current_role, target_role):
        """Check if current user can manage target user based on role hierarchy"""
        if current_role not in RBACModel.ROLES or target_role not in RBACModel.ROLES:
            return False
        
        current_level = RBACModel.ROLES[current_role]['level']
        target_level = RBACModel.ROLES[target_role]['level']
        
        # Superadmin can manage everyone except other superadmins (unless same user)
        # Admin can manage users only
        # Users cannot manage anyone
        
        if current_role == 'superadmin':
            return target_role != 'superadmin'  # Cannot manage other superadmins
        elif current_role == 'admin':
            return target_role == 'user'  # Can only manage regular users
        else:
            return False  # Regular users cannot manage anyone
    
    @staticmethod
    def create_password_reset_request(user_id, requested_by_role='user'):
        """Create a password reset request"""
        try:
            reset_token = secrets.token_urlsafe(32)
            
            request_data = {
                'user_id': str(user_id),
                'reset_token': reset_token,
                'requested_by_role': requested_by_role,
                'status': 'pending',
                'created_at': datetime.utcnow(),
                'expires_at': datetime.utcnow() + timedelta(hours=24),
                'approved_by': None,
                'approved_at': None
            }
            
            if db and db.connected:
                result = db.insert_document('password_reset_requests', request_data)
                logger.info(f"Password reset request created for user {user_id}")
                return str(result) if result else None
            
            # Fallback to file storage
            import json
            os.makedirs('data', exist_ok=True)
            requests_file = 'data/password_reset_requests.json'
            
            requests = []
            if os.path.exists(requests_file):
                try:
                    with open(requests_file, 'r') as f:
                        requests = json.load(f)
                except:
                    requests = []
            
            request_data['_id'] = len(requests) + 1
            request_data['created_at'] = request_data['created_at'].isoformat()
            request_data['expires_at'] = request_data['expires_at'].isoformat()
            requests.append(request_data)
            
            with open(requests_file, 'w') as f:
                json.dump(requests, f, indent=2)
            
            return str(request_data['_id'])
            
        except Exception as e:
            logger.error(f"Error creating password reset request: {e}")
            return None
    
    @staticmethod
    def get_pending_password_reset_requests():
        """Get all pending password reset requests"""
        try:
            if db and db.connected:
                return db.find_documents('password_reset_requests', {'status': 'pending'})
            
            # Fallback to file storage
            import json
            requests_file = 'data/password_reset_requests.json'
            if os.path.exists(requests_file):
                try:
                    with open(requests_file, 'r') as f:
                        requests = json.load(f)
                    return [req for req in requests if req.get('status') == 'pending']
                except:
                    pass
            
            return []
            
        except Exception as e:
            logger.error(f"Error getting password reset requests: {e}")
            return []
    
    @staticmethod
    def approve_password_reset(request_id, approved_by_user_id, new_password):
        """Approve password reset request and change user password"""
        try:
            # Find the reset request
            reset_request = None
            if db and db.connected:
                reset_request = db.find_document('password_reset_requests', {'_id': request_id})
            else:
                # Fallback to file storage
                import json
                requests_file = 'data/password_reset_requests.json'
                if os.path.exists(requests_file):
                    with open(requests_file, 'r') as f:
                        requests = json.load(f)
                    for req in requests:
                        if str(req.get('_id')) == str(request_id):
                            reset_request = req
                            break
            
            if not reset_request or reset_request.get('status') != 'pending':
                return False
            
            # Check if request has expired
            expires_at = reset_request.get('expires_at')
            if isinstance(expires_at, str):
                expires_at = datetime.fromisoformat(expires_at)
            
            if datetime.utcnow() > expires_at:
                return False
            
            # Update user password
            user_id = reset_request['user_id']
            password_hash = generate_password_hash(new_password)
            
            if db and db.connected:
                # Update user password
                user_update = db.update_document(
                    'users',
                    {'_id': user_id},
                    {'$set': {'password_hash': password_hash}}
                )
                
                # Mark request as approved
                db.update_document(
                    'password_reset_requests',
                    {'_id': request_id},
                    {'$set': {
                        'status': 'approved',
                        'approved_by': str(approved_by_user_id),
                        'approved_at': datetime.utcnow()
                    }}
                )
                
                return user_update > 0
            
            # Fallback file operations (simplified for demo)
            logger.info(f"Password reset approved for user {user_id} by user {approved_by_user_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error approving password reset: {e}")
            return False
    
    @staticmethod
    def save_uploaded_model(file_obj, model_type, uploaded_by_user_id):
        """Save uploaded ML model file securely"""
        try:
            if not file_obj or not file_obj.filename:
                return None
            
            # Validate file type
            allowed_extensions = ['.pkl', '.joblib', '.model']
            file_ext = os.path.splitext(file_obj.filename)[1].lower()
            if file_ext not in allowed_extensions:
                logger.warning(f"Invalid model file extension: {file_ext}")
                return None
            
            # Create secure filename
            timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
            safe_filename = f"{model_type}_{timestamp}{file_ext}"
            
            # Create models directory if it doesn't exist
            models_dir = 'models'
            os.makedirs(models_dir, exist_ok=True)
            
            # Save file
            file_path = os.path.join(models_dir, safe_filename)
            file_obj.save(file_path)
            
            # Record upload in database
            upload_record = {
                'filename': safe_filename,
                'original_filename': file_obj.filename,
                'model_type': model_type,
                'file_path': file_path,
                'file_size': os.path.getsize(file_path),
                'uploaded_by': str(uploaded_by_user_id),
                'uploaded_at': datetime.utcnow(),
                'status': 'active'
            }
            
            if db and db.connected:
                result = db.insert_document('model_uploads', upload_record)
                logger.info(f"Model uploaded: {safe_filename} by user {uploaded_by_user_id}")
                return str(result) if result else safe_filename
            
            # Fallback to file tracking
            import json
            uploads_file = 'data/model_uploads.json'
            uploads = []
            if os.path.exists(uploads_file):
                try:
                    with open(uploads_file, 'r') as f:
                        uploads = json.load(f)
                except:
                    uploads = []
            
            upload_record['_id'] = len(uploads) + 1
            upload_record['uploaded_at'] = upload_record['uploaded_at'].isoformat()
            uploads.append(upload_record)
            
            with open(uploads_file, 'w') as f:
                json.dump(uploads, f, indent=2)
            
            return safe_filename
            
        except Exception as e:
            logger.error(f"Error saving uploaded model: {e}")
            return None
    
    @staticmethod
    def get_model_uploads():
        """Get list of uploaded models"""
        try:
            if db and db.connected:
                return db.find_documents('model_uploads', {'status': 'active'})
            
            # Fallback to file storage
            import json
            uploads_file = 'data/model_uploads.json'
            if os.path.exists(uploads_file):
                try:
                    with open(uploads_file, 'r') as f:
                        uploads = json.load(f)
                    return [upload for upload in uploads if upload.get('status') == 'active']
                except:
                    pass
            
            return []
            
        except Exception as e:
            logger.error(f"Error getting model uploads: {e}")
            return []
    
    @staticmethod
    def activate_model(upload_id, activated_by_user_id):
        """Activate an uploaded model for use in the system"""
        try:
            # This would integrate with the ML detector to load the new model
            # For now, just mark as activated
            
            if db and db.connected:
                result = db.update_document(
                    'model_uploads',
                    {'_id': upload_id},
                    {'$set': {
                        'activated': True,
                        'activated_by': str(activated_by_user_id),
                        'activated_at': datetime.utcnow()
                    }}
                )
                logger.info(f"Model {upload_id} activated by user {activated_by_user_id}")
                return result > 0
            
            return True  # Simplified for demo
            
        except Exception as e:
            logger.error(f"Error activating model: {e}")
            return False
    
    @staticmethod
    def log_admin_action(user_id, action, target_user_id=None, details=None):
        """Log administrative actions for audit trail"""
        try:
            log_entry = {
                'user_id': str(user_id),
                'action': action,
                'target_user_id': str(target_user_id) if target_user_id else None,
                'details': details,
                'timestamp': datetime.utcnow(),
                'ip_address': None  # Could be captured from request context
            }
            
            if db and db.connected:
                result = db.insert_document('admin_audit_log', log_entry)
                return str(result) if result else None
            
            # Fallback to file logging
            import json
            os.makedirs('data', exist_ok=True)
            log_file = 'data/admin_audit_log.json'
            
            logs = []
            if os.path.exists(log_file):
                try:
                    with open(log_file, 'r') as f:
                        logs = json.load(f)
                except:
                    logs = []
            
            log_entry['_id'] = len(logs) + 1
            log_entry['timestamp'] = log_entry['timestamp'].isoformat()
            logs.append(log_entry)
            
            with open(log_file, 'w') as f:
                json.dump(logs, f, indent=2)
            
            logger.info(f"Admin action logged: {action} by user {user_id}")
            return str(log_entry['_id'])
            
        except Exception as e:
            logger.error(f"Error logging admin action: {e}")
            return None
    
    @staticmethod
    def decline_password_reset(request_id, declined_by_user_id):
        """Decline password reset request"""
        try:
            # Update request status to declined
            if db and db.connected:
                result = db.update_document(
                    'password_reset_requests',
                    {'_id': request_id},
                    {'$set': {
                        'status': 'declined',
                        'declined_by': str(declined_by_user_id),
                        'declined_at': datetime.utcnow()
                    }}
                )
                logger.info(f"Password reset request {request_id} declined by user {declined_by_user_id}")
                return result > 0
            
            # Fallback to file storage
            import json
            requests_file = 'data/password_reset_requests.json'
            if os.path.exists(requests_file):
                try:
                    with open(requests_file, 'r') as f:
                        requests = json.load(f)
                    
                    for req in requests:
                        if str(req.get('_id')) == str(request_id):
                            req['status'] = 'declined'
                            req['declined_by'] = str(declined_by_user_id)
                            req['declined_at'] = datetime.utcnow().isoformat()
                            break
                    
                    with open(requests_file, 'w') as f:
                        json.dump(requests, f, indent=2)
                    
                    logger.info(f"Password reset request {request_id} declined by user {declined_by_user_id}")
                    return True
                except Exception as e:
                    logger.error(f"Error updating file storage: {e}")
                    return False
            
            return False
            
        except Exception as e:
            logger.error(f"Error declining password reset: {e}")
            return False