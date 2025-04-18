import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns


def overall_analysis(data, team):
    st.write(f"Insights of {data['total_matches'].shape[0]} matches played by {team}")

    chart_data = {
        "Categories": ["Won", "Loss"],
        "Values": [data["matches_won"].shape[0], data["matches_lost"].shape[0]],
    }
    df_data = {
        "": ["Total matches played", "Won", "Loss"],
        "Overall Analysis": [
            data["total_matches"].shape[0],
            data["matches_won"].shape[0],
            data["matches_lost"].shape[0],
        ],
    }
    df = pd.DataFrame(chart_data)

    fig, ax = plt.subplots()
    ax.pie(df["Values"], labels=df["Categories"], autopct="%1.1f%%", startangle=90)
    ax.axis("equal")
    st.pyplot(fig)

    st.write(" ")
    st.write(
        f"Tabular Representation of {data['total_matches'].shape[0]} matches played by {team}"
    )
    st.dataframe(df_data)


def toss_analysis(response, team):
    st.write(f"Insights of {response['total_matches'].shape[0]} tosses held by {team}")

    # Create a 1x2 subplot layout
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))

    # Pie chart 1: Toss statistics
    toss_labels = ["Toss Won", "Toss Lost"]
    toss_sizes = [
        response["toss_analysis"]["toss_won"].shape[0],
        response["total_matches"].shape[0]
        - response["toss_analysis"]["toss_won"].shape[0],
    ]
    explode = (0.1, 0)  # explode the 1st slice

    ax1.pie(
        toss_sizes,
        explode=explode,
        labels=toss_labels,
        autopct="%1.1f%%",
        shadow=True,
        startangle=90,
        colors=["#4CAF50", "#ff6347"],
    )
    ax1.set_title("Toss Statistics", fontsize=14)

    # Pie chart 2: Match outcomes after winning toss
    outcome_labels = ["Match Won after Winning Toss", "Match Lost after Winning Toss"]
    outcome_sizes = [
        response["toss_analysis"]["toss_won_match_won"].shape[0],
        response["toss_analysis"]["toss_won"].shape[0]
        - response["toss_analysis"]["toss_won_match_won"].shape[0],
    ]
    explode = (0.1, 0)  # explode the 1st slice

    ax2.pie(
        outcome_sizes,
        explode=explode,
        labels=outcome_labels,
        autopct="%1.1f%%",
        shadow=True,
        startangle=90,
        colors=["#3776ab", "#e63946"],
    )
    ax2.set_title("Match Outcome when Toss was Won", fontsize=14)

    fig.suptitle(
        f"Statistics for {response['total_matches'].shape[0]} Total Matches",
        fontsize=16,
    )
    plt.tight_layout()

    # Display the figure in Streamlit
    st.pyplot(fig)


def overall_performance_team(data, team):
    """Creates and displays a pie chart in Streamlit."""

    overall_analysis(data, team)
