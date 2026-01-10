# chatbot/almost_hint.py

"""
This module exists to improve the usability of the chatbot when user input
is incomplete, informal, or slightly ambiguous.

Instead of immediately rejecting such input, this module provides
deterministic suggestions that help guide the user toward a valid query.

It is intentionally lightweight and rule-based, using simple string checks
and regular expressions. The module does not alter user input automatically;
it only offers suggestions when there is exactly one clear interpretation.

This module is primarily used as a fallback mechanism by the chat controller
when exact month or player resolution fails.
"""

# Importing Libraries
import re

MONTHS = {
    "jan": "JAN",
    "feb": "FEB",
    "mar": "MAR",
    "apr": "APR",
    "may": "MAY",
    "jun": "JUN",
    "jul": "JUL",
    "aug": "AUG",
    "sep": "SEP",
    "oct": "OCT",
    "nov": "NOV",
    "dec": "DEC",
}


def suggest_month(text: str) -> str | None:
    """
    Attempts to infer a valid month–year combination from informal user input.

    This function supports compact and conversational formats such as:
    - "apr25"
    - "apr 25"
    - "april 2025"

    It uses a regular expression to detect a month name or abbreviation
    followed by a 2-digit or 4-digit year. Two-digit years are normalized
    to four-digit format assuming the 2000s.

    Parameters:
        text (str): Raw user input text.

    Returns:
        str | None:
            - A suggested month string in the format "APR 2025" if a valid
              pattern is detected.
            - None if no recognizable month–year pattern is found.
    """

    t = text.lower()

    m = re.search(
        r"(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\s*(\d{2,4})",
        t
    )
    if m:
        month = MONTHS[m.group(1)]
        year = m.group(2)
        if len(year) == 2:
            year = "20" + year
        return f"{month} {year}"

    return None


def suggest_player(text: str, players: list[str]) -> str | None:
    """
    Suggests a player name based on partial or prefix matching.

    This function compares the user input against a list of known player
    names and attempts to find a single unambiguous match. Suggestions are
    only returned when exactly one player matches to avoid confusion.

    Matching rules:
    - Case-insensitive comparison
    - Matches if the player name starts with the input text
    - Matches if the input text appears anywhere in the player name

    Parameters:
        text (str): Raw user input text.
        players (list[str]): List of valid player names for the dataset.

    Returns:
        str | None:
            - The suggested player name if exactly one match is found.
            - None if no matches or multiple matches are found.
    """

    t = text.lower()
    matches = [
        p for p in players
        if p.lower().startswith(t) or t in p.lower()
    ]

    if len(matches) == 1:
        return matches[0]

    return None