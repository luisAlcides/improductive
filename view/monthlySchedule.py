from PySide6.QtCore import Qt
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
)
from connection import Connection


class MonthlySchedule(QWidget):
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
        self.combo_month.currentTextChanged.connect(self.load_month_data)

        self.header_layout.addWidget(self.label_month)
        self.header_layout.addWidget(self.combo_month)

        self.table_widget = QTableWidget()
        self.table_widget.setRowCount(0)
        self.table_widget.setColumnCount(32)  # 31 days + 1 for activities column
        self.setup_table_headers()

        self.layout.addLayout(self.header_layout)
        self.layout.addWidget(self.table_widget)

        # Fix the activity column and make other columns resizable
        self.table_widget.horizontalHeader().setSectionResizeMode(0, QHeaderView.Fixed)
        for col in range(1, 32):
            self.table_widget.horizontalHeader().setSectionResizeMode(
                col, QHeaderView.Stretch
            )
        self.table_widget.setColumnWidth(0, 150)
        self.table_widget.setHorizontalScrollMode(QTableWidget.ScrollPerPixel)

    def setup_table_headers(self):
        self.table_widget.setHorizontalHeaderItem(0, QTableWidgetItem("ACTIVIDAD"))
        for day in range(1, 32):
            self.table_widget.setHorizontalHeaderItem(day, QTableWidgetItem(str(day)))

    def load_month_data(self, month):
        self.table_widget.setRowCount(0)  # Clear existing data
        data = self.get_month_data_from_db(month)  # Fetch data from DB

        activities = list(data.keys())
        self.table_widget.setRowCount(len(activities))

        for row, activity in enumerate(activities):
            self.table_widget.setItem(row, 0, QTableWidgetItem(activity))
            for day in range(1, 32):
                if day in data[activity]:
                    value = data[activity][day]
                    item = QTableWidgetItem(str(value))
                    self.set_item_style(item, value)
                    self.table_widget.setItem(row, day, item)
                else:
                    self.table_widget.setItem(row, day, QTableWidgetItem(""))

    def set_item_style(self, item, value):
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
            item.setBackground(QColor("#84B6F4"))  # Light Blue
            item.setForeground(QColor("#000"))  # Black text for dark mode

    def get_month_data_from_db(self, month):
        month_num = self.combo_month.findText(month) + 1
        data = {}
        with Connection() as cursor:
            cursor.execute(
                """
                SELECT ch.name, strftime('%d', h.date_current), h.study_time
                FROM habit h
                JOIN category_habits ch ON h.category_id = ch.id
                WHERE strftime('%m', h.date_current) = ?
                """,
                (str(month_num).zfill(2),),
            )
            rows = cursor.fetchall()
            for row in rows:
                activity, day, study_time = row
                day = int(day)
                if activity not in data:
                    data[activity] = {}
                data[activity][day] = study_time
        return data
