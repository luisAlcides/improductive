

class HabitModel:
    def __init__(self, name_habit):
        self.__name_habit = name_habit

    @property
    def name_habit(self):
        return self.__name_habit
    
    @name_habit.setter
    def name_habit(self, value):
        self.__name_habit = value
        
    
    def __str__(self):
        return f'{self.__name_habit}'