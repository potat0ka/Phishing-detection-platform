"""
Models Package
=============

This package contains all database models and data access logic.
Each model handles specific data operations for the AI Phishing Detection Platform.

For beginners: Models are like translators that help your app talk to the database.
They handle saving, loading, and organizing data.
"""

# Import all models to make them available when importing from models package
from .user_model import UserModel
from .safety_tips_model import SafetyTipsModel
from .scan_history_model import ScanHistoryModel
from .rbac_model import RBACModel
from .analytics_model import AnalyticsModel
from .security_tips_model import SecurityTipsModel
from .phishing_model import PhishingModel

# Make models available when importing from models package
__all__ = [
    'UserModel', 
    'SafetyTipsModel', 
    'ScanHistoryModel', 
    'RBACModel', 
    'AnalyticsModel',
    'SecurityTipsModel',
    'PhishingModel'
]