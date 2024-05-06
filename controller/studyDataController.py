from model.studyDataModel import StudyDataModel

class StudyDataController:
    def __init__(self):
        self.model = StudyDataModel()
        
    
    def get_study_data(self, time_period):
        if time_period == 'Week' or time_period == 'Month':
            return self.model.get_study_data(time_period)
        return self.model.get_study_data(time_period)