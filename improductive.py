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
QPushButton {
    background-color: #f0f0f0; /* Color de fondo suave */
    border: 1px solid #ccc; /* Borde del botón */
    color: #333; /* Color del texto */
    padding: 10px;
    border-radius: 5px;
    font-size: 16px;
}

QPushButton:hover {
    background-color: #e0e0e0; /* Color de fondo suave al pasar el mouse */
}

QPushButton:pressed {
    background-color: #d0d0d0; /* Color de fondo al presionar el botón */
}

QPushButton:disabled {
    background-color: #eee; /* Color de fondo para botón deshabilitado */
    color: #ccc; /* Color del texto para botón deshabilitado */
}

QPushButton::menu-indicator {
    image: none; /* Ocultar indicador de menú si existe */
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
