from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QMessageBox,
    QComboBox,
    QPushButton,
    QHBoxLayout,
)
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt


class ChartViewAll(QWidget):
    def __init__(self, habit_controller):
        super().__init__()
        self.habit_controller = habit_controller
        self.layout = QVBoxLayout(self)
        self.chart_canvas = None

        # Add combobox for selecting month
        self.month_selector = QComboBox()
        self.month_selector.addItems(
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
        self.month_selector.currentTextChanged.connect(self.update_chart)

        # Add combobox for selecting habit
        self.habit_selector = QComboBox()
        self.update_habit_selector()

        # Add buttons for switching between monthly and yearly view
        self.button_layout = QHBoxLayout()
        self.btn_monthly = QPushButton("Monthly")
        self.btn_yearly = QPushButton("Yearly")
        self.btn_monthly.clicked.connect(self.update_chart)
        self.btn_yearly.clicked.connect(self.update_chart)
        self.button_layout.addWidget(self.btn_monthly)
        self.button_layout.addWidget(self.btn_yearly)

        self.layout.addWidget(self.habit_selector)
        self.layout.addWidget(self.month_selector)
        self.layout.addLayout(self.button_layout)

    def update_habit_selector(self):
        self.habit_selector.clear()
        habits = self.habit_controller.get_category_habits()
        for habit in habits:
            self.habit_selector.addItem(habit[0])

    def update_chart(self):
        self.clear_chart()
        selected_month = self.month_selector.currentText()
        selected_habit = self.habit_selector.currentText()
        if self.btn_monthly.isChecked():
            data = self.habit_controller.model.get_data_by_month(selected_month)
        else:
            data = self.habit_controller.model.get_yearly_data()

        if not data:
            self.show_message("No hay suficientes datos para graficar.")
            return

        plt.style.use("seaborn-v0_8-dark-palette")
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.set_title(
            f"{'Monthly' if self.btn_monthly.isChecked() else 'Yearly'} Study Time for {selected_habit}"
        )
        ax.set_xlabel("Days" if self.btn_monthly.isChecked() else "Months")
        ax.set_ylabel("Hours")

        labels, values, goals = [], [], []
        for d in data:
            if d[0] == selected_habit:
                labels.append(d[0])
                values.append(d[1])
                goals.append(d[2])

        x = range(len(labels))
        colors = ["#73FA8E" if v >= g else "#FF6347" for v, g in zip(values, goals)]
        ax.bar(x, values, label="Study Time", color=colors, edgecolor="black")
        if any(goals):
            ax.bar(
                x, goals, label="Goals", color="#C0BEBC", edgecolor="black", alpha=0.5
            )

        ax.set_xticks(x)
        ax.set_xticklabels(labels)

        for i, label in enumerate(labels):
            ax.text(x[i], values[i], label, ha="center", va="bottom")

        ax.legend(loc="upper right", fontsize=12)
        fig.autofmt_xdate()

        self.chart_canvas = FigureCanvas(fig)
        self.layout.addWidget(self.chart_canvas)
        plt.close(fig)

    def show_message(self, message):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setText(message)
        msg_box.setWindowTitle("Información")
        msg_box.exec()

    def clear_chart(self):
        if self.chart_canvas:
            self.chart_canvas.setParent(None)
            self.chart_canvas.deleteLater()
            self.chart_canvas = None

    def clean(self):
        self.clear_chart()
