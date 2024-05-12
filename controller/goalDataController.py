from model.goalModel import GoalModel


class GoalDataController:

    def __init__(self):
        self.model = GoalModel()

    def add_goal(self, goal, category_id, month_id):
        return self.model.add_goal(goal, category_id, month_id)

    def load_goals(self, table, month):
        return self.model.load(table, month)

    def get_id(self, data):
        return self.model.get_id_goal(data)

    def delete(self, goal_id):
        return self.model.delete(goal_id)

    def was_successful(self):
        return self.model.success
