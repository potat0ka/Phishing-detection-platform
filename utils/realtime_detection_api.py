import logging
import json
import time
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from collections import defaultdict
import threading

# Basic imports
try:
    from flask import Flask, request, jsonify
except ImportError:
    Flask = None

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class DetectionRequest:
    """Request structure for detection"""
    url: str = ""
    email_content: str = ""
    text_content: str = ""
    metadata: Optional[Dict] = None
    request_id: Optional[str] = None
    timestamp: Optional[str] = None

@dataclass
class DetectionResult:
    """Result structure for detection"""
    prediction: int
    confidence: float
    probability: float
    risk_level: str
    explanation: List[str]
    processing_time: float
    model_version: str
    request_id: str
    timestamp: str
    cached: bool = False

class RealtimeDetectionCache:
    """Simple in-memory cache for detection results"""
    
    def __init__(self, max_size: int = 10000, ttl_seconds: int = 3600):
        self.cache = {}
        self.access_times = {}
        self.max_size = max_size
        self.ttl_seconds = ttl_seconds
        self._lock = threading.Lock()
    
    def get(self, key: str) -> Optional[Dict]:
        """Get cached result"""
        with self._lock:
            if key in self.cache:
                # Check TTL
                if time.time() - self.access_times[key] < self.ttl_seconds:
                    self.access_times[key] = time.time()  # Update access time
                    return self.cache[key]
                else:
                    # Expired
                    del self.cache[key]
                    del self.access_times[key]
            return None
    
    def set(self, key: str, value: Dict):
        """Set cached result"""
        with self._lock:
            # Clean up if cache is full
            if len(self.cache) >= self.max_size:
                self._cleanup_old_entries()
            
            self.cache[key] = value
            self.access_times[key] = time.time()
    
    def _cleanup_old_entries(self):
        """Remove old entries to make space"""
        current_time = time.time()
        
        # Remove expired entries first
        expired_keys = [
            key for key, access_time in self.access_times.items()
            if current_time - access_time > self.ttl_seconds
        ]
        
        for key in expired_keys:
            del self.cache[key]
            del self.access_times[key]
        
        # If still full, remove oldest entries
        if len(self.cache) >= self.max_size:
            sorted_keys = sorted(self.access_times.items(), key=lambda x: x[1])
            keys_to_remove = [key for key, _ in sorted_keys[:self.max_size // 4]]
            
            for key in keys_to_remove:
                del self.cache[key]
                del self.access_times[key]
    
    def clear(self):
        """Clear all cache"""
        with self._lock:
            self.cache.clear()
            self.access_times.clear()
    
    def stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        with self._lock:
            return {
                'size': len(self.cache),
                'max_size': self.max_size,
                'ttl_seconds': self.ttl_seconds,
                'oldest_entry': min(self.access_times.values()) if self.access_times else None
            }

class RateLimiter:
    """Simple rate limiter"""
    
    def __init__(self, max_requests: int = 100, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = defaultdict(list)
        self._lock = threading.Lock()
    
    def is_allowed(self, client_id: str) -> bool:
        """Check if request is allowed"""
        with self._lock:
            current_time = time.time()
            
            # Clean old requests
            self.requests[client_id] = [
                req_time for req_time in self.requests[client_id]
                if current_time - req_time < self.window_seconds
            ]
            
            # Check limit
            if len(self.requests[client_id]) >= self.max_requests:
                return False
            
            # Add current request
            self.requests[client_id].append(current_time)
            return True
    
    def get_stats(self, client_id: str) -> Dict[str, Any]:
        """Get rate limit stats for client"""
        with self._lock:
            current_time = time.time()
            
            # Clean old requests
            self.requests[client_id] = [
                req_time for req_time in self.requests[client_id]
                if current_time - req_time < self.window_seconds
            ]
            
            return {
                'requests_in_window': len(self.requests[client_id]),
                'max_requests': self.max_requests,
                'window_seconds': self.window_seconds,
                'remaining': max(0, self.max_requests - len(self.requests[client_id]))
            }

class RealtimeDetectionAPI:
    """Real-time phishing detection API"""
    
    def __init__(self, detector=None, config: Optional[Dict] = None):
        self.config = config or {}
        self.detector = detector
        
        # Initialize cache
        cache_config = self.config.get('cache', {})
        self.cache = RealtimeDetectionCache(
            max_size=cache_config.get('max_size', 10000),
            ttl_seconds=cache_config.get('ttl_seconds', 3600)
        )
        
        # Initialize rate limiter
        rate_limit_config = self.config.get('rate_limit', {})
        self.rate_limiter = RateLimiter(
            max_requests=rate_limit_config.get('max_requests', 100),
            window_seconds=rate_limit_config.get('window_seconds', 60)
        )
        
        # Performance metrics
        self.metrics = {
            'total_requests': 0,
            'cache_hits': 0,
            'cache_misses': 0,
            'rate_limited': 0,
            'errors': 0,
            'avg_processing_time': 0.0,
            'start_time': time.time()
        }
        
        self._metrics_lock = threading.Lock()
        
        logger.info("Realtime Detection API initialized")
    
    def detect(self, request_data: DetectionRequest, client_id: str = "default") -> DetectionResult:
        """Perform real-time detection"""
        start_time = time.time()
        
        try:
            # Update metrics
            with self._metrics_lock:
                self.metrics['total_requests'] += 1
            
            # Check rate limit
            if not self.rate_limiter.is_allowed(client_id):
                with self._metrics_lock:
                    self.metrics['rate_limited'] += 1
                
                return DetectionResult(
                    prediction=0,
                    confidence=0.0,
                    probability=0.5,
                    risk_level="unknown",
                    explanation=["Rate limit exceeded"],
                    processing_time=time.time() - start_time,
                    model_version="rate_limited",
                    request_id=request_data.request_id or self._generate_request_id(),
                    timestamp=datetime.now().isoformat()
                )
            
            # Generate cache key
            cache_key = self._generate_cache_key(request_data)
            
            # Check cache
            cached_result = self.cache.get(cache_key)
            if cached_result:
                with self._metrics_lock:
                    self.metrics['cache_hits'] += 1
                
                cached_result['cached'] = True
                cached_result['processing_time'] = time.time() - start_time
                cached_result['timestamp'] = datetime.now().isoformat()
                
                return DetectionResult(**cached_result)
            
            # Cache miss
            with self._metrics_lock:
                self.metrics['cache_misses'] += 1
            
            # Perform detection
            if self.detector:
                detection_result = self.detector.predict(
                    url=request_data.url,
                    email_content=request_data.email_content,
                    text_content=request_data.text_content
                )
            else:
                # Fallback simple detection
                detection_result = self._simple_detection(request_data)
            
            # Create result
            result = DetectionResult(
                prediction=detection_result.get('prediction', 0),
                confidence=detection_result.get('confidence', 0.0),
                probability=detection_result.get('probability', 0.5),
                risk_level=self._determine_risk_level(detection_result.get('probability', 0.5)),
                explanation=self._generate_explanation(detection_result),
                processing_time=time.time() - start_time,
                model_version=detection_result.get('model_version', 'simple'),
                request_id=request_data.request_id or self._generate_request_id(),
                timestamp=datetime.now().isoformat(),
                cached=False
            )
            
            # Cache result
            self.cache.set(cache_key, asdict(result))
            
            # Update metrics
            with self._metrics_lock:
                processing_time = result.processing_time
                self.metrics['avg_processing_time'] = (
                    (self.metrics['avg_processing_time'] * (self.metrics['total_requests'] - 1) + processing_time) /
                    self.metrics['total_requests']
                )
            
            return result
            
        except Exception as e:
            logger.error(f"Error in detection: {e}")
            
            with self._metrics_lock:
                self.metrics['errors'] += 1
            
            return DetectionResult(
                prediction=0,
                confidence=0.0,
                probability=0.5,
                risk_level="error",
                explanation=[f"Detection error: {str(e)}"],
                processing_time=time.time() - start_time,
                model_version="error",
                request_id=request_data.request_id or self._generate_request_id(),
                timestamp=datetime.now().isoformat()
            )
    
    def _simple_detection(self, request_data: DetectionRequest) -> Dict[str, Any]:
        """Simple fallback detection logic"""
        score = 0.0
        
        # Check URL
        if request_data.url:
            url_lower = request_data.url.lower()
            if any(suspicious in url_lower for suspicious in ['bit.ly', 'tinyurl', 'short']):
                score += 0.3
            if not request_data.url.startswith('https://'):
                score += 0.2
            if len(request_data.url) > 100:
                score += 0.1
        
        # Check text content
        text = f"{request_data.email_content} {request_data.text_content}".lower()
        if text:
            suspicious_words = ['urgent', 'verify', 'suspended', 'click here', 'update payment']
            for word in suspicious_words:
                if word in text:
                    score += 0.15
        
        score = min(score, 1.0)
        
        return {
            'prediction': 1 if score > 0.5 else 0,
            'confidence': abs(score - 0.5) * 2,
            'probability': score,
            'model_version': 'simple_fallback'
        }
    
    def _generate_cache_key(self, request_data: DetectionRequest) -> str:
        """Generate cache key for request"""
        content = f"{request_data.url}{request_data.email_content}{request_data.text_content}"
        return hashlib.md5(content.encode()).hexdigest()
    
    def _generate_request_id(self) -> str:
        """Generate unique request ID"""
        return f"req_{int(time.time() * 1000)}_{hashlib.md5(str(time.time()).encode()).hexdigest()[:8]}"
    
    def _determine_risk_level(self, probability: float) -> str:
        """Determine risk level from probability"""
        if probability >= 0.8:
            return "critical"
        elif probability >= 0.6:
            return "high"
        elif probability >= 0.4:
            return "medium"
        elif probability >= 0.2:
            return "low"
        else:
            return "minimal"
    
    def _generate_explanation(self, detection_result: Dict) -> List[str]:
        """Generate explanation for detection result"""
        explanations = []
        
        probability = detection_result.get('probability', 0.5)
        
        if probability > 0.7:
            explanations.append("High probability of phishing detected")
        elif probability > 0.5:
            explanations.append("Moderate phishing indicators found")
        else:
            explanations.append("Content appears legitimate")
        
        # Add feature-based explanations if available
        features = detection_result.get('features', {})
        if features.get('phishing_pattern_score', 0) > 0.3:
            explanations.append("Suspicious text patterns detected")
        if features.get('is_suspicious_domain', 0) > 0:
            explanations.append("Suspicious domain detected")
        if features.get('urgency_score', 0) > 0.4:
            explanations.append("High urgency language detected")
        
        return explanations
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get API performance metrics"""
        with self._metrics_lock:
            uptime = time.time() - self.metrics['start_time']
            
            return {
                'total_requests': self.metrics['total_requests'],
                'cache_hits': self.metrics['cache_hits'],
                'cache_misses': self.metrics['cache_misses'],
                'cache_hit_rate': (
                    self.metrics['cache_hits'] / max(1, self.metrics['cache_hits'] + self.metrics['cache_misses'])
                ),
                'rate_limited': self.metrics['rate_limited'],
                'errors': self.metrics['errors'],
                'avg_processing_time': self.metrics['avg_processing_time'],
                'uptime_seconds': uptime,
                'requests_per_second': self.metrics['total_requests'] / max(1, uptime),
                'cache_stats': self.cache.stats()
            }
    
    def health_check(self) -> Dict[str, Any]:
        """Health check for the API"""
        try:
            # Test detection
            test_request = DetectionRequest(
                url="https://example.com",
                text_content="test content",
                request_id="health_check"
            )
            
            start_time = time.time()
            result = self.detect(test_request, "health_check")
            response_time = time.time() - start_time
            
            return {
                'status': 'healthy',
                'response_time': response_time,
                'detector_available': self.detector is not None,
                'cache_size': len(self.cache.cache),
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                'status': 'unhealthy',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def clear_cache(self):
        """Clear detection cache"""
        self.cache.clear()
        logger.info("Detection cache cleared")
    
    def reset_metrics(self):
        """Reset performance metrics"""
        with self._metrics_lock:
            self.metrics = {
                'total_requests': 0,
                'cache_hits': 0,
                'cache_misses': 0,
                'rate_limited': 0,
                'errors': 0,
                'avg_processing_time': 0.0,
                'start_time': time.time()
            }
        logger.info("Metrics reset")

# Flask API wrapper
class FlaskAPIWrapper:
    """Flask wrapper for the detection API"""
    
    def __init__(self, detection_api: RealtimeDetectionAPI):
        self.detection_api = detection_api
        self.app = None
        
        if Flask:
            self.app = Flask(__name__)
            self._setup_routes()
    
    def _setup_routes(self):
        """Setup Flask routes"""
        if not self.app:
            return
        
        @self.app.route('/detect', methods=['POST'])
        def detect():
            try:
                data = request.get_json()
                
                # Create detection request
                detection_request = DetectionRequest(
                    url=data.get('url', ''),
                    email_content=data.get('email_content', ''),
                    text_content=data.get('text_content', ''),
                    metadata=data.get('metadata'),
                    request_id=data.get('request_id')
                )
                
                # Get client ID
                client_id = request.remote_addr or 'unknown'
                
                # Perform detection
                result = self.detection_api.detect(detection_request, client_id)
                
                return jsonify(asdict(result))
                
            except Exception as e:
                logger.error(f"API error: {e}")
                return jsonify({
                    'error': str(e),
                    'timestamp': datetime.now().isoformat()
                }), 500
        
        @self.app.route('/metrics', methods=['GET'])
        def metrics():
            return jsonify(self.detection_api.get_metrics())
        
        @self.app.route('/health', methods=['GET'])
        def health():
            return jsonify(self.detection_api.health_check())
        
        @self.app.route('/cache/clear', methods=['POST'])
        def clear_cache():
            self.detection_api.clear_cache()
            return jsonify({'status': 'cache cleared'})
        
        @self.app.route('/metrics/reset', methods=['POST'])
        def reset_metrics():
            self.detection_api.reset_metrics()
            return jsonify({'status': 'metrics reset'})
    
    def run(self, host='0.0.0.0', port=5001, debug=False):
        """Run the Flask app"""
        if self.app:
            self.app.run(host=host, port=port, debug=debug)
        else:
            logger.error("Flask not available")

# Factory functions
def create_realtime_api(detector=None, config: Optional[Dict] = None) -> RealtimeDetectionAPI:
    """Create realtime detection API"""
    return RealtimeDetectionAPI(detector, config)

def create_flask_wrapper(detection_api: RealtimeDetectionAPI) -> Optional[FlaskAPIWrapper]:
    """Create Flask wrapper for the API"""
    if Flask:
        return FlaskAPIWrapper(detection_api)
    else:
        logger.warning("Flask not available, cannot create wrapper")
        return None

def validate_api_requirements() -> bool:
    """Validate API requirements"""
    try:
        import json
        import time
        import hashlib
        from datetime import datetime
        from dataclasses import dataclass
        return True
    except ImportError as e:
        logger.error(f"Missing required dependency: {e}")
        return False