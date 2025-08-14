#!/usr/bin/env python3
"""
Advanced ML Phishing Detection API
==================================

Secure API endpoints for the advanced self-learning phishing detection system.
Provides comprehensive analysis with real-time learning capabilities.

Features:
- Advanced ML analysis with ensemble models
- Self-learning from user feedback
- Performance metrics and confusion matrix
- Real-time data feed integration
- Security measures against data poisoning
- BERT-based semantic analysis

Author: AI Phishing Detection Platform
"""

import os
import sys
import logging
import time
from datetime import datetime
from typing import Dict, List, Optional, Any
import json
from functools import wraps

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from flask import Flask, request, jsonify, g
    from flask_cors import CORS
    from flask_limiter import Limiter
    from flask_limiter.util import get_remote_address
    import jwt
    from werkzeug.security import check_password_hash, generate_password_hash
    FLASK_AVAILABLE = True
except ImportError:
    FLASK_AVAILABLE = False
    logging.warning("Flask and related libraries not available")

from utils.advanced_ml_detector import AdvancedMLPhishingDetector, validate_detector_requirements

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('advanced_ml_api')

# Initialize Flask app if available
if FLASK_AVAILABLE:
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'advanced-ml-phishing-detector-secret-key-2024')
    
    # Enable CORS
    CORS(app, origins=['http://localhost:3000', 'http://127.0.0.1:3000'])
    
    # Rate limiting
    limiter = Limiter(
        app,
        key_func=get_remote_address,
        default_limits=["1000 per hour", "100 per minute"]
    )
else:
    app = None
    limiter = None

# Global detector instance
advanced_detector = None

# API Configuration
API_CONFIG = {
    'version': '2.0',
    'name': 'Advanced ML Phishing Detection API',
    'description': 'Self-learning phishing detection with ensemble ML models',
    'max_content_length': 10000,
    'supported_content_types': ['url', 'email', 'text', 'html'],
    'learning_enabled': True,
    'security_features': {
        'rate_limiting': True,
        'input_validation': True,
        'data_poisoning_protection': True,
        'authentication': True
    }
}

# Authentication configuration
AUTH_CONFIG = {
    'jwt_expiration_hours': 24,
    'admin_users': {
        'admin': generate_password_hash('admin123'),
        'analyst': generate_password_hash('analyst123')
    }
}

def init_advanced_detector():
    """Initialize the advanced ML detector"""
    global advanced_detector
    
    try:
        if advanced_detector is None:
            logger.info("Initializing Advanced ML Phishing Detector...")
            
            # Check requirements
            requirements = validate_detector_requirements()
            logger.info(f"Detector requirements: {requirements}")
            
            # Initialize detector
            config = {
                'enable_bert': requirements.get('bert_support', False),
                'enable_web_feeds': requirements.get('web_scraping', False),
                'learning_rate': 0.01,
                'max_features': 10000
            }
            
            advanced_detector = AdvancedMLPhishingDetector(config)
            logger.info("Advanced ML detector initialized successfully")
            
            return True
            
    except Exception as e:
        logger.error(f"Failed to initialize advanced detector: {e}")
        return False

def require_auth(f):
    """Decorator for authentication required endpoints"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not FLASK_AVAILABLE:
            return jsonify({'error': 'Flask not available'}), 500
            
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'Authentication token required'}), 401
        
        try:
            if token.startswith('Bearer '):
                token = token[7:]
            
            payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            g.current_user = payload['username']
            
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401
        
        return f(*args, **kwargs)
    
    return decorated_function

def validate_input(data: Dict, required_fields: List[str]) -> Optional[str]:
    """Validate input data"""
    try:
        # Check required fields
        for field in required_fields:
            if field not in data:
                return f"Missing required field: {field}"
        
        # Validate content length
        content = data.get('content', '')
        if len(content) > API_CONFIG['max_content_length']:
            return f"Content too long. Maximum {API_CONFIG['max_content_length']} characters allowed"
        
        if len(content.strip()) < 5:
            return "Content too short. Minimum 5 characters required"
        
        # Validate content type
        content_type = data.get('content_type', 'text')
        if content_type not in API_CONFIG['supported_content_types']:
            return f"Unsupported content type. Supported: {API_CONFIG['supported_content_types']}"
        
        return None
        
    except Exception as e:
        return f"Input validation error: {str(e)}"

if FLASK_AVAILABLE and app:
    # Initialize the detector immediately
    init_advanced_detector()
    
    @app.route('/api/v2/health', methods=['GET'])
    def health_check():
        """Health check endpoint"""
        try:
            detector_status = advanced_detector is not None
            requirements = validate_detector_requirements()
            
            return jsonify({
                'status': 'healthy' if detector_status else 'unhealthy',
                'timestamp': datetime.now().isoformat(),
                'version': API_CONFIG['version'],
                'detector_initialized': detector_status,
                'requirements': requirements,
                'features': {
                    'ml_models': requirements.get('ml_libraries', False),
                    'bert_nlp': requirements.get('bert_support', False),
                    'web_feeds': requirements.get('web_scraping', False),
                    'self_learning': True,
                    'ensemble_models': True
                }
            })
            
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return jsonify({
                'status': 'error',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }), 500
    
    @app.route('/api/v2/auth/login', methods=['POST'])
    @limiter.limit("5 per minute")
    def login():
        """Authentication endpoint"""
        try:
            data = request.get_json()
            if not data:
                return jsonify({'error': 'JSON data required'}), 400
            
            username = data.get('username')
            password = data.get('password')
            
            if not username or not password:
                return jsonify({'error': 'Username and password required'}), 400
            
            # Check credentials
            if username in AUTH_CONFIG['admin_users']:
                if check_password_hash(AUTH_CONFIG['admin_users'][username], password):
                    # Generate JWT token
                    payload = {
                        'username': username,
                        'exp': datetime.utcnow().timestamp() + (AUTH_CONFIG['jwt_expiration_hours'] * 3600)
                    }
                    
                    token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
                    
                    return jsonify({
                        'success': True,
                        'token': token,
                        'expires_in': AUTH_CONFIG['jwt_expiration_hours'] * 3600,
                        'user': username
                    })
            
            return jsonify({'error': 'Invalid credentials'}), 401
            
        except Exception as e:
            logger.error(f"Login failed: {e}")
            return jsonify({'error': 'Authentication failed'}), 500
    
    @app.route('/api/v2/analyze', methods=['POST'])
    @limiter.limit("100 per minute")
    def analyze_content():
        """Advanced content analysis endpoint"""
        start_time = time.time()
        
        try:
            # Check if detector is initialized
            if not advanced_detector:
                return jsonify({
                    'error': 'Advanced detector not initialized',
                    'suggestion': 'Check health endpoint for initialization status'
                }), 503
            
            # Get and validate input
            data = request.get_json()
            if not data:
                return jsonify({'error': 'JSON data required'}), 400
            
            validation_error = validate_input(data, ['content'])
            if validation_error:
                return jsonify({'error': validation_error}), 400
            
            content = data['content']
            content_type = data.get('content_type', 'text')
            metadata = data.get('metadata', {})
            
            # Perform analysis
            result = advanced_detector.analyze_content(
                content=content,
                content_type=content_type,
                metadata=metadata
            )
            
            # Add API metadata
            result.update({
                'api_version': API_CONFIG['version'],
                'processing_time': round(time.time() - start_time, 4),
                'request_timestamp': datetime.now().isoformat(),
                'detector_type': 'advanced_ml_ensemble'
            })
            
            # Log analysis
            logger.info(f"Analysis completed: {content_type} -> {result['threat_level']} (score: {result['risk_score']})")
            
            return jsonify(result)
            
        except Exception as e:
            logger.error(f"Analysis failed: {e}")
            return jsonify({
                'error': 'Analysis failed',
                'details': str(e),
                'timestamp': datetime.now().isoformat()
            }), 500
    
    @app.route('/api/v2/learn', methods=['POST'])
    @limiter.limit("50 per minute")
    def learn_from_feedback():
        """Learning endpoint for user feedback"""
        try:
            if not advanced_detector:
                return jsonify({'error': 'Advanced detector not initialized'}), 503
            
            data = request.get_json()
            if not data:
                return jsonify({'error': 'JSON data required'}), 400
            
            validation_error = validate_input(data, ['content', 'is_phishing'])
            if validation_error:
                return jsonify({'error': validation_error}), 400
            
            content = data['content']
            is_phishing = data['is_phishing']
            content_type = data.get('content_type', 'text')
            metadata = data.get('metadata', {})
            
            # Validate is_phishing field
            if not isinstance(is_phishing, bool):
                return jsonify({'error': 'is_phishing must be a boolean value'}), 400
            
            # Learn from feedback
            result = advanced_detector.learn_from_feedback(
                content=content,
                is_phishing=is_phishing,
                content_type=content_type,
                metadata=metadata
            )
            
            if result['success']:
                logger.info(f"Learning successful: {content_type} -> {is_phishing}")
                return jsonify({
                    'success': True,
                    'message': 'Feedback incorporated successfully',
                    'buffer_size': result.get('buffer_size', 0),
                    'timestamp': datetime.now().isoformat()
                })
            else:
                return jsonify({
                    'success': False,
                    'error': result.get('error', 'Learning failed'),
                    'timestamp': datetime.now().isoformat()
                }), 400
            
        except Exception as e:
            logger.error(f"Learning failed: {e}")
            return jsonify({
                'success': False,
                'error': 'Learning failed',
                'details': str(e)
            }), 500
    
    @app.route('/api/v2/metrics', methods=['GET'])
    @require_auth
    def get_performance_metrics():
        """Get performance metrics and confusion matrix"""
        try:
            if not advanced_detector:
                return jsonify({'error': 'Advanced detector not initialized'}), 503
            
            metrics = advanced_detector.get_performance_metrics()
            
            # Add additional metadata
            metrics.update({
                'api_version': API_CONFIG['version'],
                'timestamp': datetime.now().isoformat(),
                'detector_info': advanced_detector.get_model_info() if hasattr(advanced_detector, 'get_model_info') else {}
            })
            
            return jsonify(metrics)
            
        except Exception as e:
            logger.error(f"Metrics retrieval failed: {e}")
            return jsonify({
                'error': 'Failed to retrieve metrics',
                'details': str(e)
            }), 500
    
    @app.route('/api/v2/models/info', methods=['GET'])
    @require_auth
    def get_model_info():
        """Get detailed model information"""
        try:
            if not advanced_detector:
                return jsonify({'error': 'Advanced detector not initialized'}), 503
            
            if hasattr(advanced_detector, 'get_model_info'):
                model_info = advanced_detector.get_model_info()
            else:
                model_info = {'error': 'Model info not available'}
            
            return jsonify({
                'model_info': model_info,
                'api_config': API_CONFIG,
                'requirements': validate_detector_requirements(),
                'timestamp': datetime.now().isoformat()
            })
            
        except Exception as e:
            logger.error(f"Model info retrieval failed: {e}")
            return jsonify({
                'error': 'Failed to retrieve model info',
                'details': str(e)
            }), 500
    
    @app.route('/api/v2/models/export', methods=['POST'])
    @require_auth
    @limiter.limit("5 per hour")
    def export_model():
        """Export model state for backup"""
        try:
            if not advanced_detector:
                return jsonify({'error': 'Advanced detector not initialized'}), 503
            
            data = request.get_json() or {}
            filename = data.get('filename', f'advanced_model_export_{int(time.time())}.pkl')
            
            # Ensure filename is safe
            filename = filename.replace('/', '_').replace('\\', '_')
            filepath = os.path.join('exports', filename)
            
            # Create exports directory if it doesn't exist
            os.makedirs('exports', exist_ok=True)
            
            if hasattr(advanced_detector, 'export_model_state'):
                success = advanced_detector.export_model_state(filepath)
                
                if success:
                    return jsonify({
                        'success': True,
                        'message': 'Model exported successfully',
                        'filepath': filepath,
                        'timestamp': datetime.now().isoformat()
                    })
                else:
                    return jsonify({
                        'success': False,
                        'error': 'Model export failed'
                    }), 500
            else:
                return jsonify({
                    'error': 'Model export not supported'
                }), 501
            
        except Exception as e:
            logger.error(f"Model export failed: {e}")
            return jsonify({
                'success': False,
                'error': 'Export failed',
                'details': str(e)
            }), 500
    
    @app.route('/api/v2/security/status', methods=['GET'])
    @require_auth
    def get_security_status():
        """Get security status and validation metrics"""
        try:
            if not advanced_detector:
                return jsonify({'error': 'Advanced detector not initialized'}), 503
            
            security_status = {
                'data_validation': {
                    'enabled': True,
                    'max_daily_updates': advanced_detector.data_validation['max_daily_updates'],
                    'trusted_sources': advanced_detector.data_validation['trusted_sources']
                },
                'rate_limiting': {
                    'enabled': True,
                    'limits': ['1000 per hour', '100 per minute']
                },
                'authentication': {
                    'enabled': True,
                    'method': 'JWT'
                },
                'input_validation': {
                    'enabled': True,
                    'max_content_length': API_CONFIG['max_content_length']
                },
                'learning_buffer': {
                    'current_size': len(advanced_detector.learning_buffer['features']),
                    'max_size': advanced_detector.learning_buffer['max_size']
                }
            }
            
            return jsonify({
                'security_status': security_status,
                'timestamp': datetime.now().isoformat()
            })
            
        except Exception as e:
            logger.error(f"Security status retrieval failed: {e}")
            return jsonify({
                'error': 'Failed to retrieve security status',
                'details': str(e)
            }), 500
    
    @app.route('/api/v2/batch/analyze', methods=['POST'])
    @require_auth
    @limiter.limit("10 per minute")
    def batch_analyze():
        """Batch analysis endpoint for multiple items"""
        try:
            if not advanced_detector:
                return jsonify({'error': 'Advanced detector not initialized'}), 503
            
            data = request.get_json()
            if not data or 'items' not in data:
                return jsonify({'error': 'Items array required'}), 400
            
            items = data['items']
            if not isinstance(items, list) or len(items) == 0:
                return jsonify({'error': 'Items must be a non-empty array'}), 400
            
            if len(items) > 50:  # Limit batch size
                return jsonify({'error': 'Maximum 50 items per batch'}), 400
            
            results = []
            
            for i, item in enumerate(items):
                try:
                    validation_error = validate_input(item, ['content'])
                    if validation_error:
                        results.append({
                            'index': i,
                            'error': validation_error,
                            'success': False
                        })
                        continue
                    
                    result = advanced_detector.analyze_content(
                        content=item['content'],
                        content_type=item.get('content_type', 'text'),
                        metadata=item.get('metadata', {})
                    )
                    
                    result.update({
                        'index': i,
                        'success': True
                    })
                    
                    results.append(result)
                    
                except Exception as e:
                    results.append({
                        'index': i,
                        'error': str(e),
                        'success': False
                    })
            
            return jsonify({
                'results': results,
                'total_items': len(items),
                'successful_analyses': sum(1 for r in results if r.get('success')),
                'timestamp': datetime.now().isoformat()
            })
            
        except Exception as e:
            logger.error(f"Batch analysis failed: {e}")
            return jsonify({
                'error': 'Batch analysis failed',
                'details': str(e)
            }), 500
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'error': 'Endpoint not found',
            'available_endpoints': [
                '/api/v2/health',
                '/api/v2/auth/login',
                '/api/v2/analyze',
                '/api/v2/learn',
                '/api/v2/metrics',
                '/api/v2/models/info',
                '/api/v2/models/export',
                '/api/v2/security/status',
                '/api/v2/batch/analyze'
            ]
        }), 404
    
    @app.errorhandler(429)
    def ratelimit_handler(e):
        return jsonify({
            'error': 'Rate limit exceeded',
            'description': str(e.description),
            'retry_after': getattr(e, 'retry_after', None)
        }), 429
    
    @app.errorhandler(500)
    def internal_error(error):
        logger.error(f"Internal server error: {error}")
        return jsonify({
            'error': 'Internal server error',
            'timestamp': datetime.now().isoformat()
        }), 500

def create_app():
    """Create and configure the Flask app"""
    if not FLASK_AVAILABLE:
        raise RuntimeError("Flask is not available")
    
    # Initialize detector
    init_advanced_detector()
    
    return app

if __name__ == '__main__':
    if FLASK_AVAILABLE:
        # Initialize detector
        if init_advanced_detector():
            logger.info("Starting Advanced ML Phishing Detection API...")
            app.run(
                host='0.0.0.0',
                port=5001,
                debug=False,
                threaded=True
            )
        else:
            logger.error("Failed to initialize detector. Exiting.")
    else:
        logger.error("Flask not available. Cannot start API server.")