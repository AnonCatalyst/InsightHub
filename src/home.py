import sys
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QFrame, QPushButton, QStackedWidget, QHBoxLayout
from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtCore import Qt

class HOMEWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("InsightHub HOME")
        self.setGeometry(100, 100, 800, 600)

        # Set dark theme background
        self.set_dark_theme()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setContentsMargins(20, 20, 20, 20)  # Add margins for better spacing

        self.stacked_widget = QStackedWidget()
        self.layout.addWidget(self.stacked_widget)

        self.add_slide("Welcome to InsightHub", [
            "Your central node for OSINT mastery, providing an integrated environment for all your OSINT tasks."
        ])
        self.add_slide("Centralized OSINT Operations", [
            "InsightHub combines essential OSINT tools into a cohesive experience, eliminating the need for multiple applications.",
            "Navigate through tools with ease using a user-friendly menu system designed for seamless multitasking."
        ])
        self.add_slide("Custom-Built Tools", [
            "Each tool is designed specifically for OSINT tasks, offering a fully integrated and efficient workflow.",
            "Expect updates that allow users to import and integrate additional tools to enhance customization."
        ])
        self.add_slide("Join the Discussion", [
            "Your input is crucial as we shape InsightHub. Join us in creating a tool that meets the needs of OSINT professionals.",
            "Follow our progress and contribute your ideas for features and enhancements."
        ])

        # Navigation Buttons
        self.nav_layout = QHBoxLayout()
        self.prev_button = QPushButton("< Previous")
        self.prev_button.clicked.connect(self.show_previous_slide)
        self.next_button = QPushButton("Next >")
        self.next_button.clicked.connect(self.show_next_slide)
        self.nav_layout.addWidget(self.prev_button)
        self.nav_layout.addWidget(self.next_button)

        self.layout.addLayout(self.nav_layout)

        # Show the first slide
        self.current_slide_index = 0
        self.stacked_widget.setCurrentIndex(self.current_slide_index)

    def set_dark_theme(self):
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("#1b2b34"))  # Dark greenish-blue background
        palette.setColor(QPalette.WindowText, Qt.white)  
        self.setPalette(palette)

    def add_slide(self, title, content):
        slide_widget = QWidget()
        slide_layout = QVBoxLayout(slide_widget)
        
        title_label = QLabel(f"<h1>{title}</h1>")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: #ddd;")
        slide_layout.addWidget(title_label)

        for line in content:
            content_label = QLabel(line)
            content_label.setAlignment(Qt.AlignCenter)
            content_label.setStyleSheet("color: #eee;")
            slide_layout.addWidget(content_label)

        self.stacked_widget.addWidget(slide_widget)

    def show_next_slide(self):
        if self.current_slide_index < self.stacked_widget.count() - 1:
            self.current_slide_index += 1
            self.stacked_widget.setCurrentIndex(self.current_slide_index)

    def show_previous_slide(self):
        if self.current_slide_index > 0:
            self.current_slide_index -= 1
            self.stacked_widget.setCurrentIndex(self.current_slide_index)


