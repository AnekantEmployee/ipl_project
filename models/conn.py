import pymysql
import time
import os


def connect_to_db():
    try:
        print("Attempting to connect...")
        start_time = time.time()

        # Using PyMySQL instead of mysql.connector
        cnx = pymysql.connect(
            host=os.getenv("HOST"),
            port=int(os.getenv("PORT")),
            user=os.getenv("USER"),
            password=os.getenv("PASSWORD"),
            database=os.getenv("DB"),
            connect_timeout=5,  # Timeout in seconds
        )

        print(f"Connection established in {time.time() - start_time:.2f} seconds")

        """Converting all the team names to single ones"""
        # cursor = cnx.cursor()
        # cursor.execute("SELECT DISTINCT(team1) FROM matches")
        # print(cursor.fetchall())

        # cursor.execute("UPDATE matches SET team1 = 'Royal Challengers Bangalore' WHERE team1 = 'Royal Challengers Bengaluru'")
        # cursor.execute("UPDATE matches SET team2 = 'Royal Challengers Bangalore' WHERE team2 = 'Royal Challengers Bengaluru'")
        # cursor.execute("UPDATE matches SET toss_winner = 'Royal Challengers Bangalore' WHERE toss_winner = 'Royal Challengers Bengaluru'")
        # cursor.execute("UPDATE matches SET winner = 'Royal Challengers Bangalore' WHERE winner = 'Royal Challengers Bengaluru'")

        # cursor.execute("UPDATE matches SET team1 = 'Punjab Kings' WHERE team1 = 'Kings XI Punjab'")
        # cursor.execute("UPDATE matches SET team2 = 'Punjab Kings' WHERE team2 = 'Kings XI Punjab'")
        # cursor.execute("UPDATE matches SET toss_winner = 'Punjab Kings' WHERE toss_winner = 'Kings XI Punjab'")
        # cursor.execute("UPDATE matches SET winner = 'Punjab Kings' WHERE winner = 'Kings XI Punjab'")

        # cursor.execute("UPDATE matches SET team1 = 'Rising Pune Supergiants' WHERE team1 = 'Rising Pune Supergiant'")
        # cursor.execute("UPDATE matches SET team2 = 'Rising Pune Supergiants' WHERE team2 = 'Rising Pune Supergiant'")
        # cursor.execute("UPDATE matches SET toss_winner = 'Rising Pune Supergiants' WHERE toss_winner = 'Rising Pune Supergiant'")
        # cursor.execute("UPDATE matches SET winner = 'Rising Pune Supergiants' WHERE winner = 'Rising Pune Supergiant'")

        # cursor.execute("UPDATE matches SET team1 = 'Delhi Capitals' WHERE team1 = 'Delhi Daredevils'")
        # cursor.execute("UPDATE matches SET team2 = 'Delhi Capitals' WHERE team2 = 'Delhi Daredevils'")
        # cursor.execute("UPDATE matches SET toss_winner = 'Delhi Capitals' WHERE toss_winner = 'Delhi Daredevils'")
        # cursor.execute("UPDATE matches SET winner = 'Delhi Capitals' WHERE winner = 'Delhi Daredevils'")

        # cnx.commit()

        # cursor.execute("SELECT DISTINCT(team1) FROM matches")
        # print(cursor.fetchall())

        return cnx

    except pymysql.Error as err:
        print(f"PyMySQL Error: {err}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
