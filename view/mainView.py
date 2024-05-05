import os

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (QVBoxLayout, QLabel, QPushButton, QLineEdit, QComboBox,
                                 QFormLayout, QWidget, QTabWidget, QMainWindow, QTableWidget)

from view.addHabitView import AddHabitView
from view.addGoalView import AddGoalView

from connection import Connection

from controller.cbFillController import CbFillController
from controller.goalDataController import GoalDataController

from PySide6.QtWidgets import QMenu

from utils.func import add_to_table

script_directory = os.path.dirname(os.path.abspath(__file__))
ui_file_path = os.path.join(script_directory, 'ui', 'mainView.ui')

class MainView(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.db = Connection()
        self.db.setup_database()
        

        self.setWindowTitle("ImProductive")
        self.setGeometry(100, 100, 800, 600)

        self.create_menu_bar()
        self.create_tabs()
        self.cb_fill_category_habit_from_db()
        
        self.combo_study_of.setContextMenuPolicy(Qt.CustomContextMenu)
        self.combo_study_of.customContextMenuRequested.connect(self.show_context_menu)
        
        


    def create_menu_bar(self):
        menubar = self.menuBar()

        file_menu = menubar.addMenu('File')

        exit_action = QAction('Exit', self)
        add_habit_action = QAction('Add Habit', self)
        add_goal_action = QAction('Add Goal', self)
        
        exit_action.triggered.connect(self.close)
        add_habit_action.triggered.connect(self.add_habit_category)
        add_goal_action.triggered.connect(self.add_goal)
        
        file_menu.addAction(add_habit_action)
        file_menu.addAction(add_goal_action)
        file_menu.addAction(exit_action)

    def create_tabs(self):
        tab_widget = QTabWidget()

        tab1 = QWidget()
        self.setup_tab1(tab1)

        tab2 = QWidget()
        self.setup_tab2(tab2)

        tab_widget.addTab(tab1, "Habits")
        tab_widget.addTab(tab2, "Chart")

        self.setCentralWidget(tab_widget)

    def setup_tab1(self, tab):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignHCenter)

        form_layout = QFormLayout()

        label_minutes_study = QLabel('Minutes study today')
        layout.addWidget(label_minutes_study)

        input_minutes_study = QLineEdit()
        layout.addWidget(input_minutes_study)

        self.combo_study_of = QComboBox()
        layout.addWidget(self.combo_study_of)

        button = QPushButton("Add")
        button.clicked.connect(self.on_submit_clicked)
        layout.addWidget(button)

        #label_last_month = QLabel("Last Month")
        #table_last_month = QTableWidget()
        #layout.addWidget(label_last_month)
        #layout.addWidget(table_last_month)

        label_goal_month = QLabel("Goal Today")
        table_goal = QTableWidget()
        table_goal.setColumnCount(3)
        table_goal.setHorizontalHeaderLabels(['Habit', 'Goal', 'Month'])
        
        goals_controller = GoalDataController(table_goal)
        goals_controller.load()

        layout.addWidget(label_goal_month)
        layout.addWidget(table_goal)
        
        label_study_of = QLabel("Study of:")
        layout.addWidget(label_study_of)

        label_study_day = QLabel("Today")
        table_study_day = QTableWidget()
        layout.addWidget(label_study_day)
        layout.addWidget(table_study_day)

        layout.addLayout(form_layout)

        tab.setLayout(layout)

    def setup_tab2(self, tab):
        layout = QVBoxLayout()
        label_tab2 = QLabel("This is Tab 2")
        layout.addWidget(label_tab2)
        tab.setLayout(layout)
        
        
    def cb_fill_category_habit(self):
        self.combo_study_of.clear()
        for category in self.cb_category_habit:
            self.combo_study_of.addItem(category[0])
            
    def cb_fill_category_habit_from_db(self):
        self.cb_category_habit = CbFillController().load_category_habit()
        self.cb_fill_category_habit()


    
    def show_context_menu(self, position):
        menu = QMenu()
        update_action = menu.addAction('Actualizar')
        action = menu.exec_(self.combo_study_of.mapToGlobal(position))
        if action == update_action:
            self.cb_fill_category_habit_from_db()

    def on_submit_clicked(self):
        # Placeholder for submit button functionality
        pass

    def add_habit_category(self):
        self.add_habit_view = AddHabitView()
        
    
    def add_goal(self):
        self.add_goal_view = AddGoalView()


