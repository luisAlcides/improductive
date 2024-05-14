import shutil


class ExportImportDatabaseController:
    def __init__(self, source_path):
        self.source_path = source_path

    def exportDatabase(self, destination_path):
        try:
            shutil.copyfile(self.source_path, destination_path)
        except Exception as e:
            print(e)

    def importDatabase(self, destination_path):
        try:
            shutil.copyfile(destination_path, self.source_path)
        except Exception as e:
            print(e)
