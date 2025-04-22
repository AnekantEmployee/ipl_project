import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

from .charts import bar_chart


def overall_performance(data, team1, team2, cnx):
    """Creates and displays a pie chart in Streamlit."""

    st.write(
        f"Insights of {data['total_matches_played']} matches played between {team1} & {team2}"
    )

    chart_data = {
        "Categories": [team1, team2, "Drawn"],
        "Values": [data["won_by_team1"], data["won_by_team2"], data["drawn"]],
    }
    df_data = {
        "": ["Total matches played", team1, team2, "Drawn"],
        "Overall Analysis": [
            data["total_matches_played"],
            data["won_by_team1"],
            data["won_by_team2"],
            data["drawn"],
        ],
    }
    df = pd.DataFrame(chart_data)

    fig, ax = plt.subplots()
    ax.pie(df["Values"], labels=df["Categories"], autopct="%1.1f%%", startangle=90)
    ax.axis("equal")
    st.pyplot(fig)

    st.write(" ")
    st.write(
        f"Tabular Representation of {data['total_matches_played']} matches played between {team1} & {team2}"
    )
    st.dataframe(df_data)


def team_charts(team_name, data):
    st.write(f"Insights of {team_name} played at Home & Away")
    team1_data = {
        "": ["Home Wins", "Away Wins", "Home Losses", "Away Losses"],
        "Records": [
            data["home_wins"],
            data["away_wins"],
            data["home_losses"],
            data["away_losses"],
        ],
    }
    team1_df = pd.DataFrame(team1_data)
    bar_chart(f"{team_name} Analysis", team1_df)

    st.write(f"Tabular Representation of {team_name} played at Home & Away")
    st.dataframe(team1_df)


def home_away_analysis(data, team1, team2):
    """Creates and displays a bar chart in Streamlit."""

    team_charts(team1, data["team1"])
    st.write(" ")
    st.write(" ")
    team_charts(team2, data["team2"])
