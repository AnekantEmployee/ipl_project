def get_team_data(cnx, team):
    """Getting matches from a team

    Args:
        cnx (_type_): connection object
        team (_type_): team name

    Returns:
        _type_: dict
    """

    try:
        cursor = cnx.cursor()

        query = f"SELECT * FROM matches WHERE (team1 = '{team}' OR team2 = '{team}');"
        cursor.execute(query)
        data = cursor.fetchall()
        data = [row[1:] for row in data]
        return {"status": True, "message": "Data Fetched Successfully", "data": data}

    except Exception as e:
        return {"status": False, "message": e, "data": []}
