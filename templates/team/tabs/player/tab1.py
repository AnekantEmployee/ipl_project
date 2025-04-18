import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import traceback
import ast

# --------------------------
# Helper Functions
# --------------------------


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


def create_metric_card(value, name, highlight_player=None):
    """Create a metric card with optional player highlight"""
    if highlight_player:
        name = f"{name} - {highlight_player}"
    return f"""
    <div class="metric-card">
        <div class="metric-value">{value}</div>
        <div class="metric-name">{name}</div>
    </div>
    """


def create_batter_match_column(df):
    """Create a combined batter_match column from batter and match_id"""
    df["batter_match"] = df["batter"] + " (" + df["match_id"].astype(str) + ")"
    return df


# --------------------------
# Visualization Functions
# --------------------------


def plot_bar_chart(
    df,
    x,
    y,
    title,
    color=None,
    hover_data=None,
    labels=None,
    height=400,
    category_order=None,
):
    """Create a standardized bar chart with consistent styling"""
    fig = px.bar(
        df,
        x=x,
        y=y,
        title=title,
        color=color,
        hover_data=hover_data,
        labels=labels,
        height=height,
        category_orders=category_order,
    )
    fig.update_layout(xaxis_tickangle=-45)
    return fig


def plot_pie_chart(df, values, names, title, hole=0.4, height=400):
    """Create a standardized pie chart"""
    return px.pie(df, values=values, names=names, title=title, hole=hole, height=height)


def plot_boundary_distribution(fours_data, sixes_data):
    """Create a stacked bar chart for boundary distribution"""
    boundary_data = pd.merge(
        fours_data.rename(columns={"total_fours": "fours"}),
        sixes_data.rename(columns={"total_sixes": "sixes"}),
        on="batter",
        how="outer",
    ).fillna(0)

    boundary_data["total_boundaries"] = boundary_data["fours"] + boundary_data["sixes"]
    boundary_data = boundary_data.sort_values("total_boundaries", ascending=False)

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

    return fig, boundary_data


# --------------------------
# Tab Content Functions
# --------------------------


def display_overview_tab(data):
    """Display content for the Overview tab"""
    st.markdown(
        '<div class="subheader">Batter Performance Overview</div>',
        unsafe_allow_html=True,
    )

    # Top metrics row
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        top_run_scorer = (
            data["total_runs"].sort_values("batsman_runs", ascending=False).iloc[0]
        )
        st.markdown(
            create_metric_card(
                top_run_scorer["batsman_runs"],
                "Highest individual score",
                top_run_scorer["batter"],
            ),
            unsafe_allow_html=True,
        )

    with col2:
        total_centuries = data["centuries"]["batsman_runs"].sum()
        st.markdown(
            create_metric_card(total_centuries, "Total Centuries"),
            unsafe_allow_html=True,
        )

    with col3:
        total_fifties = data["fifties"]["batsman_runs"].sum()
        st.markdown(
            create_metric_card(total_fifties, "Total Fifties"), unsafe_allow_html=True
        )

    with col4:
        max_strike_rate = (
            data["total_runs"].sort_values("strike_rate", ascending=False).iloc[0]
        )
        st.markdown(
            create_metric_card(
                max_strike_rate["strike_rate"],
                "Highest Strike Rate",
                max_strike_rate["batter"],
            ),
            unsafe_allow_html=True,
        )

    st.markdown("---")

    # Total runs by batter
    highest_scores = data["highest_score_inning"].sort_values(
        "batsman_runs", ascending=False
    )
    fig = plot_bar_chart(
        highest_scores,
        x="batter",
        y="batsman_runs",
        title="Total Runs by Batter",
        color="batter",
        labels={"batsman_runs": "Total Runs", "batter": "Batter"},
        height=500,
    )
    fig.update_layout(xaxis_tickangle=-90)
    st.plotly_chart(fig, use_container_width=True)

    # Raw data
    st.markdown(
        '<div class="subheader">Raw Data: Total Runs by Batter</div>',
        unsafe_allow_html=True,
    )
    st.dataframe(highest_scores[["batter", "batsman_runs"]], use_container_width=True)


def display_boundary_tab(data):
    """Display content for the Boundary Statistics tab"""
    st.subheader("Boundary Statistics")

    # Fours chart
    fours_data = data["total_fours"].sort_values("total_fours", ascending=False).head(5)
    st.plotly_chart(
        plot_bar_chart(
            fours_data,
            x="batter",
            y="total_fours",
            title="Total Fours by Batter",
            color="batter",
            labels={"total_fours": "Number of Fours", "batter": "Batter"},
            height=400,
        ),
        use_container_width=True,
    )

    # Sixes chart
    sixes_data = data["total_sixes"].sort_values("total_sixes", ascending=False).head(5)
    st.plotly_chart(
        plot_bar_chart(
            sixes_data,
            x="batter",
            y="total_sixes",
            title="Total Sixes by Batter",
            color="batter",
            labels={"total_sixes": "Number of Sixes", "batter": "Batter"},
            height=400,
        ),
        use_container_width=True,
    )

    # Most fours in an innings
    st.subheader("Most Fours in an Innings")
    fours_innings = create_batter_match_column(
        data["fours_inning"].sort_values("total_fours", ascending=False).head(5)
    )
    category_order = fours_innings["batter_match"].tolist()

    fig = plot_bar_chart(
        fours_innings,
        x="batter_match",
        y="total_fours",
        title="Most Fours in an Innings",
        color="batter",
        labels={"total_fours": "Number of Fours", "batter_match": "Batter"},
        height=400,
        category_order={"batter_match": category_order},
    )
    fig.update_layout(xaxis={"categoryorder": "array", "categoryarray": category_order})
    st.plotly_chart(fig, use_container_width=True)

    # Most sixes in an innings
    st.subheader("Most Sixes in an Innings")
    sixes_innings = create_batter_match_column(
        data["sixes_inning"].sort_values("total_sixes", ascending=False).head(5)
    )
    category_order = sixes_innings["batter_match"].tolist()

    fig = plot_bar_chart(
        sixes_innings,
        x="batter_match",
        y="total_sixes",
        title="Most Sixes in an Innings",
        color="batter",
        hover_data=["match_id"],
        labels={"total_sixes": "Number of Sixes", "batter_match": "Batter"},
        height=400,
        category_order={"batter_match": category_order},
    )
    fig.update_layout(xaxis={"categoryorder": "array", "categoryarray": category_order})
    st.plotly_chart(fig, use_container_width=True)

    # Boundary data tables
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            '<div class="subheader">Total Fours Data</div>', unsafe_allow_html=True
        )
        st.dataframe(fours_data, use_container_width=True)
    with col2:
        st.markdown(
            '<div class="subheader">Total Sixes Data</div>', unsafe_allow_html=True
        )
        st.dataframe(sixes_data, use_container_width=True)


def display_innings_tab(data):
    """Display content for the Innings Analysis tab"""
    st.markdown('<div class="subheader">Innings Analysis</div>', unsafe_allow_html=True)

    # Highest individual scores
    top_innings = create_batter_match_column(
        data["total_runs"].sort_values("batsman_runs", ascending=False).head(5)
    )
    category_order = top_innings["batter_match"].tolist()

    fig = plot_bar_chart(
        top_innings,
        x="batter_match",
        y="batsman_runs",
        title="Highest Individual Scores",
        color="batter",
        hover_data=["match_id", "strike_rate"],
        labels={"batsman_runs": "Runs", "batter_match": "Batter"},
        height=500,
        category_order={"batter_match": category_order},
    )
    fig.update_traces(
        hovertemplate="<b>%{x}</b><br>Runs: %{y}<br>Strike Rate: %{customdata[1]:.2f}<extra></extra>"
    )
    st.plotly_chart(fig, use_container_width=True)

    # Strike rate comparison
    top_innings_all = (
        data["total_runs"].sort_values("batsman_runs", ascending=False).head(20)
    )
    fig = px.scatter(
        top_innings_all,
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
        },
        height=500,
    )
    st.plotly_chart(fig, use_container_width=True)

    # Raw data
    st.markdown(
        '<div class="subheader">Highest Individual Scores Data</div>',
        unsafe_allow_html=True,
    )
    st.dataframe(top_innings_all, use_container_width=True)


def display_metrics_tab(data):
    """Display content for the Performance Metrics tab"""
    st.markdown(
        '<div class="subheader">Performance Metrics</div>', unsafe_allow_html=True
    )

    # Centuries and fifties
    col1, col2 = st.columns(2)
    with col1:
        centuries = data["centuries"].sort_values("batsman_runs", ascending=False)
        st.plotly_chart(
            plot_pie_chart(
                centuries,
                values="batsman_runs",
                names="batter",
                title="Centuries Distribution",
            ),
            use_container_width=True,
        )

    with col2:
        fifties = data["fifties"].sort_values("batsman_runs", ascending=False).head(10)
        st.plotly_chart(
            plot_pie_chart(
                fifties,
                values="batsman_runs",
                names="batter",
                title="Fifties Distribution (Top 10)",
            ),
            use_container_width=True,
        )

    # Boundary distribution
    st.markdown(
        '<div class="subheader">Boundary Distribution</div>', unsafe_allow_html=True
    )
    fig, boundary_data = plot_boundary_distribution(
        data["total_fours"], data["total_sixes"]
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
            ]
        ],
        use_container_width=True,
    )


# --------------------------
# Main Function
# --------------------------


def batter_analysis(response, team):
    """Main function to display batter analysis dashboard"""
    try:
        apply_custom_css()
        data = response

        st.subheader(f"Batting Statistics of {team}")

        # Create tabs
        tab1, tab2, tab3, tab4 = st.tabs(
            [
                "Overview",
                "Boundary Statistics",
                "Innings Analysis",
                "Performance Metrics",
            ]
        )

        with tab1:
            display_overview_tab(data)
        with tab2:
            display_boundary_tab(data)
        with tab3:
            display_innings_tab(data)
        with tab4:
            display_metrics_tab(data)

    except Exception as e:
        print("Tab 1 error", traceback.print_exception(e))
        st.error(f"An error occurred: {e}")
        st.info("Please check your data format and try again.")
