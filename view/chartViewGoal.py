from PySide6.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt 

class ChartViewDay(QWidget):
    def __init__(self, goal_data=[], study_data=[]):
        super().__init__()
        self.goal_data = goal_data
        self.study_data = study_data

        self.setup_chart()

        layout = QVBoxLayout()
        layout.addWidget(self.chart_canvas)
        self.setLayout(layout)


    def setup_chart(self):
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.set_title('Study Goals and Progress')
        ax.set_xlabel('Goals')
        ax.set_ylabel('Habits')

        habits = [data[0] for data in self.study_data]
        goals = [float(data[1]) for data in self.goal_data]
        studied_hours = [float(data[1]) for data in self.study_data]
        
        max_goal = max(goals) if goals else 3
        max_studied = max(studied_hours) if studied_hours else 3

        ax.barh(habits, goals, color='#C0BEBC', label='Goals', height=0.5 if len(habits) < 3 else 0.8)
        
        colors = []

        for i in range(len(habits)):
            percentage = (studied_hours[i] / goals[i]) * 100 if goals[i] != 0 else 0

            if percentage <= 30:
                colors.append('#FA5F4B')
            elif percentage < 50:
                colors.append('#F9EC8A')
            else:
                colors.append('#73FA8E')
        ax.barh(habits, studied_hours, color=colors, label='Studied Hours', height=0.5 if len(habits) < 3 else 0.8)
        
        ax.set_xlim(0, max(max_goal, max_studied) + 2)

        legend_labels = ['Goal','< 30% Goal', '30%-50% Goal', '> 50% Goal']
        legend_colors = ['#C0BEBC','#FA5F4B', '#F9EC8A', '#73FA8E']
        legend_handles = [plt.Rectangle((0, 0), 1, 1, color=color) for color in legend_colors]
        ax.legend(legend_handles, legend_labels, loc='upper right')

        self.chart_canvas = FigureCanvas(fig)
        self.chart_canvas.draw()
