# chatbot/__init__.py

"""
chatbot package initializer for Ancient Ruins STATS BOT (Ancient Ruins Clan).

This package:
- Implements a lightweight, deterministic, rule-based chatbot system
- Handles conversational querying of structured Clash of Clans clan data
- Operates exclusively on Ancient Ruins clan datasets hosted on GitHub
- Avoids machine learning, LLMs, or probabilistic reasoning
- Ensures transparent, explainable, and reproducible responses

The package is organized into focused modules that handle:
- Input understanding and classification
- Month and range normalization
- Dataset domain routing
- Operation resolution and analytics
- Data retrieval from GitHub raw JSON
- Human-readable response generation

By defining `__all__`, this file:
- Establishes the public API surface of the chatbot package
- Controls which internal modules are exposed for external use
- Simplifies imports across the application
- Enforces clean modular boundaries

This package forms the core reasoning and analytics layer of Ancient Ruins STATS BOT.
"""

__all__ = [
    "almost_hint",
    "chat_controller",
    "domain_router",
    "month_normalizer",
    "operation_resolver",
    "raw_fetcher",
    "response_builder"
]