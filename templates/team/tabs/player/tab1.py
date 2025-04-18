import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import ast


# Function to parse the data string into dictionary and convert to DataFrames
def parse_data(data_str):
    # Convert the string to a dictionary
    data_dict = ast.literal_eval(data_str)

    # Convert each value in the dictionary to a DataFrame
    result = {}
    for key, value in data_dict.items():
        result[key] = pd.DataFrame(value)

    return result


# Apply custom CSS
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


def batter_analysis(response, team):
    try:
        # Load the data
        data = response

        # Display header
        st.subheader(f"Batting Statistics of {team}")

        # Get unique batters from total_runs dataframe
        all_batters = sorted(data["total_runs"]["batter"].unique())

        # Apply filters to the data
        for key in data:
            if "batter" in data[key].columns:
                data[key] = data[key][data[key]["batter"].isin(all_batters)]

        # Create tabs for different views
        tab1, tab2, tab3, tab4 = st.tabs(
            [
                "Overview",
                "Boundary Statistics",
                "Innings Analysis",
                "Performance Metrics",
            ]
        )

        # Tab 1: Overview
        with tab1:
            st.markdown(
                '<div class="subheader">Batter Performance Overview</div>',
                unsafe_allow_html=True,
            )

            # Top metrics in a row
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                top_run_scorer = (
                    data["total_runs"]
                    .sort_values("batsman_runs", ascending=False)
                    .iloc[0]
                )
                st.markdown(
                    f"""
                <div class="metric-card">
                    <div class="metric-value">{top_run_scorer['batsman_runs']}</div>
                    <div class="metric-name">Highest individual score - {top_run_scorer['batter']}</div>
                </div>
                """,
                    unsafe_allow_html=True,
                )

            with col2:
                total_centuries = data["centuries"]["batsman_runs"].sum()
                st.markdown(
                    f"""
                <div class="metric-card">
                    <div class="metric-value">{total_centuries}</div>
                    <div class="metric-name">Total Centuries</div>
                </div>
                """,
                    unsafe_allow_html=True,
                )

            with col3:
                total_fifties = data["fifties"]["batsman_runs"].sum()
                st.markdown(
                    f"""
                <div class="metric-card">
                    <div class="metric-value">{total_fifties}</div>
                    <div class="metric-name">Total Fifties</div>
                </div>
                """,
                    unsafe_allow_html=True,
                )

            with col4:
                max_strike_rate = (
                    data["total_runs"]
                    .sort_values("strike_rate", ascending=False)
                    .iloc[0]
                )
                st.markdown(
                    f"""
                <div class="metric-card">
                    <div class="metric-value">{max_strike_rate['strike_rate']}</div>
                    <div class="metric-name">Highest Strike Rate - {max_strike_rate['batter']}</div>
                </div>
                """,
                    unsafe_allow_html=True,
                )

            st.markdown("---")

            # Total runs by batter
            highest_scores = data["highest_score_inning"].sort_values(
                "batsman_runs", ascending=False
            )

            fig = px.bar(
                highest_scores,
                x="batter",
                y="batsman_runs",
                title="Total Runs by Batter",
                color="batter",
                labels={"batsman_runs": "Total Runs", "batter": "Batter"},
                height=500,
            )
            fig.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)

            # Show the raw data
            st.markdown(
                '<div class="subheader">Raw Data: Total Runs by Batter</div>',
                unsafe_allow_html=True,
            )
            st.dataframe(
                highest_scores[["batter", "batsman_runs"]], use_container_width=True
            )

        # Tab 2: Boundary Statistics
        with tab2:
            st.markdown(
                '<div class="subheader">Boundary Statistics</div>',
                unsafe_allow_html=True,
            )

            col1, col2 = st.columns(2)

            with col1:
                # Fours chart
                fours_data = data["total_fours"].sort_values(
                    "total_fours", ascending=False
                )
                fig = px.bar(
                    fours_data,
                    x="batter",
                    y="total_fours",
                    title="Total Fours by Batter",
                    color="batter",
                    labels={"total_fours": "Number of Fours", "batter": "Batter"},
                    height=400,
                )
                fig.update_layout(xaxis_tickangle=-45)
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                # Sixes chart
                sixes_data = data["total_sixes"].sort_values(
                    "total_sixes", ascending=False
                )
                fig = px.bar(
                    sixes_data,
                    x="batter",
                    y="total_sixes",
                    title="Total Sixes by Batter",
                    color="batter",
                    labels={"total_sixes": "Number of Sixes", "batter": "Batter"},
                    height=400,
                )
                fig.update_layout(xaxis_tickangle=-45)
                st.plotly_chart(fig, use_container_width=True)

            # Most fours in an innings
            st.markdown(
                '<div class="subheader">Most Fours in an Innings</div>',
                unsafe_allow_html=True,
            )
            fours_innings = (
                data["fours_inning"]
                .sort_values("total_fours", ascending=False)
                .head(10)
            )
            fig = px.bar(
                fours_innings,
                x="batter",
                y="total_fours",
                title="Most Fours in an Innings",
                color="batter",
                hover_data=["match_id"],
                labels={
                    "total_fours": "Number of Fours",
                    "batter": "Batter",
                    "match_id": "Match ID",
                },
                height=400,
            )
            fig.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)

            # Most sixes in an innings
            st.markdown(
                '<div class="subheader">Most Sixes in an Innings</div>',
                unsafe_allow_html=True,
            )
            sixes_innings = (
                data["sixes_inning"]
                .sort_values("total_sixes", ascending=False)
                .head(10)
            )
            fig = px.bar(
                sixes_innings,
                x="batter",
                y="total_sixes",
                title="Most Sixes in an Innings",
                color="batter",
                hover_data=["match_id"],
                labels={
                    "total_sixes": "Number of Sixes",
                    "batter": "Batter",
                    "match_id": "Match ID",
                },
                height=400,
            )
            fig.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)

            # Boundary data tables
            col1, col2 = st.columns(2)

            with col1:
                st.markdown(
                    '<div class="subheader">Total Fours Data</div>',
                    unsafe_allow_html=True,
                )
                st.dataframe(fours_data, use_container_width=True)

            with col2:
                st.markdown(
                    '<div class="subheader">Total Sixes Data</div>',
                    unsafe_allow_html=True,
                )
                st.dataframe(sixes_data, use_container_width=True)

        # Tab 3: Innings Analysis
        with tab3:
            st.markdown(
                '<div class="subheader">Innings Analysis</div>', unsafe_allow_html=True
            )

            # Highest individual scores
            top_innings = (
                data["total_runs"].sort_values("batsman_runs", ascending=False).head(10)
            )

            fig = px.bar(
                top_innings,
                x="batter",
                y="batsman_runs",
                title="Highest Individual Scores",
                color="batter",
                hover_data=["match_id", "strike_rate"],
                labels={
                    "batsman_runs": "Runs",
                    "batter": "Batter",
                    "match_id": "Match ID",
                    "strike_rate": "Strike Rate",
                },
                height=500,
            )
            fig.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)

            # Strike rate comparison for top innings
            fig = px.scatter(
                top_innings,
                x="batsman_runs",
                y="strike_rate",
                color="batter",
                size="ball",
                hover_data=["match_id"],
                title="Runs vs Strike Rate for Top Innings",
                labels={
                    "batsman_runs": "Runs",
                    "strike_rate": "Strike Rate",
                    "ball": "Balls Faced",
                    "batter": "Batter",
                    "match_id": "Match ID",
                },
                height=500,
            )
            st.plotly_chart(fig, use_container_width=True)

            # Raw data for highest scores
            st.markdown(
                '<div class="subheader">Highest Individual Scores Data</div>',
                unsafe_allow_html=True,
            )
            st.dataframe(top_innings, use_container_width=True)

        # Tab 4: Performance Metrics
        with tab4:
            st.markdown(
                '<div class="subheader">Performance Metrics</div>',
                unsafe_allow_html=True,
            )

            # Centuries and fifties
            col1, col2 = st.columns(2)

            with col1:
                centuries = data["centuries"].sort_values(
                    "batsman_runs", ascending=False
                )
                fig = px.pie(
                    centuries,
                    values="batsman_runs",
                    names="batter",
                    title="Centuries Distribution",
                    hole=0.4,
                    height=400,
                )
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                fifties = (
                    data["fifties"]
                    .sort_values("batsman_runs", ascending=False)
                    .head(10)
                )
                fig = px.pie(
                    fifties,
                    values="batsman_runs",
                    names="batter",
                    title="Fifties Distribution (Top 10)",
                    hole=0.4,
                    height=400,
                )
                st.plotly_chart(fig, use_container_width=True)

            # Boundary distribution (fours vs sixes)
            st.markdown(
                '<div class="subheader">Boundary Distribution</div>',
                unsafe_allow_html=True,
            )

            # Merge fours and sixes data
            fours_data = data["total_fours"].rename(columns={"total_fours": "fours"})
            sixes_data = data["total_sixes"].rename(columns={"total_sixes": "sixes"})
            boundary_data = pd.merge(
                fours_data, sixes_data, on="batter", how="outer"
            ).fillna(0)

            # Calculate total boundaries and boundary percentage
            boundary_data["total_boundaries"] = (
                boundary_data["fours"] + boundary_data["sixes"]
            )
            boundary_data["fours_percentage"] = (
                boundary_data["fours"] / boundary_data["total_boundaries"] * 100
            ).round(2)
            boundary_data["sixes_percentage"] = (
                boundary_data["sixes"] / boundary_data["total_boundaries"] * 100
            ).round(2)

            # Sort by total boundaries
            boundary_data = boundary_data.sort_values(
                "total_boundaries", ascending=False
            )

            # Stacked bar chart for boundary distribution
            fig = go.Figure()

            fig.add_trace(
                go.Bar(
                    x=boundary_data["batter"],
                    y=boundary_data["fours"],
                    name="Fours",
                    marker_color="#1f77b4",
                )
            )

            fig.add_trace(
                go.Bar(
                    x=boundary_data["batter"],
                    y=boundary_data["sixes"],
                    name="Sixes",
                    marker_color="#ff7f0e",
                )
            )

            fig.update_layout(
                title="Boundary Distribution by Batter",
                xaxis_title="Batter",
                yaxis_title="Number of Boundaries",
                barmode="stack",
                height=500,
                xaxis_tickangle=-45,
            )

            st.plotly_chart(fig, use_container_width=True)

            # Boundary data table
            st.markdown(
                '<div class="subheader">Boundary Distribution Data</div>',
                unsafe_allow_html=True,
            )
            st.dataframe(
                boundary_data[
                    [
                        "batter",
                        "fours",
                        "sixes",
                        "total_boundaries",
                        "fours_percentage",
                        "sixes_percentage",
                    ]
                ],
                use_container_width=True,
            )

    except Exception as e:
        st.error(f"An error occurred: {e}")
        st.info("Please check your data format and try again.")
