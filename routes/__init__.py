"""
routes/__init__.py

Central route registration module for the Ancient Ruins Clan Analytics application.

This module imports all Blueprint route modules and provides a single
registration function to attach them to the Flask application.

Purpose:
• Centralizes route registration
• Keeps app.py clean and modular
• Supports scalable architecture
• Enables separation of concerns

Architecture Role:
Acts as the routing aggregator that connects all functional route
modules to the main Flask application.

Blueprint Modules Registered:
• api_routes → Core data APIs
• github_api_routes → GitHub data integration APIs
• graph_routes → Visualization endpoints
• ai_routes → AI prediction and clustering APIs
• chatbot_routes → Chatbot interaction APIs
• report_routes → Player report generation APIs
• coc_routes → Clan data APIs
• ui_routes → Frontend page routes

Design Principle:
Modular Blueprint architecture for maintainability and scalability.
"""

# Importing Blueprint objects from route modules.
# Each Blueprint represents a functional module of the application.
from .api_routes import api_bp
from .github_api_routes import github_api_bp
from .graph_routes import graph_bp
from .ai_routes import ai_bp
from .chatbot_routes import chatbot_bp
from .report_routes import report_bp
from .coc_routes import coc_bp
from .ui_routes import ui_bp

def register_routes(app):
    """
    Registers all route blueprints with the Flask application.

    Purpose:
    Provides a single centralized function to attach all
    application routes to the Flask app instance.

    Benefits:
    • Improves modularity
    • Simplifies app initialization
    • Makes route management scalable
    • Encourages clean architecture

    Parameters:
        app (Flask):
            Main Flask application instance.

    Returns:
        None
    """

    # Core API routes
    app.register_blueprint(api_bp)

    # GitHub integration APIs
    app.register_blueprint(github_api_bp)

    # Graph visualization routes
    app.register_blueprint(graph_bp)

    # AI prediction and clustering routes
    app.register_blueprint(ai_bp)

    # Chatbot service routes
    app.register_blueprint(chatbot_bp)

    # Player report generation routes
    app.register_blueprint(report_bp)

    # Clash of Clans data routes
    app.register_blueprint(coc_bp)

    # UI rendering routes
    app.register_blueprint(ui_bp)