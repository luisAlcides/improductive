import sqlite3
import datetime

from connection import Connection


class HabitModel:
    def __init__(self):
        self.success = False
        self.db = Connection()

    def insert_into_habits(self, category):
        sql_insert = """
            INSERT INTO category_habits(name, date_current)
            VALUES(?, ?)
        """
        current_time = datetime.datetime.now().strftime("%d-%m-%y")
        values = (category, current_time)

        with self.db as cursor:
            try:
                cursor.execute(sql_insert, values)
                self.success = True
            except sqlite3.IntegrityError as e:
                print("Error adding category:", e)
                self.success = False
            except Exception as e:
                print("Error adding category:", e)
                self.success = False

    def get_category_habits(self):
        try:
            with self.db as cursor:
                sql = "SELECT name FROM category_habits"
                cursor.execute(sql)
                category_habits = cursor.fetchall()
            return category_habits
        except Exception as e:
            print("Error getting category habits:", e)
            return []

    def fetch_monthly_data(self):
        with self.db as cursor:
            cursor.execute(
                """
                SELECT m.name AS month, SUM(h.study_time) AS total_study_time, IFNULL(g.goal, 0) AS goal, c.name AS habit_name
                FROM habit h
                JOIN category_habits c ON h.category_id = c.id
                LEFT JOIN goal g ON c.id = g.category_id AND strftime('%m', h.date_current) = g.month_id
                LEFT JOIN months m ON g.month_id = m.id
                GROUP BY m.name, c.name
            """
            )
            return self.clean_data(cursor.fetchall())

    def fetch_weekly_data(self):
        with self.db as cursor:
            cursor.execute(
                """
                SELECT strftime('%Y-%W', h.date_current) AS week, SUM(h.study_time) AS total_study_time, NULL AS goal, c.name AS habit_name
                FROM habit h
                JOIN category_habits c ON h.category_id = c.id
                GROUP BY week, c.name
            """
            )
            return self.clean_data(cursor.fetchall())

    def fetch_yearly_data(self):
        with self.db as cursor:
            cursor.execute(
                """
                SELECT strftime('%Y', h.date_current) AS year, SUM(h.study_time) AS total_study_time, NULL AS goal, c.name AS habit_name
                FROM habit h
                JOIN category_habits c ON h.category_id = c.id
                GROUP BY year, c.name
            """
            )
            return self.clean_data(cursor.fetchall())

    def fetch_data_by_month(self, month):
        with self.db as cursor:
            cursor.execute(
                """
                SELECT c.name AS habit_name, SUM(h.study_time) AS total_study_time
                FROM habit h
                JOIN category_habits c ON h.category_id = c.id
                WHERE strftime('%m', h.date_current) = ?
                GROUP BY c.name
            """,
                (month,),
            )
            return self.clean_data(cursor.fetchall())

    def was_successful(self):
        return self.success

    def clean_data(self, data):
        return [row for row in data if all(col is not None for col in row)]
