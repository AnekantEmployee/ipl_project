import streamlit as st
import matplotlib.pyplot as plt


def toss_analysis(response, team):
    st.write(f"Insights of {response['total_matches'].shape[0]} tosses held by {team}")

    # First pie chart: Toss statistics
    st.subheader("Toss Statistics")
    fig1, ax1 = plt.subplots(figsize=(10, 6))

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
    ax1.set_title(
        f"Toss Win/Loss Distribution ({response['total_matches'].shape[0]} matches)"
    )

    # Display the first pie chart
    st.pyplot(fig1)

    # Second pie chart: Match outcomes after winning toss
    st.subheader("Match Outcome When Toss Was Won")
    fig2, ax2 = plt.subplots(figsize=(10, 6))

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
    ax2.set_title(
        f"Match Outcome After Winning Toss ({response['toss_analysis']['toss_won'].shape[0]} toss wins)"
    )

    # Display the second pie chart
    st.pyplot(fig2)

    # Third pie chart: Match outcomes after losing toss
    st.subheader("Match Outcome When Toss Was Lost")
    fig3, ax3 = plt.subplots(figsize=(10, 6))

    # Calculate toss losses
    toss_losses = (
        response["total_matches"].shape[0]
        - response["toss_analysis"]["toss_won"].shape[0]
    )

    loss_outcome_labels = [
        "Match Won after Losing Toss",
        "Match Lost after Losing Toss",
    ]
    loss_outcome_sizes = [
        response["toss_analysis"]["toss_loss_match_won"].shape[0],
        toss_losses - response["toss_analysis"]["toss_loss_match_won"].shape[0],
    ]
    explode = (0.1, 0)  # explode the 1st slice

    ax3.pie(
        loss_outcome_sizes,
        explode=explode,
        labels=loss_outcome_labels,
        autopct="%1.1f%%",
        shadow=True,
        startangle=90,
        colors=["#2ca02c", "#d62728"],
    )
    ax3.set_title(f"Match Outcome After Losing Toss ({toss_losses} toss losses)")

    # Display the third pie chart
    st.pyplot(fig3)
