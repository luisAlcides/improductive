

class AddHabitTimeModel:
    def __init__(self, name_habit, study_time):
        self.name_habit = name_habit
        self.study_time = study_time
        
    @property
    def name_habit(self):
        return self._name_habit
    
    @name_habit.setter
    def name_habit(self, name_habit):
        self._name_habit = name_habit
        
    @property
    def study_time(self):
        return self._study_time
    
    @study_time.setter
    def study_time(self, study_time):
        self._study_time = study_time
        
    def __str__(self):
        return f'{self.name_habit} - {self.study_time}'