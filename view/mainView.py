import os

import datetime

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QComboBox,
    QFormLayout,
    QWidget,
    QTabWidget,
    QMainWindow,
    QTableWidget,
)

from view.addHabitView import AddHabitView
from view.addGoalView import AddGoalView

from connection import Connection

from controller.cbFillController import CbFillController
from controller.goalDataController import GoalDataController
from controller.addHabitTimeController import AddHabitTimeController
from controller.studyDataController import StudyDataController
from controller.updateStudyDayHabitController import UpdateStudyDayHabitController

from model.addHabitTimeModel import AddHabitTimeModel

from view.chartViewGoal import ChartViewDay


from utils.func import (
    clean_fields,
    data_of_table_all,
    message_delete,
    data_of_table,
    delete_from_table,
    message_edit,
    edit_from_table
)
from utils.validation import validate_fields

script_directory = os.path.dirname(os.path.abspath(__file__))
ico_habit_path = os.path.join(script_directory, "icons", "add_habit.png")
ico_goal_path = os.path.join(script_directory, "icons", "add_goal.png")
ico_update_path = os.path.join(script_directory, "icons", "update.png")
ico_delete_path = os.path.join(script_directory, "icons", "delete.png")


class MainView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = Connection()
        self.db.setup_database()

        self.setWindowTitle("ImProductive")
        self.setGeometry(100, 100, 800, 600)

        self.study_day = AddHabitTimeController()
        self.study_day_controller = StudyDataController()
        self.goals_controller = GoalDataController()

        self.create_menu_bar()
        self.create_tabs()
        self.toolbar()
        self.cb_fill_category_habit_from_db()

    def create_menu_bar(self):
        menubar = self.menuBar()

        file_menu = menubar.addMenu("File")

        exit_action = QAction("Exit", self)
        add_habit_action = QAction("Add Habit", self)
        add_goal_action = QAction("Add Goal", self)

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

    def toolbar(self):
        toolbar = self.addToolBar("Toolbar")
        add_goal_action = QAction(QIcon(ico_goal_path), "Add Goal", self)
        add_habit_action = QAction(QIcon(ico_habit_path), "Add Habit", self)
        delete_action = QAction(QIcon(ico_delete_path), "Delete", self)
        update_action = QAction(QIcon(ico_update_path), "Update", self)
        add_habit_action.triggered.connect(self.add_habit_category)
        add_goal_action.triggered.connect(self.add_goal)
        delete_action.triggered.connect(self.delete)
        update_action.triggered.connect(self.update)
        toolbar.addAction(add_habit_action)
        toolbar.addAction(add_goal_action)
        toolbar.addAction(delete_action)
        toolbar.addAction(update_action)

    def setup_tab1(self, tab):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignHCenter)

        form_layout = QFormLayout()

        self.label_minutes_study = QLabel("Minutes study today")
        layout.addWidget(self.label_minutes_study)

        self.input_minutes_study = QLineEdit()
        layout.addWidget(self.input_minutes_study)

        self.label_cb_study_of = QLabel("Habit")
        layout.addWidget(self.label_cb_study_of)

        self.combo_study_of = QComboBox()
        layout.addWidget(self.combo_study_of)

        ly_ht_btn = QHBoxLayout()
        self.btn_add = QPushButton("Add")
        self.btn_add.clicked.connect(self.add_habit_time)
        ly_ht_btn.addWidget(self.btn_add)

        btn_update = QPushButton("Update")
        btn_update.clicked.connect(self.refresh)
        ly_ht_btn.addWidget(btn_update)

        layout.addLayout(ly_ht_btn)

        label_goal_month = QLabel("Goal Today")
        ly_ht_table_chart = QHBoxLayout()
        ly_vt_table = QVBoxLayout()
        ly_ht_table_chart.addLayout(ly_vt_table)

        self.table_goal = QTableWidget()
        self.table_goal.setColumnCount(3)
        self.table_goal.setHorizontalHeaderLabels(["Habit", "Goal", "Month"])

        self.current_month = datetime.datetime.now().strftime("%B")
        self.load_goals(self.table_goal, self.current_month)
        self.table_goal.setFocusPolicy(Qt.StrongFocus)

        ly_vt_table.addWidget(label_goal_month)
        ly_vt_table.addWidget(self.table_goal)

        label_study_of = QLabel("Today Study")
        ly_vt_table.addWidget(label_study_of)

        self.table_study_day = QTableWidget()
        self.table_study_day.setColumnCount(3)
        self.table_study_day.setHorizontalHeaderLabels(
            ["Habit", "Time", "Date"])
        self.study_day.load(self.table_study_day)
        self.table_study_day.setFocusPolicy(Qt.StrongFocus)

        ly_vt_table.addWidget(self.table_study_day)

        self.table_goal_data = data_of_table_all(self.table_goal)
        self.table_study_day_data = data_of_table_all(self.table_study_day)
        self.chart_view_goal = ChartViewDay()

        if self.table_goal_data and self.table_study_day_data:
            self.chart_view_goal.setup_chart(
                self.table_study_day_data, self.table_goal_data
            )

        ly_ht_table_chart.addWidget(self.chart_view_goal)
        layout.addLayout(ly_ht_table_chart)
        layout.addLayout(form_layout)

        tab.setLayout(layout)

    def setup_tab2(self, tab):
        layout = QVBoxLayout()

        self.chart_view = ChartViewDay()
        layout.addWidget(self.chart_view)
        tab.setLayout(layout)

    def cb_fill_category_habit(self):
        self.combo_study_of.clear()
        for category in self.cb_category_habit:
            self.combo_study_of.addItem(category[0])

    def cb_fill_category_habit_from_db(self):
        self.cb_category_habit = CbFillController().load_category_habit()
        self.cb_fill_category_habit()

    def load_goals(self, table, month):
        self.goals_controller.load_goals(table, month)

    def add_habit_time(self):
        fields = [
            [self.input_minutes_study, "number", self.label_minutes_study],
            [self.combo_study_of, "cb", self.label_cb_study_of],
        ]

        if not validate_fields(fields):
            return

        name_habit = self.combo_study_of.currentText()
        input_text = self.input_minutes_study.text().strip()
        study_time = float(input_text)

        model = AddHabitTimeModel(name_habit, study_time)
        self.study_day.add_habit(model)
        clean_fields(fields)
        self.refresh()

    def add_habit_category(self):
        self.add_habit_view = AddHabitView()
        self.refresh()

    def add_goal(self):
        self.add_goal_view = AddGoalView()
        self.refresh()

    def refresh(self):
        self.cb_fill_category_habit_from_db()
        self.table_goal.setRowCount(0)
        self.load_goals(self.table_goal, self.current_month)
        self.table_study_day.setRowCount(0)
        self.study_day.load(self.table_study_day)

        self.table_goal_data = data_of_table_all(self.table_goal)
        self.table_study_day_data = data_of_table_all(self.table_study_day)

        if self.table_goal_data and self.table_study_day_data:
            self.chart_view_goal.clean()
            self.chart_view_goal.setup_chart(
                self.table_study_day_data, self.table_goal_data
            )

    def delete(self):
        try:
            if self.table_goal.hasFocus():
                data = data_of_table(self.table_goal)
                message_confirm = message_delete()
                if message_confirm:
                    delete_from_table(
                        self.table_goal, self.goals_controller, data)
            elif self.table_study_day.hasFocus():
                data = data_of_table(self.table_study_day)
                message_confirm = message_delete()
                if message_confirm:
                    delete_from_table(self.table_study_day,
                                      self.study_day_controller, data)
        except Exception as e:
            print(e)
        self.refresh()

    def update(self):
        try:
            if self.table_goal.hasFocus():
                data = data_of_table(self.table_goal)
                message_confirm = message_edit()
                if message_confirm:
                    edit_from_table(self.table_goal,
                                    self.goals_controller,
                                    data)
            elif self.table_study_day.hasFocus():
                data = data_of_table(self.table_study_day)

                study_id = edit_from_table(self.table_study_day,
                                           self.study_day_controller,
                                           data)
                self.controller_update_study_day = UpdateStudyDayHabitController
                (
                    self.study_day_controller,
                    study_id)
        except Exception as e:
            print(f'Error to update: {e}')
        self.refresh()
