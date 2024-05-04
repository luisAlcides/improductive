import os

from PyQt6 import uic
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QApplication, QVBoxLayout, QLabel, QPushButton, QLineEdit, QComboBox, QFormLayout, QWidget, \
    QTabWidget, QMainWindow, QHBoxLayout

from view.AddHabitView import AddHabitView

script_directory = os.path.dirname(os.path.abspath(__file__))
ui_file_path = os.path.join(script_directory, 'ui', 'mainView.ui')


class MainView(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("ImProductive")
        self.setGeometry(100, 100, 800, 600)

        self.create_menu_bar()
        self.create_tabs()

    def create_menu_bar(self):
        menubar = self.menuBar()

        file_menu = menubar.addMenu('File')

        exit_action = QAction('Exit', self)
        self.add_habit_action = QAction('Add Habit')
        exit_action.triggered.connect(self.close)
        self.add_habit_action.triggered.connect(self.add_habit)
        file_menu.addAction(self.add_habit_action)
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
        layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        form_layout = QFormLayout()

        label_minutes_study = QLabel('Minutes study today')
        layout.addWidget(label_minutes_study)

        input_minutes_study = QLineEdit()
        layout.addWidget(input_minutes_study)

        label_study_of = QLabel("Study of:")
        layout.addWidget(label_study_of)

        combo_study_of = QComboBox()
        combo_study_of.addItems(["Day", "Week", "Month"])
        layout.addWidget(combo_study_of)

        button = QPushButton("Add")
        button.clicked.connect(self.on_submit_clicked)
        layout.addWidget(button)


        label_goal_month = QLabel("Goal Month:")
        label_goal_month_result = QLabel('0')
        form_layout.addRow(label_goal_month, label_goal_month_result)

        label_last_month = QLabel("Last Month:")
        label_last_month_result = QLabel('0')
        form_layout.addRow(label_last_month, label_last_month_result)

        label_study_day = QLabel("Day:")
        label_study_day_result = QLabel('0')
        form_layout.addRow(label_study_day, label_study_day_result)

        label_study_week = QLabel("Week:")
        label_study_week_result = QLabel('0')
        form_layout.addRow(label_study_week, label_study_week_result)

        label_study_month = QLabel("Month:")
        label_study_month_result = QLabel('0')
        form_layout.addRow(label_study_month, label_study_month_result)

        layout.addLayout(form_layout)

        tab.setLayout(layout)

    def setup_tab2(self, tab):
        layout = QVBoxLayout()
        label_tab2 = QLabel("This is Tab 2")
        layout.addWidget(label_tab2)
        tab.setLayout(layout)

    def on_submit_clicked(self):
        # Placeholder for submit button functionality
        pass


    def add_habit(self):
        self.add_habit_view = AddHabitView()
        return self.add_habit_view
