import logging
import json
import time
import sqlite3
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple, Union
from dataclasses import dataclass, asdict
from collections import defaultdict, deque
from enum import Enum
import threading
import queue
import uuid

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FeedbackType(Enum):
    """Types of user feedback"""
    CORRECT_DETECTION = "correct_detection"
    FALSE_POSITIVE = "false_positive"
    FALSE_NEGATIVE = "false_negative"
    GENERAL_FEEDBACK = "general_feedback"

class NotificationType(Enum):
    """Types of notifications"""
    THREAT_DETECTED = "threat_detected"
    SYSTEM_ALERT = "system_alert"
    MODEL_UPDATE = "model_update"
    PERFORMANCE_ALERT = "performance_alert"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"

class ConfidenceLevel(Enum):
    """Confidence levels for predictions"""
    VERY_LOW = "very_low"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"

@dataclass
class UserFeedback:
    """User feedback data structure"""
    feedback_id: str
    user_id: str
    prediction_id: str
    feedback_type: FeedbackType
    original_prediction: bool
    user_correction: Optional[bool]
    confidence_rating: Optional[int]  # 1-5 scale
    comments: Optional[str]
    timestamp: datetime
    processed: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'feedback_id': self.feedback_id,
            'user_id': self.user_id,
            'prediction_id': self.prediction_id,
            'feedback_type': self.feedback_type.value,
            'original_prediction': self.original_prediction,
            'user_correction': self.user_correction,
            'confidence_rating': self.confidence_rating,
            'comments': self.comments,
            'timestamp': self.timestamp.isoformat(),
            'processed': self.processed
        }

@dataclass
class ModelExplanation:
    """Model explanation data structure"""
    prediction_id: str
    prediction: bool
    confidence_score: float
    confidence_level: ConfidenceLevel
    key_features: List[Dict[str, Any]]
    reasoning: str
    risk_factors: List[str]
    safe_indicators: List[str]
    recommendation: str
    timestamp: datetime
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'prediction_id': self.prediction_id,
            'prediction': self.prediction,
            'confidence_score': self.confidence_score,
            'confidence_level': self.confidence_level.value,
            'key_features': self.key_features,
            'reasoning': self.reasoning,
            'risk_factors': self.risk_factors,
            'safe_indicators': self.safe_indicators,
            'recommendation': self.recommendation,
            'timestamp': self.timestamp.isoformat()
        }

@dataclass
class Notification:
    """Notification data structure"""
    notification_id: str
    user_id: Optional[str]
    notification_type: NotificationType
    title: str
    message: str
    severity: str  # info, warning, error
    data: Optional[Dict[str, Any]]
    timestamp: datetime
    read: bool = False
    dismissed: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'notification_id': self.notification_id,
            'user_id': self.user_id,
            'notification_type': self.notification_type.value,
            'title': self.title,
            'message': self.message,
            'severity': self.severity,
            'data': self.data,
            'timestamp': self.timestamp.isoformat(),
            'read': self.read,
            'dismissed': self.dismissed
        }

@dataclass
class VisualizationData:
    """Data structure for visualizations"""
    chart_type: str
    title: str
    data: Dict[str, Any]
    options: Optional[Dict[str, Any]]
    timestamp: datetime
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'chart_type': self.chart_type,
            'title': self.title,
            'data': self.data,
            'options': self.options,
            'timestamp': self.timestamp.isoformat()
        }

class ModelExplainer:
    """Simplified model explainer without heavy ML dependencies"""
    
    def __init__(self):
        self.feature_importance = {
            'url_length': 0.15,
            'domain_age': 0.12,
            'suspicious_keywords': 0.20,
            'ssl_certificate': 0.10,
            'redirect_count': 0.08,
            'ip_address_usage': 0.15,
            'suspicious_tld': 0.10,
            'url_shortener': 0.10
        }
    
    def explain_prediction(self, prediction: bool, confidence: float, 
                         features: Dict[str, Any], prediction_id: str) -> ModelExplanation:
        """Generate explanation for a prediction"""
        try:
            # Determine confidence level
            confidence_level = self._get_confidence_level(confidence)
            
            # Extract key features
            key_features = self._extract_key_features(features)
            
            # Generate reasoning
            reasoning = self._generate_reasoning(prediction, confidence, key_features)
            
            # Identify risk factors and safe indicators
            risk_factors, safe_indicators = self._analyze_factors(features)
            
            # Generate recommendation
            recommendation = self._generate_recommendation(prediction, confidence, risk_factors)
            
            return ModelExplanation(
                prediction_id=prediction_id,
                prediction=prediction,
                confidence_score=confidence,
                confidence_level=confidence_level,
                key_features=key_features,
                reasoning=reasoning,
                risk_factors=risk_factors,
                safe_indicators=safe_indicators,
                recommendation=recommendation,
                timestamp=datetime.now()
            )
            
        except Exception as e:
            logger.error(f"Error generating explanation: {e}")
            return self._create_fallback_explanation(prediction, confidence, prediction_id)
    
    def _get_confidence_level(self, confidence: float) -> ConfidenceLevel:
        """Convert confidence score to level"""
        if confidence >= 0.9:
            return ConfidenceLevel.VERY_HIGH
        elif confidence >= 0.75:
            return ConfidenceLevel.HIGH
        elif confidence >= 0.5:
            return ConfidenceLevel.MEDIUM
        elif confidence >= 0.25:
            return ConfidenceLevel.LOW
        else:
            return ConfidenceLevel.VERY_LOW
    
    def _extract_key_features(self, features: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract and rank key features"""
        key_features = []
        
        for feature_name, importance in sorted(self.feature_importance.items(), 
                                             key=lambda x: x[1], reverse=True):
            if feature_name in features:
                feature_value = features[feature_name]
                
                key_features.append({
                    'name': feature_name,
                    'value': feature_value,
                    'importance': importance,
                    'description': self._get_feature_description(feature_name, feature_value)
                })
        
        return key_features[:5]  # Top 5 features
    
    def _get_feature_description(self, feature_name: str, value: Any) -> str:
        """Get human-readable description of feature"""
        descriptions = {
            'url_length': f"URL length: {value} characters",
            'domain_age': f"Domain age: {value} days",
            'suspicious_keywords': f"Suspicious keywords found: {value}",
            'ssl_certificate': f"SSL certificate: {'Valid' if value else 'Invalid/Missing'}",
            'redirect_count': f"Number of redirects: {value}",
            'ip_address_usage': f"Uses IP address: {'Yes' if value else 'No'}",
            'suspicious_tld': f"Suspicious TLD: {'Yes' if value else 'No'}",
            'url_shortener': f"URL shortener: {'Yes' if value else 'No'}"
        }
        
        return descriptions.get(feature_name, f"{feature_name}: {value}")
    
    def _generate_reasoning(self, prediction: bool, confidence: float, 
                          key_features: List[Dict[str, Any]]) -> str:
        """Generate human-readable reasoning"""
        if prediction:  # Phishing detected
            reasoning = f"This content was classified as phishing with {confidence:.1%} confidence. "
            
            if confidence >= 0.8:
                reasoning += "The model is highly confident in this prediction based on multiple suspicious indicators."
            elif confidence >= 0.6:
                reasoning += "The model found several concerning patterns that suggest phishing."
            else:
                reasoning += "The model detected some suspicious elements, but the confidence is moderate."
                
        else:  # Safe content
            reasoning = f"This content was classified as safe with {confidence:.1%} confidence. "
            
            if confidence >= 0.8:
                reasoning += "The model found strong indicators that this content is legitimate."
            elif confidence >= 0.6:
                reasoning += "The model found mostly positive indicators with few concerning elements."
            else:
                reasoning += "The model leans towards safe, but some elements require caution."
        
        # Add key feature information
        if key_features:
            top_feature = key_features[0]
            reasoning += f" The most influential factor was: {top_feature['description']}."
        
        return reasoning
    
    def _analyze_factors(self, features: Dict[str, Any]) -> Tuple[List[str], List[str]]:
        """Analyze risk factors and safe indicators"""
        risk_factors = []
        safe_indicators = []
        
        # Check for risk factors
        if features.get('url_length', 0) > 100:
            risk_factors.append("Unusually long URL")
        
        if features.get('suspicious_keywords', 0) > 0:
            risk_factors.append(f"Contains {features['suspicious_keywords']} suspicious keywords")
        
        if features.get('ip_address_usage', False):
            risk_factors.append("Uses IP address instead of domain name")
        
        if features.get('suspicious_tld', False):
            risk_factors.append("Uses suspicious top-level domain")
        
        if features.get('url_shortener', False):
            risk_factors.append("Uses URL shortening service")
        
        if features.get('redirect_count', 0) > 2:
            risk_factors.append(f"Multiple redirects ({features['redirect_count']})")
        
        # Check for safe indicators
        if features.get('ssl_certificate', False):
            safe_indicators.append("Valid SSL certificate")
        
        if features.get('domain_age', 0) > 365:
            safe_indicators.append("Established domain (over 1 year old)")
        
        if features.get('url_length', 0) < 50:
            safe_indicators.append("Reasonable URL length")
        
        if features.get('suspicious_keywords', 0) == 0:
            safe_indicators.append("No suspicious keywords detected")
        
        return risk_factors, safe_indicators
    
    def _generate_recommendation(self, prediction: bool, confidence: float, 
                               risk_factors: List[str]) -> str:
        """Generate actionable recommendation"""
        if prediction:  # Phishing detected
            if confidence >= 0.8:
                return "⚠️ HIGH RISK: Do not interact with this content. Block and report if possible."
            elif confidence >= 0.6:
                return "⚠️ MEDIUM RISK: Exercise extreme caution. Verify through alternative means before proceeding."
            else:
                return "⚠️ LOW RISK: Some suspicious elements detected. Proceed with caution and verify authenticity."
        else:  # Safe content
            if confidence >= 0.8:
                return "✅ SAFE: Content appears legitimate. Normal interaction is safe."
            elif confidence >= 0.6:
                return "✅ LIKELY SAFE: Content appears mostly legitimate. Standard caution advised."
            else:
                return "⚠️ UNCERTAIN: Mixed signals detected. Verify authenticity before sensitive actions."
    
    def _create_fallback_explanation(self, prediction: bool, confidence: float, 
                                   prediction_id: str) -> ModelExplanation:
        """Create fallback explanation when normal processing fails"""
        return ModelExplanation(
            prediction_id=prediction_id,
            prediction=prediction,
            confidence_score=confidence,
            confidence_level=self._get_confidence_level(confidence),
            key_features=[],
            reasoning=f"Content classified as {'phishing' if prediction else 'safe'} with {confidence:.1%} confidence.",
            risk_factors=["Unable to analyze specific risk factors"],
            safe_indicators=["Unable to analyze specific safe indicators"],
            recommendation="Manual review recommended due to analysis limitations.",
            timestamp=datetime.now()
        )

class FeedbackManager:
    """Manage user feedback and learning"""
    
    def __init__(self, db_path: str = "feedback.db"):
        self.db_path = db_path
        self.feedback_queue = queue.Queue()
        self.processing_thread = None
        self.running = False
        self._init_database()
    
    def _init_database(self):
        """Initialize feedback database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS feedback (
                        feedback_id TEXT PRIMARY KEY,
                        user_id TEXT NOT NULL,
                        prediction_id TEXT NOT NULL,
                        feedback_type TEXT NOT NULL,
                        original_prediction BOOLEAN NOT NULL,
                        user_correction BOOLEAN,
                        confidence_rating INTEGER,
                        comments TEXT,
                        timestamp TEXT NOT NULL,
                        processed BOOLEAN DEFAULT FALSE
                    )
                """)
                
                conn.execute("""
                    CREATE INDEX IF NOT EXISTS idx_feedback_user_id ON feedback(user_id)
                """)
                
                conn.execute("""
                    CREATE INDEX IF NOT EXISTS idx_feedback_timestamp ON feedback(timestamp)
                """)
                
                conn.commit()
                
        except Exception as e:
            logger.error(f"Database initialization error: {e}")
    
    def start_processing(self):
        """Start background feedback processing"""
        if not self.running:
            self.running = True
            self.processing_thread = threading.Thread(target=self._process_feedback_loop)
            self.processing_thread.daemon = True
            self.processing_thread.start()
            logger.info("Feedback processing started")
    
    def stop_processing(self):
        """Stop background feedback processing"""
        self.running = False
        if self.processing_thread:
            self.processing_thread.join(timeout=5)
        logger.info("Feedback processing stopped")
    
    def submit_feedback(self, user_id: str, prediction_id: str, 
                       feedback_type: FeedbackType, original_prediction: bool,
                       user_correction: Optional[bool] = None,
                       confidence_rating: Optional[int] = None,
                       comments: Optional[str] = None) -> str:
        """Submit user feedback"""
        try:
            feedback_id = str(uuid.uuid4())
            
            feedback = UserFeedback(
                feedback_id=feedback_id,
                user_id=user_id,
                prediction_id=prediction_id,
                feedback_type=feedback_type,
                original_prediction=original_prediction,
                user_correction=user_correction,
                confidence_rating=confidence_rating,
                comments=comments,
                timestamp=datetime.now()
            )
            
            # Store in database
            self._store_feedback(feedback)
            
            # Add to processing queue
            self.feedback_queue.put(feedback)
            
            logger.info(f"Feedback submitted: {feedback_id}")
            return feedback_id
            
        except Exception as e:
            logger.error(f"Error submitting feedback: {e}")
            raise
    
    def _store_feedback(self, feedback: UserFeedback):
        """Store feedback in database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    INSERT INTO feedback (
                        feedback_id, user_id, prediction_id, feedback_type,
                        original_prediction, user_correction, confidence_rating,
                        comments, timestamp, processed
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    feedback.feedback_id,
                    feedback.user_id,
                    feedback.prediction_id,
                    feedback.feedback_type.value,
                    feedback.original_prediction,
                    feedback.user_correction,
                    feedback.confidence_rating,
                    feedback.comments,
                    feedback.timestamp.isoformat(),
                    feedback.processed
                ))
                conn.commit()
                
        except Exception as e:
            logger.error(f"Error storing feedback: {e}")
            raise
    
    def _process_feedback_loop(self):
        """Background loop to process feedback"""
        while self.running:
            try:
                # Get feedback from queue (with timeout)
                feedback = self.feedback_queue.get(timeout=1.0)
                self._process_single_feedback(feedback)
                self.feedback_queue.task_done()
                
            except queue.Empty:
                continue
            except Exception as e:
                logger.error(f"Error processing feedback: {e}")
    
    def _process_single_feedback(self, feedback: UserFeedback):
        """Process a single feedback item"""
        try:
            # Simulate feedback processing
            # In a real system, this would update model weights, retrain, etc.
            
            logger.info(f"Processing feedback {feedback.feedback_id}: {feedback.feedback_type.value}")
            
            # Mark as processed
            with sqlite3.connect(self.db_path) as conn:
                conn.execute(
                    "UPDATE feedback SET processed = TRUE WHERE feedback_id = ?",
                    (feedback.feedback_id,)
                )
                conn.commit()
            
            # Simulate processing delay
            time.sleep(0.1)
            
        except Exception as e:
            logger.error(f"Error processing feedback {feedback.feedback_id}: {e}")
    
    def get_feedback_stats(self, user_id: Optional[str] = None, 
                          days: int = 30) -> Dict[str, Any]:
        """Get feedback statistics"""
        try:
            cutoff_date = datetime.now() - timedelta(days=days)
            
            with sqlite3.connect(self.db_path) as conn:
                # Base query
                base_query = """
                    SELECT feedback_type, COUNT(*) as count
                    FROM feedback 
                    WHERE timestamp >= ?
                """
                
                params = [cutoff_date.isoformat()]
                
                if user_id:
                    base_query += " AND user_id = ?"
                    params.append(user_id)
                
                base_query += " GROUP BY feedback_type"
                
                cursor = conn.execute(base_query, params)
                feedback_counts = dict(cursor.fetchall())
                
                # Get total feedback count
                total_query = "SELECT COUNT(*) FROM feedback WHERE timestamp >= ?"
                total_params = [cutoff_date.isoformat()]
                
                if user_id:
                    total_query += " AND user_id = ?"
                    total_params.append(user_id)
                
                cursor = conn.execute(total_query, total_params)
                total_feedback = cursor.fetchone()[0]
                
                # Get processing stats
                processed_query = "SELECT COUNT(*) FROM feedback WHERE timestamp >= ? AND processed = TRUE"
                processed_params = [cutoff_date.isoformat()]
                
                if user_id:
                    processed_query += " AND user_id = ?"
                    processed_params.append(user_id)
                
                cursor = conn.execute(processed_query, processed_params)
                processed_feedback = cursor.fetchone()[0]
                
                return {
                    'total_feedback': total_feedback,
                    'processed_feedback': processed_feedback,
                    'pending_feedback': total_feedback - processed_feedback,
                    'feedback_by_type': feedback_counts,
                    'processing_rate': processed_feedback / max(total_feedback, 1),
                    'period_days': days,
                    'user_id': user_id
                }
                
        except Exception as e:
            logger.error(f"Error getting feedback stats: {e}")
            return {
                'total_feedback': 0,
                'processed_feedback': 0,
                'pending_feedback': 0,
                'feedback_by_type': {},
                'processing_rate': 0.0,
                'period_days': days,
                'user_id': user_id,
                'error': str(e)
            }

class VisualizationGenerator:
    """Generate visualization data for charts and graphs"""
    
    def __init__(self):
        self.chart_templates = {
            'confidence_distribution': {
                'type': 'histogram',
                'title': 'Prediction Confidence Distribution',
                'x_label': 'Confidence Score',
                'y_label': 'Frequency'
            },
            'detection_timeline': {
                'type': 'line',
                'title': 'Detection Timeline',
                'x_label': 'Time',
                'y_label': 'Detections'
            },
            'feature_importance': {
                'type': 'bar',
                'title': 'Feature Importance',
                'x_label': 'Features',
                'y_label': 'Importance Score'
            },
            'feedback_summary': {
                'type': 'pie',
                'title': 'User Feedback Summary',
                'x_label': 'Feedback Type',
                'y_label': 'Count'
            }
        }
    
    def generate_confidence_chart(self, predictions: List[Dict[str, Any]]) -> VisualizationData:
        """Generate confidence distribution chart"""
        try:
            # Extract confidence scores
            confidence_scores = [p.get('confidence', 0.5) for p in predictions]
            
            # Create histogram bins
            bins = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
            bin_counts = [0] * (len(bins) - 1)
            bin_labels = ['0-20%', '20-40%', '40-60%', '60-80%', '80-100%']
            
            for score in confidence_scores:
                for i in range(len(bins) - 1):
                    if bins[i] <= score < bins[i + 1]:
                        bin_counts[i] += 1
                        break
                else:
                    if score == 1.0:
                        bin_counts[-1] += 1
            
            chart_data = {
                'labels': bin_labels,
                'datasets': [{
                    'label': 'Predictions',
                    'data': bin_counts,
                    'backgroundColor': 'rgba(54, 162, 235, 0.6)',
                    'borderColor': 'rgba(54, 162, 235, 1)',
                    'borderWidth': 1
                }]
            }
            
            return VisualizationData(
                chart_type='bar',
                title='Prediction Confidence Distribution',
                data=chart_data,
                options={
                    'responsive': True,
                    'scales': {
                        'y': {
                            'beginAtZero': True,
                            'title': {
                                'display': True,
                                'text': 'Number of Predictions'
                            }
                        },
                        'x': {
                            'title': {
                                'display': True,
                                'text': 'Confidence Range'
                            }
                        }
                    }
                },
                timestamp=datetime.now()
            )
            
        except Exception as e:
            logger.error(f"Error generating confidence chart: {e}")
            return self._create_error_chart("Confidence Distribution", str(e))
    
    def generate_timeline_chart(self, detections: List[Dict[str, Any]], 
                              hours: int = 24) -> VisualizationData:
        """Generate detection timeline chart"""
        try:
            # Create hourly buckets
            now = datetime.now()
            hourly_counts = [0] * hours
            hourly_labels = []
            
            for i in range(hours):
                hour_time = now - timedelta(hours=hours-1-i)
                hourly_labels.append(hour_time.strftime('%H:%M'))
            
            # Count detections per hour
            for detection in detections:
                detection_time = datetime.fromisoformat(detection.get('timestamp', now.isoformat()))
                hours_ago = int((now - detection_time).total_seconds() / 3600)
                
                if 0 <= hours_ago < hours:
                    hourly_counts[hours-1-hours_ago] += 1
            
            chart_data = {
                'labels': hourly_labels,
                'datasets': [{
                    'label': 'Phishing Detections',
                    'data': hourly_counts,
                    'borderColor': 'rgba(255, 99, 132, 1)',
                    'backgroundColor': 'rgba(255, 99, 132, 0.2)',
                    'tension': 0.1
                }]
            }
            
            return VisualizationData(
                chart_type='line',
                title=f'Phishing Detections - Last {hours} Hours',
                data=chart_data,
                options={
                    'responsive': True,
                    'scales': {
                        'y': {
                            'beginAtZero': True,
                            'title': {
                                'display': True,
                                'text': 'Number of Detections'
                            }
                        },
                        'x': {
                            'title': {
                                'display': True,
                                'text': 'Time'
                            }
                        }
                    }
                },
                timestamp=datetime.now()
            )
            
        except Exception as e:
            logger.error(f"Error generating timeline chart: {e}")
            return self._create_error_chart("Detection Timeline", str(e))
    
    def generate_feature_importance_chart(self, feature_importance: Dict[str, float]) -> VisualizationData:
        """Generate feature importance chart"""
        try:
            # Sort features by importance
            sorted_features = sorted(feature_importance.items(), key=lambda x: x[1], reverse=True)
            
            labels = [feature[0].replace('_', ' ').title() for feature in sorted_features]
            values = [feature[1] for feature in sorted_features]
            
            chart_data = {
                'labels': labels,
                'datasets': [{
                    'label': 'Importance Score',
                    'data': values,
                    'backgroundColor': [
                        'rgba(255, 99, 132, 0.6)',
                        'rgba(54, 162, 235, 0.6)',
                        'rgba(255, 205, 86, 0.6)',
                        'rgba(75, 192, 192, 0.6)',
                        'rgba(153, 102, 255, 0.6)',
                        'rgba(255, 159, 64, 0.6)',
                        'rgba(199, 199, 199, 0.6)',
                        'rgba(83, 102, 255, 0.6)'
                    ][:len(values)],
                    'borderWidth': 1
                }]
            }
            
            return VisualizationData(
                chart_type='bar',
                title='Model Feature Importance',
                data=chart_data,
                options={
                    'responsive': True,
                    'indexAxis': 'y',
                    'scales': {
                        'x': {
                            'beginAtZero': True,
                            'title': {
                                'display': True,
                                'text': 'Importance Score'
                            }
                        }
                    }
                },
                timestamp=datetime.now()
            )
            
        except Exception as e:
            logger.error(f"Error generating feature importance chart: {e}")
            return self._create_error_chart("Feature Importance", str(e))
    
    def generate_feedback_chart(self, feedback_stats: Dict[str, Any]) -> VisualizationData:
        """Generate feedback summary chart"""
        try:
            feedback_by_type = feedback_stats.get('feedback_by_type', {})
            
            if not feedback_by_type:
                return self._create_empty_chart("User Feedback Summary", "No feedback data available")
            
            labels = [ftype.replace('_', ' ').title() for ftype in feedback_by_type.keys()]
            values = list(feedback_by_type.values())
            
            chart_data = {
                'labels': labels,
                'datasets': [{
                    'data': values,
                    'backgroundColor': [
                        'rgba(75, 192, 192, 0.6)',
                        'rgba(255, 99, 132, 0.6)',
                        'rgba(255, 205, 86, 0.6)',
                        'rgba(54, 162, 235, 0.6)'
                    ][:len(values)]
                }]
            }
            
            return VisualizationData(
                chart_type='pie',
                title='User Feedback Summary',
                data=chart_data,
                options={
                    'responsive': True,
                    'plugins': {
                        'legend': {
                            'position': 'bottom'
                        }
                    }
                },
                timestamp=datetime.now()
            )
            
        except Exception as e:
            logger.error(f"Error generating feedback chart: {e}")
            return self._create_error_chart("User Feedback Summary", str(e))
    
    def _create_error_chart(self, title: str, error_message: str) -> VisualizationData:
        """Create error chart when generation fails"""
        return VisualizationData(
            chart_type='bar',
            title=f"{title} (Error)",
            data={
                'labels': ['Error'],
                'datasets': [{
                    'label': 'Error',
                    'data': [1],
                    'backgroundColor': 'rgba(255, 0, 0, 0.6)'
                }]
            },
            options={
                'responsive': True,
                'plugins': {
                    'title': {
                        'display': True,
                        'text': f'Error: {error_message}'
                    }
                }
            },
            timestamp=datetime.now()
        )
    
    def _create_empty_chart(self, title: str, message: str) -> VisualizationData:
        """Create empty chart when no data available"""
        return VisualizationData(
            chart_type='bar',
            title=title,
            data={
                'labels': ['No Data'],
                'datasets': [{
                    'label': 'No Data',
                    'data': [0],
                    'backgroundColor': 'rgba(128, 128, 128, 0.6)'
                }]
            },
            options={
                'responsive': True,
                'plugins': {
                    'title': {
                        'display': True,
                        'text': message
                    }
                }
            },
            timestamp=datetime.now()
        )

class NotificationManager:
    """Manage real-time notifications"""
    
    def __init__(self, db_path: str = "notifications.db"):
        self.db_path = db_path
        self.subscribers = defaultdict(list)  # user_id -> list of callback functions
        self.notification_history = deque(maxlen=1000)  # Keep last 1000 notifications
        self._init_database()
    
    def _init_database(self):
        """Initialize notifications database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS notifications (
                        notification_id TEXT PRIMARY KEY,
                        user_id TEXT,
                        notification_type TEXT NOT NULL,
                        title TEXT NOT NULL,
                        message TEXT NOT NULL,
                        severity TEXT NOT NULL,
                        data TEXT,
                        timestamp TEXT NOT NULL,
                        read BOOLEAN DEFAULT FALSE,
                        dismissed BOOLEAN DEFAULT FALSE
                    )
                """)
                
                conn.execute("""
                    CREATE INDEX IF NOT EXISTS idx_notifications_user_id ON notifications(user_id)
                """)
                
                conn.execute("""
                    CREATE INDEX IF NOT EXISTS idx_notifications_timestamp ON notifications(timestamp)
                """)
                
                conn.commit()
                
        except Exception as e:
            logger.error(f"Notification database initialization error: {e}")
    
    def subscribe(self, user_id: str, callback):
        """Subscribe to notifications for a user"""
        self.subscribers[user_id].append(callback)
        logger.info(f"User {user_id} subscribed to notifications")
    
    def unsubscribe(self, user_id: str, callback):
        """Unsubscribe from notifications"""
        if user_id in self.subscribers and callback in self.subscribers[user_id]:
            self.subscribers[user_id].remove(callback)
            logger.info(f"User {user_id} unsubscribed from notifications")
    
    def send_notification(self, notification_type: NotificationType, title: str, 
                         message: str, severity: str = "info", 
                         user_id: Optional[str] = None, 
                         data: Optional[Dict[str, Any]] = None) -> str:
        """Send a notification"""
        try:
            notification_id = str(uuid.uuid4())
            
            notification = Notification(
                notification_id=notification_id,
                user_id=user_id,
                notification_type=notification_type,
                title=title,
                message=message,
                severity=severity,
                data=data,
                timestamp=datetime.now()
            )
            
            # Store in database
            self._store_notification(notification)
            
            # Add to history
            self.notification_history.append(notification)
            
            # Send to subscribers
            self._deliver_notification(notification)
            
            logger.info(f"Notification sent: {notification_id}")
            return notification_id
            
        except Exception as e:
            logger.error(f"Error sending notification: {e}")
            raise
    
    def _store_notification(self, notification: Notification):
        """Store notification in database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    INSERT INTO notifications (
                        notification_id, user_id, notification_type, title,
                        message, severity, data, timestamp, read, dismissed
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    notification.notification_id,
                    notification.user_id,
                    notification.notification_type.value,
                    notification.title,
                    notification.message,
                    notification.severity,
                    json.dumps(notification.data) if notification.data else None,
                    notification.timestamp.isoformat(),
                    notification.read,
                    notification.dismissed
                ))
                conn.commit()
                
        except Exception as e:
            logger.error(f"Error storing notification: {e}")
            raise
    
    def _deliver_notification(self, notification: Notification):
        """Deliver notification to subscribers"""
        try:
            # Send to specific user if specified
            if notification.user_id and notification.user_id in self.subscribers:
                for callback in self.subscribers[notification.user_id]:
                    try:
                        callback(notification)
                    except Exception as e:
                        logger.error(f"Error in notification callback: {e}")
            
            # Send to all subscribers if no specific user
            elif notification.user_id is None:
                for user_id, callbacks in self.subscribers.items():
                    for callback in callbacks:
                        try:
                            callback(notification)
                        except Exception as e:
                            logger.error(f"Error in notification callback: {e}")
                            
        except Exception as e:
            logger.error(f"Error delivering notification: {e}")
    
    def get_notifications(self, user_id: Optional[str] = None, 
                         limit: int = 50, unread_only: bool = False) -> List[Dict[str, Any]]:
        """Get notifications for a user"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                query = "SELECT * FROM notifications WHERE 1=1"
                params = []
                
                if user_id:
                    query += " AND (user_id = ? OR user_id IS NULL)"
                    params.append(user_id)
                
                if unread_only:
                    query += " AND read = FALSE"
                
                query += " ORDER BY timestamp DESC LIMIT ?"
                params.append(limit)
                
                cursor = conn.execute(query, params)
                rows = cursor.fetchall()
                
                notifications = []
                for row in rows:
                    notification_data = {
                        'notification_id': row[0],
                        'user_id': row[1],
                        'notification_type': row[2],
                        'title': row[3],
                        'message': row[4],
                        'severity': row[5],
                        'data': json.loads(row[6]) if row[6] else None,
                        'timestamp': row[7],
                        'read': bool(row[8]),
                        'dismissed': bool(row[9])
                    }
                    notifications.append(notification_data)
                
                return notifications
                
        except Exception as e:
            logger.error(f"Error getting notifications: {e}")
            return []
    
    def mark_as_read(self, notification_id: str, user_id: Optional[str] = None) -> bool:
        """Mark notification as read"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                query = "UPDATE notifications SET read = TRUE WHERE notification_id = ?"
                params = [notification_id]
                
                if user_id:
                    query += " AND (user_id = ? OR user_id IS NULL)"
                    params.append(user_id)
                
                cursor = conn.execute(query, params)
                conn.commit()
                
                return cursor.rowcount > 0
                
        except Exception as e:
            logger.error(f"Error marking notification as read: {e}")
            return False
    
    def dismiss_notification(self, notification_id: str, user_id: Optional[str] = None) -> bool:
        """Dismiss notification"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                query = "UPDATE notifications SET dismissed = TRUE WHERE notification_id = ?"
                params = [notification_id]
                
                if user_id:
                    query += " AND (user_id = ? OR user_id IS NULL)"
                    params.append(user_id)
                
                cursor = conn.execute(query, params)
                conn.commit()
                
                return cursor.rowcount > 0
                
        except Exception as e:
            logger.error(f"Error dismissing notification: {e}")
            return False
    
    def cleanup_old_notifications(self, days: int = 30) -> int:
        """Clean up old notifications"""
        try:
            cutoff_date = datetime.now() - timedelta(days=days)
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute(
                    "DELETE FROM notifications WHERE timestamp < ? AND dismissed = TRUE",
                    (cutoff_date.isoformat(),)
                )
                conn.commit()
                
                deleted_count = cursor.rowcount
                logger.info(f"Cleaned up {deleted_count} old notifications")
                return deleted_count
                
        except Exception as e:
            logger.error(f"Error cleaning up notifications: {e}")
            return 0

class UIEnhancements:
    """Main UI enhancements class integrating all components"""
    
    def __init__(self, feedback_db_path: str = "feedback.db", 
                 notifications_db_path: str = "notifications.db"):
        self.explainer = ModelExplainer()
        self.feedback_manager = FeedbackManager(feedback_db_path)
        self.visualization_generator = VisualizationGenerator()
        self.notification_manager = NotificationManager(notifications_db_path)
        
        # Start background processing
        self.feedback_manager.start_processing()
        
        logger.info("UI enhancements initialized")
    
    def explain_prediction(self, prediction: bool, confidence: float, 
                         features: Dict[str, Any], prediction_id: str) -> Dict[str, Any]:
        """Get explanation for a prediction"""
        explanation = self.explainer.explain_prediction(prediction, confidence, features, prediction_id)
        return explanation.to_dict()
    
    def submit_feedback(self, user_id: str, prediction_id: str, 
                       feedback_type: str, original_prediction: bool,
                       user_correction: Optional[bool] = None,
                       confidence_rating: Optional[int] = None,
                       comments: Optional[str] = None) -> str:
        """Submit user feedback"""
        feedback_type_enum = FeedbackType(feedback_type)
        return self.feedback_manager.submit_feedback(
            user_id, prediction_id, feedback_type_enum, original_prediction,
            user_correction, confidence_rating, comments
        )
    
    def get_feedback_stats(self, user_id: Optional[str] = None, days: int = 30) -> Dict[str, Any]:
        """Get feedback statistics"""
        return self.feedback_manager.get_feedback_stats(user_id, days)
    
    def generate_visualizations(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate all visualizations"""
        visualizations = {}
        
        try:
            # Confidence distribution
            if 'predictions' in data:
                visualizations['confidence_distribution'] = self.visualization_generator.generate_confidence_chart(
                    data['predictions']
                ).to_dict()
            
            # Detection timeline
            if 'detections' in data:
                visualizations['detection_timeline'] = self.visualization_generator.generate_timeline_chart(
                    data['detections']
                ).to_dict()
            
            # Feature importance
            if 'feature_importance' in data:
                visualizations['feature_importance'] = self.visualization_generator.generate_feature_importance_chart(
                    data['feature_importance']
                ).to_dict()
            
            # Feedback summary
            feedback_stats = self.get_feedback_stats()
            visualizations['feedback_summary'] = self.visualization_generator.generate_feedback_chart(
                feedback_stats
            ).to_dict()
            
        except Exception as e:
            logger.error(f"Error generating visualizations: {e}")
            visualizations['error'] = str(e)
        
        return visualizations
    
    def send_notification(self, notification_type: str, title: str, message: str,
                         severity: str = "info", user_id: Optional[str] = None,
                         data: Optional[Dict[str, Any]] = None) -> str:
        """Send notification"""
        notification_type_enum = NotificationType(notification_type)
        return self.notification_manager.send_notification(
            notification_type_enum, title, message, severity, user_id, data
        )
    
    def get_notifications(self, user_id: Optional[str] = None, 
                         limit: int = 50, unread_only: bool = False) -> List[Dict[str, Any]]:
        """Get notifications"""
        return self.notification_manager.get_notifications(user_id, limit, unread_only)
    
    def mark_notification_read(self, notification_id: str, user_id: Optional[str] = None) -> bool:
        """Mark notification as read"""
        return self.notification_manager.mark_as_read(notification_id, user_id)
    
    def dismiss_notification(self, notification_id: str, user_id: Optional[str] = None) -> bool:
        """Dismiss notification"""
        return self.notification_manager.dismiss_notification(notification_id, user_id)
    
    def get_dashboard_data(self, user_id: Optional[str] = None) -> Dict[str, Any]:
        """Get comprehensive dashboard data"""
        try:
            # Get feedback stats
            feedback_stats = self.get_feedback_stats(user_id)
            
            # Get recent notifications
            notifications = self.get_notifications(user_id, limit=10)
            
            # Generate sample data for visualizations
            sample_data = {
                'predictions': [
                    {'confidence': 0.95, 'timestamp': datetime.now().isoformat()},
                    {'confidence': 0.75, 'timestamp': datetime.now().isoformat()},
                    {'confidence': 0.45, 'timestamp': datetime.now().isoformat()}
                ],
                'detections': [
                    {'timestamp': (datetime.now() - timedelta(hours=1)).isoformat()},
                    {'timestamp': (datetime.now() - timedelta(hours=2)).isoformat()}
                ],
                'feature_importance': {
                    'url_length': 0.15,
                    'domain_age': 0.12,
                    'suspicious_keywords': 0.20,
                    'ssl_certificate': 0.10
                }
            }
            
            visualizations = self.generate_visualizations(sample_data)
            
            return {
                'feedback_stats': feedback_stats,
                'notifications': notifications,
                'visualizations': visualizations,
                'generated_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error getting dashboard data: {e}")
            return {
                'error': str(e),
                'generated_at': datetime.now().isoformat()
            }
    
    def cleanup(self):
        """Cleanup resources"""
        try:
            self.feedback_manager.stop_processing()
            self.notification_manager.cleanup_old_notifications()
            logger.info("UI enhancements cleanup completed")
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")

# Factory functions
def create_ui_enhancements(feedback_db_path: str = "feedback.db",
                          notifications_db_path: str = "notifications.db") -> UIEnhancements:
    """Create UI enhancements instance"""
    return UIEnhancements(feedback_db_path, notifications_db_path)

# Example usage
if __name__ == "__main__":
    # Create UI enhancements instance
    ui = create_ui_enhancements()
    
    # Test explanation
    explanation = ui.explain_prediction(
        prediction=True,
        confidence=0.85,
        features={
            'url_length': 150,
            'suspicious_keywords': 3,
            'ssl_certificate': False,
            'domain_age': 5
        },
        prediction_id="test_123"
    )
    print(f"Explanation generated: {explanation['reasoning']}")
    
    # Test feedback
    feedback_id = ui.submit_feedback(
        user_id="test_user",
        prediction_id="test_123",
        feedback_type="correct_detection",
        original_prediction=True,
        confidence_rating=5,
        comments="Good detection!"
    )
    print(f"Feedback submitted: {feedback_id}")
    
    # Test notification
    notification_id = ui.send_notification(
        notification_type="threat_detected",
        title="Phishing Detected",
        message="A phishing attempt was detected and blocked.",
        severity="warning",
        user_id="test_user"
    )
    print(f"Notification sent: {notification_id}")
    
    # Get dashboard data
    dashboard_data = ui.get_dashboard_data("test_user")
    print(f"Dashboard data generated with {len(dashboard_data.get('visualizations', {}))} visualizations")
    
    # Cleanup
    ui.cleanup()