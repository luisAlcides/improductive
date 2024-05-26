
from controller.habitController import HabitController
from controller.cbFillController import CbFillController
from view.updateGoalView import UpdateGoalView
from utils.func import cb_fill_category_habit, message, cb_fill_month
from PySide6.QtCore import Qt


class UpdateGoalController:
    def __init__(self, controller, data):
        self.controller_habit = HabitController()
        self.controller = controller
        self.cb_fill_month = CbFillController()
        self.data = data
        self.view = UpdateGoalView()
        self.init_view()

    def init_view(self):
        try:
            goal, category, month = self.controller.get_goal_by_id(int(self.data))
            if goal and category and month:
                self.view.input_goal.setText(str(goal))
                cb_fill_category_habit(self.view.cb_habit, self.controller_habit)
                index_cb = self.view.cb_habit.findText(category, Qt.MatchFixedString)
                if index_cb >= 0:
                    self.view.cb_habit.setCurrentIndex(index_cb)
                cb_fill_month(self.view.cb_month, self.cb_fill_month)
                index_cb_month = self.view.cb_month.findText(month, Qt.MatchFixedString)
                if index_cb_month >= 0:
                    self.view.cb_month.setCurrentIndex(index_cb_month)

                self.view.btn_update.clicked.connect(self.update_goal)
                
            else:
                print("Error: Goal or category not found.")
        except Exception as e:
            print(f"Error initializing view: {e}")

    def update_goal(self):
        try:
            goal = self.view.input_goal.text().strip()
            goal = float(goal)
            category = self.view.cb_habit.currentText()
            month = self.view.cb_month.currentText()
            if self.controller.update(goal, category, month,self.data):
                self.view.goal_updated.emit()
                self.view.close()
                message("Update successful.")
            else:
                print("Error updating goal")
        except Exception as e:
            print(f"Error updating study day habit: {e}")
