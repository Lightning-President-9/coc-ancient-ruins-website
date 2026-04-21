"""
ai_service.py

AI service module for the Ancient Ruins Clan Analytics system.

This module manages the lifecycle of the AI Prediction Graph service.
It implements a singleton pattern to ensure only one instance of the
AI prediction engine exists during the application runtime.

Responsibilities:
• Provide access to AI prediction graph service
• Manage object creation efficiently
• Prevent redundant object initialization
• Support performance optimization through reuse

Service Provided:
• AIPredictionGraph → AI forecasting and prediction visualization engine

Design Pattern:
Singleton pattern to maintain a single shared instance of the
AI prediction service.

Architecture Layer:
Service layer connecting AI graph processing modules with route handlers.
"""

from graphs import AIPredictionGraph

# Singleton instance holder for AI Prediction Graph.
# Initialized only when first requested.
apg = None

def get_apg():
    """
    Get AI Prediction Graph service instance.

    Purpose:
    Returns a singleton instance of AIPredictionGraph to
    avoid repeated object creation and improve performance.

    Workflow:
    • Check if instance exists
    • Create instance if not present
    • Return existing instance otherwise

    Returns:
        AIPredictionGraph:
            AI prediction service object.
    """

    global apg

    # Create instance only if not already initialized
    if apg is None:
        apg = AIPredictionGraph()

    return apg