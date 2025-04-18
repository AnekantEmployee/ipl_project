import streamlit as st
import pandas as pd
import plotly.express as px
import traceback


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
            .metric-card {
                background-color: #f0f2f6;
                border-radius: 10px;
                padding: 15px;
                text-align: center;
            }
            .metric-value {
                font-size: 36px;
                font-weight: bold;
                color: #1c83e1;
            }
            .metric-name {
                font-size: 16px;
                color: #555;
            }
            .match-card {
                background-color: #f9f9f9;
                border-radius: 8px;
                padding: 15px;
                margin-bottom: 15px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def create_metric_card(value, name, highlight=None):
    """Create a metric card with optional highlight"""
    if highlight:
        name = f"{name} - {highlight}"
    return f"""
    <div class="metric-card">
        <div class="metric-value">{value}</div>
        <div class="metric-name">{name}</div>
    </div>
    """


def create_match_card(match, team):
    """Create a styled card for a match with better contrast"""
    winner = match["winner"]
    margin = f"{match['result_margin']} {match['result']}"
    opponent = match["team2"] if match["team1"] == winner else match["team1"]

    return f"""
    <div class="match-card" style="background-color: #ffffff; border-left: 5px solid #1c83e1;">
        <div style="font-weight:bold; font-size:18px; margin-bottom:8px; color: #333333;">
            {match['season']} Final - {winner} vs {opponent}
        </div>
        <div style="margin-bottom:5px; color: #555555;">
            <span style="font-weight:bold; color: #333333;">Venue:</span> {match['venue']}
        </div>
        <div style="margin-bottom:5px; color: #555555;">
            <span style="font-weight:bold; color: #333333;">Date:</span> {match['date']}
        </div>
        <div style="margin-bottom:5px; color: #555555;">
            <span style="font-weight:bold; color: #333333;">Result:</span> 
            <span style="color: {'#4CAF50' if winner == team else '#e63946'}">
                {winner} won by {margin}
            </span>
        </div>
        <div style="color: #555555;">
            <span style="font-weight:bold; color: #333333;">Player of Match:</span> {match['player_of_match']}
        </div>
    </div>
    """


def non_league_matches(response, team):
    """Main function to display non-league matches (finals, qualifiers) dashboard"""
    try:
        apply_custom_css()

        # Update CSS for better visibility
        st.markdown(
            """
            <style>
                .match-card {
                    background-color: #ffffff;
                    border-radius: 8px;
                    padding: 15px;
                    margin-bottom: 15px;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                    border-left: 5px solid #1c83e1;
                }
                .match-card div {
                    color: #333333;
                }
                .stDataFrame {
                    background-color: #ffffff !important;
                }
            </style>
            """,
            unsafe_allow_html=True,
        )
        st.subheader(f"Knockout Stage Performance of {team}")

        # Calculate metrics
        trophies = response.get("final_matches_won", pd.DataFrame()).shape[0]
        finals_played = response.get("final_matches", pd.DataFrame()).shape[0]
        qualifiers_played = response.get("non_final_matches", pd.DataFrame()).shape[0]
        win_percentage = (trophies / finals_played * 100) if finals_played > 0 else 0

        # Create tabs
        tab1, tab2 = st.tabs(["Overview", "Match Details"])

        with tab1:
            # Overview metrics
            col1, col2, col3 = st.columns(3)

            with col1:
                st.markdown(
                    create_metric_card(trophies, "IPL Trophies"), unsafe_allow_html=True
                )

            with col2:
                st.markdown(
                    create_metric_card(finals_played, "Finals Played"),
                    unsafe_allow_html=True,
                )

            with col3:
                st.markdown(
                    create_metric_card(
                        f"{win_percentage:.1f}%", "Final Win Percentage"
                    ),
                    unsafe_allow_html=True,
                )

            st.markdown("---")

            # Performance visualization
            st.markdown(
                '<div class="subheader">Knockout Stage Performance</div>',
                unsafe_allow_html=True,
            )

            performance_data = {
                "Stage": ["Trophies", "Finals", "Qualifiers/Semis"],
                "Count": [trophies, finals_played, qualifiers_played],
                "Color": ["#4CAF50", "#FFA500", "#1E90FF"],
            }

            fig = px.bar(
                performance_data,
                x="Stage",
                y="Count",
                color="Stage",
                color_discrete_map={
                    "Trophies": "#4CAF50",
                    "Finals": "#FFA500",
                    "Qualifiers/Semis": "#1E90FF",
                },
                title="Knockout Stage Achievements",
                height=400,
            )
            st.plotly_chart(fig, use_container_width=True)

        with tab2:
            # Finals won details
            if (
                "final_matches_won" in response
                and not response["final_matches_won"].empty
            ):
                st.markdown(
                    '<div class="subheader" style="color: #1c83e1;">Finals Won</div>',
                    unsafe_allow_html=True,
                )

                for _, match in response["final_matches_won"].iterrows():
                    st.markdown(create_match_card(match, team), unsafe_allow_html=True)

            # Finals lost details
            if "final_matches" in response and not response["final_matches"].empty:
                finals_lost = response["final_matches"][
                    response["final_matches"]["winner"] != team
                ]

                if not finals_lost.empty:
                    st.markdown(
                        '<div class="subheader" style="color: #1c83e1;">Finals Lost</div>',
                        unsafe_allow_html=True,
                    )

                    for _, match in finals_lost.iterrows():
                        st.markdown(create_match_card(match, team), unsafe_allow_html=True)

            # Qualifiers/Semis details
            if (
                "non_final_matches" in response
                and not response["non_final_matches"].empty
            ):
                st.markdown(
                    '<div class="subheader" style="color: #1c83e1;">Qualifiers & Semi-Finals</div>',
                    unsafe_allow_html=True,
                )

                for _, match in response["non_final_matches"].iterrows():
                    st.markdown(create_match_card(match, team), unsafe_allow_html=True)

            # Raw data tables with white background
            st.markdown(
                '<div class="subheader" style="color: #1c83e1;">Raw Data</div>',
                unsafe_allow_html=True,
            )

            if (
                "final_matches_won" in response
                and not response["final_matches_won"].empty
            ):
                st.markdown("**Finals Won Data**")
                st.dataframe(
                    response["final_matches_won"][
                        [
                            "season",
                            "date",
                            "venue",
                            "team1",
                            "team2",
                            "winner",
                            "result",
                            "result_margin",
                            "player_of_match",
                        ]
                    ],
                    use_container_width=True,
                )

            if "final_matches" in response and not response["final_matches"].empty:
                finals_lost = response["final_matches"][
                    response["final_matches"]["winner"] != team
                ]
                if not finals_lost.empty:
                    st.markdown("**Finals Lost Data**")
                    st.dataframe(
                        finals_lost[
                            [
                                "season",
                                "date",
                                "venue",
                                "team1",
                                "team2",
                                "winner",
                                "result",
                                "result_margin",
                                "player_of_match",
                            ]
                        ],
                        use_container_width=True,
                    )

            if (
                "non_final_matches" in response
                and not response["non_final_matches"].empty
            ):
                st.markdown("**Qualifiers & Semi-Finals Data**")
                st.dataframe(
                    response["non_final_matches"][
                        [
                            "season",
                            "date",
                            "venue",
                            "team1",
                            "team2",
                            "winner",
                            "result",
                            "result_margin",
                            "player_of_match",
                        ]
                    ],
                    use_container_width=True,
                )

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.info("Please check your data format and try again.")
        print(traceback.format_exc())
