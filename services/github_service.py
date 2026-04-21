"""
github_service.py

GitHub data fetching service module for the Ancient Ruins Clan Analytics system.

This module provides utility functions to retrieve JSON datasets from
remote GitHub repositories and perform basic data normalization.

Responsibilities:
• Fetch remote JSON datasets from GitHub
• Convert numeric string values into integers
• Provide cleaned data to route modules
• Handle external data integration

Features:
• HTTP data retrieval using requests
• Automatic numeric type conversion
• Lightweight data preprocessing
• Reusable GitHub data access function

Dependencies:
• requests → HTTP client for fetching remote data

Design Considerations:
• Keeps data fetching logic separate from route logic
• Ensures consistent numeric data types
• Simplifies data preparation for analytics modules

Architecture Layer:
Service layer responsible for external data integration.
"""

import requests

def fetch_github_json(url):
    """
    Fetch JSON data from GitHub and normalize numeric values.

    Purpose:
    Retrieves JSON data from a given GitHub raw file URL and
    converts numeric string fields into integers for proper
    data processing.

    Parameters:
        url (str):
            Raw GitHub JSON file URL.

    Workflow:
    • Send HTTP GET request
    • Parse JSON response
    • Detect numeric strings
    • Convert numeric strings to integers
    • Return cleaned dataset

    Returns:
        list:
            List of dictionaries containing normalized data.
    """

    # Fetch data from GitHub repository
    response = requests.get(url)

    if response.status_code != 200:
        return {
            "error": "Data not found",
            "status_code": response.status_code,
            "url": url
        }, 404

    try:
        data = response.json()
    except Exception:
        return {
            "error": "Invalid JSON response from GitHub",
            "raw_response": response.text[:200]  # limit output
        }, 500

    # Normalize numeric values
    for player in data:
        for key, value in player.items():
            if isinstance(value, str) and value.isdigit():
                player[key] = int(value)

    return data