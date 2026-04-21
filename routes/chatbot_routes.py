"""
chatbot_routes.py

Chatbot routing module for the Ancient Ruins Clan Analytics system.

This module manages all routes related to chatbot interaction,
including the chatbot query API and the chatbot user interface.

Responsibilities:
• Process chatbot user queries
• Validate incoming chatbot requests
• Connect chatbot routes to the chat controller service
• Provide chatbot UI rendering route
• Return structured chatbot responses
• Support Swagger documentation for chatbot APIs

Features:
• Natural language query processing
• Input validation (message length restriction)
• Structured chatbot responses (reply, source, suggestions)
• Web interface for chatbot interaction
• REST API support for chatbot queries

Endpoints Provided:
• /api/chatbot/ → Main chatbot query processing endpoint (POST)
• /ai/chat/ → Chatbot web interface route

Workflow:
User Request → Validation → Chat Controller → Response Formatting → JSON Output

Dependencies:
• chatbot.chat_controller → Chat processing logic
• Flask Blueprint → Modular route management
• JSON responses → API communication

Design Considerations:
• Input size validation for stability
• Separation of routing and chatbot logic
• Modular chatbot service integration
• Frontend and API separation

Architecture Layer:
This module belongs to the interaction layer and acts as the bridge
between user requests and the chatbot processing engine.
"""

from flask import Blueprint, jsonify, request, render_template

from chatbot.chat_controller import handle_chat

from limiter_config import limiter

chatbot_bp = Blueprint("chatbot", __name__)

@chatbot_bp.route("/api/chatbot/", methods=["POST"])
@limiter.limit("10 per minute")
def chatbot():

    """
    Chatbot Query API
    ---
    tags:
      - Chatbot

    parameters:
      - name: body
        in: body
        required: true

        schema:
          type: object

          properties:

            message:
              type: string

              example: list feb 2026

    responses:

      200:

        description: Chatbot response

        schema:

          type: object

          properties:

            reply:
              type: string

            source:
              type: string

            suggestions:

              type: array

              items:
                type: string

      400:
        description: Message too long

      429:
        description: Too many requests (rate limit exceeded)
    """

    payload = request.get_json(silent=True) or {}

    message = payload.get("message", "")

    if len(message) > 500:

        return (
            jsonify({"reply": "Message too long", "source": None, "suggestions": []}),
            400,
        )

    response = handle_chat(message)

    return jsonify(response)

@chatbot_bp.route("/ai/chat/")
def chat():
    """
    Chatbot UI Route.

    Purpose:
    Renders the web interface for the Ancient Ruins Clan chatbot,
    allowing users to interact with the chatbot through a browser.

    Functionality:
    • Loads the chatbot frontend template
    • Provides UI for sending queries to the chatbot API
    • Acts as the human interaction entry point

    Returns:
        HTML page:
            chatbot-pages/chat.html
    """

    return render_template("/chatbot-pages/chat.html")