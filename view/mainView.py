import sys
import os
import datetime
from PySide6.QtCore import Qt, QTimer, QTime, QSize, Signal, QObject, QUrl
from PySide6.QtGui import QAction, QIcon, QPixmap
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
    QProgressBar,
    QHeaderView,
)
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput

from view.addHabitView import AddHabitView
from view.addGoalView import AddGoalView
from view.chartViewAll import ChartViewAll
from view.monthlySchedule import MonthlySchedule
from view.chartViewDay import ChartViewDay

from connection import Connection
from controller.habitController import HabitController
from controller.goalDataController import GoalDataController
from controller.addHabitTimeController import AddHabitTimeController
from controller.studyDataController import StudyDataController
from controller.updateStudyDayHabitController import UpdateStudyDayHabitController
from controller.exportImportDatabaseController import ExportImportDatabaseController
from controller.updateGoalController import UpdateGoalController
from controller.timerGoalController import TimerGoalController
from model.addHabitTimeModel import AddHabitTimeModel

from utils.func import (
    clean_fields,
    data_of_table_all,
    message_delete,
    data_of_table,
    delete_from_table,
    message,
    edit_from_table_today,
    cb_fill_category_habit,
)
from utils.validation import validate_fields

script_directory = os.path.dirname(os.path.abspath(__file__))
database_path = os.path.join(script_directory, "..", "dbimproductive.db")

# Icon paths
ico_habit_path = os.path.join(script_directory, "icons", "add_habit.png")
ico_goal_path = os.path.join(script_directory, "icons", "add_goal.png")
ico_update_path = os.path.join(script_directory, "icons", "update.png")
ico_delete_path = os.path.join(script_directory, "icons", "delete.png")
ico_add_path = os.path.join(script_directory, "icons", "add.png")
ico_refresh_path = os.path.join(script_directory, "icons", "refresh.png")
ico_start_timer_path = os.path.join(
    script_directory, "icons", "start_timer.png")
ico_stop_timer_path = os.path.join(script_directory, "icons", "stop_timer.png")
ico_pause_timer_path = os.path.join(
    script_directory, "icons", "pause_timer.png")
ico_toggle_timer_path = os.path.join(
    script_directory, "icons", "toggle_timer.png")
ico_timer_path = os.path.join(script_directory, "icons", "timer.png")
ico_clear_path = os.path.join(script_directory, "icons", "clear.png")
ico_add_in_format_timer = os.path.join(
    script_directory, 'icons', 'ico_add_format_timer.png')

# Sound path
sound_path = os.path.join(script_directory, "sounds", "sound_timer.mp3")


class Communicator(QObject):
    reset_signal = Signal()


class MainView(QMainWindow):
    habit_added = Signal()
    goal_added = Signal()
    habit_time = Signal()
    montly_schedule_signal = Signal()
    add_habit_category_signal = Signal()

    signals_connected = {
        "start_stopwatch": False,
        "pause_stopwatch": False,
        "stop_stopwatch": False,
        "start_countdown": False,
        "pause_countdown": False,
        "stop_countdown": False,
    }

    def __init__(self):
        super().__init__()
        self.db = Connection()
        self.db.setup_database()
        self.required_study_time = 0
        self.remaining_time = QTime(0, 0, 0)
        self.stop_watch = False
        self.elapsed_time = 0
        self.toggle_time_stopwatch = True

        self.setWindowTitle("ImProductive")
        self.setGeometry(100, 100, 800, 600)

        self.study_day = AddHabitTimeController()
        self.study_day_controller = StudyDataController()
        self.goals_controller = GoalDataController()
        self.habit_controller = HabitController()
        self.controller_ei_database = ExportImportDatabaseController(
            database_path)

        self.init_ui()
        self.create_connections()
        self.update_days_left()

    def init_ui(self):
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

        self.communicator = Communicator()
        self.communicator.reset_signal.connect(self.reset_timer)

        self.create_menu_bar()

        self.montly_schedule = MonthlySchedule()
        self.chart_view = ChartViewAll(self.habit_controller)

        self.create_toolbar()

        # Stopwatch Timer
        self.stopwatch_timer = QTimer(self)
        self.stopwatch_timer.timeout.connect(self.update_stopwatch_display)

        # Countdown Timer
        self.countdown_timer = QTimer(self)
        self.countdown_timer.timeout.connect(self.update_countdown_display)

        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)

        self.create_tabs()

        self.update_current_time()
        self.chart_view.update_chart()

    def create_connections(self):
        self.habit_added.connect(self.chart_view.update_habit_selector)
        self.goal_added.connect(self.chart_view.update_chart)
        self.habit_time.connect(self.chart_view.update_chart)
        self.montly_schedule_signal.connect(
            self.montly_schedule.trigger_data_update)
        self.add_habit_category_signal.connect(self.refresh)

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
        tab_widget.addTab(tab3, "Monthly schedule")
        tab_widget.addTab(tab2, "Chart")
        self.setCentralWidget(tab_widget)

    def create_toolbar(self):
        toolbar = self.addToolBar("Toolbar")
        add_goal_action = QAction(QIcon(ico_goal_path), "Add Goal", self)
        add_habit_action = QAction(QIcon(ico_habit_path), "Add Habit", self)
        delete_action = QAction(QIcon(ico_delete_path), "Delete", self)
        update_action = QAction(QIcon(ico_update_path), "Update", self)
        self.toggle_timer_action = QAction(
            QIcon(ico_toggle_timer_path), "StopWatch", self
        )
        self.timer_action = QAction(QIcon(ico_timer_path), "Timer", self)
        clear_action = QAction(QIcon(ico_clear_path), "Clear", self)
        add_in_format_timer = QAction(
            QIcon(ico_add_in_format_timer), "Add in format timer", self)

        add_habit_action.triggered.connect(self.add_habit_category)
        add_goal_action.triggered.connect(self.add_goal)
        delete_action.triggered.connect(self.delete)
        update_action.triggered.connect(self.update)
        self.toggle_timer_action.triggered.connect(self.toggle_stopwatch)
        self.timer_action.triggered.connect(self.set_timer_goal)
        clear_action.triggered.connect(self.clear_timer_stopwatch)
        add_in_format_timer.triggered.connect(self.add_in_format_timer)

        toolbar.addActions(
            [
                add_habit_action,
                add_goal_action,
                delete_action,
                update_action,
                self.toggle_timer_action,
                self.timer_action,
                clear_action,
                add_in_format_timer
            ]
        )

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

        self.btn_start_stopwatch = self.create_timer_button(
            ico_start_timer_path, "Start Stopwatch", ly_ht_btn_timer
        )
        self.btn_pause_stopwatch = self.create_timer_button(
            ico_pause_timer_path, "Pause Stopwatch", ly_ht_btn_timer
        )
        self.btn_stop_stopwatch = self.create_timer_button(
            ico_stop_timer_path, "Stop Stopwatch", ly_ht_btn_timer
        )

        ly_vt_table.addLayout(ly_ht_time)

        self.label_cb_study_of = QLabel("Habit")
        ly_vt_table.addWidget(self.label_cb_study_of)

        self.combo_study_of = QComboBox()
        ly_vt_table.addWidget(self.combo_study_of)

        try:
            cb_fill_category_habit(self.combo_study_of, self.habit_controller)
        except Exception as e:
            print(f"Error filling category habit: {e}")

        self.label_minutes_study = QLabel("Minutes study today")
        ly_vt_table.addWidget(self.label_minutes_study)

        self.input_minutes_study = QLineEdit()
        self.input_minutes_study.setPlaceholderText("in minutes")
        ly_vt_table.addWidget(self.input_minutes_study)

        ly_ht_btn = QHBoxLayout()
        self.btn_add = self.create_timer_button(
            ico_add_path, "Add habit", ly_ht_btn, self.add_habit_time
        )

        btn_update = self.create_timer_button(
            ico_refresh_path, "Refresh", ly_ht_btn, self.refresh
        )
        label_goal_month = QLabel("Goal Today")
        ly_ht_table_chart = QHBoxLayout()
        ly_ht_table_chart.addLayout(ly_vt_table)

        ly_vt_table.addLayout(ly_ht_btn)
        self.table_goal = QTableWidget()
        self.table_goal.setColumnCount(3)
        self.table_goal.setHorizontalHeaderLabels(["Habit", "Goal", "Month"])
        self.table_goal.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)

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
        self.table_study_day.horizontalHeader().setSectionResizeMode(
            0, QHeaderView.Stretch
        )
        self.study_day.load(self.table_study_day)
        self.table_study_day.setFocusPolicy(Qt.StrongFocus)

        ly_vt_table.addWidget(self.table_study_day)
        self.chart_view_goal = ChartViewDay()

        ly_ht_table_chart.addWidget(self.chart_view_goal)
        layout.addLayout(ly_ht_table_chart)
        layout.addLayout(form_layout)
        tab.setLayout(layout)

        self.update_chart()
        self.reset_timer()
        self.clear_timer_stopwatch()

    def setup_tab2(self, tab):
        layout = QVBoxLayout()
        self.chart_view = ChartViewAll(self.habit_controller)
        self.chart_view.update_chart()
        layout.addWidget(self.chart_view)
        tab.setLayout(layout)

    def setup_tab3(self, tab):
        layout = QVBoxLayout()
        layout.addWidget(self.montly_schedule)
        tab.setLayout(layout)

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

    # Timer Goal Functions
    def disconnect_signals_btn(self):
        if self.signals_connected["start_stopwatch"]:
            self.btn_start_stopwatch.clicked.disconnect()
            self.signals_connected["start_stopwatch"] = False
        if self.signals_connected["pause_stopwatch"]:
            self.btn_pause_stopwatch.clicked.disconnect()
            self.signals_connected["pause_stopwatch"] = False
        if self.signals_connected["stop_stopwatch"]:
            self.btn_stop_stopwatch.clicked.disconnect()
            self.signals_connected["stop_stopwatch"] = False
        if self.signals_connected["start_countdown"]:
            self.btn_start_stopwatch.clicked.disconnect()
            self.signals_connected["start_countdown"] = False
        if self.signals_connected["pause_countdown"]:
            self.btn_pause_stopwatch.clicked.disconnect()
            self.signals_connected["pause_countdown"] = False
        if self.signals_connected["stop_countdown"]:
            self.btn_stop_stopwatch.clicked.disconnect()
            self.signals_connected["stop_countdown"] = False

    def set_timer_goal(self):
        self.toggle_time_stopwatch = False
        self.timer_active = True

        self.input_minutes_study.setReadOnly(self.timer_active)

        self.btn_start_stopwatch.setEnabled(self.timer_active)
        self.btn_stop_stopwatch.setEnabled(self.timer_active)
        self.btn_pause_stopwatch.setEnabled(self.timer_active)

        self.btn_start_stopwatch.clicked.connect(self.start_countdown)
        self.signals_connected["start_countdown"] = True
        self.btn_pause_stopwatch.clicked.connect(self.pause_countdown)
        self.signals_connected["pause_countdown"] = True
        self.btn_stop_stopwatch.clicked.connect(self.stop_countdown)
        self.signals_connected["stop_countdown"] = True

        self.controller_timer = TimerGoalController(
            self.combo_study_of.currentText())
        self.required_study_time = self.controller_timer.get_goal()
        self.set_study_time(self.required_study_time)

    def set_study_time(self, study_time):
        # Convert hours to seconds
        total_seconds = int(float(study_time) * 3600)
        self.remaining_time = QTime(0, 0, 0).addSecs(total_seconds)
        self.update_timer_display()

    def start_countdown(self):
        self.countdown_timer.start(1000)

    def pause_countdown(self):
        self.countdown_timer.stop()

    def stop_countdown(self):
        self.countdown_timer.stop()
        self.save_study_time_for_timer()
        self.play_sound()
        self.reset_timer()
        self.clear_timer_stopwatch()
        self.refresh()

    def update_countdown_display(self):
        self.remaining_time = self.remaining_time.addSecs(-1)
        self.update_timer_display()
        if self.remaining_time == QTime(0, 0, 0):
            self.stop_countdown()

    def update_timer_display(self):
        self.input_minutes_study.setText(
            self.remaining_time.toString("hh:mm:ss"))

    def save_study_time_for_timer(self):
        try:
            name_habit = self.combo_study_of.currentText()
            from_input = (
                self.required_study_time
                if self.required_study_time is not None
                else 0
            ) * 60
            from_input = float(from_input)
            model = AddHabitTimeModel(name_habit, from_input)
            self.study_day.add_habit(model)
            self.clear_timer_stopwatch()
            message("Study time saved successfully")
        except Exception as e:
            print(f"Error to save study time for timer: {e}")

    # Stopwatch Functions
    def toggle_stopwatch(self):
        self.toggle_time_stopwatch = True
        self.stop_watch = True

        self.input_minutes_study.setReadOnly(self.stop_watch)
        self.btn_start_stopwatch.setEnabled(self.stop_watch)
        self.btn_stop_stopwatch.setEnabled(self.stop_watch)
        self.btn_pause_stopwatch.setEnabled(self.stop_watch)
        self.btn_start_stopwatch.clicked.connect(self.start_stopwatch)
        self.signals_connected["start_stopwatch"] = True
        self.btn_pause_stopwatch.clicked.connect(self.pause_stopwatch)
        self.signals_connected["pause_stopwatch"] = True
        self.btn_stop_stopwatch.clicked.connect(self.stop_stopwatch)
        self.signals_connected["stop_stopwatch"] = True

    def start_stopwatch(self):
        self.stopwatch_timer.start(1000)
        self.btn_start_stopwatch.setEnabled(False)
        self.btn_pause_stopwatch.setEnabled(True)
        self.btn_stop_stopwatch.setEnabled(True)

    def pause_stopwatch(self):
        self.stopwatch_timer.stop()
        self.btn_start_stopwatch.setEnabled(True)
        self.btn_pause_stopwatch.setEnabled(False)
        self.btn_stop_stopwatch.setEnabled(True)

    def stop_stopwatch(self):
        self.stopwatch_timer.stop()
        self.save_study_time_for_stopwatch()
        self.reset_timer()
        self.play_sound()
        self.clear_timer_stopwatch()
        self.refresh()

    def update_stopwatch_display(self):
        self.elapsed_time += 1
        hours = self.elapsed_time // 3600
        minutes = (self.elapsed_time % 3600) // 60
        seconds = self.elapsed_time % 60
        self.input_minutes_study.setText(
            f"{hours:02}:{minutes:02}:{seconds:02}")

    def save_study_time_for_stopwatch(self):
        try:
            name_habit = self.combo_study_of.currentText()
            from_input = self.input_minutes_study.text().strip().split(":")
            hours, minutes, seconds = map(int, from_input)
            study_time = hours * 60 + minutes + seconds / 60
            study_time = float(study_time)
            model = AddHabitTimeModel(name_habit, study_time)
            self.study_day.add_habit(model)
            self.clear_timer_stopwatch()
            message("Study time saved successfully")
        except Exception as e:
            print(f"Error to save study time for stopwatch: {e}")

    def clear_timer_stopwatch(self):
        self.combo_study_of.setCurrentIndex(-1)
        self.input_minutes_study.clear()
        self.elapsed_time = 0
        self.stop_watch = False
        self.toggle_time_stopwatch = False
        self.toggle_timer_action.setEnabled(True)
        self.timer_action.setEnabled(True)
        self.timer_active = False
        self.btn_start_stopwatch.setEnabled(False)
        self.btn_stop_stopwatch.setEnabled(False)
        self.btn_pause_stopwatch.setEnabled(False)
        self.disconnect_signals_btn()
        self.clear_fields()

    def reset_timer(self):
        self.elapsed_time = 0
        self.remaining_time = QTime(0, 0, 0)
        self.set_study_time(self.required_study_time)
        self.btn_start_stopwatch.setEnabled(False)
        self.btn_pause_stopwatch.setEnabled(False)
        self.btn_stop_stopwatch.setEnabled(False)
        self.input_minutes_study.setReadOnly(False)
        self.stop_watch = False
        self.timer_active = False
        self.clear_timer_stopwatch()
        self.refresh()

    def play_sound(self):
        self.player.setSource(QUrl.fromLocalFile(sound_path))
        self.player.play()

    def add_habit_category(self):
        self.add_habit_view = AddHabitView()
        self.add_habit_view.show()
        self.add_habit_view.habit_added.connect(self.on_habit_added)

    def on_habit_added(self):
        self.refresh()
        self.habit_added.emit()
        self.montly_schedule_signal.emit()

    def add_goal(self):
        self.add_goal_view = AddGoalView()
        self.add_goal_view.show()
        self.add_goal_view.goal_added.connect(self.on_goal_added)

    def on_goal_added(self):
        self.refresh()
        self.goal_added.emit()
        self.montly_schedule_signal.emit()

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
        self.play_sound()
        self.refresh()
        self.habit_time.emit()
        self.montly_schedule_signal.emit()

    def refresh(self):
        cb_fill_category_habit(self.combo_study_of, self.habit_controller)
        self.update_tables()
        self.montly_schedule.trigger_data_update()
        self.update_chart()
        self.chart_view.update_chart()
        self.clear_fields()

    def update_chart(self):
        self.table_goal_data = data_of_table_all(self.table_goal)
        self.table_study_day_data = data_of_table_all(self.table_study_day)
        self.chart_view_goal.clean()

        if self.table_goal_data or self.table_study_day_data:
            self.chart_view_goal.clean()
            self.chart_view_goal.setup_chart(
                self.table_goal_data, self.table_study_day_data
            )

    def update_tables(self):
        self.table_goal.setRowCount(0)
        self.load_goals(self.table_goal, self.current_month)
        self.table_study_day.setRowCount(0)
        self.study_day.load(self.table_study_day)

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
                if data:
                    goal_id = edit_from_table_today(
                        self.table_goal, self.goals_controller, data
                    )
                    if goal_id:
                        self.controller_update_goal = UpdateGoalController(
                            self.goals_controller, goal_id
                        )

            elif self.table_study_day.hasFocus():
                data = data_of_table(self.table_study_day)
                if data:
                    study_id = edit_from_table_today(
                        self.table_study_day, self.study_day_controller, data
                    )
                    if study_id:
                        self.controller_update_study_day = (
                            UpdateStudyDayHabitController(
                                self.study_day_controller, study_id
                            )
                        )
        except Exception as e:
            print(f"Error to update: {e}")
        self.refresh()

    def load_goals(self, table, month):
        self.goals_controller.load_goals(table, month)

    def create_timer_button(self, icon_path, tooltip, layout, callback=None):
        button = QPushButton()
        button.setIcon(QIcon(icon_path))
        button.setFixedSize(QSize(35, 35))
        button.resizeEvent = lambda event: self.adjust_icon_size(event, button)
        button.setToolTip(tooltip)
        button.setStyleSheet(
            "QPushButton {background-color: none; border: none;}")
        button.clicked.connect(callback)
        button.setStyleSheet(
            """
                QPushButton {
                    background-color: none;
                    border: none;
                }
                QPushButton:hover {
                    background-color: #dcdcdc; /* Cambia a un color de fondo ligeramente gris */
                    border: 1px solid #c0c0c0; /* Borde ligero similar a un QAction */
                }
            """
        )
        layout.addWidget(button)
        return button

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

    def clear_fields(self):
        self.input_minutes_study.clear()
        self.combo_study_of.setCurrentIndex(0)
        self.btn_add.clicked.disconnect()
        self.btn_add.clicked.connect(self.add_habit_time)
        self.input_minutes_study.setPlaceholderText('In minutes')

    def add_in_format_timer(self):
        self.input_minutes_study.setPlaceholderText('hh:mm:ss')
        self.btn_add.clicked.disconnect()
        self.btn_add.clicked.connect(self.add_habit_time_in_format_timer)

    def add_habit_time_in_format_timer(self):
        try:
            name_habit = self.combo_study_of.currentText()
            from_input = self.input_minutes_study.text().strip().split(":")
            hours, minutes, seconds = map(int, from_input)
            study_time = hours * 60 + minutes + seconds / 60
            study_time = float(study_time)
            model = AddHabitTimeModel(name_habit, study_time)
            self.study_day.add_habit(model)
            message("Study time saved successfully")
            self.play_sound()
            self.refresh()
        except Exception as e:
            print(f"Error to save study time for stopwatch: {e}")
