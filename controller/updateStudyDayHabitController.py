from controller.habitController import HabitController
from view.updateStudyDayHabitView import UpdateStudyDayHabitView
from utils.func import cb_fill_category_habit, message
from PySide6.QtCore import Qt


class UpdateStudyDayHabitController:
    def __init__(self, controller, data):
        self.controller = controller
        self.controller_habit = HabitController()
        self.data = data
        self.view = UpdateStudyDayHabitView()
        self.init_view()

    def init_view(self):
        try:
            study_time, category = self.controller.get_study_time_by_id(self.data)
            if study_time and category:
                study_time = study_time[0] * 60
                category = category[0]
                self.view.input_habit.setText(str(study_time))
                cb_fill_category_habit(self.view.cb_habit, self.controller_habit)
                index_cb = self.view.cb_habit.findText(category, Qt.MatchFixedString)
                if index_cb >= 0:
                    self.view.cb_habit.setCurrentIndex(index_cb)
                self.view.btn_update.clicked.connect(self.update_study_day_habit)
            else:
                print("Error: Study time or category not found.")
        except Exception as e:
            print(f"Error initializing view: {e}")

    def update_study_day_habit(self):
        try:
            study_time = self.view.input_habit.text().strip()
            study_time = float(study_time) / 60
            category = self.view.cb_habit.currentText()
            category_id = self.controller.get_category_id(category)
            if self.controller.update(study_time, category_id, self.data):
                self.view.habit_updated.emit()
                self.view.close()
                message("Update successful.")
            else:
                print("Error updating study data.")
        except Exception as e:
            print(f"Error updating study day habit: {e}")
