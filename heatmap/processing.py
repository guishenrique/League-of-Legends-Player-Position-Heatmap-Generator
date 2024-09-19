

import pandas as pd
import api, preprocessing

def get_user_position(gamename, tagline, api_key):
    """
    Retrieve and process a player's position data from their recent matches.

    This function fetches match data for a given player, processes the timeline
    information, and returns a DataFrame containing the player's normalized
    position coordinates throughout their recent matches.

    Args:
        gamename (str): The player's in-game name.
        tagline (str): The player's tagline (usually an alphanumeric code after a #).
        api_key (str): The Riot Games API key for authentication.

    Returns:
        pd.DataFrame: A DataFrame indexed by matchId and timestamp, containing columns:
            - x: Normalized X-coordinate of the player's position
            - y: Normalized Y-coordinate of the player's position

    Raises:
        HTTPError: If any API request fails during the data retrieval process.
        KeyError: If expected data is missing from the API responses.
        ValueError: If there are issues processing the retrieved data.

    Notes:
        - This function makes multiple API calls to retrieve player and match data.
        - The position coordinates are normalized using custom preprocessing functions.
        - The function assumes the existence of several helper functions and modules:
          api.get_puuid, api.get_matchids, api.get_match_timeline, 
          preprocessing.table_participant_id, preprocessing.norma_x, preprocessing.norma_y

    Example:
        >>> api_key = "RGAPI-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
        >>> positions = get_user_position("PlayerName", "NA1", api_key)
        >>> print(positions.head())
                                        x         y
        matchId           timestamp              
        NA1_4321098       60000    450.123  302.456
                          120000   475.789  318.901
        NA1_4321097       60000    425.654  298.765
                          120000   460.321  310.987
    """
    
    puuid = api.get_puuid(gamename, tagline,api_key)
    matchs = api.get_matchids(puuid,api_key)
    timeline = [api.get_match_timeline(match,api_key) for match in matchs]

    df_participantId = preprocessing.table_participant_id(timeline)

    df = pd.json_normalize(timeline, record_path=["info", "frames"], meta=["metadata"])
    df["matchId"] = df['metadata'].apply(lambda x:x["matchId"])
    df = df.melt(["timestamp","matchId"])

    df[["frames", "participantId", "metric", "metric2"]] = df["variable"].str.extract("(?P<frames>\w+)\.(?P<participantId>\w+)\.(?P<metric>\w+)\.(?P<metric2>.+)", expand=True)
    df = df[["timestamp","matchId", "frames", "participantId", "metric", "metric2","value"]]
    df.dropna(subset=["frames"], inplace=True)
    df["participantId"] = df["participantId"].astype('str')

    df = df.merge(df_participantId, "left", on=["participantId", "matchId"])

    df_position = df[df["metric"]=="position"].pivot(index=["puuid","matchId", "timestamp"], columns="metric2", values="value")

    table_position_puuid = df_position.loc[puuid]

    table_position_puuid["x"] = table_position_puuid["x"].apply(preprocessing.norma_x)
    table_position_puuid["y"] = table_position_puuid["y"].apply(preprocessing.norma_y)
    return table_position_puuid
