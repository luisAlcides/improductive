import sqlite3
import datetime

from connection import Connection


class AddGoalController:
    def __init__(self, goals):
        self.success = False
        self.con = Connection()
        sql_insert = '''
            INSERT INTO goal(goal, category_id, month_id, date_current)
            VALUES(?, ?, ?, ?)
        '''
        category_id, month_id = self.get_ids(goals)
        
        current_time = datetime.datetime.now().strftime('%d-%m-%y')
        
        values = (goals.goal, category_id, month_id, current_time)
        
        with self.con as cursor:
            try:
                cursor.execute(sql_insert, values)
                self.success = True
            except sqlite3.IntegrityError as e:
                print('Error adding category:', e)
                self.success = False
            except Exception as e:
                print('Error adding category:', e)
                self.success = False
        
    
    def get_ids(self, goals):
        sql_category = 'SELECT id FROM category_habits WHERE name = ?'
        sql_month = 'SELECT id FROM months WHERE name = ?'
        
        with self.con as cursor:
            cursor.execute(sql_category, (goals.habit,))
            category_id = cursor.fetchone()
            cursor.execute(sql_month, (goals.month,))
            month_id = cursor.fetchone()
        
        return (category_id[0], month_id[0])
    
    
    def was_successful(self):
        return self.success