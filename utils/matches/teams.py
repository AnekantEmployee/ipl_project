def get_teams(cnx):
    """Fetching distinct teams from the database.

    Args:
        cnx (_type_): connection

    Returns:
        dict: distinct teams response
    """

    try:
        cursor = cnx.cursor()
        cursor.execute("SELECT DISTINCT(team1) FROM matches")
        teams_data = cursor.fetchall()
        teams_data = [team[0] for team in teams_data]

        return {"status": True, "message": "Teams data fetched", "data": teams_data}

    except Exception as e:
        return {"status": False, "message": e, "data": []}
