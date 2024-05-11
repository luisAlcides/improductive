import matplotlib.pyplot as plt
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTabWidget,
    QTableWidget,
    QTableWidgetItem,
)
import sys


class HabitTrackingApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Habit Tracking App")

        # Create central widget and main layout
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Create input fields
        input_layout = QHBoxLayout()
        self.habit_input = QLineEdit()
        self.goal_input = QLineEdit()
        self.time_input = QLineEdit()
        input_layout.addWidget(QLabel("Habit:"))
        input_layout.addWidget(self.habit_input)
        input_layout.addWidget(QLabel("Goal:"))
        input_layout.addWidget(self.goal_input)
        input_layout.addWidget(QLabel("Time (hrs):"))
        input_layout.addWidget(self.time_input)

        # Create button and response label
        self.add_button = QPushButton("Add Habit/Goal")
        self.add_button.clicked.connect(self.add_habit_goal)
        self.response_label = QLabel()
        main_layout.addLayout(input_layout)
        main_layout.addWidget(self.add_button)
        main_layout.addWidget(self.response_label)

        # Create tab widget for data display
        self.tab_widget = QTabWidget()
        self.habit_tab = QWidget()
        self.goal_tab = QWidget()
        self.tab_widget.addTab(self.habit_tab, "Habit Data")
        self.tab_widget.addTab(self.goal_tab, "Goal Data")
        main_layout.addWidget(self.tab_widget)

        # Create tables for habit and goal data
        self.habit_table = QTableWidget()
        self.habit_table.setColumnCount(2)
        self.habit_table.setHorizontalHeaderLabels(["Habit", "Time (hrs)"])
        self.goal_table = QTableWidget()
        self.goal_table.setColumnCount(2)
        self.goal_table.setHorizontalHeaderLabels(["Goal", "Time (hrs)"])
        habit_layout = QVBoxLayout(self.habit_tab)
        habit_layout.addWidget(self.habit_table)
        goal_layout = QVBoxLayout(self.goal_tab)
        goal_layout.addWidget(self.goal_table)

        # Initialize progress data
        self.habits = []
        self.goals = []
        self.times = []

    def add_habit_goal(self):
        habit = self.habit_input.text()
        goal = self.goal_input.text()
        time = self.time_input.text()
        if habit and goal and time:
            self.habits.append(habit)
            self.goals.append(goal)
            self.times.append(float(time))
            self.update_tables()
            self.update_chart()
            self.response_label.setText("Habit/Goal added successfully.")
        else:
            self.response_label.setText("Please fill in all fields.")

    def update_tables(self):
        self.habit_table.setRowCount(len(self.habits))
        self.goal_table.setRowCount(len(self.goals))
        for i, habit in enumerate(self.habits):
            self.habit_table.setItem(i, 0, QTableWidgetItem(habit))
            self.habit_table.setItem(i, 1, QTableWidgetItem(str(self.times[i])))
        for i, goal in enumerate(self.goals):
            self.goal_table.setItem(i, 0, QTableWidgetItem(goal))
            self.goal_table.setItem(i, 1, QTableWidgetItem(str(self.times[i])))

    def update_chart(self):
        plt.figure(figsize=(8, 6))
        plt.bar(self.habits, self.times, color="b", label="Habits")
        plt.bar(self.goals, self.times, color="r", label="Goals")
        plt.xlabel("Habits/Goals")
        plt.ylabel("Time (hrs)")
        plt.title("Progress Chart")
        plt.legend()
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HabitTrackingApp()
    window.show()
    sys.exit(app.exec())
