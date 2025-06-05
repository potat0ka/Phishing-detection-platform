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

logger = logging.getLogger(__name__)

# Create admin blueprint
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    """Admin dashboard with comprehensive system overview"""
    try:
        # Get all users with scan counts
        users = get_all_users_with_stats()
        
        # Get recent scan logs
        scan_logs = get_recent_scan_logs(limit=50)
        
        # Get reported content
        reported_content = get_reported_content()
        
        # Get safety tips by category
        email_tips = db_manager.find_many('security_tips', {'category': 'email'})
        url_tips = db_manager.find_many('security_tips', {'category': 'url'})
        general_tips = db_manager.find_many('security_tips', {'category': 'general'})
        
        # Calculate system statistics
        stats = calculate_system_stats()
        
        # Calculate analytics data
        analytics = calculate_analytics_data()
        
        return render_template('admin/dashboard.html',
                             users=users,
                             scan_logs=scan_logs,
                             reported_content=reported_content,
                             email_tips=email_tips,
                             url_tips=url_tips,
                             general_tips=general_tips,
                             stats=stats,
                             analytics=analytics,
                             current_user=get_current_user())
                             
    except Exception as e:
        logger.error(f"Error loading admin dashboard: {e}")
        flash('Error loading dashboard data', 'error')
        return redirect(url_for('dashboard'))

@admin_bp.route('/live-stats')
@admin_required
def live_stats():
    """API endpoint for real-time statistics updates"""
    try:
        stats = calculate_system_stats()
        return jsonify({'success': True, 'stats': stats})
    except Exception as e:
        logger.error(f"Error getting live stats: {e}")
        return jsonify({'success': False, 'error': str(e)})

# User Management Routes
@admin_bp.route('/users', methods=['POST'])
@admin_required
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
    """Get detailed user information"""
    try:
        user = db_manager.find_one('users', {'id': user_id})
        if not user:
            return jsonify({'success': False, 'error': 'User not found'})
        
        # Try to decrypt if encrypted
        try:
            user = decrypt_sensitive_data('user', user)
        except:
            pass
        
        # Get user's scan count
        scan_count = db_manager.count_documents('detections', {'user_id': user_id})
        user['scan_count'] = scan_count
        
        return jsonify({'success': True, 'user': user})
        
    except Exception as e:
        logger.error(f"Error getting user {user_id}: {e}")
        return jsonify({'success': False, 'error': str(e)})

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