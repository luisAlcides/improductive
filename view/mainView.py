import sys
import os
import datetime
from PySide6.QtCore import Qt, QTimer, QSize, Signal, QObject
from PySide6.QtGui import QAction, QIcon, QPixmap, QPalette
from PySide6.QtWidgets import (
    QApplication,
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
    QFileDialog,
    QMenu,
    QSystemTrayIcon,
    QProgressBar,
)

from view.addHabitView import AddHabitView
from view.addGoalView import AddGoalView
from view.chartViewAll import ChartViewAll
from view.monthlySchedule import MonthlySchedule

from connection import Connection

from controller.habitController import HabitController
from controller.goalDataController import GoalDataController
from controller.addHabitTimeController import AddHabitTimeController
from controller.studyDataController import StudyDataController
from controller.updateStudyDayHabitController import UpdateStudyDayHabitController
from controller.exportImportDatabaseController import ExportImportDatabaseController

from model.addHabitTimeModel import AddHabitTimeModel

from view.chartViewGoal import ChartViewDay

from utils.func import (
    clean_fields,
    data_of_table_all,
    message_delete,
    data_of_table,
    delete_from_table,
    message_edit,
    edit_from_table,
    cb_fill_category_habit,
)
from utils.validation import validate_fields

script_directory = os.path.dirname(os.path.abspath(__file__))
database_path = os.path.join(script_directory, "..", "dbimproductive.db")

ico_habit_path = os.path.join(script_directory, "icons", "add_habit.png")
ico_goal_path = os.path.join(script_directory, "icons", "add_goal.png")
ico_update_path = os.path.join(script_directory, "icons", "update.png")
ico_delete_path = os.path.join(script_directory, "icons", "delete.png")
ico_add_path = os.path.join(script_directory, "icons", "add.png")
ico_refresh_path = os.path.join(script_directory, "icons", "refresh.png")
ico_start_timer_path = os.path.join(script_directory, "icons", "start_timer.png")
ico_stop_timer_path = os.path.join(script_directory, "icons", "stop_timer.png")
ico_pause_timer_path = os.path.join(script_directory, "icons", "pause_timer.png")
ico_toggle_timer_path = os.path.join(script_directory, "icons", "toggle_timer.png")


class Communicator(QObject):
    reset_signal = Signal()


class MainView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = Connection()
        self.db.setup_database()

        self.timer_mode = False
        self.elapsed_time = 0

        self.setWindowTitle("ImProductive")
        self.setGeometry(100, 100, 800, 600)

        self.study_day = AddHabitTimeController()
        self.study_day_controller = StudyDataController()
        self.goals_controller = GoalDataController()
        self.habit_controller = HabitController()
        self.controller_ei_database = ExportImportDatabaseController(database_path)

        self.label_day_left = QLabel()
        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setStyleSheet(
            """
            QProgressBar {
                border: 2px solid #B0C4DE;
                border-radius: 5px;
                text-align: center;
                font-size: 16px;
                background-color: #E6E6FA;
                color: #696969
                }
            QProgressBar::chunk {
                background-color: #87CEFA;
                width: 20px;
            }
        """
        )

        self.create_menu_bar()
        self.create_tabs()
        self.create_toolbar()
        cb_fill_category_habit(self.combo_study_of, self.habit_controller)

        self.communicator = Communicator()
        self.tray_timer = SystemTrayTimer(self)
        self.communicator.reset_signal.connect(self.reset_timer)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer_display)
        self.update_current_time()

        self.update_days_left()

    def create_menu_bar(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu("File")

        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)

        add_habit_action = QAction("Add Habit", self)
        add_habit_action.triggered.connect(self.add_habit_category)

        add_goal_action = QAction("Add Goal", self)
        add_goal_action.triggered.connect(self.add_goal)

        export_action = QAction("Export Database", self)
        export_action.triggered.connect(self.export_database)

        import_action = QAction("Import Database", self)
        import_action.triggered.connect(self.import_database)

        file_menu.addActions(
            [
                add_habit_action,
                add_goal_action,
                export_action,
                import_action,
                exit_action,
            ]
        )

    def create_tabs(self):
        tab_widget = QTabWidget()
        tab1 = QWidget()
        tab2 = QWidget()
        tab3 = QWidget()

        self.setup_tab1(tab1)
        self.setup_tab3(tab3)
        self.setup_tab2(tab2)

        tab_widget.addTab(tab1, "Habits")
        tab_widget.addTab(tab3, "Montly schedule")
        tab_widget.addTab(tab2, "Chart")
        self.setCentralWidget(tab_widget)

    def export_database(self):
        try:
            destination_path, _ = QFileDialog.getSaveFileName(
                self, "Export Database", "dbimproductive.db", "Database Files (*.db)"
            )
            if destination_path:
                self.controller_ei_database.exportDatabase(destination_path)
        except Exception as e:
            print(f"Error to export database: {e}")

    def import_database(self):
        try:
            source_path, _ = QFileDialog.getOpenFileName(
                self, "Import Database", "", "Database Files (*.db)"
            )
            if source_path:
                self.controller_ei_database.importDatabase(source_path)
        except Exception as e:
            print(f"Error to import database: {e}")

    def start_timer(self):
        self.timer.start(1000)
        self.btn_start_timer.setEnabled(False)
        self.btn_pause_timer.setEnabled(True)
        self.btn_stop_timer.setEnabled(True)

    def pause_timer(self):
        self.timer.stop()
        self.btn_start_timer.setEnabled(True)
        self.btn_pause_timer.setEnabled(False)
        self.btn_stop_timer.setEnabled(True)

    def stop_timer(self):
        self.timer.stop()
        self.input_minutes_study.setText(str(self.elapsed_time / 60))
        self.btn_start_timer.setEnabled(True)
        self.btn_pause_timer.setEnabled(False)
        self.btn_stop_timer.setEnabled(False)

    def reset_timer(self):
        self.stop_timer()
        self.elapsed_time = 0
        self.input_minutes_study.setText("00:00:00")
        self.tray_timer.update_display(self.elapsed_time)

    def update_timer_display(self):
        self.elapsed_time += 1
        hours = self.elapsed_time // 3600
        minutes = (self.elapsed_time % 3600) // 60
        seconds = self.elapsed_time % 60
        self.input_minutes_study.setText(f"{hours:02}:{minutes:02}:{seconds:02}")
        self.tray_timer.update_display(self.elapsed_time)

    def toggle_timer_manual(self):
        self.timer_mode = not self.timer_mode
        self.input_minutes_study.setReadOnly(self.timer_mode)
        self.btn_start_timer.setEnabled(self.timer_mode)
        self.btn_stop_timer.setEnabled(self.timer_mode)
        self.btn_pause_timer.setEnabled(self.timer_mode)

    def create_toolbar(self):
        toolbar = self.addToolBar("Toolbar")
        add_goal_action = QAction(QIcon(ico_goal_path), "Add Goal", self)
        add_habit_action = QAction(QIcon(ico_habit_path), "Add Habit", self)
        delete_action = QAction(QIcon(ico_delete_path), "Delete", self)
        update_action = QAction(QIcon(ico_update_path), "Update", self)
        toggle_timer_action = QAction(
            QIcon(ico_toggle_timer_path), "Toggle Timer/Manual", self
        )

        add_habit_action.triggered.connect(self.add_habit_category)
        add_goal_action.triggered.connect(self.add_goal)
        delete_action.triggered.connect(self.delete)
        update_action.triggered.connect(self.update)
        toggle_timer_action.triggered.connect(self.toggle_timer_manual)

        toolbar.addActions(
            [
                add_habit_action,
                add_goal_action,
                delete_action,
                update_action,
                toggle_timer_action,
            ]
        )

    def adjust_icon_size(self, event, btn):
        button_size = btn.size()
        btn.setIconSize(button_size)

    def update_current_time(self):
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        self.label_current_time.setText(current_time)
        current_date = datetime.datetime.now().strftime("%A %d %B %Y")
        self.label_current_date.setText(current_date)

    def update_days_left(self):
        today = datetime.datetime.today()
        end_of_year = datetime.datetime(today.year, 12, 31)
        start_of_year = datetime.datetime(today.year, 1, 1)
        days_left = (end_of_year - today).days
        total_days = (end_of_year - start_of_year).days
        progress = ((total_days - days_left) / total_days) * 100

        self.label_day_left.setText(f"Days to end the year")
        self.progress_bar.setValue(progress)
        self.progress_bar.setFormat(f"{days_left} days left")

    def setup_tab1(self, tab):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignHCenter)

        form_layout = QFormLayout()
        ly_vt_table = QVBoxLayout()
        ly_ht_time = QHBoxLayout()
        ly_ht_btn_timer = QHBoxLayout()
        ly_ht_time.addLayout(ly_ht_btn_timer)
        ly_ht_btn_timer.setAlignment(Qt.AlignLeft)

        self.label_current_time = QLabel()
        self.label_current_date = QLabel()
        self.label_day_left = QLabel()

        ly_ht_time.addWidget(self.label_current_time)
        ly_ht_time.addWidget(self.label_current_date)

        ly_vt_table.addWidget(self.label_day_left)
        ly_vt_table.addWidget(self.progress_bar)

        self.update_days_left()

        self.update_current_time()

        self.btn_start_timer = self.create_timer_button(
            ico_start_timer_path, "Start Timer", self.start_timer, ly_ht_btn_timer
        )
        self.btn_pause_timer = self.create_timer_button(
            ico_pause_timer_path, "Pause Timer", self.pause_timer, ly_ht_btn_timer
        )
        self.btn_stop_timer = self.create_timer_button(
            ico_stop_timer_path, "Stop Timer", self.stop_timer, ly_ht_btn_timer
        )

        ly_vt_table.addLayout(ly_ht_time)
        self.label_minutes_study = QLabel("Minutes study today")
        ly_vt_table.addWidget(self.label_minutes_study)

        self.input_minutes_study = QLineEdit()
        self.input_minutes_study.setPlaceholderText("in minutes")
        ly_vt_table.addWidget(self.input_minutes_study)

        self.label_cb_study_of = QLabel("Habit")
        ly_vt_table.addWidget(self.label_cb_study_of)

        self.combo_study_of = QComboBox()
        ly_vt_table.addWidget(self.combo_study_of)

        ly_ht_btn = QHBoxLayout()
        self.btn_add = self.create_timer_button(
            ico_add_path, "Add habit", self.add_habit_time, ly_ht_btn
        )

        btn_update = self.create_timer_button(
            ico_refresh_path, "Refresh", self.refresh, ly_ht_btn
        )
        label_goal_month = QLabel("Goal Today")
        ly_ht_table_chart = QHBoxLayout()
        ly_ht_table_chart.addLayout(ly_vt_table)

        ly_vt_table.addLayout(ly_ht_btn)
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
        self.table_study_day.setHorizontalHeaderLabels(["Habit", "Time", "Date"])
        self.study_day.load(self.table_study_day)
        self.table_study_day.setFocusPolicy(Qt.StrongFocus)

        ly_vt_table.addWidget(self.table_study_day)
        self.chart_view_goal = ChartViewDay()

        ly_ht_table_chart.addWidget(self.chart_view_goal)
        layout.addLayout(ly_ht_table_chart)
        layout.addLayout(form_layout)
        tab.setLayout(layout)

        self.update_chart()

    def setup_tab2(self, tab):
        layout = QVBoxLayout()
        self.chart_view = ChartViewAll(self.habit_controller)
        layout.addWidget(self.chart_view)
        tab.setLayout(layout)

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

    def setup_tab3(self, tab):
        layout = QVBoxLayout()
        self.montly_schedule = MonthlySchedule()
        layout.addWidget(self.montly_schedule)
        tab.setLayout(layout)

    def add_habit_category(self):
        self.add_habit_view = AddHabitView()
        self.refresh()

    def add_goal(self):
        self.add_goal_view = AddGoalView()
        self.refresh()

    def refresh(self):
        cb_fill_category_habit(self.combo_study_of, self.habit_controller)
        self.table_goal.setRowCount(0)
        self.load_goals(self.table_goal, self.current_month)
        self.table_study_day.setRowCount(0)
        self.study_day.load(self.table_study_day)
        self.montly_schedule.trigger_data_update()

        self.update_chart()

    def update_chart(self):
        self.table_goal_data = data_of_table_all(self.table_goal)
        self.table_study_day_data = data_of_table_all(self.table_study_day)
        self.chart_view_goal.clean()

        if self.table_goal_data or self.table_study_day_data:
            self.chart_view_goal.clean()
            self.chart_view_goal.setup_chart(
                self.table_goal_data, self.table_study_day_data
            )

    def delete(self):
        try:
            if self.table_goal.hasFocus():
                data = data_of_table(self.table_goal)
                message_confirm = message_delete()
                if message_confirm:
                    delete_from_table(self.table_goal, self.goals_controller, data)
            elif self.table_study_day.hasFocus():
                data = data_of_table(self.table_study_day)
                message_confirm = message_delete()
                if message_confirm:
                    delete_from_table(
                        self.table_study_day, self.study_day_controller, data
                    )
        except Exception as e:
            print(e)
        self.refresh()

    def update(self):
        try:
            if self.table_goal.hasFocus():
                data = data_of_table(self.table_goal)
                message_confirm = message_edit()
                if message_confirm:
                    edit_from_table(self.table_goal, self.goals_controller, data)
            elif self.table_study_day.hasFocus():
                data = data_of_table(self.table_study_day)
                study_id = edit_from_table(
                    self.table_study_day, self.study_day_controller, data
                )
                self.controller_update_study_day = UpdateStudyDayHabitController(
                    self.study_day_controller, study_id
                )
        except Exception as e:
            print(f"Error to update: {e}")
        self.refresh()

    def create_timer_button(self, icon_path, tooltip, callback, layout):
        button = QPushButton()
        button.setIcon(QIcon(icon_path))
        button.setFixedSize(QSize(35, 35))
        button.resizeEvent = lambda event: self.adjust_icon_size(event, button)
        button.setToolTip(tooltip)
        button.clicked.connect(callback)
        button.setStyleSheet("QPushButton {background-color: none; border: none;}")
        layout.addWidget(button)
        return button


class SystemTrayTimer:
    def __init__(self, main_view):
        self.main_view = main_view
        self.app = QApplication.instance() or QApplication(sys.argv)

        self.tray_icon = QSystemTrayIcon()
        self.set_tray_icon(ico_toggle_timer_path)

        self.tray_menu = QMenu()
        self.time_action = QAction("00:00:00")
        self.tray_menu.addAction(self.time_action)

        self.start_action = QAction("Start", self.main_view)
        self.start_action.triggered.connect(self.main_view.start_timer)
        self.tray_menu.addAction(self.start_action)

        self.pause_action = QAction("Pause", self.main_view)
        self.pause_action.triggered.connect(self.main_view.pause_timer)
        self.tray_menu.addAction(self.pause_action)

        self.reset_action = QAction("Reset", self.main_view)
        self.reset_action.triggered.connect(self.reset)
        self.tray_menu.addAction(self.reset_action)

        self.exit_action = QAction("Exit", self.app)
        self.exit_action.triggered.connect(self.app.quit)
        self.tray_menu.addAction(self.exit_action)

        self.tray_icon.setContextMenu(self.tray_menu)
        self.tray_icon.show()

    def reset(self):
        self.main_view.stop_timer()
        self.time_action.setText("00:00:00")

    def set_tray_icon(self, icon_path):
        pixmap = QPixmap(icon_path)
        scaled_pixmap = pixmap.scaled(
            64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
        icon = QIcon(scaled_pixmap)
        self.tray_icon.setIcon(icon)

    def update_display(self, elapsed_time):
        hours = elapsed_time // 3600
        minutes = (elapsed_time % 3600) // 60
        seconds = elapsed_time % 60
        time_string = f"{hours:02}:{minutes:02}:{seconds:02}"
        self.tray_icon.setToolTip(time_string)
        self.time_action.setText(time_string)
