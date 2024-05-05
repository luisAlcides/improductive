from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QLabel, QLineEdit, QPushButton, QVBoxLayout
from utils.validation import validate_fields, clean_fields
from utils.func import message

from controller.addGoalController import AddGoalController
from controller.cbFillController import CbFillController

from model.goalModel import GoalModel


from PySide6.QtWidgets import QComboBox

class AddGoalView(QMainWindow):
    TITLE_WINDOW = 'Add Goal'
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
        label_goal = QLabel('Goal in hours')
        label_goal.setAlignment(Qt.AlignCenter)
        layout.addWidget(label_goal)
        
        input_goal = QLineEdit()
        layout.addWidget(input_goal)

        label_habit = QLabel('Habit')
        layout.addWidget(label_habit)

        cb_habit = QComboBox()
        self.fill_cb_habit(cb_habit)
        layout.addWidget(cb_habit)
        
        label_month = QLabel('Month')
        layout.addWidget(label_month)

        cb_month = QComboBox()
        self.fill_cb_month(cb_month)
        layout.addWidget(cb_month)

        # buttons
        btn_add = QPushButton('Add')
        btn_add.clicked.connect(self.add_habit)
        
        self.fields = [[input_goal, 'number', label_goal],
                       [cb_habit, 'cb', label_habit],
                       [cb_month, 'cb', label_month]]

        
        layout.addWidget(btn_add)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        
    
    def fill_cb_habit(self, cb):
        cb.clear()
        habits = CbFillController().load_category_habit()
        for habit in habits:
            cb.addItem(habit[0])
    
    def fill_cb_month(self, cb):
        months = CbFillController().load_months()
        for month in months:
            cb.addItem(month[0])

    def add_habit(self):
        if not validate_fields(self.fields):
            return 
        
        input_goal = self.fields[0][0].text().split()
        input_goal = input_goal[0].title()
        
        cb_habit = self.fields[1][0].currentText()
        cb_month = self.fields[2][0].currentText()
                
        model = GoalModel(input_goal, cb_habit, cb_month)
        controller = AddGoalController(model)
        
        if controller.was_successful():
            message('Goal add corrently')
            clean_fields(self.fields)
        else:
            message('Error adding habit')
            
            