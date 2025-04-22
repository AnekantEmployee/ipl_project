import streamlit as st

from views import head_to_head_insights
from utils import get_teams, get_seasons
from .tabs.tabs import overall_performance, home_away_analysis


def head_to_head_screen(cnx):
    st.title("Head to Head Comparison")

    # Fetching all the teams data
    teams_data = get_teams(cnx)
    seasons_data = get_seasons(cnx)

    if not seasons_data["status"]:
        st.error(seasons_data["message"])

    seasons_data = seasons_data["data"]
    seasons_data.reverse()
    seasons_data.insert(0, "All Seasons")

    # Options to select the teams
    col1, col2, col3 = st.columns(3)
    with col1:
        team1 = st.selectbox("Team 1", teams_data["data"])
    with col2:
        team2 = st.selectbox("Team 2", teams_data["data"])
    with col3:
        season_selection = st.selectbox("Seasons", seasons_data)

    # Search button to trigger
    search_btn_pressed = st.button("Search")
    if search_btn_pressed:
        # Trigger the function to get the head to head data
        response = head_to_head_insights(cnx, team1, team2, season_selection)

        if not response["status"]:
            st.error(response["message"])
        else:
            st.markdown(" ")
            st.header(f"Head-to-Head: {team1} vs. {team2}")
            tab1, tab2, tab3 = st.tabs(
                ["Overall Performance", "Home & Away Analysis", "Player Statistics"]
            )

            with tab1:
                overall_performance(
                    response["data"]["overall_analysis"], team1, team2, cnx
                )
            with tab2:
                home_away_analysis(response["data"]["home_away_data"], team1, team2)
            with tab3:
                pass

            if len(response["data"]["overall_analysis"]["won_dataframe_team1"]) > 0:
                st.write(" ")
                st.write(f"Matches won by {team1}")
                st.dataframe(
                    response["data"]["overall_analysis"]["won_dataframe_team1"]
                )

            if len(response["data"]["overall_analysis"]["won_dataframe_team2"]) > 0:
                st.write(" ")
                st.write(f"Matches won by {team2}")
                st.dataframe(
                    response["data"]["overall_analysis"]["won_dataframe_team2"]
                )
