"""
error_handlers.py

Centralized error handling module for the Ancient Ruins Clan Analytics system.

This module defines custom error handlers for common HTTP errors and
registers them with the Flask application to provide user-friendly
error pages instead of default Flask error responses.

Responsibilities:
• Handle 404 (Page Not Found) errors
• Handle 405 (Method Not Allowed) errors
• Handle 429 (API rate limits) errors
• Handle 500 (Internal Server Error) errors
• Provide consistent UI for error responses
• Improve user experience through custom error templates

Features:
• Centralized error management
• Clean separation of error handling from route logic
• Custom HTML error pages
• Scalable error registration design

Error Codes Covered:
• 404 → Resource not found
• 405 → HTTP method not allowed
• 500 → Internal server error

Architecture Role:
Infrastructure layer component responsible for global exception
handling and UI error response rendering.
"""

from flask import render_template

def register_error_handlers(app):
    """
    Register application error handlers.

    Purpose:
    Attaches custom error handling functions to the Flask
    application instance.

    Benefits:
    • Centralized error management
    • Cleaner app.py structure
    • Consistent error UI
    • Easier maintenance

    Parameters:
        app (Flask):
            Main Flask application instance.

    Returns:
        None
    """

    @app.errorhandler(404)
    def page_not_found(e):
        """
        404 Error Handler.

        Purpose:
        Handles requests for non-existent routes or resources.

        Returns:
            Custom 404 error page.
        """

        return render_template("/error-pages/404.html"), 404

    @app.errorhandler(405)
    def method_not_allowed(e):
        """
        405 Error Handler.

        Purpose:
        Handles requests using unsupported HTTP methods.

        Returns:
            Custom 405 error page.
        """

        return render_template("/error-pages/405.html"), 405

    @app.errorhandler(429)
    def ratelimit_exceeded(e):
        """
        429 Error Handler.

        Purpose:
        Handles requests exceeding API rate limits.

        Returns:
            Custom 429 error page.
        """

        return render_template("/error-pages/429.html"), 429

    @app.errorhandler(500)
    def internal_error(e):
        """
        500 Error Handler.

        Purpose:
        Handles unexpected server errors and exceptions.

        Returns:
            Custom 500 error page.
        """

        return render_template("/error-pages/500.html"), 500