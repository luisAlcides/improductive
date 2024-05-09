from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QMainWindow, QWidget,QLabel, QLineEdit, QPushButton, QVBoxLayout
from utils.validation import validate_fields
from utils.func import message, clean_fields

from controller.addHabitController import AddHabitController


from model.habitModel import HabitModel

class AddHabitView(QMainWindow):
    TITLE_WINDOW = 'Add Habit'
    habit_added = Signal()

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
        btn_add.clicked.connect(self.add_habit)
        
        self.fields = [[input_habit, 'text', label_habit]]

        layout.addWidget(label_habit)
        layout.addWidget(input_habit)
        layout.addWidget(btn_add)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        

    def add_habit(self):
        if not validate_fields(self.fields):
            return 
        
        name_habit = self.fields[0][0].text().split()
        name_habit = name_habit[0].title()
        
       
                
        model = HabitModel(name_habit)
        controller = AddHabitController(model)
        if controller.was_successful():
            message('Habit add correctly')
            clean_fields(self.fields)
        else:
            message('Error adding habit')
