import traceback
import streamlit as st


def showing_insight(response, key, str):
    if key in response and response[key].shape[0] != 0:
        st.subheader(f"{str} ({response[key].shape[0]})")
        st.write(response[key])


def non_league_matches(response, team):
    try:
        showing_insight(response, "final_matches_won", "IPL Trophies")
        showing_insight(response, "final_matches", "Finals Played")
        showing_insight(response, "non_final_matches", "Qualifiers & Semis Played")
    except Exception as e:
        print(traceback(e))
