from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget
from PySide6.QtCore import QTimer, QTime, Qt

class CountdownTimer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Countdown Timer")
        self.setGeometry(100, 100, 300, 200)

        self.timer_label = QLabel("00:00:00", self)
        self.timer_label.setAlignment(Qt.AlignCenter)
        self.timer_label.setStyleSheet("font-size: 24px;")

        self.start_button = QPushButton("Start", self)
        self.start_button.clicked.connect(self.start_timer)

        self.stop_button = QPushButton("Stop", self)
        self.stop_button.clicked.connect(self.stop_timer)

        layout = QVBoxLayout()
        layout.addWidget(self.timer_label)
        layout.addWidget(self.start_button)
        layout.addWidget(self.stop_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.time_left = QTime(0,10, 0)  # Set the countdown time (e.g., 1 minute)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)

    def start_timer(self):
        self.timer.start(1000)  # Update every second

    def stop_timer(self):
        self.timer.stop()

    def update_timer(self):
        self.time_left = self.time_left.addSecs(-1)
        self.timer_label.setText(self.time_left.toString("hh:mm:ss"))

        if self.time_left == QTime(0, 0, 0):
            self.timer.stop()

if __name__ == "__main__":
    app = QApplication([])
    window = CountdownTimer()
    window.show()
    app.exec()
