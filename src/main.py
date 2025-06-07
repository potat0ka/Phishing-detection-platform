"""
AI Phishing Detection Platform - Main Entry Point
================================================

# Author: Bigendra Shrestha
# Built from scratch using Flask and MongoDB for my learning project
# For College "i.e. Saraswati Multiple Campus" Project propose of the 8th semester

🚀 START HERE! This is the main file to run the application.

WHAT THIS FILE DOES:
This file starts the web server for the AI Phishing Detection Platform.
Think of it as the "power button" for your web application.

HOW TO RUN THE APPLICATION:
1. Open terminal/command prompt
2. Navigate to this project folder: cd ai-phishing-detection-platform
3. Activate virtual environment: source venv/bin/activate (Linux/Mac) or venv\\Scripts\\activate (Windows)
4. Type: python main.py
5. Press Enter
6. Open browser and go to: http://localhost:8080

WHAT YOU'LL SEE:
- "Running on http://127.0.0.1:8080" = Server started successfully!
- "Debug mode: on" = Detailed error messages enabled
- Press Ctrl+C to stop the server

FOR BEGINNERS - PROJECT FILE STRUCTURE:
- main.py (THIS FILE) = Starts the web server
- app.py = Main application configuration and setup
- routes.py = Web pages for regular users (home, detection tools)
- auth_routes.py = Login and registration pages
- admin_routes.py = Admin dashboard and management features
- ml_detector.py = AI algorithms that detect phishing
- models/ = Database connection and data structures
- templates/ = HTML files for web pages
- static/ = CSS, JavaScript, and images

TROUBLESHOOTING:
- If you see "Port already in use": Another program is using port 8080
- If you see "Module not found": Run 'pip install -r requirements-local.txt'
- If pages don't load: Check if server is running and go to http://localhost:8080
"""

# Import the configured Flask application
# This brings in all the routes, database connections, and configurations
from app import app

# This block only runs when this file is executed directly (not imported)
# It's a Python best practice to use this pattern
if __name__ == "__main__":
    import os
    
    # Display startup information for beginners
    print("=" * 60)
    print("🚀 AI Phishing Detection Platform")
    print("=" * 60)
    print("📝 Author: Bigendra Shrestha")
    print("🎓 Project: Final Semester - Cybersecurity & AI")
    print("=" * 60)
    print("🌐 Starting web server...")
    print("📖 For beginners: This creates a website on your computer")
    print("🔗 Once started, open: http://localhost:8080")
    print("🛑 Press Ctrl+C to stop the server")
    print("=" * 60)
    
    # Get port from environment variable or default to 8080
    # This allows deployment platforms (like Heroku) to set their own port
    port = int(os.environ.get('PORT', 8080))
    
    # Start the Flask development server
    # host="0.0.0.0" - makes server accessible from any IP address (not just localhost)
    # port=port - uses the port number we defined above (usually 8080)
    # debug=True - enables helpful features for development:
    #   1. Shows detailed error messages when something breaks
    #   2. Automatically restarts server when you change code
    #   3. Provides debugging tools in browser
    app.run(host="0.0.0.0", port=port, debug=True)
