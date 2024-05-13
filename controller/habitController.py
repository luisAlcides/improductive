from model.habitModel import HabitModel


class HabitController:
    def __init__(self):
        self.model = HabitModel()

    def insert_into_habits(self, category):
        self.model.insert_into_habits(category)

    def get_category_habits(self):
        return self.model.get_category_habits()

    def was_successful(self):
        return self.model.was_successful()
