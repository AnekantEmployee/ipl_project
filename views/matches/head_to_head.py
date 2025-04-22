import pandas as pd
import streamlit as st

from utils import get_head_to_head_data
from constants import MATCHES_COL, PLAYERS_COL
from utils import get_team_players_data


def get_home(team_name):
    franchise_home_cities = {
        "Royal Challengers Bangalore": "Bangalore",
        "Punjab Kings": "Chandigarh",
        "Delhi Capitals": "Delhi",
        "Mumbai Indians": "Mumbai",
        "Kolkata Knight Riders": "Kolkata",
        "Rajasthan Royals": "Jaipur",
        "Deccan Chargers": "Hyderabad",
        "Chennai Super Kings": "Chennai",
        "Kochi Tuskers Kerala": "Kochi",
        "Pune Warriors": "Pune",
        "Sunrisers Hyderabad": "Hyderabad",
        "Gujarat Lions": "Rajkot",
        "Rising Pune Supergiants": "Pune",
        "Lucknow Super Giants": "Lucknow",
        "Gujarat Titans": "Ahmedabad",
    }
    return franchise_home_cities[team_name]


def get_head_to_head_analysis(data, player_response, team1, team2, season):
    df = pd.DataFrame(data, columns=MATCHES_COL)
    player_df = pd.DataFrame(
        player_response["data"], columns=PLAYERS_COL + ["match_id"] + MATCHES_COL
    )

    if season != "All Seasons":
        df = df[df["season"] >= season]
        player_df = player_df[player_df["season"] >= season]

    df.to_csv("views/matches/head_to_head.csv")
    player_df.to_csv("views/matches/players.csv")

    # Overall analysis
    overall_analysis = {
        "total_matches_played": len(df),
        "won_by_team1": len(df[df["winner"] == team1]),
        "won_by_team2": len(df[df["winner"] == team2]),
        "drawn": len(df[df["winner"].isnull()]),
        "won_dataframe_team1": df[df["winner"] == team1][
            [
                "season",
                "city",
                "date",
                "match_type",
                "player_of_match",
                "venue",
                "toss_winner",
            ]
        ],
        "won_dataframe_team2": df[df["winner"] == team2][
            [
                "season",
                "city",
                "date",
                "match_type",
                "player_of_match",
                "venue",
                "toss_winner",
            ]
        ],
    }

    # Home & Away Analysis
    home_won_by_team1 = len(
        df[(df["winner"] == team1) & (df["city"] == get_home(team1))]
    )
    home_loss_by_team1 = len(
        df[(df["winner"] == team2) & (df["city"] == get_home(team1))]
    )
    away_won_by_team1 = len(
        df[(df["winner"] == team1) & (df["city"] != get_home(team1))]
    )
    away_loss_by_team1 = len(
        df[(df["winner"] == team2) & (df["city"] != get_home(team1))]
    )

    home_won_by_team2 = len(
        df[(df["winner"] == team2) & (df["city"] == get_home(team2))]
    )
    home_loss_by_team2 = len(
        df[(df["winner"] == team1) & (df["city"] == get_home(team2))]
    )
    away_won_by_team2 = len(
        df[(df["winner"] == team2) & (df["city"] != get_home(team2))]
    )
    away_loss_by_team2 = len(
        df[(df["winner"] == team1) & (df["city"] != get_home(team2))]
    )

    home_away_data = {
        "team1": {
            "home_wins": home_won_by_team1,
            "home_losses": home_loss_by_team1,
            "away_wins": away_won_by_team1,
            "away_losses": away_loss_by_team1,
        },
        "team2": {
            "home_wins": home_won_by_team2,
            "home_losses": home_loss_by_team2,
            "away_wins": away_won_by_team2,
            "away_losses": away_loss_by_team2,
        },
    }

    # Match Statistics
    # highest_win_by_team1 = (
    #     df[(df["winner"] == team1) & (df["result"] == "runs")]
    #     .sort_values(by="result_margin", ascending=False)
    #     .iloc[0]["result_margin"]
    # )
    # highest_win_by_team2 = (
    #     df[(df["winner"] == team2) & (df["result"] == "runs")]
    #     .sort_values(by="result_margin", ascending=False)
    #     .iloc[0]["result_margin"]
    # )

    match_statistics = {
        "highest_win_by_team1": 0,
        "highest_win_by_team2": 0,
    }

    return {
        "overall_analysis": overall_analysis,
        "home_away_data": home_away_data,
        "match_statistics": match_statistics,
    }


def head_to_head_insights(cnx, team1, team2, season):

    if team1 == team2:
        return {"status": False, "message": "Teams are the same", "data": []}

    response = get_head_to_head_data(cnx, team1, team2)
    player_response = get_team_players_data(cnx, team1, team2)

    try:

        if response["status"] == False:
            return response
        else:
            insights = get_head_to_head_analysis(
                response["data"], player_response, team1, team2, season
            )
            return {
                "status": True,
                "message": "Insights fetched successfully",
                "data": insights,
            }
    except Exception as e:
        return {"status": False, "message": e, "data": []}
