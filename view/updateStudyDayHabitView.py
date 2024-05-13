from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QMainWindow, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QComboBox
from PySide6 import QtWidgets


class UpdateStudyDayHabitView(QMainWindow):
    TITLE_WINDOW = 'Update Study Day Habit'
    habit_added = Signal()

    def __init__(self, parent=None):
        super().__init__(parent=None)
        self.setWindowTitle(self.TITLE_WINDOW)
        self.setGeometry(100, 100, 800, 300)
        self.initUI()
        self.show()

    def initUI(self):

        # layout
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignHCenter)

        # labels
        self.label_habit = QLabel('Update Study Habit Today')
        self.label_habit.setAlignment(Qt.AlignCenter)
        self.label_habit.setFixedHeight(20)
        # inputs
        self.input_habit = QLineEdit()
        # combo box
        self.cb_habit = QComboBox()
        # buttons
        self.btn_update = QPushButton('update')
        layout.addWidget(self.label_habit)
        layout.addWidget(self.input_habit)
        layout.addWidget(self.cb_habit)
        layout.addWidget(self.btn_update)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
