from PySide6.QtWidgets import QWidget, QVBoxLayout, QMessageBox
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt


class ChartViewAll(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.chart_canvas = None

    def setup_chart(self, data, title, xlabel, ylabel):
        self.clear_chart()

        if not data:
            self.show_message("No hay suficientes datos para graficar.")
            return

        plt.style.use("seaborn-v0_8-dark-palette")
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)

        try:
            cleaned_data = [
                (
                    d[0] if len(d) > 0 and d[0] is not None else "",
                    d[1] if len(d) > 1 and d[1] is not None else 0,
                    d[2] if len(d) > 2 and d[2] is not None else 0,
                    d[3] if len(d) > 3 and d[3] is not None else "",
                )
                for d in data
            ]
            labels, values, goals, habits = zip(*cleaned_data)
        except ValueError as e:
            self.show_message("Error al procesar los datos: " + str(e))
            return

        # Plotting lines for each habit
        unique_habits = list(set(habits))
        habit_data = {habit: ([], []) for habit in unique_habits}

        for label, value, goal, habit in zip(labels, values, goals, habits):
            habit_data[habit][0].append(label)
            habit_data[habit][1].append(value)

        for habit in unique_habits:
            ax.plot(habit_data[habit][0], habit_data[habit][1], marker="o", label=habit)

        ax.legend(loc="upper right", fontsize=12)

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
