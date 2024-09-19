import requests
import streamlit as st
from requests.exceptions import HTTPError
@st.cache_data(ttl=600)   
def get_puuid(gamename: str, tagline:str, api_key:str) -> str:
    """
    Retrieve the PUUID (Player Universally Unique IDentifier) of a Riot Games player.

    This function makes a request to the Riot Games API to fetch the PUUID
    of a player based on their game name and tagline.

    Args:
        gamename (str): The player's in-game name.
        tagline (str): The player's tagline (usually an alphanumeric code after a #).
        api_key (str): The Riot Games API key for authentication.

    Returns:
        str: The player's PUUID.

    Raises:
        HTTPError: If the API request fails, raises an error with the status code
                   and reason for the failure.

    Example:
        >>> api_key = "RGAPI-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
        >>> puuid = get_puuid("PlayerName", "NA1", api_key)
        >>> print(puuid)
        abcdef12-3456-7890-abcd-ef1234567890
    """
    headers = {"X-Riot-Token": api_key}
    url_puuid = f"https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{gamename}/{tagline}"
    r = requests.get(url_puuid, headers=headers)
    if r.status_code == 200:
        return r.json().get("puuid")
    else:
        raise HTTPError(f"Erro HTTP {r.status_code}: {r.reason}")
        
@st.cache_data(ttl=600)     
def get_matchids(puuid: str, api_key:str, length:int= 10) -> list:
    """
    Retrieve a list of match IDs for a player's recent ranked games.

    This function queries the Riot Games API to fetch the most recent ranked match IDs
    for a player, identified by their PUUID.

    Args:
        puuid (str): The Player Universally Unique IDentifier (PUUID) of the player.
        api_key (str): The Riot Games API key for authentication.
        length (int, optional): The number of match IDs to retrieve. Defaults to 10.

    Returns:
        list: A list of match IDs as strings.

    Raises:
        HTTPError: If the API request fails, raises an error with the status code
                   and reason for the failure.

    Example:
        >>> api_key = "RGAPI-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
        >>> puuid = "abcdef12-3456-7890-abcd-ef1234567890"
        >>> match_ids = get_matchids(puuid, api_key, length=5)
        >>> print(match_ids)
        ['NA1_4321098', 'NA1_4321097', 'NA1_4321096', 'NA1_4321095', 'NA1_4321094']
    """
    headers = {"X-Riot-Token": api_key}
    params = {
        "start":0,
        "count":length,
        "type":"ranked"
        }
    url_matchids = f"https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids"
    
    r = requests.get(url_matchids, headers=headers, params=params)
    
    if r.status_code == 200:
        return r.json()
    
    else:
        raise HTTPError(f"Erro HTTP {r.status_code}: {r.reason}")
        
@st.cache_data(ttl=600)     
def get_match_timeline(matchid: str, api_key:str) -> str:
    """
    Retrieve the timeline data for a specific League of Legends match.

    This function makes a request to the Riot Games API to fetch detailed timeline
    information for a given match, identified by its match ID.

    Args:
        matchid (str): The unique identifier for the match.
        api_key (str): The Riot Games API key for authentication.

    Returns:
        dict: A dictionary containing the match timeline data. This typically includes
              information about events, participant positions, and other time-based
              data throughout the course of the match.

    Raises:
        HTTPError: If the API request fails, raises an error with the status code
                   and reason for the failure.

    Example:
        >>> api_key = "RGAPI-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
        >>> matchid = "NA1_4321098"
        >>> timeline_data = get_match_timeline(matchid, api_key)
        >>> print(timeline_data['info']['frames'][0]['timestamp'])
        60000
    """
    headers = {"X-Riot-Token": api_key}
    url_timeline = f"https://americas.api.riotgames.com/lol/match/v5/matches/{matchid}/timeline"
    r = requests.get(url_timeline, headers=headers)
    if r.status_code == 200:
        return r.json()
    else:
        raise HTTPError(f"Erro HTTP {r.status_code}: {r.reason}")