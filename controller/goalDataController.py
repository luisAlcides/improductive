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
                        m.name
                        FROM goal g 
                        JOIN category_habits c 
                        ON g.category_id = c.id
                        JOIN months m
                        ON g.month_id = m.id
                        """

            with self.con as cursor:
                cursor.execute(sql_query)
                data = cursor.fetchall()
                for goal in data:
                    add_to_table(self.table, goal)
        except Exception as e:
            print('Error loading products: ', e)
        
