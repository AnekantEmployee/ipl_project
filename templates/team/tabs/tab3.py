import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px


def apply_custom_css():
    """Apply custom CSS styles to the Streamlit app"""
    st.markdown(
        """
        <style>
            .header {
                color: #ff4b4b;
                font-size: 40px;
                font-weight: bold;
                text-align: center;
                margin-bottom: 20px;
            }
            .subheader {
                color: #1c83e1;
                font-size: 24px;
                font-weight: bold;
                margin-top: 20px;
                margin-bottom: 10px;
            }
            .score-card {
                background-color: #f0f2f6;
                border-radius: 10px;
                padding: 15px;
                margin-bottom: 20px;
            }
            .match-details {
                background-color: #ffffff;
                border-radius: 8px;
                padding: 15px;
                margin-top: 15px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            }
            .metric-value {
                font-size: 36px;
                font-weight: bold;
                color: #1c83e1;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def create_match_details(data, team, score_type):
    """Create styled match details card"""
    opponent = data["team1"] if data["team1"] != team else data["team2"]
    return f"""
    <div class="match-details">
        <div style="font-weight:bold; margin-bottom:8px; color: #333;">{score_type} Score Match Details</div>
        <div style="margin-bottom:5px; color: #555;">
            <span style="font-weight:bold;">Winner:</span> {data['winner']}
        </div>
        <div style="margin-bottom:5px; color: #555;">
            <span style="font-weight:bold;">Opponent:</span> {opponent}
        </div>
        <div style="margin-bottom:5px; color: #555;">
            <span style="font-weight:bold;">Venue:</span> {data['venue']}
        </div>
        <div style="margin-bottom:5px; color: #555;">
            <span style="font-weight:bold;">Date:</span> {data['date']}
        </div>
        <div style="color: #555;">
            <span style="font-weight:bold;">Season:</span> {data['season']}
        </div>
    </div>
    """


def template(response, team, key, scenario):
    """Template for displaying score analysis"""
    st.markdown(
        f'<div class="subheader">Score Analysis of {team} while {scenario}</div>',
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    with col1:
        if key in response["highest_score"]:
            data = response["highest_score"][key]
            score = (
                int(data["target_runs"] - 1)
                if "Bat" in scenario
                else int(data["actual_runs"])
            )

            st.markdown(
                f"""
                <div class="score-card">
                    <div style="font-size:18px; margin-bottom:10px; color: black;">Highest Score</div>
                    <div class="metric-value">{score}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.markdown(
                create_match_details(data, team, "Highest"), unsafe_allow_html=True
            )

    with col2:
        if key in response["lowest_score"]:
            data = response["lowest_score"][key]
            score = (
                int(data["target_runs"] - 1)
                if "Bat" in scenario
                else int(data["actual_runs"])
            )

            st.markdown(
                f"""
                <div class="score-card">
                    <div style="font-size:18px; margin-bottom:10px; color: black;">Lowest Score</div>
                    <div class="metric-value">{score}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.markdown(
                create_match_details(data, team, "Lowest"), unsafe_allow_html=True
            )


def score_analysis(response, team):
    """Main function for score analysis dashboard"""
    try:
        apply_custom_css()
        st.title(f"Score Analysis for {team}")

        # Add a visual summary at the top
        scenarios = [
            ("Won the Toss & Bat first", "toss_won_bat"),
            ("Won the Toss & Bowl first", "toss_won_field"),
            ("Lost the Toss & Bat first", "toss_loss_bat"),
            ("Lost the Toss & Bowl first", "toss_loss_field"),
        ]

        # Create tabs for better organization
        tabs = st.tabs([scenario[0] for scenario in scenarios])

        for tab, (scenario, key) in zip(tabs, scenarios):
            with tab:
                template(response, team, key, scenario)

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.info("Please check your data format and try again.")
