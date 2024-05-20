import sys
import os
import datetime
from PySide6.QtCore import Qt, QTimer, QTime, QSize, Signal, QObject
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
    QSystemTrayIcon,
    QToolBar
)

from view.addHabitView import AddHabitView
from view.addGoalView import AddGoalView

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
    cb_fill_category_habit
)
from utils.roundIconButton import RoundIconButton
from utils.validation import validate_fields

script_directory = os.path.dirname(os.path.abspath(__file__))
database_path = os.path.join(script_directory, '..', 'dbimproductive.db')

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
        self.timer = QTimer(self)
        self.elapsed_time = 0

        self.timer_time = QTimer(self)
        self.timer_time.timeout.connect(self.update_current_time)
        self.timer_time.start(1000)

        self.setWindowTitle("ImProductive")
        self.setGeometry(100, 100, 800, 600)

        self.study_day = AddHabitTimeController()
        self.study_day_controller = StudyDataController()
        self.goals_controller = GoalDataController()
        self.habit_controller = HabitController()
        self.controller_ei_database = ExportImportDatabaseController(database_path)

        self.create_menu_bar()
        self.create_tabs()
        self.toolbar()
        cb_fill_category_habit(self.combo_study_of, self.habit_controller)

        # Inicializar el temporizador en la barra del sistema
        self.communicator = Communicator()
        self.tray_timer = SystemTrayTimer(self.update_timer, self.elapsed_time, self.communicator.reset_signal)

        # Conectar la señal de reinicio al método de reinicio
        self.communicator.reset_signal.connect(self.reset_timer)

    def create_menu_bar(self):
        menubar = self.menuBar()

        file_menu = menubar.addMenu("File")

        exit_action = QAction("Exit", self)
        add_habit_action = QAction("Add Habit", self)
        add_goal_action = QAction("Add Goal", self)

        export_action = QAction('Export Database', self)
        export_action.triggered.connect(self.export_database)

        import_action = QAction('Import Database', self)
        import_action.triggered.connect(self.import_database)

        exit_action.triggered.connect(self.close)
        add_habit_action.triggered.connect(self.add_habit_category)
        add_goal_action.triggered.connect(self.add_goal)

        file_menu.addAction(add_habit_action)
        file_menu.addAction(add_goal_action)
        file_menu.addAction(export_action)
        file_menu.addAction(import_action)
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

    def export_database(self):
        try:
            default_name = 'dbimproductive.db'
            file_filter = 'Database Files (*.db)'
            destination_path, _ = QFileDialog.getSaveFileName(
                self, 'Export Database', default_name, file_filter)
            if destination_path:
                self.controller_ei_database.exportDatabase(destination_path)
        except Exception as e:
            print(f'Error to export database: {e}')

    def import_database(self):
        try:
            source_path, _ = QFileDialog.getOpenFileName(
                self, 'Import Database', '', 'Database Files (*.db)')
            if source_path:
                self.controller_ei_database.importDatabase(source_path)
        except Exception as e:
            print(f'Error to import database: {e}')

    def timer_start(self, interval):
        self.timer_start(interval)

    def timer_stop(self):
        self.timer.stop()

    def start_timer(self):
        self.timer.start(1000)
        self.tray_timer.start_timer()
        self.btn_start_timer.setEnabled(False)
        self.btn_pause_timer.setEnabled(True)
        self.btn_stop_timer.setEnabled(True)

    def pause_timer(self):
        self.timer.stop()
        self.tray_timer.stop_timer()
        self.btn_start_timer.setEnabled(True)
        self.btn_pause_timer.setEnabled(False)
        self.btn_stop_timer.setEnabled(True)

    def stop_timer(self):
        self.timer.stop()
        self.tray_timer.stop_timer()
        self.input_minutes_study.setText(str(self.elapsed_time / 60))
        self.btn_start_timer.setEnabled(True)
        self.btn_pause_timer.setEnabled(False)
        self.btn_stop_timer.setEnabled(False)

    def reset_timer(self):
        self.stop_timer()
        self.elapsed_time = 0
        self.input_minutes_study.setText("00:00:00")
        self.tray_timer.update_display(self.elapsed_time)

    def update_timer(self):
        self.elapsed_time += 1
        hours = self.elapsed_time // 3600
        minutes = (self.elapsed_time % 3600) // 60
        seconds = self.elapsed_time % 60
        self.input_minutes_study.setText(f"{hours:02}:{minutes:02}:{seconds:02}")
        self.tray_timer.update_display(self.elapsed_time)

    def toggle_timer_manual(self):
        if self.timer_mode:
            self.timer_mode = False
            self.input_minutes_study.setReadOnly(False)
            self.btn_start_timer.setEnabled(False)
            self.btn_stop_timer.setEnabled(False)
            self.btn_pause_timer.setEnabled(False)

        else:
            self.timer_mode = True
            self.input_minutes_study.setReadOnly(True)
            self.btn_start_timer.setEnabled(True)
            self.btn_stop_timer.setEnabled(True)
            self.btn_pause_timer.setEnabled(True)

    def toolbar(self):
        toolbar = self.addToolBar("Toolbar")
        add_goal_action = QAction(QIcon(ico_goal_path), "Add Goal", self)
        add_habit_action = QAction(QIcon(ico_habit_path), "Add Habit", self)
        delete_action = QAction(QIcon(ico_delete_path), "Delete", self)
        update_action = QAction(QIcon(ico_update_path), "Update", self)
        toggle_timer_action = QAction(QIcon(ico_toggle_timer_path), 'Toggle Timer/Manual', self)

        add_habit_action.triggered.connect(self.add_habit_category)
        add_goal_action.triggered.connect(self.add_goal)
        delete_action.triggered.connect(self.delete)
        update_action.triggered.connect(self.update)
        toggle_timer_action.triggered.connect(self.toggle_timer_manual)

        toolbar.addAction(add_habit_action)
        toolbar.addAction(add_goal_action)
        toolbar.addAction(delete_action)
        toolbar.addAction(update_action)
        toolbar.addAction(toggle_timer_action)


    def adjust_icon_size(self, event, btn):
        button_size = btn.size()
        btn.setIconSize(button_size)

    def update_current_time(self):
        current_time = datetime.datetime.now().strftime('%I:%M %p')
        self.label_current_time.setText(current_time)

        current_date = datetime.datetime.now().strftime('%A %d %B %Y')
        self.label_current_date.setText(current_date)

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
        ly_ht_time.addWidget(self.label_current_time)
        ly_ht_time.addWidget(self.label_current_date)

        self.update_current_time()

        # Timer buttons
        self.btn_start_timer = QPushButton()
        self.btn_start_timer.setIcon(QIcon(ico_start_timer_path))
        self.btn_start_timer.setFixedSize(QSize(35, 35))
        self.btn_start_timer.resizeEvent = lambda event: self.adjust_icon_size(event, self.btn_start_timer)
        self.btn_start_timer.setToolTip("Start Timer")
        self.btn_start_timer.setEnabled(False)
        self.btn_start_timer.clicked.connect(self.start_timer)
        ly_ht_btn_timer.addWidget(self.btn_start_timer)

        self.btn_pause_timer = QPushButton()
        self.btn_pause_timer.setIcon(QIcon(ico_pause_timer_path))
        self.btn_pause_timer.setToolTip("Pause Timer")
        self.btn_pause_timer.setFixedSize(QSize(35, 35))
        self.btn_pause_timer.resizeEvent = lambda event: self.adjust_icon_size(event, self.btn_pause_timer)
        self.btn_pause_timer.setEnabled(False)
        self.btn_pause_timer.clicked.connect(self.pause_timer)
        ly_ht_btn_timer.addWidget(self.btn_pause_timer)

        self.btn_stop_timer = QPushButton()
        self.btn_stop_timer.setIcon(QIcon(ico_stop_timer_path))
        self.btn_stop_timer.setToolTip("Stop Timer")
        self.btn_stop_timer.setFixedSize(QSize(35, 35))
        self.btn_stop_timer.resizeEvent = lambda event: self.adjust_icon_size(event, self.btn_stop_timer)
        self.btn_stop_timer.setEnabled(False)
        self.btn_stop_timer.clicked.connect(self.stop_timer)
        ly_ht_btn_timer.addWidget(self.btn_stop_timer)

        ly_vt_table.addLayout(ly_ht_time)
        self.label_minutes_study = QLabel("Minutes study today")
        ly_vt_table.addWidget(self.label_minutes_study)

        self.input_minutes_study = QLineEdit()
        self.input_minutes_study.setPlaceholderText('in minutes')
        ly_vt_table.addWidget(self.input_minutes_study)

        self.label_cb_study_of = QLabel("Habit")
        ly_vt_table.addWidget(self.label_cb_study_of)

        self.combo_study_of = QComboBox()
        ly_vt_table.addWidget(self.combo_study_of)

        ly_ht_btn = QHBoxLayout()

        self.btn_add = QPushButton('')
        self.btn_add.setIcon(QIcon(ico_add_path))
        self.btn_add.setFixedSize(QSize(35, 35))
        self.btn_add.resizeEvent = lambda event: self.adjust_icon_size(event, self.btn_add)
        self.btn_add.setToolTip("Add habit")
        self.btn_add.setShortcut("Ctrl+a")
        self.btn_add.clicked.connect(self.add_habit_time)
        ly_ht_btn.addWidget(self.btn_add)

        btn_update = QPushButton('')
        btn_update.setIcon(QIcon(ico_refresh_path))
        btn_update.setFixedSize(QSize(35, 35))
        btn_update.resizeEvent = lambda event: self.adjust_icon_size(event, btn_update)
        btn_update.setToolTip('Refresh')
        btn_update.setShortcut('Ctrl+r')
        btn_update.clicked.connect(self.refresh)
        ly_ht_btn.addWidget(btn_update)

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

        self.table_goal_data = data_of_table_all(self.table_goal)
        self.table_study_day_data = data_of_table_all(self.table_study_day)
        self.chart_view_goal = ChartViewDay()

        if self.table_goal_data and self.table_study_day_data:
            self.chart_view_goal.setup_chart(self.table_study_day_data, self.table_goal_data)

        ly_ht_table_chart.addWidget(self.chart_view_goal)
        layout.addLayout(ly_ht_table_chart)
        layout.addLayout(form_layout)

        tab.setLayout(layout)

    def setup_tab2(self, tab):
        layout = QVBoxLayout()

        self.chart_view = ChartViewDay()
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

        self.table_goal_data = data_of_table_all(self.table_goal)
        self.table_study_day_data = data_of_table_all(self.table_study_day)

        if self.table_goal_data and self.table_study_day_data:
            self.chart_view_goal.clean()
            self.chart_view_goal.setup_chart(self.table_study_day_data, self.table_goal_data)

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
                    delete_from_table(self.table_study_day, self.study_day_controller, data)
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

                study_id = edit_from_table(self.table_study_day, self.study_day_controller, data)
                self.controller_update_study_day = UpdateStudyDayHabitController(self.study_day_controller, study_id)
        except Exception as e:
            print(f'Error to update: {e}')
        self.refresh()

class SystemTrayTimer:
    def __init__(self, update_callback, elapsed_time, reset_signal):
        self.app = QApplication.instance() or QApplication(sys.argv)

        self.update_callback = update_callback
        self.elapsed_time = elapsed_time
        self.reset_signal = reset_signal

        # Configuración del temporizador
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)
        self.time = QTime(0, 0, 0)
        self.timer_running = False

        # Crear un icono de sistema
        self.tray_icon = QSystemTrayIcon()
        self.set_tray_icon("path/to/high_resolution_icon.png")  # Asegúrate de que la ruta del icono sea correcta

        # Crear un menú para el icono de sistema
        self.tray_menu = QMenu()

        self.time_action = QAction("00:00:00")  # Acción para mostrar el temporizador en tiempo real
        self.tray_menu.addAction(self.time_action)

        self.start_action = QAction("Iniciar")
        self.start_action.triggered.connect(self.start_timer)
        self.tray_menu.addAction(self.start_action)

        self.stop_action = QAction("Pausar")
        self.stop_action.triggered.connect(self.stop_timer)
        self.tray_menu.addAction(self.stop_action)

        self.reset_action = QAction("Reiniciar")
        self.reset_action.triggered.connect(self.reset_timer)
        self.tray_menu.addAction(self.reset_action)

        self.exit_action = QAction("Salir")
        self.exit_action.triggered.connect(self.app.quit)
        self.tray_menu.addAction(self.exit_action)

        self.tray_icon.setContextMenu(self.tray_menu)
        self.tray_icon.show()

        self.update_display()  # Inicializa la pantalla con el tiempo inicial

    def set_tray_icon(self, icon_path):
        # Cargar la imagen del icono
        pixmap = QPixmap(icon_path)

        # Escalar la imagen del icono
        scaled_pixmap = pixmap.scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        # Crear un QIcon a partir del pixmap escalado
        icon = QIcon(scaled_pixmap)

        # Establecer el icono escalado en el QSystemTrayIcon
        self.tray_icon.setIcon(icon)

    def start_timer(self):
        if not self.timer_running:
            self.timer.start(1000)
            self.timer_running = True

    def stop_timer(self):
        if self.timer_running:
            self.timer.stop()
            self.timer_running = False

    def reset_timer(self):
        self.stop_timer()
        self.elapsed_time = 0
        self.update_display()
        self.reset_signal.emit()

    def update_timer(self):
        self.elapsed_time += 1
        self.update_callback()
        self.update_display()

    def update_display(self, elapsed_time=None):
        if elapsed_time is not None:
            self.elapsed_time = elapsed_time
        hours = self.elapsed_time // 3600
        minutes = (self.elapsed_time % 3600) // 60
        seconds = self.elapsed_time % 60
        time_string = f"{hours:02}:{minutes:02}:{seconds:02}"
        self.tray_icon.setToolTip(time_string)
        self.time_action.setText(time_string)  # Actualiza el texto del QAction