# chatbot/month_normalizer.py

"""
This module is responsible for extracting and normalizing month or
month-range information from raw user input.

User queries often reference time in informal or conversational formats
(e.g., "APR 2025", "April 2025", "APR-MAY 2025"). This module converts such
references into a strict, canonical representation that can be reliably
used to locate dataset files and drive downstream logic.

The normalization process is fully deterministic and rule-based, relying
on regular expressions and predefined month mappings. No assumptions are
made beyond explicit patterns found in the input text.

This module plays a critical role in ensuring consistent data access and
preventing ambiguity when resolving time-based clan queries.
"""

import re

# Canonical month mapping
MONTH_MAP = {
    "jan": "JAN", "january": "JAN",
    "feb": "FEB", "february": "FEB",
    "mar": "MAR", "march": "MAR",
    "apr": "APR", "april": "APR",
    "may": "MAY",
    "jun": "JUN", "june": "JUN",
    "jul": "JUL", "july": "JUL",
    "aug": "AUG", "august": "AUG",
    "sep": "SEP", "sept": "SEP", "september": "SEP",
    "oct": "OCT", "october": "OCT",
    "nov": "NOV", "november": "NOV",
    "dec": "DEC", "december": "DEC",
}

YEAR_PATTERN = r"(20\d{2})"


def extract_single_month(text: str) -> str | None:
    """
    Extracts and normalizes a single month reference from user input.

    This function detects patterns such as:
    - "APR 2025"
    - "April 2025"

    When a valid match is found, the month name is converted to its
    canonical three-letter form and combined with the year using an
    underscore separator.

    Parameters:
        text (str): Raw user input text.

    Returns:
        str | None:
            - A normalized month identifier in the format "APR_2025"
              if a valid single-month reference is found.
            - None if no valid single-month pattern is detected.
    """

    text = text.lower()

    for word, code in MONTH_MAP.items():
        match = re.search(rf"\b{word}\b\s+{YEAR_PATTERN}", text)
        if match:
            year = match.group(1)
            return f"{code}_{year}"

    return None


def extract_month_range(text: str) -> str | None:
    """
    Extracts and normalizes a month-range reference from user input.

    This function detects patterns such as:
    - "APR-MAY 2025"
    - "April May 2025"

    Both months are normalized to their canonical forms and combined with
    a hyphen, followed by the year, to produce a single range identifier.

    Parameters:
        text (str): Raw user input text.

    Returns:
        str | None:
            - A normalized month-range identifier in the format
              "APR-MAY_2025" if a valid range is found.
            - None if no valid month-range pattern is detected.
    """

    text = text.lower()

    for w1, c1 in MONTH_MAP.items():
        for w2, c2 in MONTH_MAP.items():
            pattern = rf"\b{w1}\b[\s\-]+\b{w2}\b\s+{YEAR_PATTERN}"
            match = re.search(pattern, text)
            if match:
                year = match.group(1)
                return f"{c1}-{c2}_{year}"

    return None


def normalize_month(text: str) -> dict:
    """
    Performs unified month normalization for user queries.

    This function serves as the public interface of the module. It attempts
    to extract a month range first, followed by a single month if no range
    is found. This priority avoids ambiguous interpretations.

    The returned structure clearly indicates whether the query refers to a
    single month, a range of months, or no recognizable time reference.

    Parameters:
        text (str): Raw user input text.

    Returns:
        dict:
            A dictionary with the following keys:
            - "type": One of "single", "range", or None
            - "value": Normalized month or month-range identifier, or None

    This normalized output is used throughout the chatbot to route queries,
    fetch datasets, and enforce time-based constraints consistently.
    """

    month_range = extract_month_range(text)
    if month_range:
        return {"type": "range", "value": month_range}

    single = extract_single_month(text)
    if single:
        return {"type": "single", "value": single}

    return {"type": None, "value": None}