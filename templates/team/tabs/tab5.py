import traceback
import streamlit as st


def showing_insight(response, key):
    if key in response and response[key].shape[0] != 0:
        st.subheader(f"IPL Trophies ({response[key].shape[0]})")
        st.write(response[key])


def non_league_matches(response, team):
    try:
        showing_insight(response, "final_matches_won")
        showing_insight(response, "final_matches")
        showing_insight(response, "non_final_matches")
    except Exception as e:
        print(traceback(e))
