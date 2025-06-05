"""
AI Phishing Detection Platform - Main Entry Point
================================================

This is the main entry point for the AI Phishing Detection Platform.
It imports the Flask application and starts the development server.

How it works:
1. Imports the configured Flask app from app.py
2. Starts the server on port 5000 (accessible at http://localhost:5000)
3. Enables debug mode for development (automatic reloading on code changes)

To run the application:
- Open terminal/command prompt
- Navigate to the project directory
- Run: python main.py
- Open browser and go to http://localhost:5000

For beginners:
- This file is kept simple on purpose
- All the main configuration happens in app.py
- Routes (web pages) are defined in routes.py and auth_routes.py
- Database setup is in mongodb_config.py
"""

# Import the configured Flask application
# This brings in all the routes, database connections, and configurations
from app import app

# This block only runs when this file is executed directly (not imported)
# It's a Python best practice to use this pattern
if __name__ == "__main__":
    import os
    
    # Get port from environment variable or default to 5000
    # This allows deployment platforms to set their own port
    port = int(os.environ.get('PORT', 5000))
    
    # Start the Flask development server
    # host="0.0.0.0" makes it accessible from other devices on the network
    # port=port uses the port we defined above
    # debug=True enables automatic reloading when code changes
    app.run(host="0.0.0.0", port=port, debug=True)
