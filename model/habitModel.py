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

    def execute_query(self, query, params=()):
        try:
            with self.db as cursor:
                cursor.execute(query, params)
                return cursor.fetchall()

        except Exception as e:
            print("Error executing query:", e)
            return []

    def get_monthly_data(self):
        today = datetime.date.today()
        start_of_month = today.replace(day=1)
        end_of_month = (start_of_month + datetime.timedelta(days=32)).replace(
            day=1
        ) - datetime.timedelta(days=1)

        query = """
        SELECT ch.name, SUM(h.study_time) as study_time, g.goal, ch.name
        FROM habit h
        JOIN category_habits ch ON h.category_id = ch.id
        LEFT JOIN goal g ON h.category_id = g.category_id
        WHERE DATE(h.date_current) BETWEEN DATE(?) AND DATE(?)
        GROUP BY ch.name
        """
        return self.execute_query(query, (start_of_month, end_of_month))

    def get_weekly_data(self):
        today = datetime.date.today()
        start_of_week = today - datetime.timedelta(days=today.weekday())
        end_of_week = start_of_week + datetime.timedelta(days=6)

        query = """
        SELECT ch.name, SUM(h.study_time) as study_time, g.goal, ch.name
        FROM habit h
        JOIN category_habits ch ON h.category_id = ch.id
        LEFT JOIN goal g ON h.category_id = g.category_id
        WHERE DATE(h.date_current) BETWEEN DATE(?) AND DATE(?)
        GROUP BY ch.name
        """
        return self.execute_query(query, (start_of_week, end_of_week))

    def get_yearly_data(self):
        today = datetime.date.today()
        start_of_year = today.replace(month=1, day=1)
        end_of_year = today.replace(month=12, day=31)

        query = """
        SELECT ch.name, SUM(h.study_time) as study_time, g.goal, ch.name
        FROM habit h
        JOIN category_habits ch ON h.category_id = ch.id
        LEFT JOIN goal g ON h.category_id = g.category_id
        WHERE DATE(h.date_current) BETWEEN DATE(?) AND DATE(?)
        GROUP BY ch.name
        """
        return self.execute_query(query, (start_of_year, end_of_year))

    def get_data_by_month(self, month):
        query = """
        SELECT ch.name, SUM(h.study_time) as study_time, g.goal, ch.name
        FROM habit h
        JOIN category_habits ch ON h.category_id = ch.id
        LEFT JOIN goal g ON h.category_id = g.category_id
        JOIN months m ON g.month_id = m.id
        WHERE m.name = ?
        GROUP BY ch.name
        """
        return self.execute_query(query, (month,))

    def was_successful(self):
        return self.success

    def clean_data(self, data):
        return [row for row in data if all(col is not None for col in row)]
