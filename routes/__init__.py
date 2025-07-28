"""
Routes Package
=============

This package contains all Flask route blueprints organized by functionality.
Each blueprint handles specific areas of the application.

For beginners: Routes are like different pages or sections of the website.
They handle what happens when users visit different URLs.
"""

from .main_routes import main_bp
from .auth_routes import auth_bp  
from .admin_routes import admin_bp
from .rbac_routes import rbac_bp

# Make blueprints available when importing from routes package
__all__ = ['main_bp', 'auth_bp', 'admin_bp', 'rbac_bp']