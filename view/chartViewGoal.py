from PySide6.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt


class ChartViewDay(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.chart_canvas = None

    def setup_chart(self, study_day=None, goal_data=None):
        if goal_data is not None and study_day is not None:
            habits = [data[0] for data in study_day]
            goals = [float(data[1]) for data in goal_data]
            studied_hours = [float(data[1]) for data in study_day]

            # Make sure goals and studied_hours have the same length
            min_length = min(len(goals), len(studied_hours))
            habits = habits[:min_length]
            goals = goals[:min_length]
            studied_hours = studied_hours[:min_length]

            fig, ax = plt.subplots(figsize=(10, 6))
            ax.set_title("Study Goals and Progress")
            ax.set_xlabel("Goals")
            ax.set_ylabel("Habits")

            ax.barh(
                habits,
                goals,
                color="#C0BEBC",
                label="Goals",
                height=0.5 if len(habits) < 3 else 0.8,
            )

            colors = []

            for i in range(len(habits)):
                percentage = (
                    studied_hours[i] / goals[i]) * 100 if goals[i] != 0 else 0

                if percentage <= 30:
                    colors.append("#FA5F4B")
                elif percentage < 50:
                    colors.append("#F9EC8A")
                else:
                    colors.append("#73FA8E")
            ax.barh(
                habits,
                studied_hours,
                color=colors,
                label="Studied Hours",
                height=0.5 if len(habits) < 3 else 0.8,
            )

        else:
            # No data provided, create an empty chart
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.set_title("No Data")
            ax.axis("off")  # Hide axis if no data

        legend_labels = ["Goal", "< 30% Goal", "30%-50% Goal", "> 50% Goal"]
        legend_colors = ["#C0BEBC", "#FA5F4B", "#F9EC8A", "#73FA8E"]
        legend_handles = [
            plt.Rectangle((0, 0), 1, 1, color=color) for color in legend_colors
        ]
        ax.legend(legend_handles, legend_labels, loc="upper right")

        self.chart_canvas = FigureCanvas(fig)

        self.chart_canvas.draw()
        self.layout.addWidget(self.chart_canvas)
        plt.close(fig)

    def clean(self):
        if self.chart_canvas:
            self.layout.removeWidget(self.chart_canvas)
            self.chart_canvas.deleteLater()
