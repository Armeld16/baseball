from database.DB_connect import DBConnect
from model.team import Team


class DAO():

    @staticmethod
    def getAllYears():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT DISTINCT (t.`year`)
                    From teams t
                    where t.`year` >= 1980"""

        cursor.execute(query)

        for row in cursor:
            result.append(row["year"])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getTeamsOfYears(year):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT *
                    FROM teams t 
                    WHERE t.`year` = %s"""

        cursor.execute(query, (year,))

        for row in cursor:
            result.append(Team(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getSalariesOfTeam(year, idMapTeams):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT t.ID, t.teamCode, sum(s.salary) as totSalary
                    FROM salaries s , teams t , appearances a 
                    WHERE s.`year` = t.`year` AND t.`year` = a.`year` AND a.`year` = %s
                    AND t.ID = a.teamID AND a.playerID = s.playerID 
                    GROUP BY t.ID, t.teamCode 
                    """

        cursor.execute(query, (year,))

        MapSalary = {}

        for row in cursor:
            MapSalary[idMapTeams[row["ID"]]] = row["totSalary"]

        cursor.close()
        conn.close()
        return MapSalary

