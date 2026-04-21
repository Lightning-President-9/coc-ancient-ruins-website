"""
app.py

Main entry point of the Ancient Ruins Clan Analytics API application.

This module is responsible for:
• Initializing the Flask application
• Configuring Swagger API documentation
• Registering all route blueprints
• Registering centralized error handlers
• Configuring API rate limiting
• Starting the Flask server

Architecture Role:
Acts as the application bootstrap module that wires together
routes, documentation, error handling, and request protection
into a single API service.

Core Responsibilities:
• Application configuration
• API documentation setup
• Blueprint registration
• Error handler integration
• Global request rate limiting
• Server startup configuration

Technologies Used:
• Flask → Web framework
• Flasgger → Swagger API documentation
• Flask-Limiter → API rate limiting and abuse protection
• Blueprint architecture → Modular route design

Security Features:
• Global request rate limiting to prevent API abuse
• Protection against excessive request bursts
• Fair usage enforcement for public endpoints

Design Pattern Used:
Application Factory style modular structure using route registrars.
"""

from flask import Flask
from flasgger import Swagger

from routes import register_routes
from routes.error_handlers import register_error_handlers

from limiter_config import init_limiter

# Creating the main Flask application instance.
# This object serves as the central WSGI application.
app = Flask(__name__)

# Swagger/OpenAPI documentation configuration.
# Defines API metadata including title, version,
# description and project contact information.
swagger_template = {
    "info": {
        "title": "Ancient Ruins Clan Data API",
        "description": "API documentation for Ancient Ruins Clan",
        "version": "1.0.0",
        "contact": {
            "name": "COC Ancient Ruins Project",
            "url": "https://github.com/Lightning-President-9",
        },
    }
}

# Initialize Swagger documentation for automatic
# API endpoint documentation and testing interface.
Swagger(app, template=swagger_template)

# Registers all application routes using Blueprint modular structure.
# This keeps the application scalable and organized by separating
# route logic into different modules.
register_routes(app)

# Registers global error handlers (404, 500, 405 etc.)
# Provides centralized exception handling across the application.
register_error_handlers(app)

init_limiter(app)

if __name__ == "__main__":
    """
    Application execution entry point.

    Purpose:
    Starts the Flask development server.

    Configuration:
    host  → Allows external access
    port  → Application running port
    debug → Enables hot reload and debugging
    """
    app.run(host="0.0.0.0", port=10000, debug=True)