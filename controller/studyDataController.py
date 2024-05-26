
from model.studyDataModel import StudyDataModel

class StudyDataController:
    def __init__(self):
        self.model = StudyDataModel()

    def get_study_data(self, time_period):
        return self.model.get_study_data(time_period)

    def get_id(self, study):
        return self.model.get_id_study(study)

    def delete(self, study_id):
        return self.model.delete(study_id)

    def get_study_time_by_id(self, study_id):
        return self.model.get_study_time_by_id(study_id)

    def get_id_study_today(self, category_habit):
        return self.model.get_id_study_today(category_habit)

    def get_category_id(self, study):
        return self.model.get_category_id(study)

    def update(self, study_time, category_id, study_id):
        return self.model.update(study_time, category_id, study_id)

    def success(self):
        return self.model.success
