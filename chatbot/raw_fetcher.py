# chatbot/raw_fetcher.py

"""
This module is responsible for retrieving structured clan data from
GitHub-hosted JSON files using raw content URLs.

Its primary role is to abstract away all details related to:
- Constructing correct dataset URLs
- Verifying dataset availability
- Fetching JSON content safely
- Caching network requests for efficiency

By isolating data access logic in this module, the chatbot ensures that
all network interaction is centralized, predictable, and optimized for
low-resource environments.

This module does not interpret or modify the data it fetches. It simply
retrieves raw structured content for downstream processing.
"""

# Importing Libraries
import requests
from functools import lru_cache

# Base RAW GitHub URL
RAW_BASE = (
    "https://raw.githubusercontent.com/"
    "Lightning-President-9/ClanDataRepo/"
    "refs/heads/main"
)

# Domain → path mapping
DOMAIN_PATHS = {
    "CLAN_MEMBERS": "Clan%20Members/JSON",
    "CLAN_MONTHLY_ANALYSIS": "Clan%20Members/Monthly%20Analysis%20JSON",
    "FORMER_CLAN_MEMBERS": "Former%20Clan%20Members/JSON",
    "TOP_CLAN_CONTRIBUTORS": "Top%20Clan%20Contributors/JSON",
}


def _build_filename(domain: str, month_value: str) -> str:
    """
    Constructs the dataset filename based on domain and time context.

    This function applies domain-specific naming conventions to determine
    the correct JSON filename. Monthly analysis datasets use a prefixed
    naming scheme, while all other datasets use the normalized month value
    directly.

    Parameters:
        domain (str): Dataset domain identifier.
        month_value (str): Normalized month or month-range identifier.

    Returns:
        str:
            The expected JSON filename for the requested dataset.
    """

    if domain == "CLAN_MONTHLY_ANALYSIS":
        # data_APR-MAY_2025.json
        return f"data_{month_value}.json"

    # All others: APR_2025.json
    return f"{month_value}.json"


def build_raw_url(domain: str, month_value: str) -> str | None:
    """
    Builds the full GitHub raw URL for a dataset.

    This function combines the base repository URL, domain-specific path,
    and constructed filename to produce a complete URL that can be used
    to fetch the dataset.

    Parameters:
        domain (str): Dataset domain identifier.
        month_value (str): Normalized month or month-range identifier.

    Returns:
        str | None:
            - The full raw GitHub URL for the dataset if the domain is valid.
            - None if the domain is not recognized.
    """

    path = DOMAIN_PATHS.get(domain)
    if not path:
        return None

    filename = _build_filename(domain, month_value)
    return f"{RAW_BASE}/{path}/{filename}"


@lru_cache(maxsize=128)
def raw_file_exists(url: str) -> bool:
    """
    Checks whether a dataset file exists at the given URL.

    This function performs an HTTP HEAD request to verify file existence
    without downloading the full content. Results are cached to minimize
    repeated network calls.

    Parameters:
        url (str): Raw GitHub URL of the dataset.

    Returns:
        bool:
            True if the file exists and is accessible, False otherwise.

    Caching:
        Results are cached using an LRU cache to improve performance and
        reduce network overhead.
    """

    try:
        response = requests.head(url, timeout=3)
        return response.status_code == 200
    except requests.RequestException:
        return False

@lru_cache(maxsize=64)
def _fetch_json(url: str) -> list | None:
    """
    Fetches and parses JSON content from a raw GitHub URL.

    This function performs an HTTP GET request and parses the response as
    JSON. Results are cached to avoid repeated downloads of the same file.

    Parameters:
        url (str): Raw GitHub URL of the dataset.

    Returns:
        list | None:
            - Parsed JSON content as a list if successful.
            - None if the request fails or the content cannot be parsed.

    Caching:
        Uses an LRU cache to store recently fetched datasets.
    """

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        return None


def fetch_json_if_exists(domain: str, month_value: str) -> list | None:
    """
    Safely retrieves a dataset if it exists.

    This function serves as the public interface for data retrieval. It
    first constructs the expected dataset URL, verifies its existence,
    and then fetches and returns the parsed JSON content.

    If the dataset does not exist or cannot be accessed, the function
    returns None without raising exceptions.

    Parameters:
        domain (str): Dataset domain identifier.
        month_value (str): Normalized month or month-range identifier.

    Returns:
        list | None:
            - Parsed JSON dataset if available.
            - None if the dataset does not exist or cannot be retrieved.

    This defensive approach ensures that missing data is handled
    gracefully by higher-level components of the chatbot.
    """

    url = build_raw_url(domain, month_value)
    if not url:
        return None

    if not raw_file_exists(url):
        return None

    return _fetch_json(url)