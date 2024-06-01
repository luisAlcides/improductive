import sqlite3
import datetime

from connection import Connection
from utils.func import add_to_table


class AddHabitTimeController:
    def __init__(self):
        self.con = Connection()
        self.success = False

    def get_category_id(self, name_habit):
        try:
            with self.con as cursor:
                sql = 'SELECT id FROM category_habits WHERE name = ?'
                cursor.execute(sql, (name_habit,))
                category_id = cursor.fetchone()
                return category_id[0]
        except Exception as e:
            print('Error getting category id:', e)
            return None

    def add_habit(self, model):
        try:
            category_id = self.get_category_id(model.name_habit)
            study_time = float(model.study_time)/60
            current_time = datetime.datetime.now().strftime('%d-%m-%y')
            with self.con as cursor:
                sql_check = '''SELECT * FROM habit WHERE category_id = ? AND date_current = ?'''
                cursor.execute(sql_check, (category_id, current_time))
                existeing_habit = cursor.fetchone()

            if existeing_habit:
                existeing_habit_id = existeing_habit[0]

                with self.con as cursor:
                    sql_update = '''UPDATE habit SET study_time = study_time + ? WHERE id = ?'''
                    values = (study_time, existeing_habit_id)
                    cursor.execute(sql_update, values)
                    self.success = True
            else:
                with self.con as cursor:
                    sql_insert = '''INSERT INTO habit(study_time, category_id, date_current) VALUES(?, ?,?)'''
                    values = (study_time, category_id, current_time)
                    cursor.execute(sql_insert, values)
                    self.success = True
        except sqlite3.IntegrityError as e:
            print('Error adding time habit:', e)
        except Exception as e:
            print('Error adding time habit:', e)

    def load(self, table):
        current_time = datetime.datetime.now().strftime('%d-%m-%y')
        try:
            with self.con as cursor:
                sql = '''SELECT category_habits.name, habit.study_time, habit.date_current
                FROM habit
                JOIN category_habits ON habit.category_id = category_habits.id
                WHERE habit.date_current = ?
                '''
                values = (current_time,)
                cursor.execute(sql, values)
                habits = cursor.fetchall()
                data = []
                for habit_name, study_time, date_current in habits:
                    float(study_time)
                    format_study_time = "{:.2f}".format(study_time)
                    data.append((habit_name, format_study_time, date_current))
                for habit in data:
                    add_to_table(table, habit)
        except Exception as e:
            print('Error loading habits:', e)

    def was_successful(self):
        return self.success
