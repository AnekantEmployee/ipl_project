import streamlit as st
from .tabs.tab2 import toss_analysis
from .tabs.tab3 import score_analysis
from .tabs.tab5 import non_league_matches
from .tabs.tab4 import super_over_analysis
from .tabs.tab1 import overall_performance_team
from .tabs.player_analysis import show_player_analysis


def show_team_analysis(response, team):
    tab1, player_tab, tab2, tab3, tab4, tab5 = st.tabs(
        [
            "Overall Performance",
            "Player Performance",
            "Toss Analysis",
            "Score Analysis",
            "Super Over Analysis",
            "Non League Matches",
        ]
    )
    with tab1:
        st.metric(
            "Most player of the matches won by " + team,
            value=f"{response['most_player_of_match'].index[0]} ({response['most_player_of_match'].values[0]})",
        )
        overall_performance_team(response, team)
    with tab2:
        toss_analysis(response, team)
    with tab3:
        score_analysis(response, team)
    with tab4:
        super_over_analysis(response["super_over_analysis"], team)
    with tab5:
        non_league_matches(response, team)
    with player_tab:
        st.subheader(f"Batting & Bowling Figures of {team}")
        show_player_analysis(response["players_analysis"], team)
