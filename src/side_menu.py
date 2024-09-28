from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QSizePolicy
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class SideMenuWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(
            "background-color: #1b2b34; color: #ecf0f1; border-left: 2px solid #000; border-bottom: 2px solid #000;"
        )

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(15, 0, 15, 15)
        self.layout.setSpacing(10)

        # Title
        self.title = QLabel('InsightHub', self)
        self.title.setAlignment(Qt.AlignCenter)  # Center the title
        self.title.setStyleSheet(
            "border-bottom: 0px; font-size: 22px; font-weight: bold; color: #ecf0f1; border-left: 0px"
        )
        self.layout.addWidget(self.title)

        # Description with separator
        self.description = QLabel('  Open-Source Intelligence  ', self)
        self.description.setAlignment(Qt.AlignCenter)  # Center the description
        self.description.setStyleSheet(
            "font-size: 16px; color: #ecf0f1; border-top: 3px solid #000; border-bottom: 3px solid #000; border-right: 2px solid #000; padding: 5px 0;"
        )  # Adjusted padding for better spacing and appearance
        self.layout.addWidget(self.description)

        # Side Menu Buttons
        self.buttons_layout = QVBoxLayout()
        self.buttons_layout.setSpacing(10)

        # Updated button names with clearer emphasis
        button_names = [
            'Operations Dashboard',  # To track active and queued OSINT reports and investigations
            'Document Archive',  # For managing saved documents
            'Documentation Center',  # For documenting OSINT findings
            'Compression Center',  # For compressing documents or files
            'Secure File Transfer',  # For creating file-sharing links
            'GitHub Tool Integration',  # For importing tools from GitHub
            'Advanced Toolset'  # General tool suite
        ]

        # Example buttons
        self.example_buttons = []
        for name in button_names:
            button = QPushButton(name, self)
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            button.setStyleSheet(
                "background-color: #1b2b34; color: #ecf0f1; border: 1px solid #000;"
                "border-radius: 5px; padding: 10px;"
            )  # Rounded corners, padding, and consistent color
            button.setFont(QFont('Arial', 12))
            self.buttons_layout.addWidget(button)
            self.example_buttons.append(button)

        # Add buttons to the layout
        self.layout.addLayout(self.buttons_layout)

        # Set layout
        self.setLayout(self.layout)

        # Set fixed size and disable resizing
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        self.setMinimumWidth(222)  # Adjusted width for better appearance
        self.setMaximumWidth(290)  # Ensure consistent width
        self.setMinimumHeight(400)  # Adjusted minimum height

