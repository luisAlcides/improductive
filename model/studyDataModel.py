import datetime
from connection import Connection


class StudyDataModel:
    def __init__(self):
        self.db = Connection()
        self.success = False

    def get_study_data(self, time_period):
        try:
            current_time = datetime.datetime.now().strftime("%d-%m-%y")
            with self.db as cursor:
                if time_period == "Day":
                    sql = """SELECT category_habits.name, SUM(habit.study_time) 
                             FROM habit
                             JOIN category_habits ON habit.category_id = category_habits.id
                             WHERE habit.date_current = ?
                             GROUP BY category_habits.name"""
                    cursor.execute(sql, (current_time,))
                elif time_period == "Week":
                    sql = """SELECT category_habits.name, SUM(habit.study_time) 
                             FROM habit
                             JOIN category_habits ON habit.category_id = category_habits.id
                             WHERE strftime('%Y-%m-%W', habit.date_current) = strftime('%Y-%m-%W', ?)
                             GROUP BY category_habits.name"""
                    cursor.execute(sql, (current_time,))
                elif time_period == "Month":
                    sql = """SELECT category_habits.name, SUM(habit.study_time) 
                             FROM habit
                             JOIN category_habits ON habit.category_id = category_habits.id
                             WHERE strftime('%Y-%m', habit.date_current) = strftime('%Y-%m', ?)
                             GROUP BY category_habits.name"""
                    cursor.execute(sql, (current_time,))
                study_time = cursor.fetchall()
                return study_time
        except Exception as e:
            print("Error getting study data:", e)
            return []

    def get_category_id(self, study):
        try:
            sql_category_id = """SELECT id FROM category_habits WHERE name=?"""
            with self.db as cursor:
                cursor.execute(sql_category_id, (study,))
                category_id = cursor.fetchone()
            return category_id[0] if category_id else None
        except Exception as e:
            print("Error getting category ID:", e)
            return None

    def get_id_study(self, study):
        category_id = self.get_category_id(study)
        if category_id:
            try:
                with self.db as cursor:
                    sql = "SELECT id FROM habit WHERE category_id = ?"
                    cursor.execute(sql, (category_id,))
                    study_id = cursor.fetchone()
                return study_id[0] if study_id else None
            except Exception as e:
                print("Error getting study ID:", e)
                return None
        return None

    def get_study_time_by_id(self, study_id):
        current_time = datetime.datetime.now().strftime("%d-%m-%y")
        try:
            sql = "SELECT study_time, category_id FROM habit WHERE id = ?"
            with self.db as cursor:
                cursor.execute(sql, (study_id,))
                data_study_time = cursor.fetchone()
                if data_study_time:
                    study_time = data_study_time[0]
                    category_id = data_study_time[1]
                    sql = """SELECT study_time FROM habit WHERE category_id = ? AND date_current = ?"""
                    cursor.execute(
                        sql,
                        (
                            category_id,
                            current_time,
                        ),
                    )
                    study_time = cursor.fetchone()
                    sql = "SELECT name FROM category_habits WHERE id = ?"
                    cursor.execute(sql, (category_id,))
                    category = cursor.fetchone()
                    return study_time, category
                return None, None
        except Exception as e:
            print("Error getting study time by ID:", e)
            return None, None

    def delete(self, study_id):
        try:
            sql = "DELETE FROM habit WHERE id = ?"
            with self.db as cursor:
                cursor.execute(sql, (study_id,))
            return True
        except Exception as e:
            print(f"Error deleting study ID {study_id}:", e)
            return False

    def update(self, study_time, category_id, study_id):
        current_time = datetime.datetime.now().strftime("%d-%m-%y")
        try:
            sql = """UPDATE habit SET study_time = ?, category_id = ?
                     WHERE id = ? AND date_current = ?"""
            with self.db as cursor:
                cursor.execute(sql, (study_time, category_id, study_id, current_time))
            self.success = True
            return True
        except Exception as e:
            print("Error updating study data:", e)
            self.success = False
            return False
