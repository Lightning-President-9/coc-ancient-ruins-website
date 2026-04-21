"""
Clash of Clans API Data Collector
--------------------------------
This module fetches clan- and player-related coc-data from the
Clash of Clans API and stores responses as JSON files.

Features:
- Clan search by name
- Clan details by tag
- Clan members list
- Capital raid seasons
- Current war league group
- Individual player profiles (saved using player names)

All coc-data is saved under the `coc-data/` directory.
"""

import requests
import json
import os
import urllib.parse
import time
import re
from datetime import datetime

from dotenv import load_dotenv

load_dotenv()  # This loads the variables from .env into os.environ

# CONFIGURATION
API_KEY = os.environ.get("COC_API_KEY")
BASE_URL = "https://api.clashofclans.com/v1"

DATA_DIR = "coc-data"
PLAYER_DIR = os.path.join(DATA_DIR, "clan_players")

# API REQUEST HANDLER
def make_get_request(endpoint, params=None):
    """
    Sends a GET request to the Clash of Clans API.

    Args:
        endpoint (str): API endpoint (e.g. '/clans/{tag}')
        params (dict, optional): Query parameters

    Returns:
        dict: Parsed JSON response
    """
    headers = {"Authorization": f"Bearer {API_KEY}", "Accept": "application/json"}

    url = f"{BASE_URL}{endpoint}"
    response = requests.get(url, headers=headers, params=params, timeout=15)

    if response.status_code != 200:
        print("API Error")
        print("Status Code:", response.status_code)
        print("Response:", response.text)

    response.raise_for_status()
    return response.json()

def format_clash_date(ts: str) -> str:
    dt = datetime.strptime(ts, "%Y%m%dT%H%M%S.%fZ")
    return f"{dt.strftime('%b')} {dt.day}, {dt.year}"

# JSON STORAGE UTIL
def save_json(data, filepath):
    """
    Saves JSON coc-data to disk.

    Args:
        data (dict): JSON serializable coc-data
        filepath (str): Full file path
    """
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# CLAN-LEVEL FUNCTIONS
def search_clan_by_name(clan_name):
    """
    Searches clans by name.

    Equivalent to:
    curl -H "Authorization: Bearer API_KEY"
    https://api.clashofclans.com/v1/clans?name=Ancient%20Ruins
    """
    data = make_get_request("/clans", {"name": clan_name})
    save_json(data, os.path.join(DATA_DIR, "clans_search.json"))
    return data

def get_clan_by_tag(clan_tag):
    """
    Fetches clan details using clan tag.
    """
    encoded_tag = urllib.parse.quote(clan_tag)
    data = make_get_request(f"/clans/{encoded_tag}")
    save_json(data, os.path.join(DATA_DIR, "clan_details.json"))
    return data

def get_capital_raid_seasons(clan_tag):
    """
    Fetches capital raid season coc-data and formats dates.
    """
    encoded_tag = urllib.parse.quote(clan_tag)
    data = make_get_request(f"/clans/{encoded_tag}/capitalraidseasons")

    for item in data.get("items", []):
        if "startTime" in item:
            item["startTime"] = format_clash_date(item["startTime"])
        if "endTime" in item:
            item["endTime"] = format_clash_date(item["endTime"])

    save_json(data, os.path.join(DATA_DIR, "capital_raid_seasons.json"))
    return data

def get_current_war_league_group(clan_tag):
    """
    Fetches current CWL league group (if active).
    """
    encoded_tag = urllib.parse.quote(clan_tag)
    data = make_get_request(f"/clans/{encoded_tag}/currentwar/leaguegroup")
    save_json(data, os.path.join(DATA_DIR, "current_war_league_group.json"))
    return data

# PLAYER-LEVEL FUNCTIONS
def safe_filename(name):
    """
    Converts player name into a filesystem-safe filename.

    Example:
    'KAI HIWATARI' -> 'KAI_HIWATARI.json'
    """
    name = name.strip().replace(" ", "_")
    name = re.sub(r"[^A-Za-z0-9_]", "", name)
    return f"{name}.json"

def get_player_by_tag(player_tag, player_name):
    """
    Fetches a single player's full profile
    and saves it using the player's name.
    """
    encoded_tag = urllib.parse.quote(player_tag)
    data = make_get_request(f"/players/{encoded_tag}")

    filename = safe_filename(player_name)
    filepath = os.path.join(PLAYER_DIR, filename)
    save_json(data, filepath)

def fetch_all_clan_players(clan_tag):
    """
    Fetch clan members directly from API,
    clear old player files,
    then download fresh player profiles.
    """

    encoded_tag = urllib.parse.quote(clan_tag)

    # Fetch members from API
    members_data = make_get_request(f"/clans/{encoded_tag}/members")

    # Save members list (optional)
    save_json(members_data, os.path.join(DATA_DIR, "clan_members.json"))

    players = members_data.get("items", [])

    # CLEAR OLD PLAYER FILES
    if os.path.exists(PLAYER_DIR):
        for file in os.listdir(PLAYER_DIR):
            file_path = os.path.join(PLAYER_DIR, file)

            if os.path.isfile(file_path):
                os.remove(file_path)

    else:
        os.makedirs(PLAYER_DIR)

    print("Old player files cleared")

    # FETCH NEW PLAYER DATA
    print(f"Fetching data for {len(players)} players")

    for idx, player in enumerate(players, start=1):

        print(f"[{idx}/{len(players)}] {player['name']}")

        get_player_by_tag(player["tag"], player["name"])

        time.sleep(0.25)

    print("All player data updated")

def get_clan_warlog(clan_tag):
    """
    Fetches full clan war log history.

    Endpoint:
    /clans/{tag}/warlog
    """
    encoded_tag = urllib.parse.quote(clan_tag)
    data = make_get_request(f"/clans/{encoded_tag}/warlog")

    for item in data.get("items", []):
        if "endTime" in item:
            item["endTime"] = format_clash_date(item["endTime"])

    save_json(data, os.path.join(DATA_DIR, "warlog.json"))
    return data

# MAIN EXECUTION
def main():
    """
    Main pipeline execution.
    """
    clan_tag = "#2PPOP22CQ"

    search_clan_by_name("Ancient Ruins")
    get_clan_by_tag(clan_tag)
    get_capital_raid_seasons(clan_tag)
    get_clan_warlog(clan_tag)

    # league_data = get_current_war_league_group(clan_tag)
    fetch_all_clan_players(clan_tag)

    print("Data collection completed")

    # if "clans" in league_data:
    #     print("CWL clans:", len(league_data["clans"]))

if __name__ == "__main__":
    main()