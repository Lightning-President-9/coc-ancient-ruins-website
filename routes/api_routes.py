"""
api_routes.py

Core API routes module for the Ancient Ruins Clan Analytics system.

This module provides REST API endpoints for accessing clan member data
and system service status information. It serves as the primary data
exposure layer for frontend dashboards and external integrations.

Responsibilities:
• Provide current clan member data
• Provide former clan member data
• Provide service health status endpoint
• Deliver structured JSON responses
• Support Swagger API documentation
• Apply request rate limiting for API protection

Data Source:
Clan member data is loaded from a persisted pickle file
(data_file.pickle) during module initialization to reduce
repeated I/O operations.

API Features:
• Current member performance metrics
• Former member historical data
• Chatbot service health check
• Structured JSON responses
• Swagger/OpenAPI documentation support
• Per-endpoint rate limiting protection

Security Features:
• Request rate limiting to prevent API abuse
• Protection against scraping and excessive requests
• Fair usage enforcement across public endpoints

Endpoints Provided:
• /api/mem/ → Current clan members data (Rate limited)
• /api/fmem/ → Former clan members data (Rate limited)
• /chatbot-service-status → Service health check (Rate limited)

Technologies Used:
• Flask Blueprint → Modular API routing
• Flask-Limiter → Request rate limiting
• Pickle → Data persistence
• JSON → Data transport format
• Flasgger → Swagger documentation

Design Considerations:
• Read-only API design
• Lightweight data serving
• Fast response through preloaded data
• Modular API structure
• Public API protection through rate limiting

Architecture Layer:
This module belongs to the API presentation layer and interacts
with persisted datasets without business logic processing.
"""

from flask import Blueprint, jsonify
import pickle
from limiter_config import limiter

api_bp = Blueprint("api", __name__)

with open("data_file.pickle", "rb") as f:

    mem_list, fmem_list = pickle.load(f)

@api_bp.route("/api/mem/")
@limiter.limit("5 per minute")
def api_mem():
    """
    Get Current Clan Members
    ---
    tags:
      - Clan Data

    responses:
      200:
        description: List of current clan members with performance metrics

        schema:

          type: array

          items:

            type: object

            properties:

              srno:
                type: integer
                description: Serial number of player
                example: 1

              name:
                type: string
                description: Player name
                example: KAI HIWATARI

              uniqueid:
                type: string
                description: Internal clan ID
                example: COCAR#1

              playertag:
                type: string
                description: Clash of Clans player tag
                example: 2QRU2LCPP

              status:
                type: string
                description: Clan role
                example: Leader

              war:
                type: string
                description: War participation status
                example: IN

              clancapital:
                type: integer
                description: Capital raid contribution
                example: 721

              clangames:
                type: integer
                description: Clan games points
                example: 36

              clangamesmaxed:
                type: integer
                description: Number of times clan games maxed
                example: 8

              clanscore:
                type: integer
                description: Total clan contribution score
                example: 1619

              warattack:
                type: integer
                description: War attack contribution score
                example: 610

      429:
        description: Too many requests (rate limit exceeded)

        example:

          - srno: 1
            name: KAI HIWATARI
            uniqueid: COCAR#1
            playertag: 2QRU2LCPP
            status: Leader
            war: IN
            clancapital: 721
            clangames: 36
            clangamesmaxed: 8
            clanscore: 1619
            warattack: 610
    """

    return jsonify(mem_list)

@api_bp.route("/api/fmem/")
@limiter.limit("5 per minute")
def api_fmem():
    """
    Get Clan Members
    ---
    tags:
      - Clan Data

    responses:
      200:
        description: List of clan members

        schema:

          type: array

          items:

            type: object

            properties:

              srno:
                type: integer
                example: 1

              name:
                type: string
                example: KING SEENU

              uniqueid:
                type: string
                example: COCAR#47

              clancapital:
                type: integer
                example: 0

              clangames:
                type: integer
                example: 0

              clangamesmaxed:
                type: integer
                example: 0

              clanscore:
                type: integer
                example: 40

              warattack:
                type: integer
                example: 40

      429:
        description: Too many requests (rate limit exceeded)

        example:

          - srno: 1
            name: KING SEENU
            uniqueid: COCAR#47
            clancapital: 0
            clangames: 0
            clangamesmaxed: 0
            clanscore: 40
            warattack: 40

    """

    return jsonify(fmem_list)

@api_bp.route("/chatbot-service-status")
@limiter.limit("10 per minute")
def status():

    """
    Chatbot Service Status
    ---
    tags:
      - Chatbot Service Status

    responses:
      200:
        description: Service status
        schema:
          type: object
          properties:
            status:
              type: string
              example: ok

            service:
              type: string
              example: Clan Chatbot API
      429:
        description: Too many requests (rate limit exceeded)
    """

    return jsonify({"status": "ok", "service": "Clan Chatbot API"})