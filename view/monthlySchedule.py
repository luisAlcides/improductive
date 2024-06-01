from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QComboBox,
    QTableWidget,
    QTableWidgetItem,
    QWidget,
    QHeaderView,
    QFrame,
)

import datetime
from connection import Connection


class MonthlySchedule(QWidget):
    data_updated = Signal()

    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.header_layout = QHBoxLayout()

        self.label_month = QLabel("Select Month:")
        self.combo_month = QComboBox()
        self.combo_month.addItems(
            [
                "January",
                "February",
                "March",
                "April",
                "May",
                "June",
                "July",
                "August",
                "September",
                "October",
                "November",
                "December",
            ]
        )

        self.header_layout.addWidget(self.label_month)
        self.header_layout.addWidget(self.combo_month)

        self.table_widget = QTableWidget()
        self.table_widget.setRowCount(0)
        self.table_widget.setColumnCount(32)  # 31 days + 1 for activities column
        self.setup_table_headers()

        self.layout.addLayout(self.header_layout)
        self.layout.addWidget(self.table_widget)

        # Totals layout
        self.totals_frame = QFrame()
        self.totals_layout = QVBoxLayout(self.totals_frame)

        self.total_month_label = QLabel("Total Study Time for the Month:")
        self.total_month_label.setStyleSheet("font-weight: bold;")
        self.totals_layout.addWidget(self.total_month_label)

        self.total_month_table = QTableWidget()
        self.total_month_table.setColumnCount(2)
        self.total_month_table.setHorizontalHeaderLabels(
            ["Habit", "Total Time (Month)"]
        )
        self.total_month_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )
        self.totals_layout.addWidget(self.total_month_table)

        self.overall_total_label = QLabel("Overall Total Study Time:")
        self.overall_total_label.setStyleSheet("font-weight: bold;")
        self.totals_layout.addWidget(self.overall_total_label)

        self.overall_total_table = QTableWidget()
        self.overall_total_table.setColumnCount(2)
        self.overall_total_table.setHorizontalHeaderLabels(
            ["Habit", "Total Time (Overall)"]
        )
        self.overall_total_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )
        self.totals_layout.addWidget(self.overall_total_table)

        self.layout.addWidget(self.totals_frame)

        # Fix the activity column and make other columns resizable
        self.table_widget.horizontalHeader().setSectionResizeMode(0, QHeaderView.Fixed)
        for col in range(1, 32):
            self.table_widget.horizontalHeader().setSectionResizeMode(
                col, QHeaderView.Stretch
            )
        self.table_widget.setColumnWidth(0, 150)
        self.table_widget.setHorizontalScrollMode(QTableWidget.ScrollPerPixel)

        self.data_updated.connect(self.load_current_month_data)

        # Select the current month
        current_month_index = datetime.datetime.now().month - 1
        self.combo_month.setCurrentIndex(current_month_index)
        self.load_current_month_data()

        # Connect the signal to load data when the month changes
        self.combo_month.currentTextChanged.connect(self.load_current_month_data)

    def setup_table_headers(self):
        self.table_widget.setHorizontalHeaderItem(0, QTableWidgetItem("ACTIVIDAD"))
        for day in range(1, 32):
            self.table_widget.setHorizontalHeaderItem(day, QTableWidgetItem(str(day)))

    def load_current_month_data(self):
        current_month = self.combo_month.currentText()
        self.load_month_data(current_month)

    def load_month_data(self, month):
        self.table_widget.setRowCount(0)  # Clear existing data
        month_data = self.get_month_data_from_db(month)  # Fetch data from DB
        total_study_time_per_habit = self.calculate_totals(month_data)
        overall_total_study_time = sum(total_study_time_per_habit.values())

        self.display_totals(total_study_time_per_habit, month)
        self.display_overall_totals()

    def calculate_totals(self, month_data):
        activities = list(month_data.keys())
        self.table_widget.setRowCount(len(activities))
        total_study_time_per_habit = {}

        for row, activity in enumerate(activities):
            self.table_widget.setItem(row, 0, QTableWidgetItem(activity))
            total_study_time = 0
            for day in range(1, 32):
                item = QTableWidgetItem()
                if day in month_data[activity]:
                    value = month_data[activity][day]
                    total_study_time += value
                    item.setText(str(value))
                    self.set_item_style(item, value, day)
                else:
                    self.set_item_style(item, None, day)
                self.table_widget.setItem(row, day, item)
            total_study_time_per_habit[activity] = total_study_time

        return total_study_time_per_habit

    def set_item_style(self, item, value, day):
        if value is not None:
            value = float(value)
            if value < 1:
                item.setBackground(QColor("#FF6961"))  # Light Red
            elif value < 3:
                item.setBackground(QColor("#FDFD96"))  # Light Yellow
            else:
                item.setBackground(QColor("#77DD77"))  # Light Green
            item.setTextAlignment(Qt.AlignCenter)
            item.setForeground(QColor("#000"))  # Black text for dark mode
        else:
            item.setBackground(QColor("#fff"))  # White
            item.setForeground(QColor("#000"))  # Black text for dark mode

        if self.is_sunday(day):
            item.setBackground(QColor("#e5e5e5"))  # Light Pink for Sundays
            item.setForeground(QColor("#000000"))  # Black text for Sundays

    def is_sunday(self, day):
        current_month = self.combo_month.currentIndex() + 1
        current_year = datetime.datetime.now().year
        try:
            date = datetime.date(current_year, current_month, day)
            return date.weekday() == 6  # 6 corresponds to Sunday
        except ValueError:
            return False

    def get_month_data_from_db(self, month):
        month_num = self.combo_month.findText(month) + 1
        month_data = {}
        with Connection() as cursor:
            cursor.execute(
                """
                SELECT ch.name, substr(h.date_current, 1, 2), h.study_time
                FROM habit h
                JOIN category_habits ch ON h.category_id = ch.id
                WHERE substr(h.date_current, 4, 2) = ?
                """,
                (str(month_num).zfill(2),),
            )
            rows = cursor.fetchall()
            for row in rows:
                activity, day, study_time = row
                day = int(day)
                if activity not in month_data:
                    month_data[activity] = {}
                month_data[activity][day] = round(study_time, 2)
        return month_data

    def get_total_study_time_all_months(self):
        total_study_time_all_months = {}
        with Connection() as cursor:
            cursor.execute(
                """
                SELECT ch.name, h.study_time
                FROM habit h
                JOIN category_habits ch ON h.category_id = ch.id
                """
            )
            rows = cursor.fetchall()
            for row in rows:
                activity, study_time = row
                if activity not in total_study_time_all_months:
                    total_study_time_all_months[activity] = 0
                total_study_time_all_months[activity] += round(study_time, 2)
        return total_study_time_all_months

    def display_totals(self, total_study_time_per_habit, month):
        self.total_month_table.setRowCount(0)
        sorted_totals = sorted(
            total_study_time_per_habit.items(), key=lambda x: x[1], reverse=True
        )
        for habit, time in sorted_totals:
            row_position = self.total_month_table.rowCount()
            self.total_month_table.insertRow(row_position)
            self.total_month_table.setItem(row_position, 0, QTableWidgetItem(habit))
            self.total_month_table.setItem(row_position, 1, QTableWidgetItem(str(time)))
            self.colorize_total_row(self.total_month_table, row_position, time)

        self.total_month_label.setText(
            f"Total Study Time for {month}: {sum(total_study_time_per_habit.values())} hours"
        )

    def display_overall_totals(self):
        total_study_time_all_months = self.get_total_study_time_all_months()
        sorted_totals = sorted(
            total_study_time_all_months.items(), key=lambda x: x[1], reverse=True
        )
        self.overall_total_table.setRowCount(0)
        for habit, time in sorted_totals:
            row_position = self.overall_total_table.rowCount()
            self.overall_total_table.insertRow(row_position)
            self.overall_total_table.setItem(row_position, 0, QTableWidgetItem(habit))
            self.overall_total_table.setItem(
                row_position, 1, QTableWidgetItem(str(time))
            )
            self.colorize_total_row_overall(
                self.overall_total_table, row_position, time
            )

    def colorize_total_row(self, table, row, time):
        item = table.item(row, 1)
        if time < 10:
            item.setBackground(QColor("#FF6961"))  # Light Red
        elif time < 20:
            item.setBackground(QColor("#FDFD96"))  # Light Yellow
        else:
            item.setBackground(QColor("#77DD77"))  # Light Green
        item.setTextAlignment(Qt.AlignCenter)
        item.setForeground(QColor("#000"))

    def colorize_total_row_overall(self, table, row, time):
        item = table.item(row, 1)
        if time < 100:
            item.setBackground(QColor("#FF6961"))  # Light Red
        elif time < 150:
            item.setBackground(QColor("#FDFD96"))  # Light Yellow
        else:
            item.setBackground(QColor("#77DD77"))  # Light Green
        item.setTextAlignment(Qt.AlignCenter)
        item.setForeground(QColor("#000"))  # Black text for dark mode

    def trigger_data_update(self):
        self.data_updated.emit()
