from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout

class LOGGINGWindow(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        label = QLabel("Hello World from LOGGING")
        label.setStyleSheet("color: #ecf0f1; font-size: 24px; font-weight: bold;")
        layout.addWidget(label)
        self.setLayout(layout)
