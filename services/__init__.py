"""
services/__init__.py

Service layer aggregation module for the Ancient Ruins Clan Analytics system.

This module centralizes imports of all service layer functions and exposes
them through a single interface. It simplifies imports across the application
by acting as a service registry.

Responsibilities:
• Aggregate graph services
• Aggregate AI services
• Aggregate report services
• Aggregate GitHub data services
• Provide clean service exports

Purpose:
Allows other modules to import required services from one location instead
of importing from multiple service files.

Example:
Instead of:
from services.graph_service import get_cmg

Use:
from services import get_cmg

Services Included:
Graph Services:
• get_cmg → Clan member graph service
• get_fmg → Former member graph service
• get_mag → Monthly analysis graph service
• get_amg → All month analysis service
• get_mcg → Member clustering service

AI Services:
• get_apg → AI prediction graph service

Report Services:
• get_all_players → Player listing service
• generate_report → Player PDF report service

GitHub Services:
• fetch_github_json → Remote JSON data fetcher

Design Pattern:
Service aggregation pattern for clean architecture.

Architecture Layer:
Service layer abstraction between routes and data/processing modules.
"""

from .graph_service import get_cmg, get_fmg, get_mag, get_amg, get_mcg

from .ai_service import get_apg

from .report_service import get_all_players, generate_report

from .github_service import fetch_github_json

# Explicitly defines public service functions available for import.
# Prevents unintended internal functions from being exposed.
__all__ = [
    "get_cmg",
    "get_fmg",
    "get_mag",
    "get_amg",
    "get_mcg",
    "get_apg",
    "get_all_players",
    "generate_report",
    "fetch_github_json",
]