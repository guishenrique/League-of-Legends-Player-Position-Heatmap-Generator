import os


import streamlit as st
from pydantic import BaseModel, Field, ValidationError, field_validator
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.image import imread
from requests.exceptions import HTTPError
from dotenv import load_dotenv

from processing import get_user_position

class UserInput(BaseModel):
    game_name: str = Field(min_length=3, max_length=16)
    tag: str = Field(min_length=3, max_length=6)
    
    @field_validator('tag')
    def remove_hash_from_tag(cls, v):
        if v.startswith('#'):
            return v[1:]
        return v
    
@st.cache_resource
def construct_image(table:pd.DataFrame)-> plt.Figure:
    """
    Construct a heatmap visualization of player positions on the League of Legends map.

    This function creates a visualization that overlays player position data on the
    game map, including both a scatter plot of individual positions and a kernel
    density estimation (KDE) heatmap.

    Args:
        table (pd.DataFrame): A DataFrame containing the player's position data.
            Expected to have columns 'x' and 'y' with normalized coordinates.

    Returns:
        plt.Figure: A matplotlib Figure object containing the constructed visualization.

    Notes:
        - The function expects a League of Legends map image file at '../dados/image/lol_map.jpg'.
        - The visualization includes:
            1. The game map as a background image.
            2. A scatter plot of individual player positions.
            3. A KDE heatmap showing the density of player positions.
        - The coordinate system is assumed to be normalized to a 800x800 grid.
        - The resulting plot has no axis labels or ticks for a cleaner appearance.

    Dependencies:
        - matplotlib.pyplot
        - seaborn
        - imageio.v2 (for imread)

    Example:
        >>> positions_df = pd.DataFrame({'x': [400, 450, 500], 'y': [300, 350, 400]})
        >>> fig = construct_image(positions_df)
        >>> plt.show()  # This will display the constructed image
    """
    mapa_jogo = imread('../dados/image/lol_map.jpg')
    
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.imshow(mapa_jogo,norm="linear", origin='lower', extent=[0, 800, 800, 0])
    sns.scatterplot(x=table["x"], y=table["y"])
    sns.kdeplot(
        data=table,
        x="x",
        y="y",
        cmap="YlOrRd",
        fill=True,
        cbar=True,
        alpha=0.3,
        ax=ax
    )
    ax.set(xticklabels=[], yticklabels=[])  # remove the tick labels
    ax.tick_params(bottom=False,left=False )  # remove the ticks
    plt.xlim([0, 800])
    plt.ylim([0, 800])
    return fig

def main():
    load_dotenv(override=True)
    api_key = os.getenv("api_key_riot")
    
    st.title("League of Legends - Position Analysis")
    st.write("Analyze a player's position in the last 10 ranked games.")

    game_name = st.text_input("Enter the Game Name")
    tag = st.text_input("Enter the tag")
    
    if st.button("Submit"):
        try:
            # Validate input
            user_input = UserInput(game_name=game_name, tag=tag)
            
            # If validation passes, proceed with analysis
            load_state = st.text('Loading data...')
            table = get_user_position(user_input.game_name, user_input.tag, api_key)
            mask_10min = table.index.get_level_values(1) < 600000
            mask_20min = table.index.get_level_values(1) <= 1200000
            mask_20min_plus = table.index.get_level_values(1) > 1200000
            table.loc[mask_20min_plus, "Time"] = "After 20 minutes"
            table.loc[mask_20min, "Time"] = "Before 20 minutes"
            table.loc[mask_10min, "Time"] = "Before 10 minutes"
            load_state.text('Loading data... done!')
            
            create_graph = st.text('Creating graph...')
            st.subheader("Before 10 minutes")
            fig = construct_image(table[table["Time"]=="Before 10 minutes"])
            st.pyplot(fig)
            
            st.subheader("Between 10 and 20 minutes")
            fig = construct_image(table[table["Time"]=="Before 20 minutes"])
            st.pyplot(fig)
            
            st.subheader("After 20 minutes")
            fig = construct_image(table[table["Time"]=="After 20 minutes"])
            st.pyplot(fig)    
            
            create_graph.text('Creating graph... done!')
        except ValidationError as e:
            for error in e.errors():
                st.error(f"{error['loc'][0]}: {error['msg']}")
            st.stop()
            
        except HTTPError as e:
            st.error(f"Failed: {str(e)}")
            st.stop()
        
if __name__ =="__main__": 
    load_dotenv()
    main()
    
