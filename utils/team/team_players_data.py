# def get_team_players_data(cnx):
#     """Getting players from a team

#     Args:
#         cnx (_type_): connection object
#         team (_type_): team name

#     Returns:
#         _type_: dict
#     """

#     try:
#         cursor = cnx.cursor()

#         query = f"SELECT * FROM deliveries;"
#         cursor.execute(query)
#         data = cursor.fetchall()
#         data = [row for row in data]
#         return {"status": True, "message": "Data Fetched Successfully", "data": data}

#     except Exception as e:
#         return {"status": False, "message": e, "data": []}


def get_team_players_data(cnx, team1, team2):
    """Getting players from a team

    Args:
        cnx (_type_): connection object
        team (_type_): team name

    Returns:
        _type_: dict
    """

    try:
        cursor = cnx.cursor()

        query = f"SELECT * FROM deliveries INNER JOIN matches ON deliveries.match_id = matches.id WHERE (matches.team1 = '{team1}' AND matches.team2 = '{team2}') OR (matches.team1 = '{team2}' AND matches.team2 = '{team1}');"
        cursor.execute(query)
        data = cursor.fetchall()
        data = [row for row in data]
        return {"status": True, "message": "Data Fetched Successfully", "data": data}

    except Exception as e:
        return {"status": False, "message": e, "data": []}
