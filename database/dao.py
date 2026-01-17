from database.DB_connect import DBConnect
from model.team import Team


class DAO:

    @staticmethod
    def get_teams(year):
        conn = DBConnect.get_connection()
        result = []

        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT t.id, t.year, t.team_code
            FROM team t
            WHERE t.year = %s
            ORDER BY t.team_code
        """

        cursor.execute(query, (year,))
        for row in cursor:
            result.append(Team(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_years_from_1980():
        conn = DBConnect.get_connection()
        result = []

        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT DISTINCT year
            FROM team
            WHERE year >= 1980
            ORDER BY year
        """

        cursor.execute(query)
        for row in cursor:
            result.append(row["year"])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_team_salary(year):

        conn = DBConnect.get_connection()
        result = {}

        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT s.team_code, SUM(s.salary) AS total
            FROM salary s
            WHERE s.year = %s
            GROUP BY s.team_code
        """

        cursor.execute(query, (year,))
        for row in cursor:
            result[row["team_code"]] = row["total"]

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_all_coppie(year):

        conn = DBConnect.get_connection()
        result = []

        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT t1.id AS id1, t2.id AS id2
            FROM team t1, team t2
            WHERE t1.year = %s
              AND t2.year = %s
              AND t1.id < t2.id
        """

        cursor.execute(query, (year, year))
        for row in cursor:
            result.append((row["id1"], row["id2"]))

        cursor.close()
        conn.close()
        return result
