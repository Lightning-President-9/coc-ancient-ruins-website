# chatbot/input_classifier.py

"""
This module exists to perform an initial, lightweight classification of
raw user input before deeper parsing and analysis is attempted.

Its purpose is not to fully understand the query, but to quickly identify
simple conversational cases such as greetings, empty input, or nonsensical
text. This allows the chatbot to respond appropriately without invoking
the full data-processing pipeline.

The classification logic is intentionally minimal, deterministic, and
rule-based to keep performance overhead low and behavior predictable.
"""

# Importing Libraries
import re

# Greetings string
GREETINGS = {
    "hi", "hello", "hey",
    "who are you","who are you?", "tell me about yourself"
}

def classify_input(text: str) -> str:
    """
        Classifies raw user input into a high-level category.

        This function performs basic normalization and then applies a small
        set of deterministic rules to categorize the input. The result is
        used by the chat controller to decide how the query should be handled.

        Classification rules:
        - Empty input is classified as EMPTY.
        - Exact matches against known greeting phrases are classified as GREETING.
        - Very short alphabetic strings with no recognizable month references
          are classified as GIBBERISH.
        - All other input is treated as a potential clan-related query.

        Parameters:
            text (str): Raw user input text.

        Returns:
            str:
                One of the following classification labels:
                - "EMPTY": No meaningful input was provided.
                - "GREETING": A recognized greeting or identity query.
                - "GIBBERISH": Likely nonsensical or accidental input.
                - "POSSIBLE_CLAN_QUERY": Input that may contain a valid clan query.

        This early classification step helps improve user experience by
        handling trivial cases quickly and avoiding unnecessary processing.
    """

    text = text.strip().lower()

    if not text:
        return "EMPTY"

    if text in GREETINGS:
        return "GREETING"

    # Gibberish: random short alphabetic strings
    if (
        len(text) <= 8
        and text.isalpha()
        and not re.search(r"(apr|may|jun|jul|aug|sep|oct|nov|dec|jan|feb)", text)
    ):
        return "GIBBERISH"

    return "POSSIBLE_CLAN_QUERY"