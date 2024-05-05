

class GoalModel:
    def __init__(self, goal, habit, month):
        self.__goal = goal
        self.__habit = habit
        self.__month = month
        
    
    @property
    def goal(self):
        return self.__goal
    
    @goal.setter
    def goal(self, value):
        self.__goal = value
        
    
    @property
    def habit(self):
        return self.__habit
    
    @habit.setter
    def habit(self, value):
        self.__habit = value
        
    
    @property
    def month(self):
        return self.__month
    
    @month.setter
    def month(self, value):
        self.__month = value
        
    
    def __str__(self):
        return f'{self.__goal}, {self.__habit}, {self.__month}'

    