import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import traceback

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


def create_bowler_match_column(df):
    """Create a combined bowler_match column from bowler and match_id"""
    df["bowler_match"] = df["bowler"] + " (" + df["match_id"].astype(str) + ")"
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


def plot_economy_vs_strike_rate(df):
    """Create a scatter plot of economy rate vs strike rate"""
    fig = px.scatter(
        df,
        x="strike_rate",
        y="economy_rate",
        color="bowler",
        size="total_wickets",
        hover_data=["total_runs", "total_balls"],
        title="Economy Rate vs Strike Rate",
        labels={
            "strike_rate": "Strike Rate",
            "economy_rate": "Economy Rate",
            "total_wickets": "Total Wickets",
            "bowler": "Bowler",
        },
        height=500,
    )
    fig.update_layout(
        xaxis_title="Strike Rate (Balls per Wicket)",
        yaxis_title="Economy Rate (Runs per Over)",
    )
    return fig


# --------------------------
# Tab Content Functions
# --------------------------


def display_overview_tab(data):
    """Display content for the Overview tab"""
    st.markdown(
        '<div class="subheader">Bowling Performance Overview</div>',
        unsafe_allow_html=True,
    )

    # Top metrics row
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        top_wicket_taker = (
            data["wickets_total"].sort_values("total_wickets", ascending=False).iloc[0]
        )
        st.markdown(
            create_metric_card(
                top_wicket_taker["total_wickets"],
                "Most Wickets",
                top_wicket_taker["bowler"],
            ),
            unsafe_allow_html=True,
        )

    with col2:
        best_figures = (
            data["wickets_inning"]
            .sort_values(by=["total_wickets", "total_runs"], ascending=[False, True])
            .iloc[0]
        )
        st.markdown(
            create_metric_card(
                f"{best_figures['total_wickets']}/{best_figures['total_runs']}",
                "Best Bowling Figures",
                best_figures["bowler"],
            ),
            unsafe_allow_html=True,
        )

    with col3:
        best_economy = data["wickets_total"].sort_values("economy_rate").iloc[0]
        st.markdown(
            create_metric_card(
                f"{best_economy['economy_rate']:.2f}",
                "Best Economy Rate",
                best_economy["bowler"],
            ),
            unsafe_allow_html=True,
        )

    with col4:
        best_strike_rate = data["wickets_total"].sort_values("strike_rate").iloc[0]
        st.markdown(
            create_metric_card(
                f"{best_strike_rate['strike_rate']:.2f}",
                "Best Strike Rate",
                best_strike_rate["bowler"],
            ),
            unsafe_allow_html=True,
        )

    st.markdown("---")

    # Total wickets by bowler
    total_wickets = (
        data["wickets_total"].sort_values("total_wickets", ascending=False).head(10)
    )
    fig = plot_bar_chart(
        total_wickets,
        x="bowler",
        y="total_wickets",
        title="Total Wickets by Bowler",
        color="bowler",
        labels={"total_wickets": "Total Wickets", "bowler": "Bowler"},
        height=500,
    )
    fig.update_layout(xaxis_tickangle=-90)
    st.plotly_chart(fig, use_container_width=True)

    # Raw data
    st.markdown(
        '<div class="subheader">Raw Data: Total Wickets by Bowler</div>',
        unsafe_allow_html=True,
    )
    st.dataframe(
        total_wickets[["bowler", "total_wickets", "economy_rate", "strike_rate"]],
        use_container_width=True,
    )


def display_innings_tab(data):
    """Display content for the Innings Analysis tab"""
    st.markdown('<div class="subheader">Innings Analysis</div>', unsafe_allow_html=True)

    # Best bowling figures in an innings
    best_figures = (
        data["wickets_inning"]
        .sort_values(by=["total_wickets", "total_runs"], ascending=[False, True])
        .head(10)
    )
    best_figures = create_bowler_match_column(best_figures)

    # Create a combined metric for display
    best_figures["figures"] = (
        best_figures["total_wickets"].astype(str)
        + "/"
        + best_figures["total_runs"].astype(str)
    )

    category_order = best_figures["bowler_match"].tolist()

    fig = plot_bar_chart(
        best_figures,
        x="bowler_match",
        y="total_wickets",
        title="Best Bowling Figures in an Innings",
        color="bowler",
        hover_data=["total_runs", "overs"],
        labels={"total_wickets": "Wickets", "bowler_match": "Bowler"},
        height=500,
        category_order={"bowler_match": category_order},
    )
    fig.update_traces(
        hovertemplate="<b>%{x}</b><br>Wickets: %{y}<br>Runs: %{customdata[0]}<br>Overs: %{customdata[1]}<extra></extra>"
    )
    st.plotly_chart(fig, use_container_width=True)

    # Economy vs Strike Rate scatter plot
    st.markdown(
        '<div class="subheader">Economy Rate vs Strike Rate</div>',
        unsafe_allow_html=True,
    )
    fig = plot_economy_vs_strike_rate(data["wickets_total"])
    st.plotly_chart(fig, use_container_width=True)

    # Raw data
    st.markdown(
        '<div class="subheader">Best Bowling Figures Data</div>',
        unsafe_allow_html=True,
    )
    st.dataframe(
        best_figures[["bowler", "match_id", "total_wickets", "total_runs", "overs"]],
        use_container_width=True,
    )


def display_innings_tab(data):
    """Display content for the Innings Analysis tab"""
    st.markdown('<div class="subheader">Innings Analysis</div>', unsafe_allow_html=True)

    # Create a copy to avoid modifying the original data
    best_figures = (
        data["wickets_inning"]
        .sort_values(by=["total_wickets", "total_runs"], ascending=[False, True])
        .head(10)
        .copy()
    )  # Explicit copy here

    # Create new columns using .loc
    best_figures.loc[:, "bowler_match"] = (
        best_figures["bowler"] + " (" + best_figures["match_id"].astype(str) + ")"
    )
    best_figures.loc[:, "figures"] = (
        best_figures["total_wickets"].astype(str)
        + "/"
        + best_figures["total_runs"].astype(str)
    )

    category_order = best_figures["bowler_match"].tolist()

    fig = plot_bar_chart(
        best_figures,
        x="bowler_match",
        y="total_wickets",
        title="Best Bowling Figures in an Innings",
        color="bowler",
        hover_data=["total_runs", "overs"],
        labels={"total_wickets": "Wickets", "bowler_match": "Bowler"},
        height=500,
        category_order={"bowler_match": category_order},
    )
    fig.update_traces(
        hovertemplate="<b>%{x}</b><br>Wickets: %{y}<br>Runs: %{customdata[0]}<br>Overs: %{customdata[1]}<extra></extra>"
    )
    st.plotly_chart(fig, use_container_width=True)

    # Economy vs Strike Rate scatter plot
    st.markdown(
        '<div class="subheader">Economy Rate vs Strike Rate</div>',
        unsafe_allow_html=True,
    )
    fig = plot_economy_vs_strike_rate(data["wickets_total"])
    st.plotly_chart(fig, use_container_width=True)

    # Raw data
    st.markdown(
        '<div class="subheader">Best Bowling Figures Data</div>',
        unsafe_allow_html=True,
    )
    st.dataframe(
        best_figures[["bowler", "match_id", "total_wickets", "total_runs", "overs"]],
        use_container_width=True,
    )


def display_metrics_tab(data):
    """Display content for the Performance Metrics tab"""
    st.markdown(
        '<div class="subheader">Performance Metrics</div>', unsafe_allow_html=True
    )

    # Wickets distribution
    top_wicket_takers = (
        data["wickets_total"]
        .sort_values("total_wickets", ascending=False)
        .head(10)
        .copy()
    )
    st.plotly_chart(
        plot_pie_chart(
            top_wicket_takers,
            values="total_wickets",
            names="bowler",
            title="Wickets Distribution (Top 10)",
        ),
        use_container_width=True,
    )

    # 5-wicket hauls
    five_wicket_hauls = data["wickets_inning"][
        data["wickets_inning"]["total_wickets"] >= 5
    ].copy()
    if not five_wicket_hauls.empty:
        st.markdown(
            '<div class="subheader">5-Wicket Hauls</div>',
            unsafe_allow_html=True,
        )
        five_wicket_hauls.loc[:, "bowler_match"] = (
            five_wicket_hauls["bowler"]
            + " ("
            + five_wicket_hauls["match_id"].astype(str)
            + ")"
        )
        five_wicket_hauls.loc[:, "figures"] = (
            five_wicket_hauls["total_wickets"].astype(str)
            + "/"
            + five_wicket_hauls["total_runs"].astype(str)
        )

        fig = plot_bar_chart(
            five_wicket_hauls,
            x="bowler_match",
            y="total_wickets",
            title="5-Wicket Hauls",
            color="bowler",
            hover_data=["total_runs", "overs"],
            labels={"total_wickets": "Wickets", "bowler_match": "Bowler"},
            height=400,
        )
        st.plotly_chart(fig, use_container_width=True)

        st.dataframe(
            five_wicket_hauls[
                ["bowler", "match_id", "total_wickets", "total_runs", "overs"]
            ],
            use_container_width=True,
        )
    else:
        st.info("No 5-wicket hauls recorded")

    # 4-wicket hauls
    four_wicket_hauls = data["wickets_inning"][
        (data["wickets_inning"]["total_wickets"] >= 4)
        & (data["wickets_inning"]["total_wickets"] < 5)
    ].copy()
    if not four_wicket_hauls.empty:
        st.markdown(
            '<div class="subheader">4-Wicket Hauls</div>',
            unsafe_allow_html=True,
        )
        four_wicket_hauls.loc[:, "bowler_match"] = (
            four_wicket_hauls["bowler"]
            + " ("
            + four_wicket_hauls["match_id"].astype(str)
            + ")"
        )
        four_wicket_hauls.loc[:, "figures"] = (
            four_wicket_hauls["total_wickets"].astype(str)
            + "/"
            + four_wicket_hauls["total_runs"].astype(str)
        )

        fig = plot_bar_chart(
            four_wicket_hauls.sort_values("total_wickets", ascending=False),
            x="bowler_match",
            y="total_wickets",
            title="4-Wicket Hauls",
            color="bowler",
            hover_data=["total_runs", "overs"],
            labels={"total_wickets": "Wickets", "bowler_match": "Bowler"},
            height=400,
        )
        st.plotly_chart(fig, use_container_width=True)

        st.dataframe(
            four_wicket_hauls[
                ["bowler", "match_id", "total_wickets", "total_runs", "overs"]
            ],
            use_container_width=True,
        )
    else:
        st.info("No 4-wicket hauls recorded")


# --------------------------
# Main Function
# --------------------------


def bowler_analysis(response, team):
    """Main function to display bowling analysis dashboard"""
    try:
        apply_custom_css()
        data = response

        st.subheader(f"Bowling Statistics of {team}")

        # Create tabs
        tab1, tab2, tab3 = st.tabs(
            [
                "Overview",
                "Innings Analysis",
                "Performance Metrics",
            ]
        )

        with tab1:
            display_overview_tab(data)
        with tab2:
            display_innings_tab(data)
        with tab3:
            display_metrics_tab(data)

    except Exception as e:
        print("Error in bowling analysis:", traceback.print_exception(e))
        st.error(f"An error occurred: {e}")
        st.info("Please check your data format and try again.")
