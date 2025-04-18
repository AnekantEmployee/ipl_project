import streamlit as st
import plotly.express as px
import pandas as pd


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
            .performance-card {
                background-color: #ffffff;
                border-radius: 8px;
                padding: 15px;
                margin-bottom: 15px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            }
            /* Fix for white background in tables */
            .stDataFrame {
                background-color: white !important;
            }
            /* Fix for text visibility in tables */
            .stDataFrame td, .stDataFrame th {
                color: #333333 !important;
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


def overall_analysis(data, team):
    """Main function to display overall team performance dashboard"""
    try:
        apply_custom_css()

        total_matches = data["total_matches"].shape[0]
        matches_won = data["matches_won"].shape[0]
        matches_lost = data["matches_lost"].shape[0]
        win_percentage = (matches_won / total_matches) * 100 if total_matches > 0 else 0

        st.subheader(f"Overall Performance of {team}")

        # Key metrics
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown(
                create_metric_card(total_matches, "Total Matches"),
                unsafe_allow_html=True,
            )

        with col2:
            st.markdown(
                create_metric_card(matches_won, "Matches Won"),
                unsafe_allow_html=True,
            )

        with col3:
            st.markdown(
                create_metric_card(f"{win_percentage:.1f}%", "Win Percentage"),
                unsafe_allow_html=True,
            )

        st.markdown("---")

        # Win/Loss distribution
        st.markdown(
            '<div class="subheader">Match Results Distribution</div>',
            unsafe_allow_html=True,
        )

        performance_data = pd.DataFrame(
            {
                "Result": ["Won", "Lost"],
                "Count": [matches_won, matches_lost],
            }
        )

        fig = px.pie(
            performance_data,
            values="Count",
            names="Result",
            color="Result",
            color_discrete_map={"Won": "#4CAF50", "Lost": "#e63946"},
            title=f"Win/Loss Distribution ({total_matches} matches)",
            hole=0.4,
            height=400,
        )
        st.plotly_chart(fig, use_container_width=True)

        # Win percentage by season (if available)
        if "matches_won_by_season" in data:
            st.markdown(
                '<div class="subheader">Win Percentage by Season</div>',
                unsafe_allow_html=True,
            )

            season_data = data["matches_won_by_season"].copy()
            season_data["win_percentage"] = (
                season_data["matches_won"] / season_data["total_matches"]
            ) * 100

            fig = px.bar(
                season_data,
                x="season",
                y="win_percentage",
                title="Win Percentage by Season",
                labels={"season": "Season", "win_percentage": "Win Percentage"},
                color="win_percentage",
                color_continuous_scale="Viridis",
            )
            st.plotly_chart(fig, use_container_width=True)

        # Raw data table - Fixed Arrow serialization by ensuring proper data types
        st.markdown(
            '<div class="subheader">Raw Performance Data</div>',
            unsafe_allow_html=True,
        )

        summary_data = pd.DataFrame(
            {
                "Metric": [
                    "Total Matches",
                    "Matches Won",
                    "Matches Lost",
                    "Win Percentage",
                ],
                "Value": [
                    str(total_matches),
                    str(matches_won),
                    str(matches_lost),
                    f"{win_percentage:.1f}%",
                ],
            }
        )

        st.dataframe(summary_data, use_container_width=True, hide_index=True)

        # Season-wise data if available
        if "matches_won_by_season" in data:
            st.markdown(
                '<div class="subheader">Season-wise Performance</div>',
                unsafe_allow_html=True,
            )
            season_df = data["matches_won_by_season"].copy()
            # Ensure numeric columns are properly typed
            numeric_cols = ["matches_won", "total_matches"]
            for col in numeric_cols:
                if col in season_df:
                    season_df[col] = pd.to_numeric(season_df[col], errors="coerce")
            st.dataframe(season_df, use_container_width=True)

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.info("Please check your data format and try again.")


def overall_performance_team(data, team):
    """Wrapper function to maintain compatibility"""
    overall_analysis(data, team)
