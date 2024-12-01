from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QScrollArea, QFrame
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt


class ABOUTWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Set the window title and size
        self.setWindowTitle("About InsightHub")
        self.setFixedSize(935, 450)

        # Create layout
        layout = QVBoxLayout()

        # Create a scroll area for long text
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_widget = QWidget()
        scroll_area.setWidget(scroll_widget)

        # Create content inside the scrollable area
        content_layout = QVBoxLayout()

        # Create styled text for the about section
        about_text = """InsightHub is an all-in-one solution for OSINT practitioners, integrating custom-built tools with a centralized and intuitive interface.

Key Features:
- Dashboard for tracking active OSINT investigations and queued reports.
- Document management, including individual or mass documentation & advanced file management.
- Github tool Importer and Executor for integrating external tools.
- Greatly speeds up your investigative workflow whether you are a beginner or an expert.
- Live status updates and feedback during tool execution.
- Encourages team effort for large scale operations.
- Structured repository management for imported tools."""

        # Create a label for the about text
        label = QLabel(about_text)
        label.setWordWrap(True)

        # Set custom font, size, and color
        label.setFont(QFont("Courier New", 10, QFont.Normal))  # Use Courier New for terminal-like font
        label.setStyleSheet("color: #ecf0f1; font-weight: bold; text-align: center;")  # Light text color (off-white)

        # Add label to the content layout
        content_layout.addWidget(label, alignment=Qt.AlignCenter)

        # Add the scrollable widget to the scroll area
        scroll_widget.setLayout(content_layout)

        # Add the scroll area to the main layout
        layout.addWidget(scroll_area)

        # Set the dark background and layout
        self.setStyleSheet("""background-color: #1b2b34; color: #c0c5ce; border-left: 3px solid #000;""")
        self.setLayout(layout)

        # Optional: Add a frame around the text for visual separation
        frame = QFrame()
        frame.setFrameShape(QFrame.StyledPanel)
        frame.setStyleSheet("background-color: #c0c5ce; color: #1b2b34;")
        layout.addWidget(frame)
