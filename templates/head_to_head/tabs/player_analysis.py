import streamlit as st

def matches_statistics(data, team1, team2):
    """Creates and displays a match analysis."""
    df_data = {
        "": [f"Highest Win by {team1}", f"Highest Win by {team2}"],
        "Values": [data["highest_win_by_team1"], data["highest_win_by_team2"]],
    }
    # st.write(f"Tabular Representation of {team_name} played at Home & Away")
    st.dataframe(df_data)
