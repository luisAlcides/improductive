from PySide6.QtWidgets import QApplication, QMainWindow, QProgressBar
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Crear una instancia de QProgressBar
        self.progressBar = QProgressBar()

        # Configurar las propiedades del ProgressBar
        self.progressBar.setMinimum(0)
        self.progressBar.setMaximum(100)
        self.progressBar.setValue(50)
        self.progressBar.setFormat("%p%")

        # Mostrar el ProgressBar
        self.setCentralWidget(self.progressBar)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
    sys.exit(app.exec())
