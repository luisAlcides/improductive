from connection import Connection
from model.goalModel import GoalModel

class GoalDataController:

    def __init__(self):
        self.model = GoalModel()
    
    
    def add_goal(self, goal, category_id, month_id):
        return self.model.add_goal(goal, category_id, month_id)
    
    def load_goals(self, table):
        return self.model.load(table)
    
    def was_successful(self):
        return self.model.success


        
