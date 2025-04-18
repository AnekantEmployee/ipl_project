def get_fours_total(batter_df):
    fours_total = (
        batter_df[batter_df["batsman_runs"] == 4]
        .groupby(["batter"])["batsman_runs"]
        .count()
        .reset_index()
    )
    fours_total = fours_total.sort_values(by="batsman_runs", ascending=False).head(10)
    fours_total.rename(columns={"batsman_runs": "total_fours"}, inplace=True)
    return fours_total


def get_four_inning(batter_df):
    four_inning = (
        batter_df[batter_df["batsman_runs"] == 4]
        .groupby(["batter", "match_id"])["batsman_runs"]
        .count()
        .reset_index()
    )
    four_inning = four_inning.sort_values(by="batsman_runs", ascending=False).head(10)
    four_inning.rename(columns={"batsman_runs": "total_fours"}, inplace=True)
    return four_inning


def get_total_sixes(batter_df):
    sixes_total = (
        batter_df[batter_df["batsman_runs"] == 6]
        .groupby(["batter"])["batsman_runs"]
        .count()
        .reset_index()
    )
    sixes_total = sixes_total.sort_values(by="batsman_runs", ascending=False).head(10)
    sixes_total.rename(columns={"batsman_runs": "total_sixes"}, inplace=True)
    return sixes_total


def get_sixes_inning(batter_df):
    sixes_inning = (
        batter_df[batter_df["batsman_runs"] == 6]
        .groupby(["batter", "match_id"])["batsman_runs"]
        .count()
        .reset_index()
    )
    sixes_inning = sixes_inning.sort_values(by="batsman_runs", ascending=False).head(10)
    sixes_inning.rename(columns={"batsman_runs": "total_sixes"}, inplace=True)
    return sixes_inning


def get_highest_score_inning(batter_df):
    highest_score = batter_df.groupby(["batter"])["batsman_runs"].sum().reset_index()
    highest_score_sorted = highest_score.sort_values(
        by="batsman_runs", ascending=False
    ).head(10)
    return highest_score_sorted


def get_total_runs(batter_df):
    highest_score = (
        batter_df.groupby(["batter", "match_id"])["batsman_runs"].sum().reset_index()
    )
    highest_score_sorted = highest_score.sort_values(
        by="batsman_runs", ascending=False
    ).head(10)

    balls_faced = (
        batter_df[(batter_df.extras_type != "wides")]
        .groupby(["match_id", "batter"])["ball"]
        .count()
        .reset_index()
    )
    highest_score_with_balls = pd.merge(
        highest_score_sorted, balls_faced, on=["batter", "match_id"], how="left"
    )
    highest_score_with_balls["strike_rate"] = round(
        (highest_score_with_balls["batsman_runs"] / highest_score_with_balls["ball"])
        * 100,
        2,
    )
    return highest_score_with_balls


def get_fifties(batter_df):
    fifty_scored = (
        batter_df.groupby(["batter", "match_id"])["batsman_runs"].sum().reset_index()
    )
    fifty_scored_sorted = fifty_scored[
        (fifty_scored.batsman_runs >= 50) & (fifty_scored.batsman_runs < 100)
    ]
    fifty_scored_sorted = (
        fifty_scored_sorted.groupby("batter", as_index=False)
        .count()
        .sort_values("batsman_runs", ascending=False)
    )
    return fifty_scored_sorted


def get_centuries(batter_df):
    century_scored = (
        batter_df.groupby(["batter", "match_id"])["batsman_runs"].sum().reset_index()
    )
    century_scored_sorted = century_scored[(century_scored.batsman_runs >= 100)]
    century_scored_sorted = (
        century_scored_sorted.groupby("batter", as_index=False)
        .count()
        .sort_values("batsman_runs", ascending=False)
    )
    return century_scored_sorted
