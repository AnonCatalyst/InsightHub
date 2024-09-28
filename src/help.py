from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextBrowser
from PyQt5.QtCore import Qt

class HELPWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('InsightHub Help')
        self.setStyleSheet("background-color: #1b2b34; color: #ecf0f1;")

        layout = QVBoxLayout(self)

        help_label = QLabel("InsightHub Help")
        help_label.setAlignment(Qt.AlignCenter)
        help_label.setStyleSheet("color: #ecf0f1; font-size: 20px;")
        layout.addWidget(help_label)

        help_content = QTextBrowser()
        help_content.setOpenExternalLinks(True)
        help_content.setStyleSheet("color: #ecf0f1;")
        help_content.setHtml("""
            <p>InsightHub is a tool designed to streamline various OSINT tasks, providing a user-friendly interface and efficient management of documents and data.</p>

            <h3>Getting Started</h3>
            <p>To get started with InsightHub, explore the different features using the side menu. Visit the HOME window to learn more about its functionalities.</p>

            <h3>Support and Contact</h3>
            <ul>
                <li>Email: hard2find.co.01@gmail.com</li>
                <li>Instagram: @istoleyourbutter</li>
                <li>Github: AnonCatalyst</li>
                <li>Discord: 6TFBKgjaAz</li>
            </ul>
        """)
        layout.addWidget(help_content)

        self.setLayout(layout)

