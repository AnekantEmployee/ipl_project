import streamlit as st

from views import get_team_analysis
from utils import get_teams, get_seasons
from .show_team_analysis import show_team_analysis


def team_analysis(cnx):
    st.title("Team Detailed Analysis")

    # Fetching all the teams data
    teams_data = get_teams(cnx)

    seasons_data = get_seasons(cnx)
    if not seasons_data["status"]:
        st.error(seasons_data["message"])
    seasons_data = seasons_data["data"]
    seasons_data.reverse()
    seasons_data.insert(0, "All Seasons")

    # Options to select the teams
    col1, col2 = st.columns(2)
    with col1:
        team = st.selectbox("Team", teams_data["data"])
    with col2:
        season_selection = st.selectbox("Seasons", seasons_data)

    # Search button to trigger
    search_btn_pressed = st.button("Search")
    if search_btn_pressed:
        response = get_team_analysis(cnx, team, season_selection)

        st.markdown(" ")
        st.header(f"Team Analysis: {team}")
        show_team_analysis(response, team)
