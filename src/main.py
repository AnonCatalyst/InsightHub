from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QToolBar,
    QAction, QStatusBar, QLabel, QSizePolicy, QHBoxLayout, QFrame
)
from PyQt5.QtCore import Qt, QTimer
import psutil
import sys
from side_menu import SideMenuWidget 
from content_loader import load_content  
import time

class TerminalStatusBar(QStatusBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(
            "background-color: #000000; color: #c0c5ce; border: 2px solid #000;"
        )  # Dark theme with a black border
        self.setFixedHeight(30)  # Set a fixed height for terminal feel

        # Initialize the QLabel for displaying the time
        self.time_label = QLabel(self)
        self.time_label.setStyleSheet("color: #c0c5ce;")  # Terminal-like text color
        self.addWidget(self.time_label)

        # Initialize the QLabel for displaying system statistics
        self.stats_label = QLabel(self)
        self.stats_label.setStyleSheet("color: #c0c5ce;")  # Terminal-like text color
        self.addWidget(self.stats_label)

        # Set up the timers to update the time and statistics
        self.time_timer = QTimer(self)
        self.time_timer.timeout.connect(self.update_time)
        self.time_timer.start(1000)  # Update every second

        self.stats_timer = QTimer(self)
        self.stats_timer.timeout.connect(self.update_stats)
        self.stats_timer.start(5000)  # Update every 5 seconds

        self.update_time()  # Initialize time display
        self.update_stats()  # Initialize system statistics display

    def update_time(self):
        current_time = time.strftime("%H:%M:%S")
        self.time_label.setText(f"Time: {current_time}")

    def update_stats(self):
        cpu_usage = psutil.cpu_percent(interval=1)
        memory_info = psutil.virtual_memory()
        memory_usage = memory_info.percent
        self.stats_label.setText(f"CPU: {cpu_usage}% | Memory: {memory_usage}%")



class InsightHubMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('InsightHub')
        self.setGeometry(100, 100, 1200, 600)
        self.setStyleSheet("background-color: #1b2b34; color: #c0c5ce;")  # Dark blueish-green theme

        # Main Widget Setup
        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)

        # Main Layout Setup
        self.main_layout = QVBoxLayout(self.main_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)  # No margins to use full available space
        self.main_layout.setSpacing(0)  

        # Create a horizontal layout to arrange the side menu and the central content
        self.horizontal_layout = QHBoxLayout()
        self.horizontal_layout.setContentsMargins(0, 0, 0, 0)  # No margins for the horizontal layout
        self.horizontal_layout.setSpacing(0)  

        # Initialize the side menu
        self.init_side_menu()

        # Central content widget
        self.central_content_widget = QWidget()
        self.central_content_layout = QVBoxLayout(self.central_content_widget)
        self.central_content_layout.setContentsMargins(0, 0, 0, 0) 
        self.central_content_layout.setSpacing(0) 
        
        # Create a frame to hold the content loaded from toolbar actions
        self.content_frame = QFrame()
        self.content_frame.setStyleSheet("background-color: #1b2b34;")  # Dark background for the frame
        self.content_frame.setLayout(QVBoxLayout())  # Ensure a layout is set
        self.central_content_layout.addWidget(self.content_frame)

        # Add widgets to the horizontal layout
        self.horizontal_layout.addWidget(self.central_content_widget)  # Main content on the left
        self.horizontal_layout.addWidget(self.side_menu)  # Side menu on the right

        # Add the horizontal layout to the main layout
        self.main_layout.addLayout(self.horizontal_layout)

        # Status Bar
        self.status_bar = TerminalStatusBar()
        self.main_layout.addWidget(self.status_bar)  # Add the status bar to the layout

        # Bottom Toolbar
        self.toolbar = QToolBar()
        self.toolbar.setMovable(False)
        self.toolbar.setStyleSheet(
            "background-color: #0a1a1f; padding: 7px; border-top: 2px solid #000;"
        )
        self.addToolBar(Qt.BottomToolBarArea, self.toolbar)

        # Toolbar Actions
        buttons = ['HOME', 'CONTACTS', 'HELP', 'ABOUT', 'LOGGING']
        actions = {name: QAction(name, self) for name in buttons}
        for action in actions.values():
            self.toolbar.addAction(action)

        # Connect actions
        for name, action in actions.items():
            action.triggered.connect(lambda checked, n=name: load_content(self.content_frame, n))

        # Load default content
        load_content(self.content_frame, 'HOME')

    def init_side_menu(self):
        # Create the side menu as a widget and display it on the right side
        self.side_menu = QWidget()  # Use QWidget for side menu
        self.side_menu.setStyleSheet(
            "background-color: #1b2b34; color: #ecf0f1;"
        )  

        # Use the SideMenuWidget defined in side-menu.py
        self.side_menu_widget = SideMenuWidget()
        self.side_menu.setLayout(QVBoxLayout())  # Use vertical layout for the side menu
        self.side_menu.layout().addWidget(self.side_menu_widget)

        # Set size policies for the side menu
        self.side_menu.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        self.side_menu.setMinimumWidth(200)  # Minimum width for the side menu
        self.side_menu.setMaximumWidth(300)  # Adjust as needed

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = InsightHubMainWindow()
    window.show()
    sys.exit(app.exec_())
