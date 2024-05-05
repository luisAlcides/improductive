from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QLabel, QLineEdit, QPushButton, QVBoxLayout


class AddHabitView(QMainWindow):
    TITLE_WINDOW = 'Add Habit'

    def __init__(self):
        super().__init__()
        self.setWindowTitle(self.TITLE_WINDOW)
        self.setGeometry(100, 100, 800, 300)
        self.setWindowModality(Qt.ApplicationModal)
        self.initUI()
        self.show()

    def initUI(self):

        # layout
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignHCenter)

        # labels
        label_habit = QLabel('Habit or Event')
        label_habit.setAlignment(Qt.AlignCenter)
        label_habit.setFixedHeight(20)

        # inputs
        input_habit = QLineEdit()

        # buttons
        btn_add = QPushButton('Add')

        layout.addWidget(label_habit)
        layout.addWidget(input_habit)
        layout.addWidget(btn_add)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)