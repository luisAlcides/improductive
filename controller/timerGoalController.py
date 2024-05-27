
from controller.goalDataController import GoalDataController

class TimerGoalController:
    def __init__(self, category):
        self.category = category
        self.controller = GoalDataController()

    def get_goal(self):
        return self.controller.get_goal_by_category(self.category) 
        


