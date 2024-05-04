import os

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication

from view.mainView import MainView

script_directory = os.path.dirname(os.path.abspath(__file__))
view_directory = os.path.join(script_directory, '', 'view')
icon_system_path = os.path.join(view_directory, 'icons', 'system.png')

stylesheet = '''
    QLabel{
        font-size: 15px;
    }
    QComboBox{
        height: 25;
    }
    QLineEdit{
        height: 25;
    }
    QPushButton{
        height: 25;
    }
'''

class ImProductive:
    def __init__(self):
        self.app = QApplication([])
        self.app.setWindowIcon(QIcon(icon_system_path))
        self.app.setStyleSheet(stylesheet)
        self.ui = MainView()
        self.ui.show()
        self.app.exec()