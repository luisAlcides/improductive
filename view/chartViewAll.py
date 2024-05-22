from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QComboBox,
    QPushButton,
    QHBoxLayout,
    QMessageBox,
)
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import datetime


class ChartViewAll(QWidget):
    def __init__(self, habit_controller):
        super().__init__()
        self.habit_controller = habit_controller
        self.layout = QVBoxLayout(self)
        self.chart_canvas = None
        self.view_mode = "Monthly"

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
        self.set_current_month()
        self.month_selector.currentTextChanged.connect(self.update_chart)

        # Add combobox for selecting habit
        self.habit_selector = QComboBox()
        self.update_habit_selector()
        self.habit_selector.currentTextChanged.connect(self.update_chart)

        # Add buttons for switching between monthly and yearly view
        btn_layout = QHBoxLayout()
        self.btn_monthly = QPushButton("Monthly")
        self.btn_yearly = QPushButton("Yearly")
        self.btn_monthly.clicked.connect(self.switch_to_monthly)
        self.btn_yearly.clicked.connect(self.switch_to_yearly)

        btn_layout.addWidget(self.btn_monthly)
        btn_layout.addWidget(self.btn_yearly)

        cb_layout = QHBoxLayout()
        cb_layout.addWidget(self.habit_selector)
        cb_layout.addWidget(self.month_selector)

        self.layout.addLayout(btn_layout)
        self.layout.addLayout(cb_layout)

        # Set default view mode and update chart
        self.switch_to_monthly()

    def set_current_month(self):
        current_month = datetime.datetime.now().month - 1
        self.month_selector.setCurrentIndex(current_month)

    def switch_to_monthly(self):
        self.view_mode = "Monthly"
        self.month_selector.setEnabled(True)
        self.habit_selector.setEnabled(False)
        self.update_chart()

    def switch_to_yearly(self):
        self.view_mode = "Yearly"
        self.month_selector.setEnabled(False)
        self.habit_selector.setEnabled(True)
        self.update_chart()

    def update_habit_selector(self):
        self.habit_selector.clear()
        habits = self.habit_controller.get_category_habits()
        for habit in habits:
            self.habit_selector.addItem(habit[0])

    def update_chart(self):
        self.clear_chart()
        plt.style.use("seaborn-v0_8-dark-palette")
        fig, ax = plt.subplots(figsize=(12, 6))

        if self.view_mode == "Monthly":
            selected_month = self.month_selector.currentText()
            month_num = self.month_selector.findText(selected_month) + 1
            month_num = str(month_num).zfill(2)
            data = self.habit_controller.show_data_by_month(month_num)

            if not data:
                self.show_message("No hay suficientes datos para graficar.")
                return

            ax.set_title(f"{self.view_mode} Study Time")
            ax.set_xlabel("Habits")
            ax.set_ylabel("Hours")
            bar_width = 0.6

            labels, values, goals = [], [], []
            for d in data:
                labels.append(d[0])
                values.append(d[1])
                goals.append(d[2] if d[2] is not None else 0)

            x = range(len(labels))
            colors = []
            for value, goal in zip(values, goals):
                if goal > 0:
                    ratio = value / goal
                    if ratio >= 1:
                        colors.append("#00FF00")  # Green for 100% or more
                    elif ratio >= 0.75:
                        colors.append("#ADFF2F")  # YellowGreen for 75% or more
                    elif ratio >= 0.5:
                        colors.append("#FFFF00")  # Yellow for 50% or more
                    elif ratio >= 0.25:
                        colors.append("#FFD700")  # Gold for 25% or more
                    else:
                        colors.append("#FF6347")  # Tomato for less than 25%
                else:
                    colors.append("#FF6347")  # Tomato if no goal

            ax.bar(
                x,
                values,
                width=bar_width,
                label="Study Time",
                color=colors,
                edgecolor="black",
                alpha=0.5,
            )

            if any(goals):
                ax.bar(
                    x,
                    goals,
                    width=bar_width,
                    label="Goals",
                    color="#C0BEBC",
                    edgecolor="black",
                    alpha=0.5,
                )

            if len(labels) == 1:
                x_min = -0.5
                x_max = 0.5
            else:
                x_min = -0.5
                x_max = len(labels) - 0.5

            ax.set_xticks(x)
            ax.set_xticklabels(labels, rotation=45, ha="right")
            ax.set_xlim(x_min, x_max)

            for i, label in enumerate(labels):
                ax.text(i, values[i], values[i], ha="center", va="bottom")

        elif self.view_mode == "Yearly":
            selected_habit = self.habit_selector.currentText()
            data = self.habit_controller.show_data_by_year(selected_habit)

            if not data:
                self.show_message("No hay suficientes datos para graficar.")
                return

            ax.set_title(f"{self.view_mode} Study Time for {selected_habit}")
            ax.set_xlabel("Months")
            ax.set_ylabel("Hours")
            bar_width = 0.6

            months = [
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
            values = {month: 0 for month in months}
            goals = {month: 0 for month in months}

            for d in data:
                month_num, total_hours, goal = d
                if month_num is not None:
                    month_index = int(month_num) - 1
                    month_name = months[month_index]
                    values[month_name] = total_hours
                    goals[month_name] = goal

            labels = list(values.keys())
            values = list(values.values())
            goals = list(goals.values())

            max_value = max(values)
            min_value = min(values)
            x = range(len(labels))
            colors = []
            for value in values:
                if max_value > min_value:
                    color_ratio = (value - min_value) / (max_value - min_value)
                else:
                    color_ratio = 0
                color = plt.cm.RdYlGn(color_ratio)
                colors.append(color)

            ax.bar(
                x,
                values,
                width=bar_width,
                label="Study Time",
                color=colors,
                edgecolor="black",
                alpha=0.5,
            )

            if any(goals):
                goals_filtered = [goal if goal > 0 else None for goal in goals]
                ax.bar(
                    x,
                    [goal if goal is not None else 0 for goal in goals_filtered],
                    width=bar_width,
                    label="Goals",
                    color="#C0BEBC",
                    edgecolor="black",
                    alpha=0.5,
                )

            ax.set_xticks(x)
            ax.set_xticklabels(labels, rotation=45, ha="right")

            for i, label in enumerate(labels):
                ax.text(i, values[i], values[i], ha="center", va="bottom")

        ax.yaxis.grid(True, linestyle="--", alpha=0.6)
        ax.xaxis.grid(False)
        ax.legend(
            handles=[
                plt.Line2D([0], [0], color="#00FF00", lw=4, label=">= 100%"),
                plt.Line2D([0], [0], color="#ADFF2F", lw=4, label=">= 75%"),
                plt.Line2D([0], [0], color="#FFFF00", lw=4, label=">= 50%"),
                plt.Line2D([0], [0], color="#FFD700", lw=4, label=">= 25%"),
                plt.Line2D([0], [0], color="#FF6347", lw=4, label="< 25% / No Goal"),
            ],
            loc="upper right",
        )
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
