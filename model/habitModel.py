import sqlite3
import datetime

from connection import Connection


class HabitModel:
    def __init__(self):
        self.success = False
        self.db = Connection()

    def insert_into_habits(self, category):
        sql_insert = '''
            INSERT INTO category_habits(name, date_current)
            VALUES(?, ?)
        '''
        current_time = datetime.datetime.now().strftime('%d-%m-%y')
        values = (category, current_time)

        with self.db as cursor:
            try:
                cursor.execute(sql_insert, values)
                self.success = True
            except sqlite3.IntegrityError as e:
                print('Error adding category:', e)
                self.success = False
            except Exception as e:
                print('Error adding category:', e)
                self.success = False

    def get_category_habits(self):
        try:
            with self.db as cursor:
                sql = 'SELECT name FROM category_habits'
                cursor.execute(sql)
                category_habits = cursor.fetchall()
            return category_habits
        except Exception as e:
            print('Error getting category habits:', e)
            return []

    def was_successful(self):
        return self.success
