"""
Main Entry Point for AI Phishing Detection Platform
==================================================

This file imports and runs the Flask application.
It serves as the entry point that Replit uses to start the server.

For beginners: This is the file that starts your website when you click "Run".
"""

import logging
from app import app

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    # Initialize models
    with app.app_context():
        try:
            from models.safety_tips_model import SafetyTipsModel
            from models.scan_history_model import ScanHistoryModel
            from utils.mongodb_utils import setup_test_users
            logger.info("Scan history model imported successfully")

            # Check if safety tips model exists before importing
            try:
                from models.safety_tips_model import SafetyTipsModel
                SafetyTipsModel.initialize_default_tips()
                logger.info("Safety tips model initialized successfully")
            except ImportError:
                logger.info("Safety tips model not found - skipping initialization")

        except Exception as e:
            logger.error(f"Failed to initialize models: {e}")

    app.run(host='0.0.0.0', port=8080, debug=True)