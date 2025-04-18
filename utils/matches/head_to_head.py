def get_head_to_head_data(cnx, team1, team2):
    """Getting match data between the two teams

    Args:
        cnx (_type_): connection object
        team1 (_type_): team 1 name
        team2 (_type_): team 2 name

    Returns:
        _type_: dict
    """
    
    try:
        cursor = cnx.cursor()
        
        query = f"SELECT * FROM matches WHERE (team1 = '{team1}' AND team2 = '{team2}') OR (team1 = '{team2}' AND team2 = '{team1}');"
        cursor.execute(query)
        data = cursor.fetchall()
        data = [row[1:] for row in data]
        
        return {"status": True, "message": "Data Fetched Successfully", "data": data}
    
    except Exception as e:
        return {"status": False, "message": e, "data": []}
