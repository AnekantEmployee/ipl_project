import streamlit as st
import matplotlib.pyplot as plt


def super_over_analysis(response, team):
    if "total_super_over" in response and response["total_super_over"].shape[0] != 0:
        st.write(
            f"Insights of {response['total_super_over'].shape[0]} super over played by {team}"
        )

        # First pie chart: Toss statistics
        st.subheader("Super Over Analysis")
        fig1, ax1 = plt.subplots(figsize=(10, 6))

        toss_labels = ["Super Over Won", "Super Over Lost"]
        toss_sizes = [
            response["total_super_over_won"].shape[0],
            response["total_super_over"].shape[0]
            - response["total_super_over_won"].shape[0],
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
            f"Super Over Win/Loss Distribution ({response['total_super_over'].shape[0]} matches)"
        )

        # Display the first pie chart
        st.pyplot(fig1)

        st.write(
            f"Tabular Representation of {response['total_super_over'].shape[0]} super over played by {team}"
        )
        st.write(
            response["total_super_over"][
                ["season", "city", "venue", "team1", "team2", "winner"]
            ].sort_values(by="winner")
        )
    else:
        st.error("No Data to Display")
