
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QComboBox,
)


class UpdateGoalView(QMainWindow):
    TITLE_WINDOW = "Update Goal"
    goal_updated = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(self.TITLE_WINDOW)
        self.setGeometry(100, 100, 800, 300)
        self.initUI()
        self.show()

    def initUI(self):
        # layout
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignHCenter)

        # labels
        self.label_goal = QLabel("Update Goal")
        self.label_goal.setAlignment(Qt.AlignCenter)
        self.label_goal.setFixedHeight(20)

        # inputs
        self.input_goal = QLineEdit()
        self.input_goal.setPlaceholderText("Enter your goal in hours")

        # combo box
        self.cb_habit = QComboBox()
        self.cb_month = QComboBox()

        # buttons
        self.btn_update = QPushButton("Update")
        layout.addWidget(self.label_goal)
        layout.addWidget(self.input_goal)
        layout.addWidget(self.cb_habit)
        layout.addWidget(self.cb_month)
        layout.addWidget(self.btn_update)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
