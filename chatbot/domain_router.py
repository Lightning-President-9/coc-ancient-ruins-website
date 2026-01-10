# chatbot/domain_router.py

"""
This module is responsible for determining which dataset domain should be
used to answer a given user query. It acts as a lightweight routing layer
that maps user intent and temporal context to the appropriate data source.

The routing decision is based on:
- Keywords present in the user query (e.g., "former", "top", "most")
- The type of time reference detected (single month vs month range)

By centralizing domain selection logic in this module, the chatbot ensures:
- Clear separation of concerns
- Consistent dataset usage across all queries
- Predictable and deterministic routing behavior

This module does not inspect or manipulate the data itself; it only selects
the correct dataset domain identifier to be used by downstream components.
"""

def route_domain(text: str, month_info: dict) -> str | None:
    """
    Determines the appropriate dataset domain for a user query.

    This function analyzes the normalized user input and the extracted
    month information to decide which category of clan data should be queried.

    Supported domains:
    - CLAN_MEMBERS: Monthly data for active clan members
    - CLAN_MONTHLY_ANALYSIS: Aggregated analysis across a range of months
    - FORMER_CLAN_MEMBERS: Monthly data for players who have left the clan
    - TOP_CLAN_CONTRIBUTORS: Monthly top contributors based on clanscore

    Routing rules:
    - Queries containing "former" or "ex member" with a single month
      are routed to former clan member data.
    - Queries referencing a month range are routed to monthly analysis data.
    - Queries requesting top or most clanscore for a single month are routed
      to the top clan contributors dataset.
    - All other single-month queries default to active clan member data.

    Parameters:
        text (str): Raw user input text.
        month_info (dict): Normalized month information containing:
            - type: "single", "range", or None
            - value: Normalized month or range identifier

    Returns:
        str | None:
            - A domain identifier string corresponding to the dataset to use.
            - None if no valid domain can be determined for the query.

    This function is intentionally conservative: when ambiguity exists,
    it prefers explicit routing rules and otherwise falls back to safe defaults.
    """

    text = text.lower()
    month_type = month_info.get("type")

    # Former Clan Members
    if "former" in text or "ex member" in text:
        if month_type == "single":
            return "FORMER_CLAN_MEMBERS"

    # Monthly Analysis
    if month_type == "range":
        return "CLAN_MONTHLY_ANALYSIS"

    # Top Clan Contributors (ONLY clanscore)
    if month_type == "single":
        if "clanscore" in text and ("top" in text or "most" in text):
            return "TOP_CLAN_CONTRIBUTORS"

    # Clan Members (default)
    if month_type == "single":
        return "CLAN_MEMBERS"

    return None
