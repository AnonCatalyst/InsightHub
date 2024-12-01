import subprocess
import sys
import threading
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QSizePolicy, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class SideMenuWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(
            "background-color: #1b2b34; color: #ecf0f1; border-left: 2px solid #000; border-bottom: 2px solid #000;"
        )

        # Main Layout for Side Menu
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

        # Side Menu Buttons Layout
        self.buttons_layout = QVBoxLayout()
        self.buttons_layout.setSpacing(10)

        # List of button names
        button_names = [
            'Operations Dashboard',  # To track active and queued OSINT reports and investigations
            'Document Archive',  # For managing saved documents
            'Documentation Center',  # For documenting OSINT findings
            'Compression Center',  # For compressing documents or files
            'Secure File Transfer',  # For creating file-sharing links
            'GitHub Tool Integration',  # For importing tools from GitHub
            'Advanced Toolset'  # General tool suite
        ]

        # Create buttons dynamically
        self.buttons = {}
        for name in button_names:
            button = QPushButton(name, self)
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            button.setStyleSheet(
                "background-color: #1b2b34; color: #ecf0f1; border: 1px solid #000;"
                "border-radius: 5px; padding: 10px;"
            )  # Rounded corners, padding, and consistent color
            button.setFont(QFont('Arial', 12))
            button.clicked.connect(self.on_button_click)
            self.buttons[name] = button  # Store buttons in a dictionary for easy reference
            self.buttons_layout.addWidget(button)

        # Add buttons layout to main layout
        self.layout.addLayout(self.buttons_layout)

        # Set layout and fixed size for the side menu
        self.setLayout(self.layout)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        self.setMinimumWidth(222)  # Adjusted width for better appearance
        self.setMaximumWidth(290)  # Ensure consistent width
        self.setMinimumHeight(400)  # Adjusted minimum height

    def on_button_click(self):
        """Handle button click event to open relevant functionality"""
        clicked_button = self.sender()
        button_name = clicked_button.text()

        # Here you can add logic to open specific sections when a button is clicked
        if button_name == "Operations Dashboard":
            print("Opening Operations Dashboard...")
            self.run_script_in_background('src/sidemenu/op.py')
        elif button_name == "Document Archive":
            print("Opening Document Archive...")
            self.run_script_in_background('src/sidemenu/documents.py')
        elif button_name == "Documentation Center":
            print("Opening Documentation Center...")
            self.run_script_in_background('src/sidemenu/documenter.py')
        elif button_name == "Compression Center":
            print("Opening Compression Center...")
            # Add logic to open Compression Center
        elif button_name == "Secure File Transfer":
            print("Opening Secure File Transfer...")
            # Add logic to open Secure File Transfer
        elif button_name == "GitHub Tool Integration":
            print("Opening GitHub Tool Integration...")
            # Add logic for GitHub Tool Integration
        elif button_name == "Advanced Toolset":
            print("Opening Advanced Toolset...")
            # Add logic for Advanced Toolset

    def run_script_in_background(self, script_path):
        """Run the script in a separate thread to prevent freezing"""
        thread = threading.Thread(target=self._run_script, args=(script_path,))
        thread.start()

    def _run_script(self, script_path):
        """Run the script in subprocess"""
        try:
            subprocess.run([sys.executable, script_path], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error occurred while trying to run {script_path}: {e}")
            self.show_error_message(f"Error occurred while trying to run {script_path}: {e}")

    def show_error_message(self, message):
        """Show an error message in a dialog"""
        error_dialog = QMessageBox(self)
        error_dialog.setIcon(QMessageBox.Critical)
        error_dialog.setText("An error occurred")
        error_dialog.setInformativeText(message)
        error_dialog.setWindowTitle("Error")
        error_dialog.exec_()
