
import datetime
from connection import Connection

class StudyDataModel:
    def __init__(self):
        self.db = Connection()
        self.success = False

    def get_study_data(self, time_period):
        try:
            current_time = datetime.datetime.now().strftime("%d-%m-%y")
            sql = self._build_sql_query(time_period)
            with self.db as cursor:
                cursor.execute(sql, (current_time,))
                return cursor.fetchall()
        except Exception as e:
            print("Error getting study data:", e)
            return []

    def _build_sql_query(self, time_period):
        base_query = """
            SELECT category_habits.name, SUM(habit.study_time)
            FROM habit
            JOIN category_habits ON habit.category_id = category_habits.id
            WHERE strftime(?, habit.date_current) = strftime(?, ?)
            GROUP BY category_habits.name
        """
        time_formats = {
            "Day": "%d-%m-%y",
            "Week": "%y-%W",
            "Month": "%y-%m"
        }
        return base_query.replace("?", time_formats[time_period])

    def get_category_id(self, study):
        try:
            sql = "SELECT id FROM category_habits WHERE name=?"
            with self.db as cursor:
                cursor.execute(sql, (study,))
                result = cursor.fetchone()
            return result[0] if result else None
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
                    result = cursor.fetchone()
                return result[0] if result else None
            except Exception as e:
                print("Error getting study ID:", e)
                return None
        return None

    def get_id_study_today(self, category_habit):
        category_id = self.get_category_id(category_habit)
        if category_id:
            try:
                current_time = datetime.datetime.now().strftime("%d-%m-%y")
                with self.db as cursor:
                    sql = "SELECT id FROM habit WHERE category_id = ? AND date_current = ?"
                    cursor.execute(sql, (category_id, current_time))
                    result = cursor.fetchone()
                return result[0] if result else None
            except Exception as e:
                print("Error getting study ID today:", e)
                return None
        return None

    def get_study_time_by_id(self, category_id):
        try:
            sql = "SELECT study_time, category_id FROM habit WHERE id = ?"
            with self.db as cursor:
                cursor.execute(sql, (category_id,))
                result = cursor.fetchone()
                if result:
                    return self._fetch_additional_study_time(result)
            return None, None
        except Exception as e:
            print("Error getting study time by ID:", e)
            return None, None

    def _fetch_additional_study_time(self, result):
        study_time, category_id = result
        current_time = datetime.datetime.now().strftime("%d-%m-%y")
        with self.db as cursor:
            sql = "SELECT study_time FROM habit WHERE category_id = ? AND date_current = ?"
            cursor.execute(sql, (category_id, current_time))
            study_time = cursor.fetchone()
            sql = "SELECT name FROM category_habits WHERE id = ?"
            cursor.execute(sql, (category_id,))
            category = cursor.fetchone()
        return study_time, category

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
        try:
            current_time = datetime.datetime.now().strftime("%d-%m-%y")
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
