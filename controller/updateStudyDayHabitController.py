from controller.habitController import HabitController

from view.updateStudyDayHabitView import UpdateStudyDayHabitView
from utils.func import cb_fill_category_habit


class UpdateStudyDayHabitController:
    def __init__(self, controller, data):
        self.controller = controller
        self.controller_habit = HabitController()
        self.data = data
        self.view = UpdateStudyDayHabitView()
        study_time, category = self.controller.get_study_time_by_id(
            data)
        study_time = study_time[0] * 60
        category = category[0]
        self.view.input_habit.setText(str(study_time))
        cb_fill_category_habit(self.view.cb_habit, self.controller_habit)
        self.view.cb_habit.setCurrentText(category)
        self.view.input_habit.setText(str(study_time))
        self.view.cb_habit.addItem(category)
        self.view.btn_update.clicked.connect(
            lambda: self.update_study_day_habit(data))

    def update_study_day_habit(self, data):
        study_time = self.view.input_habit.text().strip()
        study_time = float(study_time) / 60
        category = self.view.cb_habit.currentText()
        category_id = self.controller.get_category_id(category)
        self.controller.update(
            study_time, category_id, data)
        if self.controller.success:
            self.view.close()
