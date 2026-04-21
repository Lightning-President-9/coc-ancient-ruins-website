"""
github_api_routes.py

GitHub data integration routes module for the Ancient Ruins Clan Analytics system.

This module provides API endpoints that dynamically fetch clan datasets
stored in the project's GitHub data repository. It acts as a data proxy
layer between the GitHub JSON storage and the application frontend.

Responsibilities:
• Fetch clan member monthly data from GitHub
• Fetch monthly analysis datasets
• Fetch clan performance history
• Fetch former clan member records
• Fetch top contributor statistics
• Provide structured API access to remote JSON datasets

Data Source:
All datasets are stored in the ClanDataRepo GitHub repository and
retrieved dynamically using raw GitHub URLs.

Features:
• Dynamic month/year based dataset retrieval
• Remote JSON data access
• Centralized GitHub data service integration
• Swagger API documentation support
• Error handling for missing datasets

Endpoints Provided:
• /api/github/clan-members/<month>/<year> → Monthly clan members data
• /api/github/monthly-analysis/<start>/<end>/<year> → Monthly performance analysis
• /api/github/clan-performance/<month>/<year> → Historical performance trends
• /api/github/former-members/<month>/<year> → Former member records
• /api/github/top-contributors/<month>/<year> → Top contributor statistics

Dependencies:
• services.github_service → GitHub data fetching logic
• Flask Blueprint → Modular routing
• JSON datasets → Remote data storage

Design Considerations:
• Decouples storage from application
• Supports dataset versioning through GitHub
• Reduces database dependency
• Enables easy data updates via repository commits

Architecture Layer:
This module belongs to the data access API layer and serves as
an integration point between remote GitHub storage and the application.
"""

from flask import Blueprint

from services.github_service import fetch_github_json

from limiter_config import limiter

github_api_bp = Blueprint("github_api", __name__)

@github_api_bp.route("/api/github/clan-members/<month>/<int:year>/")
@limiter.limit("10 per minute")
def clan_members(month, year):
    """
    Clan Members JSON
    ---
    tags:
      - GitHub Data

    parameters:

      - name: month
        in: path
        type: string
        example: FEB

      - name: year
        in: path
        type: integer
        example: 2026

    responses:

      200:
        description: Clan members data

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
                example: KAI HIWATARI

              status:
                type: string
                example: Leader

              war:
                type: string
                example: IN

              clancapital:
                type: integer
                example: 745

              clangames:
                type: integer
                example: 37

              clangamesmaxed:
                type: integer
                example: 8

              clanscore:
                type: integer
                example: 1664

              warattack:
                type: integer
                example: 623
      404:
        description: Data not found
    """

    month = month.upper()

    url = f"https://raw.githubusercontent.com/Lightning-President-9/ClanDataRepo/main/Clan%20Members/JSON/{month}_{year}.json"

    return fetch_github_json(url)

@github_api_bp.route("/api/github/monthly-analysis/<start>/<end>/<int:year>/")
@limiter.limit("10 per minute")
def monthly(start, end, year):
    """
    Monthly Analysis JSON
    ---
    tags:
      - GitHub Data

    parameters:

      - name: start
        in: path
        type: string

      - name: end
        in: path
        type: string

      - name: year
        in: path
        type: integer

    responses:

      200:
        description: Monthly analysis metrics

        schema:

          type: array

          items:

            type: object

            properties:

              name:
                type: string
                example: KAI HIWATARI

              clancapital:
                type: integer
                example: 24

              clangames:
                type: integer
                example: 1

              clangamesmaxed:
                type: integer
                example: 0

              clanscore:
                type: integer
                example: 38

              warattack:
                type: integer
                example: 13
      404:
        description: Data not found
    """

    start = start.upper()
    end = end.upper()

    url = f"https://raw.githubusercontent.com/Lightning-President-9/ClanDataRepo/main/Clan%20Members/Monthly%20Analysis%20JSON/data_{start}-{end}_{year}.json"

    return fetch_github_json(url)

@github_api_bp.route("/api/github/clan-performance/<month>/<int:year>/")
@limiter.limit("10 per minute")
def performance(month, year):
    """
    Clan Performance History
    ---
    tags:
      - GitHub Data

    parameters:

      - name: month
        in: path
        type: string
        example: FEB

      - name: year
        in: path
        type: integer
        example: 2026

    responses:

      200:
        description: Historical clan performance metrics

        schema:

          type: array

          items:

            type: object

            properties:

              name:
                type: string
                example: KAI HIWATARI

              clanscore_JAN-FEB_2026:
                type: integer
                example: 38

              warattack_JAN-FEB_2026:
                type: integer
                example: 13

              clancapital_JAN-FEB_2026:
                type: integer
                example: 24

              clanscore_DEC-JAN_2026:
                type: integer
                example: 43

              warattack_DEC-JAN_2026:
                type: integer
                example: 18

              clancapital_DEC-JAN_2026:
                type: integer
                example: 24
      404:
        description: Data not found
    """

    month = month.upper()

    url = f"https://raw.githubusercontent.com/Lightning-President-9/ClanDataRepo/main/Clan%20Members/Clan%20Monthly%20Performance%20JSON/clan_monthly_performance_JUL_2024_to_{month}_{year}.json"

    return fetch_github_json(url)

@github_api_bp.route("/api/github/former-members/<month>/<int:year>/")
@limiter.limit("10 per minute")
def former(month, year):
    """
    Former Members JSON
    ---
    tags:
      - GitHub Data

    parameters:

      - name: month
        in: path
        type: string

      - name: year
        in: path
        type: integer

    responses:

      200:
        description: Former clan members

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
      404:
        description: Data not found
    """

    month = month.upper()

    url = f"https://raw.githubusercontent.com/Lightning-President-9/ClanDataRepo/main/Former%20Clan%20Members/JSON/{month}_{year}.json"

    return fetch_github_json(url)

@github_api_bp.route("/api/github/top-contributors/<month>/<int:year>/")
@limiter.limit("10 per minute")
def contributors(month, year):
    """
    Top Contributors JSON
    ---
    tags:
      - GitHub Data

    parameters:

      - name: month
        in: path
        type: string

      - name: year
        in: path
        type: integer

    responses:

      200:
        description: Top clan contributors

        schema:

          type: array

          items:

            type: object

            properties:

              name:
                type: string
                example: KAI HIWATARI

              clanscore:
                type: integer
                example: 1664
      404:
        description: Data not found
    """

    month = month.upper()

    url = f"https://raw.githubusercontent.com/Lightning-President-9/ClanDataRepo/main/Top%20Clan%20Contributors/JSON/{month}_{year}.json"

    return fetch_github_json(url)