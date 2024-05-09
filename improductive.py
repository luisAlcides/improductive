import os

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QWidget

from view.mainView import MainView  # Assuming this remains the same


stylesheet = """
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
"""


path = os.path.dirname(os.path.abspath(__file__))
icon_path = os.path.join(path, "icons", "system.png")


class ImProductive(QWidget):
    def __init__(self):
        self.app = QApplication([])
        self.app.setWindowIcon(QIcon(icon_path))
        self.app.setStyleSheet(stylesheet)
        self.ui = MainView()
        self.ui.showMaximized()
        self.app.exec_()
