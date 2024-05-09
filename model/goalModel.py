import sqlite3
import datetime
from connection import Connection
from utils.func import add_to_table


class GoalModel:
    def __init__(self):
        self.success = False
        self.con = Connection()
        
    
    def add_goal(self, goal, category, month):
        category_id, month_id = self.get_ids(category, month)
        current_time = datetime.datetime.now().strftime('%d-%m-%y')
        values = (goal, category_id, month_id, current_time)
        
        try:
            with self.con as cursor:
                sql_check = '''SELECT * FROM goal WHERE category_id = ? AND month_id = ?'''
                cursor.execute(sql_check, (category_id, month_id,))
                existing_goal = cursor.fetchone()

                if existing_goal:
                    goal_id = existing_goal[0]
                    sql_update = '''UPDATE goal SET goal = ?, WHERE id'''
                    cursor.execute(sql_update,(goal, goal_id))
                else:
                    sql_insert = '''INSERT INTO goal(goal, category_id, month_id, date_current) VALUES(?, ?,?,?)'''
                    cursor.execute(sql_insert, values)

                self.success = True
        except sqlite3.IntegrityError as e:
            print('Error adding category:', e)
            self.success = False
        except Exception as e:
            print('Error adding category:', e)
            self.success = False
        
    
    def get_ids(self, category, month):
        sql_category = 'SELECT id FROM category_habits WHERE name = ?'
        sql_month = 'SELECT id FROM months WHERE name = ?'
        
        with self.con as cursor:
            cursor.execute(sql_category, (category,))
            category_id = cursor.fetchone()
            cursor.execute(sql_month, (month,))
            month_id = cursor.fetchone()
        
        return (category_id[0], month_id[0])

    def get_id_month(self, month):
        sql_month = 'SELECT id FROM months WHERE name = ?'

        with self.con as cursor:
            cursor.execute(sql_month, (month,))
            month_id = cursor.fetchone()

        return month_id[0]

    def load(self, table, month):
        month_id = self.get_id_month(month)
        print(month_id)
        try:
            sql_query = """SELECT c.name, 
                        g.goal, 
                        m.name,
                        strftime('%Y', g.date_current) as year
                        FROM goal g 
                        JOIN category_habits c 
                        ON g.category_id = c.id
                        JOIN months m
                        ON g.month_id = m.id 
                        WHERE g.month_id=?
                        """

            with self.con as cursor:
                cursor.execute(sql_query,(month_id,))
                res = cursor.fetchall()
                print(res)
                data = []
                for habit, goal, month, year in res:
                    div = self.day_month(month, year)
                    goal_calc = float(goal)/div
                    format_goal = "{:.2f}".format(goal_calc)
                    data.append((habit, format_goal, month))
                    
                for dat in data:
                    add_to_table(table, dat)
        except Exception as e:
            print('Error loading goals: ', e)

    def day_month(self,month, year):
        month_31 = [1, 3, 5, 7, 8, 10, 12]

        if month in month_31:
            return 31

        elif month == 2:
            if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
                return 29
            else:
                return 28

        else:
            return 30
    
