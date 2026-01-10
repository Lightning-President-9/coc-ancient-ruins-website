# chatbot/chat_controller.py

"""
This module acts as the central orchestration layer of the chatbot system.
It is responsible for receiving raw user input, interpreting intent,
coordinating data access, invoking analytical operations, and returning
a structured response suitable for UI or API consumption.

The controller does not perform analytics itself. Instead, it coordinates
specialized modules for classification, normalization, routing, data
retrieval, operation resolution, and response formatting. This design
keeps the chatbot deterministic, modular, and easy to reason about.

The module also handles all static and informational queries such as:
- greetings and help
- bot identity and capabilities
- metric explanations
- polite conversational responses

In the overall architecture of Ancient Ruins STATS BOT, this file serves as the
single entry point for all chatbot interactions.
"""

# Importing Libraries
from chatbot.month_normalizer import normalize_month
from chatbot.domain_router import route_domain
from chatbot.raw_fetcher import fetch_json_if_exists, build_raw_url
from chatbot.operation_resolver import resolve_operation
from chatbot.response_builder import build_response
from chatbot.input_classifier import classify_input
from chatbot.almost_hint import suggest_month

# STATIC METRIC EXPLANATIONS
METRIC_EXPLANATIONS = {
    "warattack": "Total war attacks performed by a player in the given month.",
    "clanscore": "Overall contribution score representing player performance.",
    "clangamesmaxed": "Whether the player fully completed Clan Games.",
    "clangames": "Points contributed by the player in Clan Games.",
    "clancapital": "Contribution made by the player to Clan Capital raids."
}

def build_suggestions(op_type: str, domain: str, month_value: str) -> list[str]:
    """
        Builds a contextual list of follow-up query suggestions.

        This function generates meaningful next-step questions based on the
        type of operation that was just executed. The goal is to guide users
        toward valid and relevant queries without overwhelming them.

        Suggestions are:
        - Operation-aware (based on op_type)
        - Month-specific (derived from month_value)
        - Domain-safe (only valid for the resolved dataset)

        Parameters:
            op_type (str): The resolved operation type returned by the
                           operation resolver.
            domain (str): The dataset domain used for the current query.
            month_value (str): Normalized month or month-range value.

        Returns:
            list[str]:
                A list of suggested follow-up questions that the user can
                immediately ask next.
        """

    m = month_value.replace("_", " ")

    if op_type == "PLAYER_METRIC":
        return [
            f"display data of this player in {m}",
            f"compare this player vs another in {m}",
            f"what is the average clanscore in {m}"
        ]

    if op_type in {"MOST_OF_METRIC", "LEAST_OF_METRIC"}:
        return [
            f"top 5 clanscore in {m}",
            f"lowest non-zero warattack in {m}",
            f"group clanscore in {m}"
        ]

    if op_type == "TOP_N_METRIC":
        return [
            f"top 3 lowest clanscore in {m}",
            f"group warattack in {m}",
            f"what is the average warattack in {m}"
        ]

    if op_type == "GROUP_BY_VALUE":
        return [
            f"top 5 warattack in {m}",
            f"lowest non-zero warattack in {m}",
            f"total warattack in {m}"
        ]

    if op_type == "COMPARE_PLAYERS":
        return [
            f"what is the average clanscore in {m}",
            f"top 5 clanscore in {m}",
            f"display data of one of these players in {m}"
        ]

    if op_type in {"AVERAGE_METRIC", "TOTAL_METRIC"}:
        return [
            f"top 5 clanscore in {m}",
            f"group clanscore in {m}",
            f"compare two players in {m}"
        ]

    if op_type == "PLAYER_MEMBERSHIP_CHECK":
        return [
            f"display data of this player in {m}",
            f"is this player active in {m}",
            f"compare this player vs another in {m}"
        ]

    # Safe fallback
    return [
        f"list all names in {m}",
        f"top 5 clanscore in {m}",
        f"what is the average warattack in {m}"
    ]

def handle_chat(user_text: str) -> dict:
    """
    Main chatbot entry point.

    This function processes a single user query end-to-end and returns
    a structured response for consumption by a UI or API client.

    High-level responsibilities:
    - Enforce input constraints (length, emptiness)
    - Handle help, greeting, and informational queries
    - Normalize and validate month or month-range expressions
    - Determine the correct data domain to query
    - Fetch structured clan data from GitHub-hosted JSON
    - Resolve the analytical operation requested by the user
    - Convert structured results into a human-readable response
    - Attach source links and contextual follow-up suggestions

    The function is fully deterministic: given the same input and data,
    it will always produce the same output.

    Processing flow:
        1. Validate raw input
        2. Handle static and conversational queries
        3. Normalize month information
        4. Route to the appropriate dataset domain
        5. Fetch dataset for the resolved month
        6. Resolve the requested operation
        7. Build a formatted response
        8. Attach source metadata and suggestions

    Parameters:
        user_text (str): Raw input text provided by the user.

    Returns:
        dict:
            A structured response object with the following keys:
            - reply (str): Human-readable chatbot response
            - source (str | None): GitHub raw URL of the dataset used
            - suggestions (list[str]): Contextual follow-up questions

    Error handling:
        - Gracefully handles invalid input, missing data, unsupported
          operations, and ambiguous queries.
        - Provides helpful clarification prompts instead of failing silently.

    This function represents the public conversational interface of
    AR STATS BOT and should be treated as the system’s primary control
    surface.
    """

    if len(user_text) > 500:
        return {
            "reply": "Your message is too long. Please keep it under 500 characters.",
            "source": None,
            "suggestions": []
        }

    text = user_text.strip()
    text_lower = text.lower()

    # EMPTY INPUT
    if not text:
        return {
            "reply": "Please ask a clan-related question.",
            "source": None,
            "suggestions": []
        }

    # HELP COMMAND (MUST BE FIRST)
    if text_lower in {"help", "/help", "commands"}:
        return {
            "reply": (
                "Here’s what I can help you with (Ancient Ruins clan only):\n\n"

                "GENERAL\n"
                "- who are you\n"
                "- what can you do\n"
                "- what metrics can I ask about\n"
                "- what does <metric> mean\n\n"

                "CLAN MEMBERS (monthly)\n"
                "- list all names in APR 2025\n"
                "- display data of KAI HIWATARI in APR 2025\n"
                "- what is the status of Chief in APR 2025\n\n"

                "FORMER CLAN MEMBERS\n"
                "- list all former members in DEC 2024\n"
                "- display data of KING SEENU in APR 2025\n\n"

                "TOP CLAN CONTRIBUTORS\n"
                "- who had most clanscore in APR 2025\n"
                "- is Bennie in top contributors for APR 2025\n\n"

                "RANKINGS & STATS\n"
                "- who had most warattack in APR 2025\n"
                "- who had lowest non-zero warattack in APR 2025\n"
                "- top 10 warattack in APR 2025\n"
                "- top 5 lowest clanscore in APR 2025\n\n"

                "AGGREGATES\n"
                "- what is the average warattack in APR 2025\n"
                "- total clanscore in APR 2025\n\n"

                "GROUPING\n"
                "- group warattack in APR 2025\n"
                "- group non-zero clanscore in APR 2025\n\n"

                "COMPARISONS\n"
                "- compare Chief vs KAI HIWATARI in APR 2025\n"
                "- compare former KING SEENU vs RAVI in DEC 2024\n\n"

                "MEMBERSHIP CHECKS\n"
                "- is Chief a clan member in APR 2025\n"
                "- is KING SEENU a former member in DEC 2024\n\n"

                "Notes:\n"
                "- All queries are month-based\n"
                "- Rankings handle ties automatically\n"
                "- Top N refers to top N values, not players\n"
                "- I only answer questions about the Ancient Ruins clan"
            ),
            "source": None,
            "suggestions": []
        }

    # INPUT CLASSIFICATION
    category = classify_input(text)

    if category == "GREETING":
        return {
            "reply": (
                "Hello! I am kARsb, Clan Data Assistant for the Ancient Ruins clan.\n\n"
                "I specialize only in Ancient Ruins clan data and can help you with:\n"
                "- Monthly clan member statistics\n"
                "- Performance analysis\n"
                "- Rankings and comparisons\n\n"
                "Type `help` to see example questions."
            ),
            "source": None,
            "suggestions": []
        }

    if category == "GIBBERISH":
        return {
            "reply": (
                "I couldn’t understand your message.\n"
                "Please ask something related to the Ancient Ruins clan "
                "or type `help` to see example questions."
            ),
            "source": None,
            "suggestions": []
        }

    # STATIC / INFORMATIONAL QUERIES

    # Who are you
    if "who are you" in text_lower:
        return {
            "reply": (
                "I am KARSB, Clan Data Assistant for the Ancient Ruins clan.\n\n"
                "I specialize only in Ancient Ruins clan data. "
                "I can help you with monthly stats, performance, and rankings."
            ),
            "source": None,
            "suggestions": []
        }

    # What can you do
    if "what can you do" in text_lower:
        return {
            "reply": (
                "I can help you with:\n"
                "- Clan member statistics by month\n"
                "- Former clan member data\n"
                "- Top clan contributors\n"
                "- Rankings (top, lowest, averages, totals)\n"
                "- Player comparisons\n"
                "- Grouped performance analysis\n\n"
                "All data is specific to the Ancient Ruins clan."
            ),
            "source": None,
            "suggestions": []
        }

    # What metrics can I ask about
    if "what metrics" in text_lower:
        metrics = ", ".join(sorted(METRIC_EXPLANATIONS.keys()))
        return {
            "reply": (
                "You can ask about the following metrics:\n"
                f"{metrics}"
            ),
            "source": None,
            "suggestions": []
        }

    # What does <metric> mean
    if "what does" in text_lower and "mean" in text_lower:
        for metric, explanation in METRIC_EXPLANATIONS.items():
            if metric in text_lower:
                return {
                    "reply": f"**{metric}** means:\n{explanation}",
                    "source": None,
                    "suggestions": []
                }

    # Thanks / Thank you
    if any(k in text_lower for k in ("thanks", "thank you", "thnx")):
        return {
            "reply": "You're welcome! If you need more clan insights, just ask.",
            "source": None,
            "suggestions": []
        }

    # CLAN LOGIC

    # STEP A: Normalize month / range
    month_info = normalize_month(text)
    month_value = month_info.get("value")

    if not month_value:
        hint = suggest_month(text)

        if hint:
            return {
                "reply": (
                    f"I couldn't find an exact match for the date.\n"
                    f"Did you mean **{hint}**?"
                ),
                "source": None,
                "suggestions": []
            }

        return {
            "reply": (
                "Please specify a valid month and year, "
                "e.g. 'APR 2025' or 'APR-MAY 2025'."
            ),
            "source": None,
            "suggestions": []
        }

    # STEP B: Route domain
    domain = route_domain(text, month_info)
    if not domain:
        return {
            "reply": "I could not determine which clan data to use.",
            "source": None,
            "suggestions": []
        }

    # STEP C: Fetch data
    data = fetch_json_if_exists(domain, month_value)
    if data is None:
        return {
            "reply": f"No data available for {month_value.replace('_', ' ')}.",
            "source": None,
            "suggestions": []
        }

    # STEP D: Resolve operation
    operation_result = resolve_operation(text, domain, data)
    if not operation_result:
        return {
            "reply": "I could not understand the requested operation.",
            "source": None,
            "suggestions": []
        }

    # STEP E: Build response
    reply_text = build_response(operation_result, month_value)

    source_url = build_raw_url(domain, month_value)

    suggestions = build_suggestions(
        operation_result.get("type"),
        domain,
        month_value
    )

    return {
        "reply": reply_text,
        "source": source_url,
        "suggestions": suggestions
    }