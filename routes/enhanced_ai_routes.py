from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from functools import wraps
import json
import logging
from datetime import datetime, timedelta
import traceback

# Import the enhanced AI components
try:
    from utils.enhanced_ensemble_detector import create_enhanced_detector
    from utils.realtime_detection_api import create_realtime_api
    from utils.accuracy_tracker import AccuracyTracker
    from utils.security_hardening import SecurityHardening
    from utils.ui_enhancements import UIEnhancements
    from utils.enhanced_ai_api import EnhancedAIAPI
except ImportError as e:
    logging.warning(f"Enhanced AI components not available: {e}")
    # Fallback to basic components if enhanced ones are not available
    create_enhanced_detector = None
    create_realtime_api = None
    AccuracyTracker = None
    SecurityHardening = None
    UIEnhancements = None
    EnhancedAIAPI = None

# Create Blueprint
enhanced_ai_bp = Blueprint('enhanced_ai', __name__)

# Global instances (will be initialized when needed)
enhanced_detector = None
realtime_api = None
accuracy_tracker = None
security_hardening = None
ui_enhancements = None
enhanced_ai_api = None

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def require_auth(f):
    """Decorator to require authentication for enhanced AI routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            if request.is_json:
                return jsonify({'error': 'Authentication required'}), 401
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def initialize_components():
    """Initialize all enhanced AI components"""
    global enhanced_detector, realtime_api, accuracy_tracker, security_hardening, ui_enhancements, enhanced_ai_api
    
    try:
        if create_enhanced_detector and not enhanced_detector:
            logger.info("Initializing Enhanced Ensemble Detector...")
            enhanced_detector = create_enhanced_detector()
            
        if create_realtime_api and not realtime_api:
            logger.info("Initializing Real-time Detection API...")
            realtime_api = create_realtime_api(enhanced_detector)
            
        if AccuracyTracker and not accuracy_tracker:
            logger.info("Initializing Accuracy Tracker...")
            accuracy_tracker = AccuracyTracker()
            
        if SecurityHardening and not security_hardening:
            logger.info("Initializing Security Hardening...")
            security_hardening = SecurityHardening()
            
        if UIEnhancements and not ui_enhancements:
            logger.info("Initializing UI Enhancements...")
            ui_enhancements = UIEnhancements(enhanced_detector)
            
        if EnhancedAIAPI and not enhanced_ai_api:
            logger.info("Initializing Enhanced AI API...")
            enhanced_ai_api = EnhancedAIAPI()
            
        logger.info("All enhanced AI components initialized successfully")
        return True
        
    except Exception as e:
        logger.error(f"Error initializing enhanced AI components: {e}")
        logger.error(traceback.format_exc())
        return False



@enhanced_ai_bp.route('/api/enhanced-detect', methods=['POST'])
@require_auth
def enhanced_detect():
    """Enhanced detection endpoint with real-time processing"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
            
        # Validate input using security hardening
        if security_hardening:
            validation_result = security_hardening.validate_input(data)
            if not validation_result['is_valid']:
                return jsonify({
                    'error': 'Invalid input',
                    'details': validation_result['errors']
                }), 400
        
        # Extract detection parameters
        url = data.get('url', '')
        email_content = data.get('email_content', '')
        text_content = data.get('text_content', '')
        
        # Perform enhanced detection
        if realtime_api:
            result = realtime_api.detect(
                url=url,
                email_content=email_content,
                text_content=text_content,
                user_id=session.get('user_id')
            )
        elif enhanced_detector:
            # Fallback to direct detector usage
            result = enhanced_detector.predict(
                url=url,
                email_content=email_content,
                text_content=text_content
            )
        else:
            return jsonify({'error': 'Enhanced detection not available'}), 503
            
        # Generate explanations if UI enhancements are available
        if ui_enhancements and result.get('prediction') is not None:
            explanation = ui_enhancements.explain_prediction(
                url=url,
                email_content=email_content,
                text_content=text_content,
                prediction=result['prediction']
            )
            result['explanation'] = explanation
            
        # Record prediction for accuracy tracking
        if accuracy_tracker:
            accuracy_tracker.record_prediction(
                input_data={
                    'url': url,
                    'email_content': email_content,
                    'text_content': text_content
                },
                prediction=result.get('prediction', 0),
                confidence=result.get('confidence', 0.0),
                model_version=result.get('model_version', '1.0'),
                user_id=session.get('user_id')
            )
            
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error in enhanced detection: {e}")
        logger.error(traceback.format_exc())
        return jsonify({'error': 'Detection failed', 'details': str(e)}), 500

@enhanced_ai_bp.route('/api/feedback', methods=['POST'])
@require_auth
def submit_feedback():
    """Submit user feedback for model improvement"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No feedback data provided'}), 400
            
        # Validate feedback data
        required_fields = ['prediction_id', 'feedback_type', 'is_correct']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
                
        # Submit feedback to accuracy tracker
        if accuracy_tracker:
            feedback_id = accuracy_tracker.add_feedback(
                prediction_id=data['prediction_id'],
                feedback_type=data['feedback_type'],
                is_correct=data['is_correct'],
                user_feedback=data.get('user_feedback', ''),
                user_id=session.get('user_id')
            )
            
            # Update model with feedback if enhanced detector supports it
            if enhanced_detector and hasattr(enhanced_detector, 'update_with_feedback'):
                enhanced_detector.update_with_feedback(
                    prediction_id=data['prediction_id'],
                    is_correct=data['is_correct']
                )
                
            return jsonify({
                'success': True,
                'feedback_id': feedback_id,
                'message': 'Feedback submitted successfully'
            })
        else:
            return jsonify({'error': 'Feedback system not available'}), 503
            
    except Exception as e:
        logger.error(f"Error submitting feedback: {e}")
        return jsonify({'error': 'Failed to submit feedback', 'details': str(e)}), 500



@enhanced_ai_bp.route('/api/metrics')
@require_auth
def get_metrics():
    """Get detailed metrics for monitoring"""
    try:
        metrics = {}
        
        # Get accuracy metrics
        if accuracy_tracker:
            metrics['accuracy'] = accuracy_tracker.get_performance_metrics()
            
        # Get model performance metrics
        if enhanced_detector and hasattr(enhanced_detector, 'get_model_metrics'):
            metrics['model_performance'] = enhanced_detector.get_model_metrics()
            
        # Get security metrics
        if security_hardening and hasattr(security_hardening, 'get_security_metrics'):
            metrics['security'] = security_hardening.get_security_metrics()
            
        # Get system resource metrics
        import psutil
        metrics['system'] = {
            'cpu_percent': psutil.cpu_percent(),
            'memory_percent': psutil.virtual_memory().percent,
            'disk_percent': psutil.disk_usage('/').percent if hasattr(psutil.disk_usage('/'), 'percent') else 0
        }
        
        return jsonify(metrics)
        
    except Exception as e:
        logger.error(f"Error getting metrics: {e}")
        return jsonify({'error': 'Failed to get metrics', 'details': str(e)}), 500

@enhanced_ai_bp.route('/api/model-info')
@require_auth
def get_model_info():
    """Get information about the current models"""
    try:
        model_info = {}
        
        if enhanced_detector:
            model_info = {
                'model_type': 'Enhanced Ensemble Detector',
                'version': getattr(enhanced_detector, 'version', '1.0'),
                'last_trained': getattr(enhanced_detector, 'last_trained', 'Unknown'),
                'features_count': getattr(enhanced_detector, 'features_count', 'Unknown'),
                'models': [
                    'XGBoost Classifier',
                    'Random Forest',
                    'Deep Learning Model',
                    'CatBoost',
                    'BERT/DistilBERT'
                ]
            }
            
            # Get model-specific information if available
            if hasattr(enhanced_detector, 'get_model_info'):
                model_info.update(enhanced_detector.get_model_info())
                
        return jsonify(model_info)
        
    except Exception as e:
        logger.error(f"Error getting model info: {e}")
        return jsonify({'error': 'Failed to get model info', 'details': str(e)}), 500

@enhanced_ai_bp.route('/api/retrain', methods=['POST'])
@require_auth
def retrain_model():
    """Trigger model retraining"""
    try:
        # Check if user has admin privileges
        user_role = session.get('role', 'user')
        if user_role not in ['admin', 'analyst']:
            return jsonify({'error': 'Insufficient privileges'}), 403
            
        if enhanced_detector and hasattr(enhanced_detector, 'retrain'):
            # Start retraining in background
            result = enhanced_detector.retrain()
            return jsonify({
                'success': True,
                'message': 'Model retraining initiated',
                'job_id': result.get('job_id', 'unknown')
            })
        else:
            return jsonify({'error': 'Model retraining not available'}), 503
            
    except Exception as e:
        logger.error(f"Error retraining model: {e}")
        return jsonify({'error': 'Failed to retrain model', 'details': str(e)}), 500

@enhanced_ai_bp.route('/api/export-data', methods=['POST'])
@require_auth
def export_data():
    """Export detection data and metrics"""
    try:
        # Check if user has admin privileges
        user_role = session.get('role', 'user')
        if user_role not in ['admin', 'analyst']:
            return jsonify({'error': 'Insufficient privileges'}), 403
            
        data = request.get_json()
        export_type = data.get('export_type', 'metrics')
        date_range = data.get('date_range', 7)  # days
        
        export_data = {}
        
        if export_type in ['metrics', 'all'] and accuracy_tracker:
            # Export accuracy metrics
            end_date = datetime.now()
            start_date = end_date - timedelta(days=date_range)
            export_data['metrics'] = accuracy_tracker.get_metrics_for_period(start_date, end_date)
            
        if export_type in ['predictions', 'all'] and accuracy_tracker:
            # Export prediction data
            export_data['predictions'] = accuracy_tracker.get_predictions_for_period(start_date, end_date)
            
        if export_type in ['feedback', 'all'] and accuracy_tracker:
            # Export feedback data
            export_data['feedback'] = accuracy_tracker.get_feedback_for_period(start_date, end_date)
            
        return jsonify({
            'success': True,
            'data': export_data,
            'export_timestamp': datetime.now().isoformat(),
            'date_range': f"{start_date.isoformat()} to {end_date.isoformat()}"
        })
        
    except Exception as e:
        logger.error(f"Error exporting data: {e}")
        return jsonify({'error': 'Failed to export data', 'details': str(e)}), 500

@enhanced_ai_bp.route('/api/health')
def health_check():
    """Health check endpoint for monitoring"""
    try:
        health_status = {
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'components': {
                'enhanced_detector': enhanced_detector is not None,
                'realtime_api': realtime_api is not None,
                'accuracy_tracker': accuracy_tracker is not None,
                'security_hardening': security_hardening is not None,
                'ui_enhancements': ui_enhancements is not None
            }
        }
        
        # Check component health if methods are available
        for component_name, component in [
            ('enhanced_detector', enhanced_detector),
            ('realtime_api', realtime_api),
            ('accuracy_tracker', accuracy_tracker),
            ('security_hardening', security_hardening),
            ('ui_enhancements', ui_enhancements)
        ]:
            if component and hasattr(component, 'health_check'):
                try:
                    component_health = component.health_check()
                    health_status['components'][component_name] = component_health
                except Exception as e:
                    health_status['components'][component_name] = {'status': 'error', 'error': str(e)}
                    
        # Determine overall status
        if not any(health_status['components'].values()):
            health_status['status'] = 'unhealthy'
        elif not all(isinstance(v, bool) and v for v in health_status['components'].values()):
            health_status['status'] = 'degraded'
            
        status_code = 200 if health_status['status'] == 'healthy' else 503
        return jsonify(health_status), status_code
        
    except Exception as e:
        logger.error(f"Error in health check: {e}")
        return jsonify({
            'status': 'error',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

# Initialize components when blueprint is registered
# Note: before_app_first_request is deprecated in newer Flask versions
# Components will be initialized on first use instead
def initialize_enhanced_ai():
    """Initialize enhanced AI components when needed"""
    logger.info("Initializing Enhanced AI components...")
    initialize_components()

# Initialize components immediately when module is loaded
try:
    initialize_enhanced_ai()
except Exception as e:
    logger.warning(f"Failed to initialize enhanced AI components: {e}")

# Error handlers
@enhanced_ai_bp.errorhandler(404)
def not_found(error):
    if request.is_json:
        return jsonify({'error': 'Endpoint not found'}), 404
    return render_template('error.html', error="Page not found"), 404

@enhanced_ai_bp.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal server error: {error}")
    if request.is_json:
        return jsonify({'error': 'Internal server error'}), 500
    return render_template('error.html', error="Internal server error"), 500

@enhanced_ai_bp.errorhandler(503)
def service_unavailable(error):
    if request.is_json:
        return jsonify({'error': 'Service temporarily unavailable'}), 503
    return render_template('error.html', error="Service temporarily unavailable"), 503