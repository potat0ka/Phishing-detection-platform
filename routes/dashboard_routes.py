"""
User Dashboard Routes - Personal Scan History and Statistics
==========================================================

This blueprint handles user-specific dashboard functionality including:
- Personal scan history display
- User statistics and analytics
- Account management for scan data

Author: AI Phishing Detection Platform
"""

import logging
from datetime import datetime
from flask import Blueprint, render_template, session, redirect, url_for, flash, jsonify, request
from models.scan_history_model import ScanHistoryModel

logger = logging.getLogger(__name__)

# Create blueprint for dashboard routes
dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
def dashboard_redirect():
    """
    Redirect old dashboard route to proper RBAC dashboard based on user role
    """
    user_id = session.get('user_id')
    if not user_id:
        flash('Please log in to view your dashboard', 'warning')
        return redirect(url_for('auth.login'))
    
    user_role = session.get('role', 'user')
    
    if user_role == 'superadmin':
        return redirect(url_for('rbac.superadmin_dashboard'))
    elif user_role == 'admin':
        return redirect(url_for('rbac.admin_dashboard'))
    else:
        return redirect(url_for('rbac.user_dashboard'))

@dashboard_bp.route('/api/user-stats')
def api_user_stats():
    """
    API endpoint for user statistics (for AJAX updates)
    
    Returns JSON data for real-time dashboard updates
    """
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'error': 'Authentication required'}), 401
        
        # Get current user statistics
        user_stats = ScanHistoryModel.get_user_scan_stats(user_id)
        recent_scans = ScanHistoryModel.get_user_scan_history(user_id, limit=10)
        
        response_data = {
            'stats': user_stats,
            'recent_scans': [
                {
                    'content': scan.get('content', '')[:50] + '...' if len(scan.get('content', '')) > 50 else scan.get('content', ''),
                    'content_type': scan.get('content_type', ''),
                    'threat_level': scan.get('threat_level', 'unknown'),
                    'confidence_score': scan.get('confidence_score', 0.0),
                    'created_at': scan.get('created_at', '').strftime('%Y-%m-%d %H:%M') if scan.get('created_at') else 'Unknown'
                }
                for scan in recent_scans
            ],
            'last_updated': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')
        }
        
        return jsonify(response_data)
        
    except Exception as e:
        logger.error(f"Error getting user stats: {str(e)}")
        return jsonify({'error': 'Failed to load statistics'}), 500

@dashboard_bp.route('/scan-history')
def scan_history():
    """
    Detailed scan history page with pagination
    
    Shows comprehensive scan history with filtering and pagination options
    """
    try:
        user_id = session.get('user_id')
        if not user_id:
            flash('Please log in to view your scan history', 'warning')
            return redirect(url_for('auth.login'))
        
        # Get pagination parameters
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))
        offset = (page - 1) * per_page
        
        # Get user's scan history with pagination
        user_scans = ScanHistoryModel.get_user_scan_history(user_id, limit=per_page, offset=offset)
        
        # Get total count for pagination
        total_scans = len(ScanHistoryModel.get_user_scan_history(user_id, limit=1000))  # Get approximate total
        
        # Calculate pagination info
        total_pages = (total_scans + per_page - 1) // per_page
        has_prev = page > 1
        has_next = page < total_pages
        
        pagination_context = {
            'user_scans': user_scans,
            'page': page,
            'per_page': per_page,
            'total_scans': total_scans,
            'total_pages': total_pages,
            'has_prev': has_prev,
            'has_next': has_next,
            'prev_page': page - 1 if has_prev else None,
            'next_page': page + 1 if has_next else None
        }
        
        return render_template('admin/scan_history.html', **pagination_context)
        
    except Exception as e:
        logger.error(f"Error loading scan history: {str(e)}")
        flash('Error loading scan history. Please try again.', 'error')
        return render_template('admin/scan_history.html', user_scans=[], page=1)