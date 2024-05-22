from PySide6.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt


class ChartViewDay(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.chart_canvas = None

    def setup_chart(self, goal_data=None, study_day=None):
        self.clear_chart()  # Limpiar el gráfico antes de configurarlo

        plt.style.use("seaborn-v0_8-dark-palette")
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.set_title("Study Goals and Progress")
        ax.set_xlabel("Goals")
        ax.set_ylabel("Habits")

        # Leyenda y colores
        legend_labels = [
            "Goal",
            "Habit without Goal",
            ">= 100% of Goal",
            "75%-99% of Goal",
            "50%-74% of Goal",
            "25%-49% of Goal",
            "< 25% of Goal",
        ]
        legend_colors = [
            "#C0BEBC",  # Goal
            "#448BDB",  # Habit without Goal
            "#00FF00",  # >= 100%
            "#ADFF2F",  # 75%-99%
            "#FFFF00",  # 50%-74%
            "#FFD700",  # 25%-49%
            "#FF6347",  # < 25%
        ]

        goals_name = []
        goals = []
        if goal_data:
            goals = [float(data[1]) for data in goal_data if len(data) >= 2]
            goals_name = [data[0] for data in goal_data if len(data) >= 2]
            ax.barh(
                goals_name,
                goals,
                color="#C0BEBC",
                edgecolor="black",
                label="Goals",
                height=0.5,
                alpha=0.8,
            )

        if study_day:
            habits = [float(data[1]) for data in study_day if len(data) >= 2]
            habits_name = [data[0] for data in study_day if len(data) >= 2]

            studied_hours = [float(data[1]) for data in study_day if len(data) >= 2]
            colors = []

            for i in range(len(habits)):
                habit_name = habits_name[i]
                if habit_name in goals_name:
                    goal_index = goals_name.index(habit_name)
                    goal = goals[goal_index]
                    percentage = (studied_hours[i] / goal) * 100 if goal != 0 else 0
                    if percentage >= 100:
                        colors.append("#00FF00")  # Green for 100% or more
                    elif percentage >= 75:
                        colors.append("#ADFF2F")  # YellowGreen for 75% or more
                    elif percentage >= 50:
                        colors.append("#FFFF00")  # Yellow for 50% or more
                    elif percentage >= 25:
                        colors.append("#FFD700")  # Gold for 25% or more
                    else:
                        colors.append("#FF6347")  # Tomato for less than 25%
                else:
                    colors.append("#448BDB")  # Blue for habits without goals

            ax.barh(
                habits_name,
                habits,
                color=colors,
                edgecolor="black",
                label="Studied Hours",
                height=0.5,
                alpha=0.8,
            )

        legend_handles = [
            plt.Rectangle((0, 0), 1, 1, color=color) for color in legend_colors
        ]
        ax.legend(legend_handles, legend_labels, loc="upper right", fontsize=12)

        self.chart_canvas = FigureCanvas(fig)
        self.layout.addWidget(self.chart_canvas)
        plt.close(fig)

    def clear_chart(self):
        if self.chart_canvas:
            self.chart_canvas.setParent(None)
            self.chart_canvas.deleteLater()
            self.chart_canvas = None

    def clean(self):
        self.clear_chart()
