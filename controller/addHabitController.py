import sqlite3 
import datetime

from connection import Connection


class AddHabitController:
    def __init__(self, category):
        self.success = False
        con = Connection()
        sql_insert = '''
            INSERT INTO category_habits(name, date_current)
            VALUES(?, ?)
        '''
        current_time = datetime.datetime.now().strftime('%d-%m-%y')
        values = (category.name_habit,current_time)
        
        with con as cursor:
            try:
                cursor.execute(sql_insert, values)
                self.success = True
            except sqlite3.IntegrityError as e:
                print('Error adding category:', e)
                self.success = False
            except Exception as e:
                print('Error adding category:', e)
                self.success = False
        
    
    def was_successful(self):
        return self.success