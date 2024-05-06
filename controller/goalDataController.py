from connection import Connection
from utils.func import add_to_table


class GoalDataController:

    def __init__(self, table):
        self.con = Connection()
        self.table = table
    

    def load(self):
        try:
            sql_query = """SELECT c.name, 
                        g.goal, 
                        m.name,
                        strftime('%Y', g.current_time) as year
                        FROM goal g 
                        JOIN category_habits c 
                        ON g.category_id = c.id
                        JOIN months m
                        ON g.month_id = m.id
                        """

            with self.con as cursor:
                cursor.execute(sql_query)
                res = cursor.fetchall()
                self.data = []
                for habit, goal, month, year in res:
                    div = self.day_month(month, year)
                    goal_calc = float(goal)/div
                    format_goal = "{:.2f}".format(goal_calc)
                    self.data.append((habit, format_goal, month))
                    

                    
                for dat in self.data:
                    add_to_table(self.table, dat)
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
        
