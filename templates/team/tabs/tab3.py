import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def get_details(data, team, str):
    st.write(f"**Details of the Match with {str} Score:**")
    st.write(f"- **Winner:** {data['winner']}")
    st.write(
        f"- **Opponent:** {data['team1'] if data['team1'] != team else data['team2']}"
    )
    st.write(f"- **Venue:** {data['venue']}")
    st.write(f"- **Date:** {data['date']}")
    st.write(f"- **Season:** {data['season']}")


def template(response, team, key, str):
    st.subheader(f"Score Analysis of {team} while {str}")

    col1, col2 = st.columns(2)

    with col1:
        if key in response["highest_score"]:
            data = response["highest_score"][key]

            st.metric(
                "Highest Score",
                (
                    int(data["target_runs"] - 1)
                    if str.find("Bat") != -1
                    else (
                        int(data["actual_runs"])
                        if not np.isnan(data["actual_runs"])
                        else ""
                    )
                ),
            )
            get_details(data, team, "Highest")

    with col2:
        if key in response["lowest_score"]:
            data = response["lowest_score"][key]
            st.metric(
                "Lowest Score",
                (
                    int(data["target_runs"] - 1)
                    if str.find("Bat") != -1
                    else (
                        int(data["actual_runs"])
                        if not np.isnan(data["actual_runs"])
                        else data["actual_runs"]
                    )
                ),
            )
            get_details(data, team, "Lowest")


def score_analysis(response, team):
    template(response, team, "toss_won_bat", "Won the Toss & Bat first")
    template(response, team, "toss_won_field", "Won the Toss & Bowl first")
    template(response, team, "toss_loss_bat", "Lost the Toss & Bat first")
    template(response, team, "toss_loss_field", "Lost the Toss & Bowl first")
