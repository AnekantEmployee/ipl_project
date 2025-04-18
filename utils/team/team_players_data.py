def get_team_players_data(cnx):
    """Getting players from a team

    Args:
        cnx (_type_): connection object
        team (_type_): team name

    Returns:
        _type_: dict
    """

    try:
        cursor = cnx.cursor()

        query = f"SELECT * FROM deliveries;"
        cursor.execute(query)
        data = cursor.fetchall()
        data = [row for row in data]
        return {"status": True, "message": "Data Fetched Successfully", "data": data}

    except Exception as e:
        return {"status": False, "message": e, "data": []}
