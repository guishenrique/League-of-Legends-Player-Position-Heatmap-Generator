# League of Legends Player Position Heatmap Generator

## Project Overview

This project generates heatmaps of player positions in League of Legends matches. By analyzing the last 10 ranked games of a given player, it creates three heatmaps showing the player's position distribution across different game phases:

1. 0-10 minutes
2. 10-20 minutes
3. 20+ minutes

## Features

- Fetches player data using Riot Games API
- Processes match timeline data to extract player positions
- Normalizes game coordinates to a standardized grid
- Generates heatmaps overlaid on the League of Legends map
- Provides a Streamlit web interface for easy interaction

## Project Structure

```
├── dados
│   └── image
│       └── lol_map.jpg
├── heatmap
│   ├── __init__.py
│   ├── api.py
│   ├── main.py
│   ├── preprocessing.py
│   └── processing.py
└── requirements.txt
```

- `dados/image/lol_map.jpg`: Background image of the LoL map used in heatmap generation
- `heatmap/api.py`: Contains functions for interacting with the Riot Games API
- `heatmap/main.py`: Streamlit app for running the heatmap generation process
- `heatmap/preprocessing.py`: Functions for data preprocessing and normalization
- `heatmap/processing.py`: Functions for generating the heatmap visualizations
- `requirements.txt`: List of Python dependencies for the project

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/guishenrique/League-of-Legends-Player-Position-Heatmap-Generator.git
   cd League-of-Legends-Player-Position-Heatmap-Generator
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Obtain a Riot Games API key from the [Riot Developer Portal](https://developer.riotgames.com/).

4. Create a `.env` file in the project root and add your API key:
   ```
   api_key_riot=YOUR_API_KEY_HERE
   ```

## Usage

Run the Streamlit app with the following command:

```
streamlit run heatmap/main.py
```

This will start a local web server and open the app in your default web browser. In the app:

1. Enter the player's Game Name
2. Enter the player's tag (with or without the '#' symbol)
3. Click "Submit" to generate the heatmaps

The app will display three heatmaps:
- Player positions from 0 to 10 minutes
- Player positions from 10 to 20 minutes
- Player positions after 20 minutes

## Dependencies

- streamlit
- pydantic
- numpy
- pandas
- matplotlib
- seaborn
- requests
- python-dotenv
- imageio

See `requirements.txt` for specific version information.


## Acknowledgments

- Riot Games for providing the API that makes this project possible
- The League of Legends community for inspiration and support
- Streamlit for the easy-to-use web app framework

## Disclaimer

This project isn't endorsed by Riot Games and doesn't reflect the views or opinions of Riot Games or anyone officially involved in producing or managing League of Legends. League of Legends and Riot Games are trademarks or registered trademarks of Riot Games, Inc. League of Legends © Riot Games, Inc.
