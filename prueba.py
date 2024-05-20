import sys
from PySide6.QtCore import QTimer, QTime, Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QMenu, QSystemTrayIcon
from PySide6.QtGui import QIcon, QAction

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Temporizador")
        self.setGeometry(300, 300, 250, 150)
        
        # Label para mostrar el temporizador
        self.label = QLabel("00:00:00", self)
        self.label.setAlignment(Qt.AlignCenter)
        self.setCentralWidget(self.label)

        # Configuración del temporizador
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.time = QTime(0, 0, 0)
        self.timer_running = False

        # Crear un icono de sistema
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon("path/to/icon.png"))  # Asegúrate de que la ruta del icono sea correcta

        # Crear un menú para el icono de sistema
        self.tray_menu = QMenu()
        
        self.time_action = QAction("00:00:00", self)  # Acción para mostrar el temporizador en tiempo real
        self.tray_menu.addAction(self.time_action)

        self.start_action = QAction("Iniciar", self)
        self.start_action.triggered.connect(self.start_timer)
        self.tray_menu.addAction(self.start_action)
        self.stop_action = QAction("Pausar", self)
        self.stop_action.triggered.connect(self.stop_timer)
        self.tray_menu.addAction(self.stop_action)
        self.reset_action = QAction("Reiniciar", self)
        self.reset_action.triggered.connect(self.reset_timer)
        self.tray_menu.addAction(self.reset_action)
        self.exit_action = QAction("Salir", self)
        self.exit_action.triggered.connect(QApplication.instance().quit)
        self.tray_menu.addAction(self.exit_action)

        self.tray_icon.setContextMenu(self.tray_menu)
        self.tray_icon.show()

    def start_timer(self):
        if not self.timer_running:
            self.timer.start(1000)
            self.timer_running = True

    def stop_timer(self):
        if self.timer_running:
            self.timer.stop()
            self.timer_running = False

    def reset_timer(self):
        self.stop_timer()
        self.time = QTime(0, 0, 0)
        self.update_display()

    def update_timer(self):
        self.time = self.time.addSecs(1)
        self.update_display()

    def update_display(self):
        time_string = self.time.toString("hh:mm:ss")
        self.label.setText(time_string)
        self.tray_icon.setToolTip(time_string)
        self.time_action.setText(time_string)  # Actualiza el texto del QAction

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    window.update_display()  # Inicializa la pantalla con el tiempo inicial
    sys.exit(app.exec())
