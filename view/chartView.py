from PySide6.QtWidgets import QWidget, QVBoxLayout,QHBoxLayout, QPushButton
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import numpy as np

from controller.studyDataController import StudyDataController


class ChartView(QWidget):
    def __init__(self):
        super().__init__()
        
        self.controller = StudyDataController()
        self.show()
        
        self.chart_canvas = FigureCanvas(plt.Figure(figsize=(8, 6)))
        
        self.btn_day = QPushButton('Day')
        self.btn_day.clicked.connect(lambda: self.update_chart('Day'))

        self.btn_week = QPushButton('Week')
        self.btn_week.clicked.connect(lambda: self.update_chart('Week'))

        self.btn_month = QPushButton('Month')
        self.btn_month.clicked.connect(lambda: self.update_chart('Month'))
        
        layout = QVBoxLayout()
        layout_horizontal = QHBoxLayout()
        layout_horizontal.addWidget(self.btn_day)
        layout_horizontal.addWidget(self.btn_week)
        layout_horizontal.addWidget(self.btn_month)
        layout.addLayout(layout_horizontal)
        layout.addWidget(self.chart_canvas)
        self.setLayout(layout)
        
        self.colors = ['red', 'blue', 'green', 'yellow', 'purple', 'orange', 'black', 'pink', 'cyan', 'magenta']
        self.color_index = 0
    
    def setup_chart(self, time_period='Day'):
        self.chart_canvas.figure.clear()
        study_data = self.controller.get_study_data(time_period)
        
        categories, times = zip(*study_data)
        colors = plt.cm.get_cmap('tab10', len(categories))
        
        def assing_color(hour):
            color_scale = [(0, '#ffeda0'), (5, '#feb24c'), (10, '#f03b20')]
            for limit, color in color_scale:
                if hour<= limit:
                    return color
            return color_scale[-1][1]
        
        colors = [assing_color(time) for time in times]
        fig, ax = plt.subplots(figsize=(8, 7))
        bars = ax.bar(categories, times, color=colors)
        
        for bar in bars:
            yval = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, yval + 1, f'{yval:.2f}', ha='center', va='bottom')
        
        ax.set_xlabel('Habit')
        ax.set_ylabel('Study Time hours')
        ax.set_title(f'Study time Analysis for {time_period}')
        ax.tick_params(axis='x', rotation=45)
        
        legend_labels = ['< 0h', '0-5h', '5-10h', '> 10h']
        legend_colors = ['green', 'yellow', 'orange', 'red']
        legend_handles = [plt.Rectangle((0, 0), 1, 1, color=color) for color in legend_colors]
        ax.legend(legend_handles, legend_labels, loc='upper right')
        
        self.chart_canvas.figure = fig        
        
        self.chart_canvas.draw()
        
    
    def update_chart(self, time_period):
        self.setup_chart(time_period)
        
    
    