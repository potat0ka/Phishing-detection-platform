#!/usr/bin/env python3
"""
Enhanced AI API Integration Module

This module provides a unified API interface for the upgraded AI Core system,
integrating all enhanced components:
- Enhanced Ensemble Detector
- Real-time Detection API
- Accuracy Tracker
- Security Hardening
- UI Enhancements

Author: AI Assistant
Date: 2024
"""

import os
import json
import time
import logging
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any, Union
from dataclasses import dataclass, asdict
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import threading

# Flask components
try:
    from flask import Flask, request, jsonify, render_template, session
    from flask_cors import CORS
    from flask_limiter import Limiter
    from flask_limiter.util import get_remote_address
    from flask_caching import Cache
    FLASK_AVAILABLE = True
except ImportError:
    FLASK_AVAILABLE = False
    Flask = None
    CORS = None
    Limiter = None
    Cache = None

# JWT for API authentication
try:
    import jwt
    JWT_AVAILABLE = True
except ImportError:
    JWT_AVAILABLE = False
    jwt = None

# Prometheus monitoring
try:
    from prometheus_client import Counter, Histogram, Gauge, generate_latest
    PROMETHEUS_AVAILABLE = True
except ImportError:
    PROMETHEUS_AVAILABLE = False
    Counter = None
    Histogram = None
    Gauge = None
    generate_latest = None

# Import our enhanced modules
try:
    from utils.enhanced_ensemble_detector import create_enhanced_detector
    from utils.realtime_detection_api import create_realtime_api
    from utils.accuracy_tracker import AccuracyTracker
    from utils.security_hardening import SecurityHardening
    from utils.ui_enhancements import UIEnhancements
    ENHANCED_MODULES_AVAILABLE = True
except ImportError:
    ENHANCED_MODULES_AVAILABLE = False
    create_enhanced_detector = None
    create_realtime_api = None
    AccuracyTracker = None
    SecurityHardening = None
    UIEnhancements = None

# Helper functions for missing modules
def create_accuracy_tracker():
    """Fallback function for accuracy tracker"""
    return None

def create_security_hardening(config):
    """Fallback function for security hardening"""
    return None

def create_ui_enhancements(data_dir):
    """Fallback function for UI enhancements"""
    return None

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class APIConfig:
    """Configuration for Enhanced AI API"""
    # Flask settings
    host: str = "0.0.0.0"
    port: int = 5000
    debug: bool = False
    
    # Security settings
    secret_key: str = "your-secret-key-change-this"
    jwt_secret: str = "your-jwt-secret-change-this"
    rate_limit: str = "100 per hour"
    
    # Cache settings
    cache_type: str = "simple"
    cache_timeout: int = 300  # 5 minutes
    
    # Model settings
    model_update_interval: int = 3600  # 1 hour
    batch_size: int = 32
    max_workers: int = 4
    
    # Storage settings
    data_dir: str = "data"
    model_dir: str = "models"
    logs_dir: str = "logs"
    
    # Feature flags
    enable_real_time: bool = True
    enable_security: bool = True
    enable_ui_enhancements: bool = True
    enable_monitoring: bool = True
    enable_auto_learning: bool = True


@dataclass
class DetectionRequest:
    """Enhanced detection request"""
    content: str
    content_type: str  # 'url', 'email', 'text', 'file'
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    metadata: Optional[Dict] = None
    require_explanation: bool = True
    confidence_threshold: float = 0.5


@dataclass
class DetectionResponse:
    """Enhanced detection response"""
    request_id: str
    prediction: str
    confidence: float
    risk_score: float
    processing_time: float
    explanation: Optional[Dict] = None
    recommendations: List[str] = None
    security_validation: Optional[Dict] = None
    model_version: str = "enhanced_v1.0"
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()


class EnhancedAIAPI:
    """Enhanced AI API with all upgraded components"""
    
    def __init__(self, config: Optional[APIConfig] = None):
        self.config = config or APIConfig()
        self.app = None
        self.executor = ThreadPoolExecutor(max_workers=self.config.max_workers)
        
        # Initialize components
        self.detector = None
        self.realtime_api = None
        self.accuracy_tracker = None
        self.security_hardening = None
        self.ui_enhancements = None
        
        # Monitoring metrics
        self.metrics = self._initialize_metrics()
        
        # Background tasks
        self.background_tasks = []
        self.shutdown_event = threading.Event()
        
        # Initialize all components
        self._initialize_components()
        self._initialize_flask_app()
        
        logger.info("Enhanced AI API initialized")
    
    def _initialize_metrics(self) -> Dict:
        """Initialize Prometheus metrics"""
        if not PROMETHEUS_AVAILABLE:
            return {}
        
        return {
            'requests_total': Counter('api_requests_total', 'Total API requests', ['endpoint', 'method']),
            'request_duration': Histogram('api_request_duration_seconds', 'Request duration'),
            'detections_total': Counter('detections_total', 'Total detections', ['prediction', 'confidence_level']),
            'model_accuracy': Gauge('model_accuracy', 'Current model accuracy'),
            'active_users': Gauge('active_users', 'Number of active users'),
            'cache_hits': Counter('cache_hits_total', 'Cache hits'),
            'cache_misses': Counter('cache_misses_total', 'Cache misses'),
            'security_violations': Counter('security_violations_total', 'Security violations', ['type'])
        }
    
    def _initialize_components(self):
        """Initialize all enhanced components"""
        try:
            # Create data directories
            for dir_name in [self.config.data_dir, self.config.model_dir, self.config.logs_dir]:
                Path(dir_name).mkdir(parents=True, exist_ok=True)
            
            # Initialize enhanced detector
            if ENHANCED_MODULES_AVAILABLE:
                if create_enhanced_detector:
                    self.detector = create_enhanced_detector()
                else:
                    self.detector = None
                logger.info("Enhanced ensemble detector initialized")
                
                # Initialize real-time API
                if create_realtime_api:
                    self.realtime_api = create_realtime_api()
                else:
                    self.realtime_api = None
                logger.info("Real-time detection API initialized")
                
                # Initialize accuracy tracker
                if AccuracyTracker:
                    self.accuracy_tracker = AccuracyTracker()
                else:
                    self.accuracy_tracker = create_accuracy_tracker()
                logger.info("Accuracy tracker initialized")
                
                # Initialize security hardening
                if SecurityHardening:
                    self.security_hardening = SecurityHardening()
                else:
                    self.security_hardening = create_security_hardening(None)
                logger.info("Security hardening initialized")
                
                # Initialize UI enhancements
                if UIEnhancements:
                    self.ui_enhancements = UIEnhancements()
                else:
                    self.ui_enhancements = create_ui_enhancements(None)
                logger.info("UI enhancements initialized")
            
            else:
                logger.warning("Enhanced modules not available, using fallback implementations")
                
        except Exception as e:
            logger.error(f"Failed to initialize components: {e}")
    
    def _initialize_flask_app(self):
        """Initialize Flask application"""
        if not FLASK_AVAILABLE:
            logger.error("Flask not available")
            return
        
        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = self.config.secret_key
        
        # Enable CORS
        if CORS:
            CORS(self.app)
        
        # Initialize rate limiter
        if Limiter:
            limiter = Limiter(
                app=self.app,
                key_func=get_remote_address,
                default_limits=[self.config.rate_limit]
            )
        
        # Initialize cache
        if Cache:
            cache = Cache(self.app, config={'CACHE_TYPE': self.config.cache_type})
        
        # Register routes
        self._register_routes()
        
        logger.info("Flask application initialized")
    
    def _register_routes(self):
        """Register API routes"""
        if not self.app:
            return
        
        @self.app.route('/api/detect', methods=['POST'])
        def detect():
            """Enhanced detection endpoint"""
            start_time = time.time()
            
            try:
                # Parse request
                data = request.get_json()
                if not data:
                    return jsonify({'error': 'No data provided'}), 400
                
                detection_request = DetectionRequest(
                    content=data.get('content', ''),
                    content_type=data.get('content_type', 'text'),
                    user_id=data.get('user_id'),
                    session_id=session.get('session_id'),
                    metadata=data.get('metadata'),
                    require_explanation=data.get('require_explanation', True),
                    confidence_threshold=data.get('confidence_threshold', 0.5)
                )
                
                # Perform detection
                response = self._perform_detection(detection_request)
                
                # Update metrics
                processing_time = time.time() - start_time
                self._update_metrics('detect', 'POST', processing_time, response)
                
                return jsonify(asdict(response))
                
            except Exception as e:
                logger.error(f"Detection error: {e}")
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/api/feedback', methods=['POST'])
        def submit_feedback():
            """Submit user feedback"""
            try:
                data = request.get_json()
                if not data:
                    return jsonify({'error': 'No data provided'}), 400
                
                if self.ui_enhancements:
                    feedback_id = self.ui_enhancements.submit_user_feedback(data)
                    return jsonify({'feedback_id': feedback_id, 'status': 'success'})
                else:
                    return jsonify({'error': 'Feedback system not available'}), 503
                
            except Exception as e:
                logger.error(f"Feedback error: {e}")
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/api/metrics', methods=['GET'])
        def get_metrics():
            """Get system metrics"""
            try:
                metrics = self._get_system_metrics()
                return jsonify(metrics)
            except Exception as e:
                logger.error(f"Metrics error: {e}")
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/api/health', methods=['GET'])
        def health_check():
            """Health check endpoint"""
            health_status = self._get_health_status()
            status_code = 200 if health_status['status'] == 'healthy' else 503
            return jsonify(health_status), status_code
        
        # Dashboard route removed - analytics functionality has been removed from the platform
        
        @self.app.route('/api/notifications', methods=['GET'])
        def get_notifications():
            """Get user notifications"""
            try:
                user_id = request.args.get('user_id')
                if self.ui_enhancements:
                    notifications = self.ui_enhancements.get_user_notifications(user_id)
                    return jsonify({'notifications': notifications})
                else:
                    return jsonify({'notifications': []})
            except Exception as e:
                logger.error(f"Notifications error: {e}")
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/api/notifications/<notification_id>/read', methods=['POST'])
        def mark_notification_read(notification_id):
            """Mark notification as read"""
            try:
                if self.ui_enhancements:
                    success = self.ui_enhancements.mark_notification_read(notification_id)
                    return jsonify({'success': success})
                else:
                    return jsonify({'success': False})
            except Exception as e:
                logger.error(f"Mark notification error: {e}")
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/prometheus', methods=['GET'])
        def prometheus_metrics():
            """Prometheus metrics endpoint"""
            if PROMETHEUS_AVAILABLE:
                return generate_latest(), 200, {'Content-Type': 'text/plain'}
            else:
                return "Prometheus not available", 503
        
        # Web interface routes removed
    
    def _perform_detection(self, request: DetectionRequest) -> DetectionResponse:
        """Perform enhanced detection"""
        start_time = time.time()
        request_id = f"req_{int(time.time() * 1000)}"
        
        try:
            # Security validation
            security_result = None
            if self.security_hardening:
                security_result = self.security_hardening.validate_and_sanitize(
                    request.content, request.content_type, 
                    request.metadata.get('source_ip') if request.metadata else None
                )
                
                if not security_result.is_valid:
                    return DetectionResponse(
                        request_id=request_id,
                        prediction="Blocked",
                        confidence=1.0,
                        risk_score=security_result.risk_score,
                        processing_time=time.time() - start_time,
                        explanation={'reason': 'Security validation failed', 'issues': security_result.issues},
                        recommendations=["Content blocked due to security concerns"],
                        security_validation=asdict(security_result)
                    )
            
            # Use sanitized content if available
            content_to_analyze = security_result.sanitized_content if security_result else request.content
            
            # Perform detection
            if self.realtime_api and request.content_type in ['url', 'email']:
                # Use real-time API for URLs and emails
                detection_result = self.realtime_api.detect(
                    content_to_analyze, request.content_type
                )
                
                prediction = "Phishing" if detection_result.is_phishing else "Safe"
                confidence = detection_result.confidence
                risk_score = detection_result.risk_score
                
            elif self.detector:
                # Use enhanced detector
                result = self.detector.predict_with_explanation(
                    content_to_analyze, request.content_type
                )
                
                prediction = result.get('prediction', 'Unknown')
                confidence = result.get('confidence', 0.5)
                risk_score = result.get('risk_score', 0.5)
                
            else:
                # Fallback prediction
                prediction = "Unknown"
                confidence = 0.5
                risk_score = 0.5
            
            # Generate explanation if requested
            explanation = None
            recommendations = []
            
            if request.require_explanation and self.ui_enhancements:
                try:
                    enhanced_result = self.ui_enhancements.create_enhanced_result(
                        self.detector, content_to_analyze
                    )
                    explanation = enhanced_result
                    recommendations = enhanced_result.get('recommendations', [])
                except Exception as e:
                    logger.warning(f"Failed to generate explanation: {e}")
            
            # Record prediction for accuracy tracking
            if self.accuracy_tracker:
                self.accuracy_tracker.record_prediction(
                    request_id, prediction, confidence, request.content_type
                )
            
            processing_time = time.time() - start_time
            
            return DetectionResponse(
                request_id=request_id,
                prediction=prediction,
                confidence=confidence,
                risk_score=risk_score,
                processing_time=processing_time,
                explanation=explanation,
                recommendations=recommendations,
                security_validation=asdict(security_result) if security_result else None
            )
            
        except Exception as e:
            logger.error(f"Detection failed: {e}")
            return DetectionResponse(
                request_id=request_id,
                prediction="Error",
                confidence=0.0,
                risk_score=1.0,
                processing_time=time.time() - start_time,
                explanation={'error': str(e)},
                recommendations=["Manual review required due to processing error"]
            )
    
    def _update_metrics(self, endpoint: str, method: str, 
                       processing_time: float, response: DetectionResponse):
        """Update Prometheus metrics"""
        if not self.metrics:
            return
        
        try:
            self.metrics['requests_total'].labels(endpoint=endpoint, method=method).inc()
            self.metrics['request_duration'].observe(processing_time)
            
            if response.prediction != "Error":
                confidence_level = "high" if response.confidence > 0.8 else "medium" if response.confidence > 0.5 else "low"
                self.metrics['detections_total'].labels(
                    prediction=response.prediction, 
                    confidence_level=confidence_level
                ).inc()
        except Exception as e:
            logger.warning(f"Failed to update metrics: {e}")
    
    def _get_system_metrics(self) -> Dict:
        """Get comprehensive system metrics"""
        metrics = {
            'timestamp': datetime.now().isoformat(),
            'uptime': time.time() - getattr(self, '_start_time', time.time()),
            'components': {
                'detector': self.detector is not None,
                'realtime_api': self.realtime_api is not None,
                'accuracy_tracker': self.accuracy_tracker is not None,
                'security_hardening': self.security_hardening is not None,
                'ui_enhancements': self.ui_enhancements is not None
            }
        }
        
        # Add accuracy metrics
        if self.accuracy_tracker:
            try:
                accuracy_metrics = self.accuracy_tracker.get_current_metrics()
                metrics['accuracy'] = accuracy_metrics
            except Exception as e:
                logger.warning(f"Failed to get accuracy metrics: {e}")
        
        # Add security metrics
        if self.security_hardening:
            try:
                security_metrics = self.security_hardening.get_security_metrics()
                metrics['security'] = security_metrics
            except Exception as e:
                logger.warning(f"Failed to get security metrics: {e}")
        
        return metrics
    
    def _get_health_status(self) -> Dict:
        """Get system health status"""
        health = {
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'components': {}
        }
        
        # Check component health
        components = {
            'detector': self.detector,
            'realtime_api': self.realtime_api,
            'accuracy_tracker': self.accuracy_tracker,
            'security_hardening': self.security_hardening,
            'ui_enhancements': self.ui_enhancements
        }
        
        for name, component in components.items():
            if component is not None:
                try:
                    # Try to call a simple method to check if component is working
                    if hasattr(component, 'get_status'):
                        status = component.get_status()
                    else:
                        status = 'operational'
                    health['components'][name] = status
                except Exception as e:
                    health['components'][name] = f'error: {str(e)}'
                    health['status'] = 'degraded'
            else:
                health['components'][name] = 'not_available'
        
        return health
    
    def start_background_tasks(self):
        """Start background tasks"""
        if self.config.enable_auto_learning and self.detector:
            # Start model update task
            update_task = threading.Thread(
                target=self._model_update_task,
                daemon=True
            )
            update_task.start()
            self.background_tasks.append(update_task)
        
        # Start metrics collection task
        if self.config.enable_monitoring:
            metrics_task = threading.Thread(
                target=self._metrics_collection_task,
                daemon=True
            )
            metrics_task.start()
            self.background_tasks.append(metrics_task)
        
        logger.info(f"Started {len(self.background_tasks)} background tasks")
    
    def _model_update_task(self):
        """Background task for model updates"""
        while not self.shutdown_event.is_set():
            try:
                if self.detector and hasattr(self.detector, 'update_models'):
                    logger.info("Updating models...")
                    self.detector.update_models()
                    logger.info("Models updated successfully")
                
                # Wait for next update
                self.shutdown_event.wait(self.config.model_update_interval)
                
            except Exception as e:
                logger.error(f"Model update task error: {e}")
                self.shutdown_event.wait(60)  # Wait 1 minute before retry
    
    def _metrics_collection_task(self):
        """Background task for metrics collection"""
        while not self.shutdown_event.is_set():
            try:
                # Update accuracy metrics
                if self.accuracy_tracker and self.metrics.get('model_accuracy'):
                    current_metrics = self.accuracy_tracker.get_current_metrics()
                    if current_metrics:
                        accuracy = current_metrics.get('accuracy', 0.0)
                        self.metrics['model_accuracy'].set(accuracy)
                
                # Wait for next collection
                self.shutdown_event.wait(60)  # Collect every minute
                
            except Exception as e:
                logger.error(f"Metrics collection task error: {e}")
                self.shutdown_event.wait(60)
    
    def run(self, host: Optional[str] = None, port: Optional[int] = None, 
           debug: Optional[bool] = None):
        """Run the enhanced AI API"""
        if not self.app:
            logger.error("Flask app not initialized")
            return
        
        # Start background tasks
        self.start_background_tasks()
        
        # Record start time
        self._start_time = time.time()
        
        # Run Flask app
        self.app.run(
            host=host or self.config.host,
            port=port or self.config.port,
            debug=debug or self.config.debug,
            threaded=True
        )
    
    def shutdown(self):
        """Shutdown the API gracefully"""
        logger.info("Shutting down Enhanced AI API...")
        
        # Signal background tasks to stop
        self.shutdown_event.set()
        
        # Wait for background tasks to complete
        for task in self.background_tasks:
            if task.is_alive():
                task.join(timeout=5)
        
        # Shutdown executor
        self.executor.shutdown(wait=True)
        
        logger.info("Enhanced AI API shutdown complete")


# Factory functions
def create_enhanced_ai_api(config: Optional[APIConfig] = None) -> EnhancedAIAPI:
    """Create enhanced AI API instance"""
    return EnhancedAIAPI(config)


def validate_api_requirements() -> Dict[str, bool]:
    """Validate API requirements"""
    return {
        'flask': FLASK_AVAILABLE,
        'jwt': JWT_AVAILABLE,
        'prometheus': PROMETHEUS_AVAILABLE,
        'enhanced_modules': ENHANCED_MODULES_AVAILABLE
    }


if __name__ == "__main__":
    # Example usage
    config = APIConfig(
        host="localhost",
        port=8080,
        debug=True,
        enable_real_time=True,
        enable_security=True,
        enable_ui_enhancements=True,
        enable_monitoring=True
    )
    
    # Validate requirements
    requirements = validate_api_requirements()
    print(f"API requirements: {requirements}")
    
    # Create and run API
    api = create_enhanced_ai_api(config)
    
    try:
        logger.info("Starting Enhanced AI API...")
        api.run()
    except KeyboardInterrupt:
        logger.info("Received shutdown signal")
    finally:
        api.shutdown()