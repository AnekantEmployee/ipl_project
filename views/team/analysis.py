import pandas as pd

from constants import MATCHES_COL, PLAYERS_COL
from utils import (
    get_team_data,
    get_team_players_data,
)
from .player.batter import *
from .player.bowler import *


def my_func(x):
    if x["winner"] == x["toss_winner"]:
        return (
            x["target_runs"]
            if x["result"] != "runs"
            else x["target_runs"] + x["result_margin"]
        )
    else:
        return (x["target_runs"] - x["result_margin"]) - 1


def get_actual_score(x):
    if x["winner"] != x["toss_winner"]:
        return x["target_runs"] if x["result"] != "runs" else 0
    else:
        return x["target_runs"] - x["result_margin"] - 1 if x["result"] == "runs" else 0


def get_players_analysis(df, team):
    most_player_of_match = df["player_of_match"].value_counts()[:5]

    batter_df = df[
        (
            (df["toss_winner"] != team)
            & (df["toss_decision"] == "bat")
            & (df["inning"] == 2)
        )
        | (
            (df["toss_winner"] != team)
            & (df["toss_decision"] == "field")
            & (df["inning"] == 1)
        )
        | (
            (df["toss_winner"] == team)
            & (df["toss_decision"] == "field")
            & (df["inning"] == 2)
        )
        | (
            (df["toss_winner"] == team)
            & (df["toss_decision"] == "bat")
            & (df["inning"] == 1)
        )
    ]
    bowler_df = df[
        (
            (df["toss_winner"] != team)
            & (df["toss_decision"] == "bat")
            & (df["inning"] == 1)
        )
        | (
            (df["toss_winner"] != team)
            & (df["toss_decision"] == "field")
            & (df["inning"] == 2)
        )
        | (
            (df["toss_winner"] == team)
            & (df["toss_decision"] == "field")
            & (df["inning"] == 1)
        )
        | (
            (df["toss_winner"] == team)
            & (df["toss_decision"] == "bat")
            & (df["inning"] == 2)
        )
    ]

    batter_analysis = {
        "total_fours": get_fours_total(batter_df),
        "fours_inning": get_four_inning(batter_df),
        "total_sixes": get_total_sixes(batter_df),
        "sixes_inning": get_sixes_inning(batter_df),
        "highest_score_inning": get_highest_score_inning(batter_df),
        "total_runs": get_total_runs(batter_df),
        "fifties": get_fifties(batter_df),
        "centuries": get_centuries(batter_df),
    }
    bowler_analysis = {
        "wickets_total": get_bowler_wickets(bowler_df),
        "wickets_inning": get_wicket_inning(bowler_df),
    }

    return {
        "most_player_of_match": most_player_of_match,
        "batter_analysis": batter_analysis,
        "bowler_analysis": bowler_analysis,
    }


def get_highest_score(df, team):
    result = {}

    # Check if filtered DataFrame has rows before accessing iloc[0]
    toss_won_bat_df = df[
        (df["toss_winner"] == team) & (df["toss_decision"] == "bat")
    ].sort_values(by="target_runs", ascending=False)
    if not toss_won_bat_df.empty:
        result["toss_won_bat"] = toss_won_bat_df.iloc[0]

    df["actual_runs"] = df[
        (df["toss_winner"] == team) & (df["toss_decision"] == "field")
    ].apply(my_func, axis=1)
    toss_won_field_df = df.sort_values(by="actual_runs", ascending=False)
    if not toss_won_field_df.empty:
        result["toss_won_field"] = toss_won_field_df.iloc[0]

    toss_loss_bat_df = df[
        (df["toss_winner"] != team)
        & (df["toss_decision"] == "field")
        & (df["result"] == "runs")
    ].sort_values(by="target_runs", ascending=False)
    if not toss_loss_bat_df.empty:
        result["toss_loss_bat"] = toss_loss_bat_df.iloc[0]

    df["actual_runs"] = df[
        (df["toss_winner"] != team) & (df["toss_decision"] == "bat")
    ].apply(get_actual_score, axis=1)
    toss_loss_field_df = df.sort_values(by="actual_runs", ascending=False)
    if not toss_loss_field_df.empty:
        result["toss_loss_field"] = toss_loss_field_df.iloc[0]

    return result


def get_lowest_score(df, team):
    result = {}

    # Check if filtered DataFrame has rows before accessing iloc[0]
    toss_won_bat_df = df[
        (df["toss_winner"] == team) & (df["toss_decision"] == "bat")
    ].sort_values(
        by="target_runs", ascending=True
    )  # Changed to ascending=True
    if not toss_won_bat_df.empty:
        result["toss_won_bat"] = toss_won_bat_df.iloc[0]

    df["actual_runs"] = df[
        (df["toss_winner"] == team) & (df["toss_decision"] == "field")
    ].apply(my_func, axis=1)
    toss_won_field_df = df.sort_values(by="actual_runs", ascending=True)
    if not toss_won_field_df.empty:
        result["toss_won_field"] = toss_won_field_df.iloc[0]

    toss_loss_bat_df = df[
        (df["toss_winner"] != team)
        & (df["toss_decision"] == "field")
        & (df["result"] == "runs")
    ].sort_values(by="target_runs", ascending=True)
    if not toss_loss_bat_df.empty:
        result["toss_loss_bat"] = toss_loss_bat_df.iloc[0]

    df["actual_runs"] = df[
        (df["toss_winner"] != team) & (df["toss_decision"] == "bat")
    ].apply(get_actual_score, axis=1)
    toss_loss_field_df = df.sort_values(by="actual_runs", ascending=True)
    if not toss_loss_field_df.empty:
        result["toss_loss_field"] = toss_loss_field_df.iloc[0]

    return result


def get_team_analysis(cnx, team, season):
    data = get_team_data(cnx, team)
    player_data = get_team_players_data(cnx)

    df = pd.DataFrame(data["data"], columns=MATCHES_COL)
    df.rename(columns={"id": "match_id"}, inplace=True)

    batter_df = pd.DataFrame(player_data["data"], columns=PLAYERS_COL)
    batter_df = pd.merge(df, batter_df, on="match_id")
    batter_df = batter_df[(batter_df["team1"] == team) | (batter_df["team2"] == team)]

    if season != "All Seasons":
        df = df[df["season"] >= season]
        batter_df = batter_df[(batter_df["season"] >= season)]

    df.to_csv("views/team/team_analysis.csv")
    batter_df.to_csv("views/team/batter_analysis.csv")

    matches_won = df[df["winner"] == team]
    matches_lost = df[df["winner"] != team]

    home_won_by_team = len(df[(df["winner"] == team) & (df["city"] == "Bangalore")])
    home_loss_by_team = len(df[(df["winner"] != team) & (df["city"] == "Bangalore")])
    away_won_by_team = len(df[(df["winner"] == team) & (df["city"] != "Bangalore")])
    away_loss_by_team = len(df[(df["winner"] != team) & (df["city"] != "Bangalore")])
    home_away = {
        "home_won_by_team": home_won_by_team,
        "home_loss_by_team": home_loss_by_team,
        "away_won_by_team": away_won_by_team,
        "away_loss_by_team": away_loss_by_team,
    }

    toss_won = df[df["toss_winner"] == team]
    toss_won_match_won = df[(df["toss_winner"] == team) & (df["winner"] == team)]
    toss_loss_match_won = df[(df["toss_winner"] != team) & (df["winner"] == team)]
    toss_analysis = {
        "toss_won": toss_won,
        "toss_won_match_won": toss_won_match_won,
        "toss_loss_match_won": toss_loss_match_won,
    }

    total_super_over = df[(df["super_over"] == "Y")]
    total_super_over_won = df[(df["super_over"] == "Y") & (df["winner"] == team)]
    super_over_analysis = {
        "total_super_over": total_super_over,
        "total_super_over_won": total_super_over_won,
    }

    final_matches = df[(df["match_type"] != "League") & (df["match_type"] == "Final")]
    final_matches_won = df[
        (df["match_type"] != "League")
        & (df["match_type"] == "Final")
        & (df["winner"] == team)
    ]
    non_final_matches = df[
        (df["match_type"] != "League") & (df["match_type"] != "Final")
    ]

    team_response = {
        "total_matches": df,
        "matches_won": matches_won,
        "matches_lost": matches_lost,
        "home_away": home_away,
        "toss_analysis": toss_analysis,
        "highest_score": get_highest_score(df, team),
        "lowest_score": get_lowest_score(df, team),
        "super_over_analysis": super_over_analysis,
        "final_matches_won": final_matches_won,
        "final_matches": final_matches,
        "non_final_matches": non_final_matches,
        "players_analysis": get_players_analysis(batter_df, team),
    }
    return team_response
