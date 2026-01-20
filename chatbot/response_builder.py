# chatbot/response_builder.py

"""
This module is responsible for converting structured operation results
(produced by the operation_resolver) into clean, human-readable text
responses suitable for display in the chat UI or export to PDF.

It acts as the final presentation layer of the chatbot pipeline and
contains no business logic or data computation. All inputs to this
module are assumed to be validated and structured beforehand.

Key responsibilities:
- Safely formatting player names and values
- Generating consistent, readable output for each operation type
- Handling ties, groupings, aggregates, and comparisons
- Producing clear error and guidance messages when needed
"""

def _safe_names(names: list) -> list[str]:
    """
    Normalize and sanitize a list of names for display.

    This helper function ensures that all player names included in
    responses are safe to print and visually consistent.

    It:
    - Converts all values to strings
    - Removes None values
    - Filters out empty or whitespace-only entries

    Parameters:
        names (list):
            Raw list of names extracted from dataset rows.

    Returns:
        list[str]:
            Cleaned list of printable player names.
    """

    return [str(n) for n in names if n is not None and str(n).strip()]


def build_response(result: dict, month_value: str) -> str:
    """
    Convert a structured operation result into a readable response string.

    This function inspects the operation `type` field and formats the
    response accordingly. Each supported operation type has a dedicated
    formatting block to ensure clarity and consistency.

    The function does not modify or compute data; it only formats the
    result provided by the resolver.

    Parameters:
        result (dict):
            Structured output from the operation_resolver module,
            containing operation type and associated data.
        month_value (str):
            Normalized month identifier (e.g., "APR_2025", "APR-MAY_2025").

    Returns:
        str:
            A human-readable response ready for display in the UI.

    Behavior by operation type:
    - LIST_NAMES:
        Lists clan members, former members, or top contributors.
    - MOST_OF_METRIC / LEAST_OF_METRIC:
        Displays highest or lowest metric values with tie handling.
    - TOP_N_METRIC:
        Displays top N metric values grouped by value.
    - GROUP_BY_VALUE:
        Groups players by exact metric value.
    - PLAYER_METRIC:
        Shows a single player's metric for the given month.
    - PLAYER_STATUS:
        Displays clan membership status.
    - PLAYER_FULL_DATA:
        Outputs all available fields for a player in key-value format.
    - COMPARE_PLAYERS:
        Side-by-side numeric comparison of two players.
    - AVERAGE_METRIC / TOTAL_METRIC:
        Displays aggregate statistics with player counts.
    - PLAYER_MEMBERSHIP_CHECK:
        Confirms whether a player exists in a given dataset.
    - ERROR_*:
        Returns informative, user-friendly error messages.

    Design notes:
    - All formatting is text-based and deterministic.
    - No HTML or UI logic is included.
    - Output is optimized for chat display and PDF export.
    - Tie cases are handled explicitly to avoid misleading rankings.
    """

    if not result:
        return "I could not understand the request or the data is unavailable."

    rtype = result.get("type")
    month_readable = month_value.replace("_", " ")

    # LIST NAMES
    if rtype == "LIST_NAMES":
        names = _safe_names(result.get("names", []))
        domain = result.get("domain")

        if not names:
            return f"No data found for {month_readable}."

        if domain == "FORMER_CLAN_MEMBERS":
            title = f"Former clan members for {month_readable}"
        elif domain == "TOP_CLAN_CONTRIBUTORS":
            title = f"Top clan contributors for {month_readable}"
        else:
            title = f"Clan members for {month_readable}"

        return title + ":\n" + ", ".join(names)

    # TOTAL METRIC
    if rtype == "TOTAL_METRIC":
        metric = result["metric"]
        total = result["total"]
        count = result["count"]

        return (
            f"The total {metric} done by the clan in {month_readable} "
            f"was {total}, across {count} players."
        )

    # MOST OF METRIC
    if rtype == "MOST_OF_METRIC":
        metric = result["metric"]
        value = result["value"]
        names = _safe_names(result["names"])

        return (
            f"In {month_readable}, the highest {metric} was {value}, "
            f"achieved by: {', '.join(names)}."
        )

    # LEAST OF METRIC
    if rtype == "LEAST_OF_METRIC":
        metric = result["metric"]
        value = result["value"]
        names = _safe_names(result["names"])

        return (
            f"In {month_readable}, the lowest {metric} was {value}, "
            f"recorded by: {', '.join(names)}."
        )

    # COMPARE PLAYERS
    if rtype == "COMPARE_PLAYERS":
        players = result["players"]
        metrics = result["metrics"]

        lines = [
            f"Comparison for {players[0]} vs {players[1]} in {month_readable}:"
        ]

        for metric, values in metrics.items():
            lines.append(
                f"{metric:<14}: "
                f"{players[0]} = {values[players[0]]}, "
                f"{players[1]} = {values[players[1]]}"
            )

        if "status" in result:
            status = result["status"]
            lines.append(
                f"status         : "
                f"{players[0]} = {status.get(players[0])}, "
                f"{players[1]} = {status.get(players[1])}"
            )

        return "\n".join(lines)

    # TOP N METRIC
    if rtype == "TOP_N_METRIC":
        metric = result["metric"]
        limit = result["limit"]
        mode = result["mode"]
        groups = result["groups"]

        lines = [
            f"Top {limit} {mode} {metric} in {month_readable}:"
        ]

        for value in sorted(groups.keys(), reverse=(mode == "highest")):
            names = _safe_names(groups[value])
            lines.append(f"{value}: {', '.join(names)}")

        return "\n".join(lines)

    # GROUP BY VALUE
    if rtype == "GROUP_BY_VALUE":
        metric = result["metric"]
        groups = result["groups"]

        lines = [
            f"{metric.capitalize()} grouped by value in {month_readable}:"
        ]

        for value, names in groups.items():
            safe = _safe_names(names)
            lines.append(f"{value}: {', '.join(safe)}")

        return "\n".join(lines)

    # PLAYER STATUS
    if rtype == "PLAYER_STATUS":
        return (
            f"{result['player']}'s status in {month_readable} "
            f"was {result['status']}."
        )

    # PLAYER METRIC
    if rtype == "PLAYER_METRIC":
        return (
            f"{result['player']}'s {result['metric']} in {month_readable} "
            f"was {result['value']}."
        )

    # PLAYER FULL DATA
    if rtype == "PLAYER_FULL_DATA":
        data = result["data"]
        lines = []

        for key in sorted(data.keys()):
            lines.append(f"{key:<14}: {data[key]}")

        return "\n".join(lines)

    # AVERAGE METRIC
    if rtype == "AVERAGE_METRIC":
        metric = result["metric"]
        avg = result["average"]
        count = result["count"]

        return (
            f"The average {metric} in {month_readable} "
            f"was {avg} based on {count} players."
        )

    # PLAYER MEMBERSHIP CHECK
    if rtype == "PLAYER_MEMBERSHIP_CHECK":
        player = result["player"]
        domain = result["domain"]
        exists = result["exists"]

        domain_label = {
            "CLAN_MEMBERS": "a clan member",
            "FORMER_CLAN_MEMBERS": "a former member",
            "TOP_CLAN_CONTRIBUTORS": "in top contributors"
        }.get(domain, "present")

        if exists:
            return (
                f"Yes, {player} was {domain_label} "
                f"in {month_readable}."
            )
        else:
            return (
                f"No, {player} was not {domain_label} "
                f"in {month_readable}."
            )

    # ERRORS
    if rtype == "ERROR_UNSUPPORTED_METRIC":
        metrics = ", ".join(result["allowed"])
        return (
            "I could not identify the metric you requested. "
            f"Supported metrics are: {metrics}."
        )

    if rtype == "ERROR_FIELD_NOT_SUPPORTED":
        field = result["field"]
        allowed = ", ".join(result["allowed"])
        return (
            f"The field '{field}' is not available for this dataset. "
            f"Supported fields are: {allowed}."
        )

    if rtype == "ERROR_PLAYER_NOT_FOUND":
        players = _safe_names(result["players"])
        return (
            "I could not find that player for this month. "
            f"Available players are: {', '.join(players)}."
        )

    if rtype == "ERROR_NO_NON_ZERO_VALUES":
        return (
            f"All values for {result['metric']} are zero in {month_readable}. "
            "No non-zero data is available."
        )

    if rtype == "ERROR_UNCLEAR_OPERATION":
        return (
            "I could not understand the requested operation.\n"
            "Try questions like:\n"
            "- list all names in APR 2025\n"
            "- top 5 warattack in APR 2025\n"
            "- lowest non-zero clanscore in APR 2025\n"
            "- group warattack in APR 2025"
        )

    if rtype == "ERROR_COMPARE_PLAYERS_NOT_FOUND":
        players = ", ".join(result["players"])
        return (
            "I could not find exactly two players to compare for this month.\n"
            f"Available players are: {players}."
        )

    if rtype == "ERROR_NO_DATA_FOR_AVERAGE":
        return (
            f"No valid data available to calculate the average "
            f"for {result['metric']} in {month_readable}."
        )

    if rtype == "ERROR_NO_DATA_FOR_TOTAL":
        return (
            f"No valid data available to calculate the total "
            f"for {result['metric']} in {month_readable}."
        )

    return "I could not process the request."