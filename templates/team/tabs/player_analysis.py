import streamlit as st
from .player.tab1 import batter_analysis
from .player.tab2 import bowler_analysis


def show_player_analysis(response, team):
    tab1, tab2 = st.tabs(["Batting Analysis", "Bowling Figures"])
    with tab1:
        batter_analysis(response["batter_analysis"], team)
    with tab2:
        bowler_analysis(response["bowler_analysis"], team)
