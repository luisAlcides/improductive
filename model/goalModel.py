import sqlite3
import datetime
from connection import Connection
from utils.func import add_to_table, message


class GoalModel:
    def __init__(self):
        self.success = False
        self.con = Connection()

    def add_goal(self, goal, category, month):
        category_id, month_id = self.get_ids(category, month)
        current_time = datetime.datetime.now().strftime('%d-%m-%y')
        values = (float(goal), category_id, month_id, current_time)

        try:
            with self.con as cursor:
                sql_check = '''SELECT * FROM goal
                                WHERE category_id = ?
                                AND month_id = ?'''
                cursor.execute(sql_check, (category_id, month_id,))
                existing_goal = cursor.fetchone()

                if existing_goal:
                    goal_id = existing_goal[0]
                    with self.con as cursor:
                        sql_update = '''UPDATE goal SET goal = goal + ?
                                        WHERE id = ?'''
                        cursor.execute(sql_update, (goal, goal_id,))
                        self.success = True
                else:
                    with self.con as cursor:
                        sql_insert = '''INSERT INTO goal(
                                                    goal,
                                                    category_id,
                                                    month_id,
                                                    date_current)
                                        VALUES(?, ?,?,?)'''
                        cursor.execute(sql_insert, values)
                        self.success = True

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

    def get_id_category(self, category):
        sql_category = 'SELECT id FROM category_habits WHERE name = ?'
        with self.con as cursor:
            cursor.execute(sql_category, (category,))
            category_id = cursor.fetchone()
        return category_id[0]

    def get_id_month(self, month):
        sql_month = 'SELECT id FROM months WHERE name = ?'

        with self.con as cursor:
            cursor.execute(sql_month, (month,))
            month_id = cursor.fetchone()

        return month_id[0]

    def get_category_by_id(self, category_id):
        try:
            sql = 'SELECT name FROM category_habits WHERE id = ?'
            with self.con as cursor:
                cursor.execute(sql, (category_id,))
                category = cursor.fetchone()
                return category[0]
        except Exception as e:
            print('Error getting category by id:', e)
            return None
    def get_month_by_id(self, month_id):
        try:
            sql = 'SELECT name FROM months WHERE id = ?'
            with self.con as cursor:
                cursor.execute(sql, (month_id,))
                month = cursor.fetchone()
                return month[0]
        except Exception as e:
            print('Error getting month by id:', e)
            return None

    def get_goal_by_id(self, goal_id):
        try:
            sql = '''SELECT goal, category_id, month_id FROM goal WHERE id = ?'''
            with self.con as cursor:
                cursor.execute(sql, (goal_id,))
                result = cursor.fetchone()
                goal = result[0]
                category_id = result[1]
                month_id = result[2]

                category = self.get_category_by_id(category_id)
                month = self.get_month_by_id(month_id)

                return goal, category, month
        except Exception as e:
            print('Error getting goal by id:', e)
            return None

    def get_goal_by_category(self, category):
        try:
            category_id = self.get_id_category(category)
            month = datetime.datetime.now().month
            year = datetime.datetime.now().year
            sql = 'SELECT goal FROM goal WHERE category_id = ? AND month_id = ?'
            with self.con as cursor:
                cursor.execute(sql, (category_id, month,))
                goal = cursor.fetchone()
                goal = goal[0]
            div = self.day_month(month, year)
            result = float(goal)/div
            result = float(result)
            return result
        except Exception as e:
            print('Error getting goal by category:', e)
            return None


    def get_id_goal(self, data):
        category_id = self.get_id_category(data)
        sql = 'SELECT id FROM goal WHERE category_id = ?'
        with self.con as cursor:
            cursor.execute(sql, (category_id,))
            goal_id = cursor.fetchone()
        return goal_id[0]

    def load(self, table, month):
        month_id = self.get_id_month(month)
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
                cursor.execute(sql_query, (month_id,))
                res = cursor.fetchall()
                data = []
                for habit, goal, month, year in res:
                    div = self.day_month(month_id, year)
                    goal_calc = float(goal)/div
                    float(goal_calc)
                    format_goal = "{:.2f}".format(goal_calc)
                    data.append((habit, format_goal, month))

                for dat in data:
                    add_to_table(table, dat)
        except Exception as e:
            print('Error loading goals: ', e)

    def day_month(self, month, year):
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

    def delete(self, goal_id):
        try:
            with self.con as cursor:
                sql_delete = 'DELETE FROM goal WHERE id = ?'
                cursor.execute(sql_delete, (goal_id,))
                self.success = True
        except Exception as e:
            print('Error deleting goal:', e)
            self.success = False


    def update(self, goal, category, month, goal_id):
        category_id = self.get_id_category(category)
        month_id = self.get_id_month(month)
        values = (goal, category_id, month_id, goal_id)

        try:
            with self.con as cursor:
                sql = '''UPDATE goal SET goal = ?, category_id = ?, month_id = ?
                        WHERE id = ?'''
                cursor.execute(sql, values)
                self.success = True
                message('Update successful.')
                return True
        except Exception as e:
            print('Error updating goal:', e)
            self.success = False

