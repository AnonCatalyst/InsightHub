from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout

class HOMEWindow(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        label = QLabel("Hello World from HOME")
        label.setStyleSheet("color: #ecf0f1; font-size: 24px; font-weight: bold;")
        layout.addWidget(label)
        self.setLayout(layout)
