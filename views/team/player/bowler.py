import pandas as pd


def get_bowler_wickets(bowler_df):
    wickets_total = (
        bowler_df[
            (bowler_df["is_wicket"] == 1) & (bowler_df.dismissal_kind != "run out")
        ]
        .groupby(["bowler"])["is_wicket"]
        .count()
        .reset_index()
    )
    wickets_total.rename(columns={"is_wicket": "total_wickets"}, inplace=True)

    runs_conceded = bowler_df.groupby(["bowler"])["total_runs"].sum().reset_index()

    balls_bowled = (
        bowler_df[bowler_df.extras_type.isnull()]
        .groupby(["bowler"])["ball"]
        .count()
        .reset_index()
    )
    balls_bowled["overs"] = balls_bowled["ball"] // 6 + (balls_bowled["ball"] % 6) / 10
    balls_bowled.rename(columns={"ball": "total_balls"}, inplace=True)

    wickets_runs_balls = pd.merge(
        wickets_total, runs_conceded, on=["bowler"], how="left"
    )
    wickets_runs_balls = pd.merge(
        wickets_runs_balls, balls_bowled, on=["bowler"], how="left"
    )
    wickets_runs_balls["strike_rate"] = round(
        wickets_runs_balls["total_runs"] / wickets_runs_balls["total_wickets"], 2
    )
    wickets_runs_balls["economy_rate"] = round(
        wickets_runs_balls["total_runs"] / wickets_runs_balls["overs"], 2
    )

    wickets_runs_balls_sorted = wickets_runs_balls.sort_values(
        by=["total_wickets", "economy_rate"], ascending=[False, True]
    )
    return wickets_runs_balls_sorted


def get_wicket_inning(bowler_df):
    wickets_total = (
        bowler_df[
            (bowler_df["is_wicket"] == 1) & (bowler_df["dismissal_kind"] != "run out")
        ]
        .groupby(["bowler", "match_id"])["is_wicket"]
        .count()
        .reset_index()
    )
    wickets_total.rename(columns={"is_wicket": "total_wickets"}, inplace=True)

    runs_conceded = (
        bowler_df.groupby(["bowler", "match_id"])["total_runs"].sum().reset_index()
    )

    balls_bowled = (
        bowler_df[bowler_df.extras_type.isnull()]
        .groupby(["bowler", "match_id"])["ball"]
        .count()
        .reset_index()
    )
    balls_bowled["overs"] = balls_bowled["ball"] // 6 + (balls_bowled["ball"] % 6) / 10
    balls_bowled.rename(columns={"ball": "total_balls"}, inplace=True)

    wickets_runs_balls = pd.merge(
        wickets_total, runs_conceded, on=["bowler", "match_id"], how="left"
    )
    wickets_runs_balls = pd.merge(
        wickets_runs_balls, balls_bowled, on=["bowler", "match_id"], how="left"
    )
    wickets_runs_balls["strike_rate"] = round(
        wickets_runs_balls["total_runs"] / wickets_runs_balls["total_wickets"], 2
    )
    wickets_runs_balls["economy_rate"] = round(
        wickets_runs_balls["total_runs"] / wickets_runs_balls["overs"], 2
    )

    wickets_runs_balls_sorted = wickets_runs_balls.sort_values(
        by=["total_wickets", "economy_rate"], ascending=[False, True]
    )
    return wickets_runs_balls_sorted
