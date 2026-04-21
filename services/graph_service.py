"""
graph_service.py

Graph service management module for the Ancient Ruins Clan Analytics system.

This module provides centralized access to all graph processing classes
used in the application. It implements a singleton pattern for each graph
type to ensure efficient memory usage and avoid repeated initialization
of heavy graph processing objects.

Responsibilities:
• Manage graph object lifecycle
• Provide singleton instances of graph classes
• Reduce redundant object creation
• Improve performance through object reuse
• Act as service layer between routes and graph modules

Graph Services Provided:
• ClanMemberGraph → Current clan member analytics
• FormerMemberGraph → Former member analysis
• MonthlyAnalysisGraph → Monthly performance analysis
• AllMonthGraph → Long-term trend analysis
• MemberClusterGraph → AI clustering analysis

Design Pattern:
Singleton pattern used for each graph service to maintain a single
instance during application execution.

Benefits:
• Better memory management
• Faster graph generation
• Centralized service access
• Clean separation between routes and graph logic

Architecture Layer:
Service layer connecting route controllers with graph processing modules.
"""

from graphs import (
    ClanMemberGraph,
    FormerMemberGraph,
    MonthlyAnalysisGraph,
    AllMonthGraph,
    MemberClusterGraph,
)

# Singleton instance holders for graph services.
# Each object is created only when first requested.
cmg = None  # Clan Member Graph
fmg = None  # Former Member Graph
mag = None  # Monthly Analysis Graph
amg = None  # All Month Analysis Graph
mcg = None  # Member Cluster Graph

def get_cmg():
    """
    Get Clan Member Graph service instance.

    Purpose:
    Returns a singleton instance of ClanMemberGraph.

    Returns:
        ClanMemberGraph object.
    """

    global cmg

    if cmg is None:
        cmg = ClanMemberGraph()

    return cmg

def get_fmg():
    """
    Get Former Member Graph service instance.

    Purpose:
    Returns a singleton instance of FormerMemberGraph.

    Returns:
        FormerMemberGraph object.
    """

    global fmg

    if fmg is None:
        fmg = FormerMemberGraph()

    return fmg

def get_mag():
    """
    Get Monthly Analysis Graph service instance.

    Purpose:
    Returns a singleton instance of MonthlyAnalysisGraph.

    Returns:
        MonthlyAnalysisGraph object.
    """

    global mag

    if mag is None:
        mag = MonthlyAnalysisGraph()

    return mag

def get_amg():
    """
    Get All Month Analysis Graph service instance.

    Purpose:
    Returns a singleton instance of AllMonthGraph.

    Returns:
        AllMonthGraph object.
    """

    global amg

    if amg is None:
        amg = AllMonthGraph()

    return amg

def get_mcg():
    """
    Get Member Cluster Graph service instance.

    Purpose:
    Returns a singleton instance of MemberClusterGraph
    used for clustering based analysis.

    Returns:
        MemberClusterGraph object.
    """

    global mcg

    if mcg is None:
        mcg = MemberClusterGraph()

    return mcg