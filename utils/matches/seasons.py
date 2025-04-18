def get_seasons(cnx):
    """Fetching distinct teams from the database.

    Args:
        cnx (_type_): connection

    Returns:
        dict: distinct teams response
    """

    try:
        cursor = cnx.cursor()
        cursor.execute("SELECT DISTINCT(season) FROM matches")
        seasons_data = cursor.fetchall()
        seasons_data = [season[0] for season in seasons_data]

        return {"status": True, "message": "Seasons data fetched", "data": seasons_data}

    except Exception as e:
        return {"status": False, "message": e, "data": []}
