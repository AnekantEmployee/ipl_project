import streamlit as st
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go


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


def toss_analysis(response, team):
    """Main function to display toss analysis dashboard"""
    try:
        apply_custom_css()

        st.subheader(f"Toss Statistics of {team}")

        # Calculate metrics
        total_matches = response["total_matches"].shape[0]
        toss_won = response["toss_analysis"]["toss_won"].shape[0]
        toss_lost = total_matches - toss_won
        toss_win_percentage = (toss_won / total_matches) * 100
        match_won_after_toss_win = response["toss_analysis"][
            "toss_won_match_won"
        ].shape[0]
        match_lost_after_toss_win = toss_won - match_won_after_toss_win
        match_won_after_toss_loss = response["toss_analysis"][
            "toss_loss_match_won"
        ].shape[0]
        match_lost_after_toss_loss = toss_lost - match_won_after_toss_loss

        # Create tabs
        tab1, tab2 = st.tabs(["Overview", "Detailed Analysis"])

        with tab1:
            # Overview metrics
            col1, col2, col3 = st.columns(3)

            with col1:
                st.markdown(
                    create_metric_card(
                        f"{toss_win_percentage:.1f}%", "Toss Win Percentage"
                    ),
                    unsafe_allow_html=True,
                )

            with col2:
                st.markdown(
                    create_metric_card(
                        f"{(match_won_after_toss_win/toss_won*100):.1f}%",
                        "Win % After Toss Win",
                    ),
                    unsafe_allow_html=True,
                )

            with col3:
                st.markdown(
                    create_metric_card(
                        f"{(match_won_after_toss_loss/toss_lost*100):.1f}%",
                        "Win % After Toss Loss",
                    ),
                    unsafe_allow_html=True,
                )

            st.markdown("---")

            # Toss win/loss pie chart
            st.markdown(
                '<div class="subheader">Toss Win/Loss Distribution</div>',
                unsafe_allow_html=True,
            )

            toss_data = {
                "Result": ["Toss Won", "Toss Lost"],
                "Count": [toss_won, toss_lost],
                "Color": ["#4CAF50", "#ff6347"],
            }

            fig = px.pie(
                toss_data,
                values="Count",
                names="Result",
                color="Result",
                color_discrete_map={"Toss Won": "#4CAF50", "Toss Lost": "#ff6347"},
                title=f"Toss Outcomes ({total_matches} matches)",
                hole=0.4,
                height=400,
            )
            st.plotly_chart(fig, use_container_width=True)

        with tab2:
            # Detailed analysis
            col1, col2 = st.columns(2)

            with col1:
                # Match outcome after winning toss
                st.markdown(
                    '<div class="subheader">After Winning Toss</div>',
                    unsafe_allow_html=True,
                )

                win_data = {
                    "Result": ["Match Won", "Match Lost"],
                    "Count": [match_won_after_toss_win, match_lost_after_toss_win],
                    "Color": ["#3776ab", "#e63946"],
                }

                fig = px.pie(
                    win_data,
                    values="Count",
                    names="Result",
                    color="Result",
                    color_discrete_map={
                        "Match Won": "#3776ab",
                        "Match Lost": "#e63946",
                    },
                    title=f"Match Outcomes After Toss Win ({toss_won} matches)",
                    hole=0.4,
                    height=400,
                )
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                # Match outcome after losing toss
                st.markdown(
                    '<div class="subheader">After Losing Toss</div>',
                    unsafe_allow_html=True,
                )

                loss_data = {
                    "Result": ["Match Won", "Match Lost"],
                    "Count": [match_won_after_toss_loss, match_lost_after_toss_loss],
                    "Color": ["#2ca02c", "#d62728"],
                }

                fig = px.pie(
                    loss_data,
                    values="Count",
                    names="Result",
                    color="Result",
                    color_discrete_map={
                        "Match Won": "#2ca02c",
                        "Match Lost": "#d62728",
                    },
                    title=f"Match Outcomes After Toss Loss ({toss_lost} matches)",
                    hole=0.4,
                    height=400,
                )
                st.plotly_chart(fig, use_container_width=True)

            # Raw data table
            st.markdown(
                '<div class="subheader">Toss Statistics Data</div>',
                unsafe_allow_html=True,
            )

            stats_data = {
                "Metric": [
                    "Total Matches",
                    "Tosses Won",
                    "Tosses Lost",
                    "Matches Won After Toss Win",
                    "Matches Lost After Toss Win",
                    "Matches Won After Toss Loss",
                    "Matches Lost After Toss Loss",
                ],
                "Count": [
                    total_matches,
                    toss_won,
                    toss_lost,
                    match_won_after_toss_win,
                    match_lost_after_toss_win,
                    match_won_after_toss_loss,
                    match_lost_after_toss_loss,
                ],
                "Percentage": [
                    100,
                    (toss_won / total_matches) * 100,
                    (toss_lost / total_matches) * 100,
                    (match_won_after_toss_win / toss_won) * 100 if toss_won > 0 else 0,
                    (match_lost_after_toss_win / toss_won) * 100 if toss_won > 0 else 0,
                    (
                        (match_won_after_toss_loss / toss_lost) * 100
                        if toss_lost > 0
                        else 0
                    ),
                    (
                        (match_lost_after_toss_loss / toss_lost) * 100
                        if toss_lost > 0
                        else 0
                    ),
                ],
            }

            st.dataframe(pd.DataFrame(stats_data), use_container_width=True)

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.info("Please check your data format and try again.")
