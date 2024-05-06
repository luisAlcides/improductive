import datetime
from connection import Connection


class StudyDataModel:
    def __init__(self):
        self.db = Connection()
        
    
    def get_study_data(self, time_period):
        try:
            current_time = datetime.datetime.now().strftime('%d-%m-%y')
            with self.db as cursor:
                if time_period == 'Day':
                    sql = '''SELECT category_habits.name, SUM(habit.study_time) 
                             FROM habit
                             JOIN category_habits ON habit.category_id = category_habits.id
                             WHERE habit.date_current = ?
                             GROUP BY category_habits.name'''
                    cursor.execute(sql, (current_time,))
                elif time_period == 'Week':
                    sql = '''SELECT category_habits.name, SUM(habit.study_time) 
                             FROM habit
                             JOIN category_habits ON habit.category_id = category_habits.id
                             WHERE strftime('%Y-%m-%W', habit.date_current) = strftime('%Y-%m-%W', ?)
                             GROUP BY category_habits.name'''
                    cursor.execute(sql, (current_time,))
                elif time_period == 'Month':
                    sql = '''SELECT category_habits.name, SUM(habit.study_time) 
                             FROM habit
                             JOIN category_habits ON habit.category_id = category_habits.id
                             WHERE strftime('%Y-%m', habit.date_current) = strftime('%Y-%m', ?)
                             GROUP BY category_habits.name'''
                    cursor.execute(sql, (current_time,))
                
                study_time = cursor.fetchall()
                return study_time
        except Exception as e:
            print('Error getting study data:', e)
            return [(0)]