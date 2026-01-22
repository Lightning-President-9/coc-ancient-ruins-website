# graphs/__init__.py

"""
graphs package initializer for the Clash of Clans – Ancient Ruins Clan Website.

This module:
- Aggregates and exposes all graph-related classes used by the application
- Centralizes imports for different graph types (member, former member,
  monthly analysis, all-month analysis, and AI prediction)
- Exposes player report utilities
- Re-exports commonly used constants for graph configuration

By defining `__all__`, this file provides a clean public interface for the
graphs package and simplifies imports throughout the application.
"""

from .ai_prediction_graph import AIPredictionGraph
from .all_month_graph import AllMonthGraph
from .clan_member_graph import ClanMemberGraph
from .former_member_graph import FormerMemberGraph
from .monthly_analysis_graph import MonthlyAnalysisGraph
from .member_cluster_graph import MemberClusterGraph
from .player_report import get_players, generate_player_report
from constants import LATEST_MONTH, PREDICTED_MONTH, LATEST_MONTH_RANGE, CLAN_MONTHLY_PERFORMANCE_RANGE

__all__ = ["AIPredictionGraph", "AllMonthGraph", "ClanMemberGraph",
           "FormerMemberGraph", "MonthlyAnalysisGraph", "get_players",
           "MemberClusterGraph",
           "generate_player_report", "LATEST_MONTH", "PREDICTED_MONTH",
           "LATEST_MONTH_RANGE", "CLAN_MONTHLY_PERFORMANCE_RANGE"]