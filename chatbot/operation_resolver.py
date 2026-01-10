# chatbot/operation_resolver.py

"""
This module functions as the core inference and decision-making engine of
the chatbot. Its responsibility is to translate a validated user query
into a precise analytical operation that can be executed on structured
clan data.

The resolver is fully deterministic and rule-based. It does not perform
any natural language generation; instead, it interprets user intent using
explicit rules, keyword detection, and controlled heuristics.

Key responsibilities of this module include:
- Identifying which metric a user is referring to
- Detecting analytical intent (top, lowest, average, total, group, compare)
- Validating whether a metric is allowed for a given data domain
- Resolving player-specific, aggregate, and comparative operations
- Returning a structured result object describing what was computed

This module does not format responses for presentation. It returns
machine-readable results that are later converted into human-readable
text by the response builder.

Within the AR STATS BOT architecture, this module acts as the
expert-system–style inference engine.
"""

# Importing Libraries
import re

# DOMAIN → ALLOWED METRICS
DOMAIN_ALLOWED_FIELDS = {
    "CLAN_MEMBERS": {
        "war", "warattack", "clancapital",
        "clangames", "clangamesmaxed",
        "clanscore", "status"
    },
    "CLAN_MONTHLY_ANALYSIS": {
        "warattack", "clancapital",
        "clangames", "clangamesmaxed",
        "clanscore"
    },
    "FORMER_CLAN_MEMBERS": {
        "warattack", "clancapital",
        "clangames", "clangamesmaxed",
        "clanscore"
    },
    "TOP_CLAN_CONTRIBUTORS": {
        "clanscore"
    }
}

# SUPPORTED METRICS
SUPPORTED_METRICS = {
    "warattack",
    "clancapital",
    "clangames",
    "clangamesmaxed",
    "clanscore",
}

def detect_metric(text: str) -> str | None:
    """
        Detects which supported metric is referenced in the user query.

        The function performs a simple substring search against the set of
        supported metrics. Only one metric is returned, and the first match
        encountered is used.

        Parameters:
            text (str): Raw user input text.

        Returns:
            str | None:
                - The detected metric name if found.
                - None if no supported metric is referenced.
    """

    text = text.lower()
    for m in SUPPORTED_METRICS:
        if m in text:
            return m
    return None

def detect_two_players(text: str, data: list) -> list[str]:
    """
        Detects exactly two distinct player names from the user query.

        This function scans the input text against known player names present
        in the dataset. It preserves the order of appearance and removes
        duplicates. A valid result is returned only when exactly two unique
        players are found.

        Parameters:
            text (str): Raw user input text.
            data (list): Dataset containing player records.

        Returns:
            list[str]:
                - A list of exactly two player names if detected.
                - An empty list otherwise.
    """

    found = []
    text_lower = text.lower()

    for row in data:
        name = row.get("name", "")
        if name and name.lower() in text_lower:
            found.append(name)

    # remove duplicates while preserving order
    unique = []
    for n in found:
        if n not in unique:
            unique.append(n)

    return unique if len(unique) == 2 else []

def detect_group_by(text: str) -> bool:
    """
        Determines whether the user query requests grouping by metric value.

        Parameters:
            text (str): Raw user input text.

        Returns:
            bool:
                True if the query contains grouping intent, False otherwise.
    """

    return "group" in text.lower()

def detect_average(text: str) -> bool:
    """
        Determines whether the user query requests an average calculation.

        Parameters:
            text (str): Raw user input text.

        Returns:
            bool:
                True if average-related keywords are detected, False otherwise.
    """

    text = text.lower()
    return "average" in text or "avg" in text or "mean" in text

def detect_total(text: str) -> bool:
    """
        Determines whether the user query requests a total or sum calculation.

        Parameters:
            text (str): Raw user input text.

        Returns:
            bool:
                True if total-related keywords are detected, False otherwise.
    """

    text = text.lower()
    return "total" in text or "sum" in text

def detect_top_n(text: str) -> int | None:
    """
        Detects a request for a top-N ranking.

        This function parses expressions such as "top 5" or "top 10" and
        enforces an upper bound to prevent excessive computation.

        Parameters:
            text (str): Raw user input text.

        Returns:
            int | None:
                - The requested N value if valid.
                - None if no top-N pattern is detected.
    """

    m = re.search(r"\btop\s+(\d{1,2})\b", text.lower())
    if not m:
        return None
    n = int(m.group(1))
    return n if 1 <= n <= 50 else None

def detect_membership_query(text: str) -> bool:
    """
        Determines whether the query is asking about player membership or
        existence within a specific dataset domain.

        Parameters:
            text (str): Raw user input text.

        Returns:
            bool:
                True if membership-related intent is detected, False otherwise.
    """

    text = text.lower()
    return any(k in text for k in ("is", "a member", "a former", "in top"))

def detect_non_zero(text: str) -> bool:
    """
        Determines whether the query specifies exclusion of zero-valued metrics.

        Parameters:
            text (str): Raw user input text.

        Returns:
            bool:
                True if non-zero filtering is requested, False otherwise.
    """

    text = text.lower()
    return "non-zero" in text or "non zero" in text

def detect_player_name(text: str, data: list) -> str | None:
    """
        Detects a single player name referenced in the user query.

        The function matches player names present in the dataset using a
        case-insensitive substring search.

        Parameters:
            text (str): Raw user input text.
            data (list): Dataset containing player records.

        Returns:
            str | None:
                - The detected player name if found.
                - None if no player name is detected.
    """

    text_lower = text.lower()
    for row in data:
        name = row.get("name", "")
        if name.lower() in text_lower:
            return name
    return None

def resolve_operation(text: str, domain: str, data: list) -> dict | None:
    """
    Resolves the exact analytical operation requested by the user.

    This is the main entry point of the operation resolver. It interprets
    user intent, validates metric and domain compatibility, and constructs
    a structured result describing the operation outcome.

    The resolution process supports:
    - Player-specific metric queries
    - Rankings (top, lowest, non-zero, top-N with ties)
    - Group-by metric analysis
    - Aggregate statistics (average, total)
    - Player comparisons
    - Membership and existence checks

    Resolution follows a strict priority order to avoid ambiguity, ensuring
    that more specific intents (such as player metrics) are handled before
    more general analytical operations.

    Parameters:
        text (str): Raw user input text.
        domain (str): Resolved dataset domain identifier.
        data (list): Structured dataset for the selected domain and month.

    Returns:
        dict | None:
            - A structured result object describing the resolved operation.
            - None if no valid operation can be determined.

    Error handling:
        - Returns explicit error result types for unsupported fields,
          missing players, invalid metrics, or ambiguous queries.
        - Ensures deterministic behavior with no partial execution.

    This function embodies the expert-system logic of AR STATS BOT and is
    central to its analytical correctness and reliability.
    """

    # Defensive guard
    if not data or not isinstance(data, list):
        return None

    text_lower = text.lower()

    # intent flags
    is_lowest = any(k in text_lower for k in ("lowest", "least", "minimum", "min"))
    is_highest = (("top" in text_lower) or ("most" in text_lower)) and not is_lowest
    non_zero_only = detect_non_zero(text_lower)
    top_n = detect_top_n(text_lower)

    metric = detect_metric(text)
    player = detect_player_name(text, data)

    # METRIC VALIDATION
    if metric:
        allowed = DOMAIN_ALLOWED_FIELDS.get(domain, set())
        if metric not in allowed:
            return {
                "type": "ERROR_FIELD_NOT_SUPPORTED",
                "field": metric,
                "allowed": sorted(allowed)
            }

        # numeric safety check
        for row in data:
            val = row.get(metric, 0)
            if val in (None, ""):
                continue
            try:
                int(val)
            except (TypeError, ValueError):
                return {
                    "type": "ERROR_UNSUPPORTED_METRIC",
                    "allowed": sorted(SUPPORTED_METRICS)
                }
            break

    # PLAYER METRIC (ABSOLUTE PRIORITY)
    if player and metric:
        row = next(r for r in data if r.get("name") == player)
        return {
            "type": "PLAYER_METRIC",
            "player": player,
            "metric": metric,
            "value": int(row.get(metric, 0))
        }

    if "status" in text_lower and domain != "CLAN_MEMBERS":
        return {
            "type": "ERROR_FIELD_NOT_SUPPORTED",
            "field": "status",
            "allowed": sorted(DOMAIN_ALLOWED_FIELDS.get(domain, []))
        }

    if "most" in text_lower and not metric:
        return {
            "type": "ERROR_UNSUPPORTED_METRIC",
            "allowed": sorted(SUPPORTED_METRICS)
        }

    if player and metric:
        row = next(r for r in data if r.get("name") == player)
        return {
            "type": "PLAYER_METRIC",
            "player": player,
            "metric": metric,
            "value": int(row.get(metric, 0))
        }

    # LIST NAMES
    if "list" in text_lower:
        return {
            "type": "LIST_NAMES",
            "domain": domain,
            "names": [row.get("name") for row in data]
        }

    # PLAYER INTENT GUARARD
    if metric and " of " in text_lower and not player:
        return {
            "type": "ERROR_PLAYER_NOT_FOUND",
            "players": [row.get("name") for row in data]
        }

    # COMPARE TWO PLAYERS
    if "compare" in text_lower:
        players = detect_two_players(text, data)

        if not players:
            return {
                "type": "ERROR_COMPARE_PLAYERS_NOT_FOUND",
                "players": [row.get("name") for row in data]
            }

        p1, p2 = players

        row1 = next(r for r in data if r.get("name") == p1)
        row2 = next(r for r in data if r.get("name") == p2)

        # numeric metrics only
        metrics = DOMAIN_ALLOWED_FIELDS.get(domain, set()) - {"status"}

        comparison = {}
        for m in metrics:
            try:
                v1 = int(row1.get(m, 0))
                v2 = int(row2.get(m, 0))
            except (TypeError, ValueError):
                continue

            comparison[m] = {
                p1: v1,
                p2: v2
            }

        result = {
            "type": "COMPARE_PLAYERS",
            "players": players,
            "metrics": comparison
        }

        # include status only for clan members
        if domain == "CLAN_MEMBERS":
            result["status"] = {
                p1: row1.get("status"),
                p2: row2.get("status")
            }

        return result

    # TOTAL OF METRIC
    if metric and detect_total(text_lower):
        total = 0
        count = 0

        for row in data:
            try:
                v = int(row.get(metric, 0))
            except (TypeError, ValueError):
                continue

            total += v
            count += 1

        if count == 0:
            return {
                "type": "ERROR_NO_DATA_FOR_TOTAL",
                "metric": metric
            }

        return {
            "type": "TOTAL_METRIC",
            "metric": metric,
            "total": total,
            "count": count
        }

    # AVERAGE OF METRIC
    if metric and detect_average(text_lower):
        values = []
        for row in data:
            try:
                v = int(row.get(metric, 0))
            except (TypeError, ValueError):
                continue
            values.append(v)

        if not values:
            return {
                "type": "ERROR_NO_DATA_FOR_AVERAGE",
                "metric": metric
            }

        avg = sum(values) / len(values)

        return {
            "type": "AVERAGE_METRIC",
            "metric": metric,
            "average": round(avg, 2),
            "count": len(values)
        }

    # METRIC-BASED OPERATIONS
    if metric:
        values = []
        for row in data:
            try:
                v = int(row.get(metric, 0))
            except (TypeError, ValueError):
                continue

            if non_zero_only and v == 0:
                continue

            values.append(v)

        if not values:
            if non_zero_only:
                return {
                    "type": "ERROR_NO_NON_ZERO_VALUES",
                    "metric": metric
                }
            return None

        unique_values = sorted(
            set(values),
            reverse=is_highest
        )

        # GROUP BY VALUE (STAND-ALONE)
        if detect_group_by(text_lower) and not top_n:
            groups = {}
            for row in data:
                try:
                    v = int(row.get(metric, 0))
                except (TypeError, ValueError):
                    continue

                if non_zero_only and v == 0:
                    continue

                groups.setdefault(v, []).append(row.get("name"))

            if not groups:
                if non_zero_only:
                    return {
                        "type": "ERROR_NO_NON_ZERO_VALUES",
                        "metric": metric
                    }
                return None

            return {
                "type": "GROUP_BY_VALUE",
                "metric": metric,
                "groups": dict(sorted(groups.items()))
            }

        # TOP N (WITH TIES)
        if top_n:
            selected = unique_values[:top_n]

            groups = {
                v: [
                    row.get("name")
                    for row in data
                    if int(row.get(metric, 0)) == v
                ]
                for v in selected
            }

            return {
                "type": "TOP_N_METRIC",
                "metric": metric,
                "mode": "lowest" if is_lowest else "highest",
                "limit": top_n,
                "groups": groups
            }

        # SINGLE HIGHEST / LOWEST
        extreme = unique_values[0]
        names = [
            row.get("name")
            for row in data
            if int(row.get(metric, 0)) == extreme
        ]

        return {
            "type": "LEAST_OF_METRIC" if is_lowest else "MOST_OF_METRIC",
            "metric": metric,
            "names": names,
            "value": extreme
        }

    # MEMBERSHIP / EXISTENCE CHECK
    if detect_membership_query(text_lower) and player:
        exists = any(
            row.get("name") == player
            for row in data
        )

        return {
            "type": "PLAYER_MEMBERSHIP_CHECK",
            "player": player,
            "domain": domain,
            "exists": exists
        }

    # PLAYER-SPECIFIC QUERIES
    if player is None and (
        "status" in text_lower
        or "display" in text_lower
        or ("of" in text_lower and metric)
    ):
        return {
            "type": "ERROR_PLAYER_NOT_FOUND",
            "players": [row.get("name") for row in data]
        }

    if domain == "CLAN_MEMBERS" and "status" in text_lower and player:
        row = next(r for r in data if r.get("name") == player)
        return {
            "type": "PLAYER_STATUS",
            "player": player,
            "status": row.get("status")
        }

    if player and ("display" in text_lower or "show" in text_lower):
        row = next(r for r in data if r.get("name") == player)
        return {
            "type": "PLAYER_FULL_DATA",
            "player": player,
            "data": row
        }

    # FALLBACK
    return {
        "type": "ERROR_UNCLEAR_OPERATION"
    }