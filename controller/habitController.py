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

    def show_weekly_data(self, view):
        data = self.model.get_weekly_data()
        view.setup_chart(data, "Weekly Study Time", "Days", "Hours", "bar")

    def show_monthly_data(self, view):
        data = self.model.get_monthly_data()
        view.setup_chart(data, "Monthly Study Time", "Days", "Hours", "line")

    def show_yearly_data(self, view):
        data = self.model.get_yearly_data()
        view.setup_chart(data, "Yearly Study Time", "Months", "Hours", "line")

    def show_data_by_month(self, month, view):
        data = self.model.get_data_by_month(month)
        view.setup_chart(data, f"Study Time for {month}", "Habits", "Hours", "bar")
