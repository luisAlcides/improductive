import os

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, QComboBox,
                                 QFormLayout, QWidget, QTabWidget, QMainWindow, QTableWidget)

from view.addHabitView import AddHabitView
from view.addGoalView import AddGoalView

from connection import Connection

from controller.cbFillController import CbFillController
from controller.goalDataController import GoalDataController
from controller.addHabitTimeController import AddHabitTimeController

from model.addHabitTimeModel import AddHabitTimeModel

from view.chartView import ChartView

from PySide6.QtWidgets import QMenu

from utils.func import  clean_fields
from utils.validation import validate_fields

script_directory = os.path.dirname(os.path.abspath(__file__))
ui_file_path = os.path.join(script_directory, 'ui', 'mainView.ui')

class MainView(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.db = Connection()
        self.db.setup_database()
        

        self.setWindowTitle("ImProductive")
        self.setGeometry(100, 100, 800, 600)
        
        self.study_day = AddHabitTimeController()
        self.goals_controller = GoalDataController()
        

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
        tab1.customContextMenuRequested.connect(self.show_context_menu)
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
       
        self.label_minutes_study = QLabel('Minutes study today')
        layout.addWidget(self.label_minutes_study)

        self.input_minutes_study = QLineEdit()
        layout.addWidget(self.input_minutes_study)
        
        self.label_cb_study_of = QLabel('Habit')
        layout.addWidget(self.label_cb_study_of)

        self.combo_study_of = QComboBox()
        layout.addWidget(self.combo_study_of)

        horizontal_layout = QHBoxLayout()
        btn_add = QPushButton("Add")
        btn_add.clicked.connect(self.add_habit_time)
        horizontal_layout.addWidget(btn_add)

        btn_update = QPushButton('Update')
        btn_update.clicked.connect(self.refresh)
        horizontal_layout.addWidget(btn_update)

        layout.addLayout(horizontal_layout)

        #label_last_month = QLabel("Last Month")
        #table_last_month = QTableWidget()
        #layout.addWidget(label_last_month)
        #layout.addWidget(table_last_month)

        label_goal_month = QLabel("Goal Today")
        self.table_goal = QTableWidget()
        self.table_goal.setColumnCount(3)
        self.table_goal.setHorizontalHeaderLabels(['Habit', 'Goal', 'Month'])
        
        self.load_goals(self.table_goal) 
        

        layout.addWidget(label_goal_month)
        layout.addWidget(self.table_goal)
        
        label_study_of = QLabel("Study of:")
        layout.addWidget(label_study_of)

        label_study_day = QLabel("Today")
        self.table_study_day = QTableWidget()
        self.table_study_day.setColumnCount(3)
        self.table_study_day.setHorizontalHeaderLabels(['Habit', 'Time', 'Date'])
        self.study_day.load(self.table_study_day)
        layout.addWidget(label_study_day)
        layout.addWidget(self.table_study_day)

        layout.addLayout(form_layout)

        tab.setLayout(layout)

    def setup_tab2(self, tab):
        layout = QVBoxLayout()
        
        self.chart_view = ChartView()
        layout.addWidget(self.chart_view)
        tab.setLayout(layout)
        
        
    def cb_fill_category_habit(self):
        self.combo_study_of.clear()
        for category in self.cb_category_habit:
            self.combo_study_of.addItem(category[0])
            
    def cb_fill_category_habit_from_db(self):
        self.cb_category_habit = CbFillController().load_category_habit()
        self.cb_fill_category_habit()
    
    def load_goals(self, table):
        self.goals_controller.load_goals(table, 'May')
         
    
    def show_context_menu(self, position):
        menu = QMenu()
        update_action = menu.addAction('Actualizar')
        action = menu.exec_(self.combo_study_of.mapToGlobal(position))
        #if action == update_action:
        self.cb_fill_category_habit_from_db()
        self.refresh()
    
    def add_habit_time(self):
        fields = [[self.input_minutes_study, 'number', self.label_minutes_study],
                  [self.combo_study_of, 'cb', self.label_cb_study_of]]
        
        if not validate_fields(fields):
            return 
        
        name_habit = self.combo_study_of.currentText()
        input_text = self.input_minutes_study.text().strip()
        study_time = float(input_text)
        
        model = AddHabitTimeModel(name_habit, study_time)
        self.study_day.add_habit(model)
        clean_fields(fields)
        
        

    def add_habit_category(self):
        self.add_habit_view = AddHabitView()
        
    
    def add_goal(self):
        self.add_goal_view = AddGoalView()

    def refresh(self):
        self.cb_fill_category_habit_from_db()
        self.table_goal.setRowCount(0)
        self.load_goals(self.table_goal)
        self.table_study_day.setRowCount(0)
        self.study_day.load(self.table_study_day)
