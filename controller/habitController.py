from model.habitModel import HabitModel
from view.monthlySchedule import MonthlySchedule


class HabitController:
    def __init__(self):
        self.model = HabitModel()
        self.monthly_schedule = MonthlySchedule()

    def insert_into_habits(self, category):
        self.model.insert_into_habits(category)
        self.monthly_schedule.trigger_data_update()

    def get_category_habits(self):
        return self.model.get_category_habits()

    def was_successful(self):
        return self.model.was_successful()

    def show_weekly_data(self):
        data = self.model.get_weekly_data()
        return data

    def show_monthly_data(self):
        data = self.model.get_monthly_data()
        return data

    def show_data_by_year(self, habit):
        data = self.model.get_yearly_data(habit)

        formatted_data = []
        for row in data:
            month, total_hours, goal = row
            formatted_data.append((month, total_hours, goal))
        return formatted_data

    def show_data_by_month(self, month):
        data = self.model.get_data_by_month(month)
        return data
