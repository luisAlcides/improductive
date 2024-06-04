from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from PySide6.QtGui import QIcon
import sys
import os

path = os.path.dirname(os.path.abspath(__file__))
icon_path = os.path.join(path, "view/icons", "system.png")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Aplicación con Ícono")
        self.setWindowIcon(QIcon(icon_path))

        label = QLabel("¡Hola, PySide6 con Ícono!")
        layout = QVBoxLayout()
        layout.addWidget(label)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
