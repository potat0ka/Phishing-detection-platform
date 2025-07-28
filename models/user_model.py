"""
User Model
=========

This model handles user authentication and management in MongoDB.
It manages user accounts, sessions, and role-based access control.

Author: Bigendra Shrestha
"""

from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from .database import db

class UserModel:
    """
    User Model for MongoDB operations
    
    This class handles:
    - User registration and authentication
    - Password hashing and verification
    - Role-based access control
    """
    
    @staticmethod
    def create_user(username, email, password, role='user'):
        """Create a new user account with bcrypt hashing"""
        try:
            # Hash the password with bcrypt
            import bcrypt
            password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            
            user_data = {
                'username': username,
                'email': email,
                'password_hash': password_hash,
                'role': role,
                'is_active': True,
                'created_at': datetime.utcnow(),
                'last_login': None,
                'login_attempts': 0
            }
            
            # Try database connection first
            if db:
                db.test_connection()
                if db.connected:
                    result = db.insert_document('users', user_data)
                    if result:
                        return str(result)
            
            # If MongoDB fails, fall back to a simple file-based storage for demo
            import json
            import os
            
            # Create users directory if it doesn't exist
            os.makedirs('data', exist_ok=True)
            users_file = 'data/users.json'
            
            # Load existing users
            users = []
            if os.path.exists(users_file):
                try:
                    with open(users_file, 'r') as f:
                        users = json.load(f)
                except:
                    users = []
            
            # Add new user with simple ID
            user_data['_id'] = len(users) + 1
            user_data['created_at'] = user_data['created_at'].isoformat()
            users.append(user_data)
            
            # Save users back to file
            with open(users_file, 'w') as f:
                json.dump(users, f, indent=2)
            
            return str(user_data['_id'])
            
        except Exception as e:
            import logging
            logging.error(f"Error creating user: {e}")
            return None
    
    @staticmethod
    def find_user_by_email(email):
        """Find user by email address"""
        try:
            # Try MongoDB first
            if db:
                db.test_connection()
                if db.connected:
                    users = db.find_documents('users', {'email': email})
                    return users[0] if users else None
            
            # Fall back to file storage
            import json
            import os
            
            users_file = 'data/users.json'
            if os.path.exists(users_file):
                try:
                    with open(users_file, 'r') as f:
                        users = json.load(f)
                    for user in users:
                        if user.get('email') == email:
                            return user
                except:
                    pass
            
            return None
        except Exception as e:
            import logging
            logging.error(f"Error finding user by email: {e}")
            return None
    
    @staticmethod
    def find_user_by_username(username):
        """Find user by username"""
        try:
            # Try MongoDB first
            if db:
                db.test_connection()
                if db.connected:
                    users = db.find_documents('users', {'username': username})
                    return users[0] if users else None
            
            # Fall back to file storage
            import json
            import os
            
            users_file = 'data/users.json'
            if os.path.exists(users_file):
                try:
                    with open(users_file, 'r') as f:
                        users = json.load(f)
                    for user in users:
                        if user.get('username') == username:
                            return user
                except:
                    pass
            
            return None
        except Exception as e:
            import logging
            logging.error(f"Error finding user by username: {e}")
            return None
    
    @staticmethod
    def verify_password(user, password):
        """Verify user password with bcrypt"""
        try:
            if user and 'password_hash' in user:
                import bcrypt
                stored_password = user['password_hash'].encode('utf-8')
                password_bytes = password.encode('utf-8')
                return bcrypt.checkpw(password_bytes, stored_password)
            return False
        except Exception:
            return False
    
    @staticmethod
    def get_user_by_id(user_id):
        """Get user by ID"""
        try:
            # Try MongoDB first
            if db:
                db.test_connection()
                if db.connected:
                    users = db.find_documents('users', {'_id': user_id})
                    return users[0] if users else None
            
            # Fall back to file storage
            import json
            import os
            
            users_file = 'data/users.json'
            if os.path.exists(users_file):
                try:
                    with open(users_file, 'r') as f:
                        users = json.load(f)
                    for user in users:
                        if str(user.get('_id')) == str(user_id):
                            return user
                except:
                    pass
            
            return None
        except Exception as e:
            import logging
            logging.error(f"Error finding user by ID: {e}")
            return None
    
    @staticmethod
    def update_user_password(user_id, new_password):
        """Update user password with bcrypt"""
        try:
            # Hash the new password with bcrypt
            import bcrypt
            hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            
            # Try MongoDB first
            if db and db.connected:
                result = db.update_document(
                    'users',
                    {'_id': user_id},
                    {'$set': {
                        'password_hash': hashed_password,
                        'updated_at': datetime.utcnow()
                    }}
                )
                return result > 0
            
            # Fall back to file storage
            import json
            import os
            
            users_file = 'data/users.json'
            if os.path.exists(users_file):
                try:
                    with open(users_file, 'r') as f:
                        users = json.load(f)
                    
                    # Find and update user
                    for i, user in enumerate(users):
                        if str(user.get('_id')) == str(user_id):
                            users[i]['password_hash'] = hashed_password
                            users[i]['updated_at'] = datetime.utcnow().isoformat()
                            
                            # Save back to file
                            with open(users_file, 'w') as f:
                                json.dump(users, f, indent=2, default=str)
                            return True
                except Exception as e:
                    import logging
                    logging.error(f"Error updating password in file: {e}")
            
            return False
        except Exception as e:
            import logging
            logging.error(f"Error updating user password: {e}")
            return False
    
    @staticmethod
    def update_last_login(user_id):
        """Update user's last login time"""
        if db and db.connected:
            return db.update_document(
                'users',
                {'_id': user_id},
                {'$set': {'last_login': datetime.utcnow()}}
            )
        return 0
    
    @staticmethod
    def get_user_count():
        """Get total number of users"""
        try:
            if db and db.connected:
                users = db.find_documents('users', {})
                return len(users) if users else 0
            
            # File-based fallback
            import json
            import os
            users_file = 'data/users.json'
            if os.path.exists(users_file):
                with open(users_file, 'r') as f:
                    users = json.load(f)
                return len(users)
            return 0
        except Exception:
            return 0
    
    @staticmethod
    def get_admin_count():
        """Get number of admin users"""
        try:
            if db and db.connected:
                users = db.find_documents('users', {'role': 'admin'})
                return len(users) if users else 0
            
            # File-based fallback
            import json
            import os
            users_file = 'data/users.json'
            if os.path.exists(users_file):
                with open(users_file, 'r') as f:
                    users = json.load(f)
                return len([u for u in users if u.get('role') == 'admin'])
            return 0
        except Exception:
            return 0
    
    @staticmethod
    def get_superadmin_count():
        """Get number of superadmin users"""
        try:
            if db and db.connected:
                users = db.find_documents('users', {'role': 'superadmin'})
                return len(users) if users else 0
            
            # File-based fallback
            import json
            import os
            users_file = 'data/users.json'
            if os.path.exists(users_file):
                with open(users_file, 'r') as f:
                    users = json.load(f)
                return len([u for u in users if u.get('role') == 'superadmin'])
            return 0
        except Exception:
            return 0
    
    @staticmethod
    def get_all_users():
        """Get all users"""
        try:
            if db and db.connected:
                return db.find_documents('users', {})
            
            # File-based fallback
            import json
            import os
            users_file = 'data/users.json'
            if os.path.exists(users_file):
                with open(users_file, 'r') as f:
                    return json.load(f)
            return []
        except Exception:
            return []
    
    @staticmethod
    def get_users_by_role(role):
        """Get users by specific role"""
        try:
            if db and db.connected:
                return db.find_documents('users', {'role': role})
            
            # File-based fallback
            import json
            import os
            users_file = 'data/users.json'
            if os.path.exists(users_file):
                with open(users_file, 'r') as f:
                    users = json.load(f)
                return [u for u in users if u.get('role') == role]
            return []
        except Exception:
            return []
    
    @staticmethod
    def find_user_by_id(user_id):
        """Find user by ID"""
        try:
            if db and db.connected:
                users = db.find_documents('users', {'_id': user_id})
                return users[0] if users else None
            
            # File-based fallback
            import json
            import os
            users_file = 'data/users.json'
            if os.path.exists(users_file):
                with open(users_file, 'r') as f:
                    users = json.load(f)
                for user in users:
                    if str(user.get('_id')) == str(user_id):
                        return user
            return None
        except Exception:
            return None
    
    @staticmethod
    def find_user_by_email(email):
        """Find user by email"""
        try:
            if db and db.connected:
                users = db.find_documents('users', {'email': email})
                return users[0] if users else None
            
            # File-based fallback
            import json
            import os
            users_file = 'data/users.json'
            if os.path.exists(users_file):
                with open(users_file, 'r') as f:
                    users = json.load(f)
                for user in users:
                    if user.get('email') == email:
                        return user
            return None
        except Exception:
            return None
    
    @staticmethod
    def find_user_by_username(username):
        """Find user by username"""
        try:
            if db and db.connected:
                users = db.find_documents('users', {'username': username})
                return users[0] if users else None
            
            # File-based fallback
            import json
            import os
            users_file = 'data/users.json'
            if os.path.exists(users_file):
                with open(users_file, 'r') as f:
                    users = json.load(f)
                for user in users:
                    if user.get('username') == username:
                        return user
            return None
        except Exception:
            return None
    
    @staticmethod
    def verify_password(user, password):
        """Verify user password using bcrypt"""
        try:
            import bcrypt
            stored_password = user.get('password_hash', '').encode('utf-8')
            password_bytes = password.encode('utf-8')
            return bcrypt.checkpw(password_bytes, stored_password)
        except Exception:
            return False
    
    @staticmethod
    def is_admin(user):
        """Check if user has admin role"""
        return user and user.get('role') in ['admin', 'superadmin']
    
    @staticmethod
    def is_superadmin(user):
        """Check if user has superadmin role"""
        return user and user.get('role') == 'superadmin'
    
    @staticmethod
    def update_user_role(user_id, new_role):
        """Update user's role (admin function)"""
        try:
            if db and db.connected:
                result = db.update_document(
                    'users',
                    {'_id': user_id},
                    {'$set': {'role': new_role, 'role_updated_at': datetime.utcnow()}}
                )
                return result
            
            # Fallback to file storage
            import json
            import os
            users_file = 'data/users.json'
            if os.path.exists(users_file):
                try:
                    with open(users_file, 'r') as f:
                        users = json.load(f)
                    
                    for i, user in enumerate(users):
                        if str(user.get('_id')) == str(user_id):
                            users[i]['role'] = new_role
                            users[i]['role_updated_at'] = datetime.utcnow().isoformat()
                            break
                    
                    with open(users_file, 'w') as f:
                        json.dump(users, f, indent=2)
                    
                    return 1
                except:
                    pass
            
            return 0
        except Exception as e:
            import logging
            logging.error(f"Error updating user role: {e}")
            return 0
    
    @staticmethod
    def deactivate_user(user_id):
        """Deactivate user account"""
        if db and db.connected:
            return db.update_document(
                'users',
                {'_id': user_id},
                {'$set': {'is_active': False}}
            )
        return 0
    
    @staticmethod
    def get_user_creation_date(user_id):
        """Get user account creation date"""
        try:
            if db and db.connected:
                user = db.find_document('users', {'_id': user_id})
                if user:
                    return user.get('created_at')
            
            # Fallback to file storage
            import json
            import os
            users_file = 'data/users.json'
            if os.path.exists(users_file):
                try:
                    with open(users_file, 'r') as f:
                        users = json.load(f)
                    for user in users:
                        if str(user.get('_id')) == str(user_id):
                            return user.get('created_at')
                except:
                    pass
            return None
        except Exception as e:
            import logging
            logging.error(f"Error getting user creation date: {e}")
            return None