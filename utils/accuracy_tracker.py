import logging
import json
import time
import sqlite3
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from collections import defaultdict, deque
import statistics
import os

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class PredictionRecord:
    """Record of a prediction made by the model"""
    prediction_id: str
    timestamp: str
    input_data: str
    input_type: str  # 'url', 'email', 'text'
    prediction: int  # 0 or 1
    confidence: float
    probability: float
    model_version: str
    processing_time: float
    features: Optional[Dict] = None
    feedback: Optional[int] = None  # Actual label when available
    feedback_timestamp: Optional[str] = None
    user_id: Optional[str] = None

@dataclass
class PerformanceMetrics:
    """Performance metrics for a time period"""
    period_start: str
    period_end: str
    total_predictions: int
    total_feedback: int
    true_positives: int
    true_negatives: int
    false_positives: int
    false_negatives: int
    precision: float
    recall: float
    f1_score: float
    accuracy: float
    avg_confidence: float
    avg_processing_time: float
    model_version: str

@dataclass
class DriftAlert:
    """Model drift alert"""
    alert_id: str
    timestamp: str
    metric_name: str
    current_value: float
    baseline_value: float
    threshold: float
    severity: str  # 'low', 'medium', 'high', 'critical'
    description: str
    recommendations: List[str]

class AccuracyTracker:
    """Accuracy tracking and model monitoring system"""
    
    def __init__(self, db_path: str = "accuracy_tracker.db", config: Optional[Dict] = None):
        self.db_path = db_path
        self.config = config or {}
        self._lock = threading.Lock()
        
        # Performance thresholds
        self.thresholds = {
            'precision_min': self.config.get('precision_min', 0.85),
            'recall_min': self.config.get('recall_min', 0.80),
            'f1_min': self.config.get('f1_min', 0.82),
            'accuracy_min': self.config.get('accuracy_min', 0.85),
            'drift_threshold': self.config.get('drift_threshold', 0.05)
        }
        
        # In-memory cache for recent predictions
        self.recent_predictions = deque(maxlen=1000)
        self.recent_metrics = deque(maxlen=100)
        
        # Drift detection baseline
        self.baseline_metrics = {}
        
        # Initialize database
        self._init_database()
        
        # Load baseline metrics
        self._load_baseline_metrics()
        
        logger.info(f"Accuracy tracker initialized with database: {db_path}")
    
    def _init_database(self):
        """Initialize SQLite database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Predictions table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS predictions (
                        prediction_id TEXT PRIMARY KEY,
                        timestamp TEXT NOT NULL,
                        input_data TEXT NOT NULL,
                        input_type TEXT NOT NULL,
                        prediction INTEGER NOT NULL,
                        confidence REAL NOT NULL,
                        probability REAL NOT NULL,
                        model_version TEXT NOT NULL,
                        processing_time REAL NOT NULL,
                        features TEXT,
                        feedback INTEGER,
                        feedback_timestamp TEXT,
                        user_id TEXT
                    )
                """)
                
                # Performance metrics table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS performance_metrics (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        period_start TEXT NOT NULL,
                        period_end TEXT NOT NULL,
                        total_predictions INTEGER NOT NULL,
                        total_feedback INTEGER NOT NULL,
                        true_positives INTEGER NOT NULL,
                        true_negatives INTEGER NOT NULL,
                        false_positives INTEGER NOT NULL,
                        false_negatives INTEGER NOT NULL,
                        precision REAL NOT NULL,
                        recall REAL NOT NULL,
                        f1_score REAL NOT NULL,
                        accuracy REAL NOT NULL,
                        avg_confidence REAL NOT NULL,
                        avg_processing_time REAL NOT NULL,
                        model_version TEXT NOT NULL,
                        created_at TEXT NOT NULL
                    )
                """)
                
                # Drift alerts table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS drift_alerts (
                        alert_id TEXT PRIMARY KEY,
                        timestamp TEXT NOT NULL,
                        metric_name TEXT NOT NULL,
                        current_value REAL NOT NULL,
                        baseline_value REAL NOT NULL,
                        threshold_value REAL NOT NULL,
                        severity TEXT NOT NULL,
                        description TEXT NOT NULL,
                        recommendations TEXT NOT NULL,
                        resolved BOOLEAN DEFAULT FALSE,
                        resolved_at TEXT
                    )
                """)
                
                # Create indexes
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_predictions_timestamp ON predictions(timestamp)")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_predictions_model_version ON predictions(model_version)")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_metrics_period ON performance_metrics(period_start, period_end)")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_alerts_timestamp ON drift_alerts(timestamp)")
                
                conn.commit()
                
        except Exception as e:
            logger.error(f"Database initialization error: {e}")
            raise
    
    def record_prediction(self, record: PredictionRecord):
        """Record a prediction"""
        try:
            with self._lock:
                # Add to in-memory cache
                self.recent_predictions.append(record)
                
                # Store in database
                with sqlite3.connect(self.db_path) as conn:
                    cursor = conn.cursor()
                    
                    features_json = json.dumps(record.features) if record.features else None
                    
                    cursor.execute("""
                        INSERT OR REPLACE INTO predictions (
                            prediction_id, timestamp, input_data, input_type,
                            prediction, confidence, probability, model_version,
                            processing_time, features, feedback, feedback_timestamp, user_id
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        record.prediction_id, record.timestamp, record.input_data,
                        record.input_type, record.prediction, record.confidence,
                        record.probability, record.model_version, record.processing_time,
                        features_json, record.feedback, record.feedback_timestamp, record.user_id
                    ))
                    
                    conn.commit()
                    
        except Exception as e:
            logger.error(f"Error recording prediction: {e}")
    
    def add_feedback(self, prediction_id: str, actual_label: int, user_id: Optional[str] = None):
        """Add feedback for a prediction"""
        try:
            with self._lock:
                timestamp = datetime.now().isoformat()
                
                # Update database
                with sqlite3.connect(self.db_path) as conn:
                    cursor = conn.cursor()
                    
                    cursor.execute("""
                        UPDATE predictions 
                        SET feedback = ?, feedback_timestamp = ?, user_id = COALESCE(?, user_id)
                        WHERE prediction_id = ?
                    """, (actual_label, timestamp, user_id, prediction_id))
                    
                    if cursor.rowcount == 0:
                        logger.warning(f"Prediction ID {prediction_id} not found for feedback")
                        return False
                    
                    conn.commit()
                    
                # Update in-memory cache
                for record in self.recent_predictions:
                    if record.prediction_id == prediction_id:
                        record.feedback = actual_label
                        record.feedback_timestamp = timestamp
                        if user_id:
                            record.user_id = user_id
                        break
                
                logger.info(f"Feedback added for prediction {prediction_id}: {actual_label}")
                return True
                
        except Exception as e:
            logger.error(f"Error adding feedback: {e}")
            return False
    
    def calculate_metrics(self, start_time: Optional[str] = None, end_time: Optional[str] = None, 
                         model_version: Optional[str] = None) -> Optional[PerformanceMetrics]:
        """Calculate performance metrics for a time period"""
        try:
            if not end_time:
                end_time = datetime.now().isoformat()
            if not start_time:
                start_time = (datetime.now() - timedelta(hours=24)).isoformat()
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Build query
                query = """
                    SELECT prediction, feedback, confidence, processing_time, model_version
                    FROM predictions 
                    WHERE timestamp >= ? AND timestamp <= ? AND feedback IS NOT NULL
                """
                params = [start_time, end_time]
                
                if model_version:
                    query += " AND model_version = ?"
                    params.append(model_version)
                
                cursor.execute(query, params)
                results = cursor.fetchall()
                
                if not results:
                    logger.warning("No predictions with feedback found for the specified period")
                    return None
                
                # Calculate confusion matrix
                tp = tn = fp = fn = 0
                confidences = []
                processing_times = []
                model_versions = set()
                
                for prediction, feedback, confidence, proc_time, mv in results:
                    confidences.append(confidence)
                    processing_times.append(proc_time)
                    model_versions.add(mv)
                    
                    if prediction == 1 and feedback == 1:
                        tp += 1
                    elif prediction == 0 and feedback == 0:
                        tn += 1
                    elif prediction == 1 and feedback == 0:
                        fp += 1
                    elif prediction == 0 and feedback == 1:
                        fn += 1
                
                # Calculate metrics
                total_predictions = len(results)
                total_feedback = total_predictions  # All have feedback
                
                precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
                recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
                f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
                accuracy = (tp + tn) / total_predictions if total_predictions > 0 else 0.0
                
                avg_confidence = statistics.mean(confidences) if confidences else 0.0
                avg_processing_time = statistics.mean(processing_times) if processing_times else 0.0
                
                # Get total predictions (including those without feedback)
                cursor.execute("""
                    SELECT COUNT(*) FROM predictions 
                    WHERE timestamp >= ? AND timestamp <= ?
                """, [start_time, end_time])
                total_all_predictions = cursor.fetchone()[0]
                
                metrics = PerformanceMetrics(
                    period_start=start_time,
                    period_end=end_time,
                    total_predictions=total_all_predictions,
                    total_feedback=total_feedback,
                    true_positives=tp,
                    true_negatives=tn,
                    false_positives=fp,
                    false_negatives=fn,
                    precision=precision,
                    recall=recall,
                    f1_score=f1_score,
                    accuracy=accuracy,
                    avg_confidence=avg_confidence,
                    avg_processing_time=avg_processing_time,
                    model_version=model_version or ','.join(model_versions)
                )
                
                # Store metrics
                self._store_metrics(metrics)
                
                # Add to recent metrics cache
                self.recent_metrics.append(metrics)
                
                return metrics
                
        except Exception as e:
            logger.error(f"Error calculating metrics: {e}")
            return None
    
    def _store_metrics(self, metrics: PerformanceMetrics):
        """Store performance metrics in database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    INSERT INTO performance_metrics (
                        period_start, period_end, total_predictions, total_feedback,
                        true_positives, true_negatives, false_positives, false_negatives,
                        precision, recall, f1_score, accuracy, avg_confidence,
                        avg_processing_time, model_version, created_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    metrics.period_start, metrics.period_end, metrics.total_predictions,
                    metrics.total_feedback, metrics.true_positives, metrics.true_negatives,
                    metrics.false_positives, metrics.false_negatives, metrics.precision,
                    metrics.recall, metrics.f1_score, metrics.accuracy, metrics.avg_confidence,
                    metrics.avg_processing_time, metrics.model_version, datetime.now().isoformat()
                ))
                
                conn.commit()
                
        except Exception as e:
            logger.error(f"Error storing metrics: {e}")
    
    def check_drift(self, current_metrics: PerformanceMetrics) -> List[DriftAlert]:
        """Check for model drift"""
        alerts = []
        
        try:
            # Compare with baseline metrics
            for metric_name, current_value in [
                ('precision', current_metrics.precision),
                ('recall', current_metrics.recall),
                ('f1_score', current_metrics.f1_score),
                ('accuracy', current_metrics.accuracy)
            ]:
                baseline_value = self.baseline_metrics.get(metric_name, current_value)
                
                # Calculate drift
                if baseline_value > 0:
                    drift = abs(current_value - baseline_value) / baseline_value
                    
                    if drift > self.thresholds['drift_threshold']:
                        severity = self._calculate_drift_severity(drift)
                        
                        alert = DriftAlert(
                            alert_id=f"drift_{metric_name}_{int(time.time())}",
                            timestamp=datetime.now().isoformat(),
                            metric_name=metric_name,
                            current_value=current_value,
                            baseline_value=baseline_value,
                            threshold=self.thresholds['drift_threshold'],
                            severity=severity,
                            description=f"{metric_name.title()} has drifted by {drift:.2%} from baseline",
                            recommendations=self._get_drift_recommendations(metric_name, drift)
                        )
                        
                        alerts.append(alert)
                        self._store_drift_alert(alert)
            
            # Check against minimum thresholds
            for metric_name, threshold_key in [
                ('precision', 'precision_min'),
                ('recall', 'recall_min'),
                ('f1_score', 'f1_min'),
                ('accuracy', 'accuracy_min')
            ]:
                current_value = getattr(current_metrics, metric_name)
                threshold = self.thresholds[threshold_key]
                
                if current_value < threshold:
                    alert = DriftAlert(
                        alert_id=f"threshold_{metric_name}_{int(time.time())}",
                        timestamp=datetime.now().isoformat(),
                        metric_name=metric_name,
                        current_value=current_value,
                        baseline_value=threshold,
                        threshold=threshold,
                        severity='high',
                        description=f"{metric_name.title()} ({current_value:.3f}) is below minimum threshold ({threshold:.3f})",
                        recommendations=self._get_threshold_recommendations(metric_name)
                    )
                    
                    alerts.append(alert)
                    self._store_drift_alert(alert)
            
            return alerts
            
        except Exception as e:
            logger.error(f"Error checking drift: {e}")
            return []
    
    def _calculate_drift_severity(self, drift: float) -> str:
        """Calculate drift severity based on drift magnitude"""
        if drift > 0.2:
            return 'critical'
        elif drift > 0.1:
            return 'high'
        elif drift > 0.05:
            return 'medium'
        else:
            return 'low'
    
    def _get_drift_recommendations(self, metric_name: str, drift: float) -> List[str]:
        """Get recommendations for drift mitigation"""
        recommendations = [
            "Review recent training data for quality issues",
            "Check for changes in data distribution",
            "Consider retraining the model with recent data"
        ]
        
        if metric_name == 'precision':
            recommendations.extend([
                "Investigate false positive patterns",
                "Review feature importance changes"
            ])
        elif metric_name == 'recall':
            recommendations.extend([
                "Investigate false negative patterns",
                "Check for new phishing techniques"
            ])
        
        if drift > 0.1:
            recommendations.append("Consider immediate model retraining")
        
        return recommendations
    
    def _get_threshold_recommendations(self, metric_name: str) -> List[str]:
        """Get recommendations for threshold violations"""
        return [
            f"Immediate attention required for {metric_name}",
            "Review model performance and training data",
            "Consider emergency model rollback if available",
            "Increase monitoring frequency",
            "Schedule urgent model retraining"
        ]
    
    def _store_drift_alert(self, alert: DriftAlert):
        """Store drift alert in database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                recommendations_json = json.dumps(alert.recommendations)
                
                cursor.execute("""
                    INSERT OR REPLACE INTO drift_alerts (
                        alert_id, timestamp, metric_name, current_value,
                        baseline_value, threshold_value, severity, description,
                        recommendations
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    alert.alert_id, alert.timestamp, alert.metric_name,
                    alert.current_value, alert.baseline_value, alert.threshold,
                    alert.severity, alert.description, recommendations_json
                ))
                
                conn.commit()
                
        except Exception as e:
            logger.error(f"Error storing drift alert: {e}")
    
    def _load_baseline_metrics(self):
        """Load baseline metrics from recent good performance"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Get recent metrics with good performance
                cursor.execute("""
                    SELECT precision, recall, f1_score, accuracy
                    FROM performance_metrics
                    WHERE precision >= ? AND recall >= ? AND f1_score >= ?
                    ORDER BY created_at DESC
                    LIMIT 10
                """, (
                    self.thresholds['precision_min'],
                    self.thresholds['recall_min'],
                    self.thresholds['f1_min']
                ))
                
                results = cursor.fetchall()
                
                if results:
                    # Calculate average of recent good metrics
                    precisions, recalls, f1s, accuracies = zip(*results)
                    
                    self.baseline_metrics = {
                        'precision': statistics.mean(precisions),
                        'recall': statistics.mean(recalls),
                        'f1_score': statistics.mean(f1s),
                        'accuracy': statistics.mean(accuracies)
                    }
                    
                    logger.info(f"Loaded baseline metrics: {self.baseline_metrics}")
                else:
                    # Use thresholds as baseline if no good metrics found
                    self.baseline_metrics = {
                        'precision': self.thresholds['precision_min'],
                        'recall': self.thresholds['recall_min'],
                        'f1_score': self.thresholds['f1_min'],
                        'accuracy': self.thresholds['accuracy_min']
                    }
                    
                    logger.info("No baseline metrics found, using thresholds")
                    
        except Exception as e:
            logger.error(f"Error loading baseline metrics: {e}")
            # Fallback to thresholds
            self.baseline_metrics = {
                'precision': self.thresholds['precision_min'],
                'recall': self.thresholds['recall_min'],
                'f1_score': self.thresholds['f1_min'],
                'accuracy': self.thresholds['accuracy_min']
            }
    
    def get_recent_alerts(self, hours: int = 24) -> List[DriftAlert]:
        """Get recent drift alerts"""
        try:
            start_time = (datetime.now() - timedelta(hours=hours)).isoformat()
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT alert_id, timestamp, metric_name, current_value,
                           baseline_value, threshold_value, severity, description,
                           recommendations
                    FROM drift_alerts
                    WHERE timestamp >= ? AND resolved = FALSE
                    ORDER BY timestamp DESC
                """, [start_time])
                
                alerts = []
                for row in cursor.fetchall():
                    alert = DriftAlert(
                        alert_id=row[0],
                        timestamp=row[1],
                        metric_name=row[2],
                        current_value=row[3],
                        baseline_value=row[4],
                        threshold=row[5],
                        severity=row[6],
                        description=row[7],
                        recommendations=json.loads(row[8])
                    )
                    alerts.append(alert)
                
                return alerts
                
        except Exception as e:
            logger.error(f"Error getting recent alerts: {e}")
            return []
    
    def generate_report(self, days: int = 7) -> Dict[str, Any]:
        """Generate performance report"""
        try:
            end_time = datetime.now()
            start_time = end_time - timedelta(days=days)
            
            # Get metrics for the period
            metrics = self.calculate_metrics(
                start_time.isoformat(),
                end_time.isoformat()
            )
            
            if not metrics:
                return {'error': 'No data available for the specified period'}
            
            # Get trend data
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT DATE(created_at) as date, 
                           AVG(precision) as avg_precision,
                           AVG(recall) as avg_recall,
                           AVG(f1_score) as avg_f1,
                           AVG(accuracy) as avg_accuracy,
                           COUNT(*) as measurements
                    FROM performance_metrics
                    WHERE created_at >= ?
                    GROUP BY DATE(created_at)
                    ORDER BY date
                """, [start_time.isoformat()])
                
                trend_data = cursor.fetchall()
            
            # Get recent alerts
            alerts = self.get_recent_alerts(days * 24)
            
            # Calculate summary statistics
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT 
                        COUNT(*) as total_predictions,
                        COUNT(CASE WHEN feedback IS NOT NULL THEN 1 END) as total_feedback,
                        AVG(confidence) as avg_confidence,
                        AVG(processing_time) as avg_processing_time
                    FROM predictions
                    WHERE timestamp >= ?
                """, [start_time.isoformat()])
                
                summary = cursor.fetchone()
            
            report = {
                'report_period': {
                    'start': start_time.isoformat(),
                    'end': end_time.isoformat(),
                    'days': days
                },
                'current_metrics': asdict(metrics) if metrics else None,
                'summary_statistics': {
                    'total_predictions': summary[0],
                    'total_feedback': summary[1],
                    'feedback_rate': summary[1] / max(summary[0], 1),
                    'avg_confidence': summary[2] or 0.0,
                    'avg_processing_time': summary[3] or 0.0
                },
                'trend_data': [
                    {
                        'date': row[0],
                        'precision': row[1],
                        'recall': row[2],
                        'f1_score': row[3],
                        'accuracy': row[4],
                        'measurements': row[5]
                    } for row in trend_data
                ],
                'recent_alerts': [asdict(alert) for alert in alerts],
                'baseline_metrics': self.baseline_metrics,
                'thresholds': self.thresholds,
                'generated_at': datetime.now().isoformat()
            }
            
            return report
            
        except Exception as e:
            logger.error(f"Error generating report: {e}")
            return {'error': str(e)}
    
    def cleanup_old_data(self, days_to_keep: int = 90):
        """Clean up old data to manage database size"""
        try:
            cutoff_date = (datetime.now() - timedelta(days=days_to_keep)).isoformat()
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Clean old predictions
                cursor.execute("DELETE FROM predictions WHERE timestamp < ?", [cutoff_date])
                predictions_deleted = cursor.rowcount
                
                # Clean old metrics (keep more metrics than predictions)
                metrics_cutoff = (datetime.now() - timedelta(days=days_to_keep * 2)).isoformat()
                cursor.execute("DELETE FROM performance_metrics WHERE created_at < ?", [metrics_cutoff])
                metrics_deleted = cursor.rowcount
                
                # Clean resolved alerts older than cutoff
                cursor.execute("""
                    DELETE FROM drift_alerts 
                    WHERE timestamp < ? AND resolved = TRUE
                """, [cutoff_date])
                alerts_deleted = cursor.rowcount
                
                conn.commit()
                
                # Vacuum database to reclaim space
                cursor.execute("VACUUM")
                
                logger.info(f"Cleanup completed: {predictions_deleted} predictions, "
                           f"{metrics_deleted} metrics, {alerts_deleted} alerts deleted")
                
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get tracker statistics"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Get counts
                cursor.execute("SELECT COUNT(*) FROM predictions")
                total_predictions = cursor.fetchone()[0]
                
                cursor.execute("SELECT COUNT(*) FROM predictions WHERE feedback IS NOT NULL")
                total_feedback = cursor.fetchone()[0]
                
                cursor.execute("SELECT COUNT(*) FROM performance_metrics")
                total_metrics = cursor.fetchone()[0]
                
                cursor.execute("SELECT COUNT(*) FROM drift_alerts WHERE resolved = FALSE")
                active_alerts = cursor.fetchone()[0]
                
                # Get database size
                db_size = os.path.getsize(self.db_path) if os.path.exists(self.db_path) else 0
                
                return {
                    'total_predictions': total_predictions,
                    'total_feedback': total_feedback,
                    'feedback_rate': total_feedback / max(total_predictions, 1),
                    'total_metrics_calculated': total_metrics,
                    'active_alerts': active_alerts,
                    'recent_predictions_cached': len(self.recent_predictions),
                    'recent_metrics_cached': len(self.recent_metrics),
                    'database_size_bytes': db_size,
                    'baseline_metrics': self.baseline_metrics,
                    'thresholds': self.thresholds
                }
                
        except Exception as e:
            logger.error(f"Error getting stats: {e}")
            return {'error': str(e)}

# Factory functions
def create_accuracy_tracker(db_path: str = "accuracy_tracker.db", 
                           config: Optional[Dict] = None) -> AccuracyTracker:
    """Create accuracy tracker instance"""
    return AccuracyTracker(db_path, config)

def validate_tracker_requirements() -> bool:
    """Validate tracker requirements"""
    try:
        import sqlite3
        import json
        import statistics
        from datetime import datetime, timedelta
        from dataclasses import dataclass
        return True
    except ImportError as e:
        logger.error(f"Missing required dependency: {e}")
        return False