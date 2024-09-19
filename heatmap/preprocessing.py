import pandas as pd

def table_participant_id(timeline:list) -> pd.DataFrame:
    """
    Create a DataFrame of participant IDs and match information from timeline data.

    This function processes a list of match timeline data and extracts participant
    information, including their IDs and associated match IDs.

    Args:
        timeline (list): A list of dictionaries, each containing timeline data for a match.
            Each dictionary is expected to have an 'info' key with a 'participants' list
            and a 'metadata' key with match information.

    Returns:
        pd.DataFrame: A pandas DataFrame containing the following columns:
            - Columns from the 'participants' data
            - 'matchId': The unique identifier for each match
            - 'participantId': The participant's ID as a string

    Raises:
        KeyError: If the expected nested structure is not found in the timeline data.
        ValueError: If there are issues normalizing the JSON data.

    Example:
        >>> timeline_data = [{'info': {'participants': [{'participantId': 1, 'summonerName': 'Player1'}]},
        ...                   'metadata': {'matchId': 'NA1_4321098'}}]
        >>> df = table_participant_id(timeline_data)
        >>> print(df)
           participantId summonerName      matchId
        0              1      Player1  NA1_4321098

    Note:
        This function uses pandas' json_normalize to flatten nested JSON data.
        It assumes a specific structure in the input timeline data. Ensure your
        data matches this structure or modify the function accordingly.
    """
    df = pd.json_normalize(
        data=timeline,
        record_path=['info', 'participants'],
        meta=['metadata'],
        errors='ignore'
    )
    df["matchId"] = df['metadata'].apply(lambda x:x["matchId"])
    df["participantId"] = df["participantId"].astype('str')
    return df

def table_frames(timelines:list):
    """
    Process match timeline data into a structured DataFrame of frame-by-frame information.

    This function takes a list of match timelines and transforms it into a long-format
    DataFrame, where each row represents a specific metric for a participant at a given
    timestamp.

    Args:
        timelines (list): A list of dictionaries, each containing timeline data for a match.
            Each dictionary is expected to have an 'info' key with a 'frames' list
            and a 'metadata' key with match information.

    Returns:
        pd.DataFrame: A pandas DataFrame with the following columns:
            - timestamp: The time of the frame in milliseconds from the start of the match
            - matchId: The unique identifier for each match
            - frames: The type of frame data (e.g., 'participantFrames')
            - participantId: The participant's ID as a string
            - metric: The primary metric being measured (e.g., 'position')
            - metric2: A secondary metric or sub-category (e.g., 'x' or 'y' for position)
            - value: The value of the metric

    Raises:
        KeyError: If the expected nested structure is not found in the timeline data.
        ValueError: If there are issues normalizing or melting the JSON data.

    Example:
        >>> timeline_data = [{'info': {'frames': [{'timestamp': 60000,
        ...                                        'participantFrames': {'1': {'position': {'x': 1000, 'y': 1000}}}}]},
        ...                   'metadata': {'matchId': 'NA1_4321098'}}]
        >>> df = table_frames(timeline_data)
        >>> print(df)
           timestamp    matchId            frames participantId metric metric2  value
        0      60000  NA1_4321098  participantFrames            1 position      x   1000
        1      60000  NA1_4321098  participantFrames            1 position      y   1000

    Note:
        This function uses complex pandas operations including json_normalize, melt,
        and string extraction with regular expressions. It assumes a specific nested
        structure in the input timeline data. Ensure your data matches this structure
        or modify the function accordingly.
    """
    df = pd.json_normalize(timelines, record_path=["info", "frames"], meta=["metadata"])
    df["matchId"] = df['metadata'].apply(lambda x:x["matchId"])
    df = df.melt(["timestamp","matchId"])
    df[["frames", "participantId", "metric", "metric2"]] = df["variable"].str.extract("(?P<frames>\w+)\.(?P<participantId>\w+)\.(?P<metric>\w+)\.(?P<metric2>.+)", expand=True)
    df = df[["timestamp","matchId", "frames", "participantId", "metric", "metric2","value"]]
    df.dropna(subset=["frames"], inplace=True)
    df["participantId"] = df["participantId"].astype('str')
    return df

def norma_x(X):
    X_normalizado = 10 + ((X - 335) * (800-0))/(14700-0) #Normalizando
    return X_normalizado

def norma_y(Y):
    Y_normalizado = 10 + ((Y - 335) * (800-0))/(14700-0)
    return Y_normalizado