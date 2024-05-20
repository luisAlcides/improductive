
from PySide6.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt


class ChartViewDay(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.chart_canvas = None

    def setup_chart(self, study_day=None, goal_data=None):
        plt.rcParams.update({
            "axes.facecolor": "#2e2e2e",  # Fondo de los ejes
            "axes.edgecolor": "white",    # Color del borde de los ejes
            "axes.labelcolor": "white",   # Color de las etiquetas de los ejes
            "figure.facecolor": "#2e2e2e",  # Fondo de la figura
            "xtick.color": "white",       # Color de los ticks en el eje x
            "ytick.color": "white",       # Color de los ticks en el eje y
            "text.color": "white",        # Color del texto
            "legend.facecolor": "#2e2e2e",  # Fondo de la leyenda
            "legend.edgecolor": "white",  # Borde de la leyenda
        })
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.set_title("Study Goals and Progress")
        ax.set_xlabel("Goals")
        ax.set_ylabel("Habits")
        legend_labels = ["Goal", 'Habit within Goal', "< 30% Goal",
                         "30%-50% Goal", "> 50% Goal"]
        legend_colors = ["#C0BEBC", '#448BDB', "#FA5F4B", "#F9EC8A", "#73FA8E"]
        goals_name = ''

        if goal_data is not None:
            goals = [float(data[1]) for data in goal_data if len(data) >= 1]
            goals_name = [data[0]
                          for data in goal_data if len(data) >= 1]
            ax.barh(
                goals_name,
                goals,
                color="#C0BEBC",
                edgecolor='black',
                label="Goals",
                height=0.5,
                alpha=0.8
            )

        if study_day is not None:
            habits = [float(data[1]) for data in study_day if len(data) >= 1]
            habits_name = [data[0] for data in study_day if len(data) >= 1]

            studied_hours = [float(data[1])
                             for data in study_day if len(data) >= 2]
            colors = []

            for i in range(len(habits)):
                habit_name = habits_name[i]
                if habit_name in goals_name:
                    goal_index = goals_name.index(habit_name)
                    goal = goals[goal_index]
                    percentage = (
                        studied_hours[i] / goal) * 100 if goal != 0 else 0
                    if percentage <= 30:
                        colors.append("#FA5F4B")
                    elif percentage < 50:
                        colors.append("#F9EC8A")
                    else:
                        colors.append("#73FA8E")
                else:
                    colors.append('#448BDB')
            ax.barh(
                habits_name,
                habits,
                color=colors,
                edgecolor='black',
                label="Studied Hours",
                height=0.5,
                alpha=0.8
            )

        else:
            self.clear_chart()

        legend_handles = [
            plt.Rectangle((0, 0), 1, 1, color=color) for color in legend_colors
        ]
        ax.legend(legend_handles, legend_labels,
                  loc="upper right", fontsize=12)

        self.chart_canvas = FigureCanvas(fig)
        self.layout.addWidget(self.chart_canvas)
        plt.close(fig)

    def clear_chart(self):
        # Limpiar el widget del gráfico si está presente
        if self.chart_canvas:
            self.chart_canvas.setParent(None)
            self.chart_canvas.deleteLater()
            self.chart_canvas = None

    def clean(self):
        self.clear_chart()
