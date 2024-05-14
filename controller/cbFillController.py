import sqlite3
import datetime
from connection import Connection


class CbFillController:
    def __init__(self):
        self.con = Connection()

    def load_category_habit(self):
        with self.con as cursor:
            query = '''SELECT name FROM category_habits'''
            res = cursor.execute(query)
            categories = res.fetchall()
            return categories

    def load_months(self):
        with self.con as cursor:
            query = '''SELECT name FROM months'''
            res = cursor.execute(query)
            months = res.fetchall()
            return months

    def get_current_month(self):
        return datetime.datetime.now().strftime('%B')
