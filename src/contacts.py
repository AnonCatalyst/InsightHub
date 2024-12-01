from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt

class CONTACTSWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setStyleSheet("background-color: #1b2b34;")  # Dark background

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Title
        title = QLabel("📇 Contact Information")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #ecf0f1; font-size: 28px; font-weight: bold;")
        layout.addWidget(title)

        # Twitter/X
        x_label = QLabel("🐦 X: <span style='color: #1da1f2;'>AnonCatalyst</span>")
        x_label.setAlignment(Qt.AlignLeft)
        x_label.setStyleSheet("font-size: 18px;")
        layout.addWidget(x_label)

        # Instagram
        instagram_label = QLabel("📸 Instagram: <span style='color: #e1306c;'>istoleyourbutter</span>")
        instagram_label.setAlignment(Qt.AlignLeft)
        instagram_label.setStyleSheet("font-size: 18px;")
        layout.addWidget(instagram_label)

        # GitHub
        github_label = QLabel("🐙 GitHub: <span style='color: #f05033;'>AnonCatalyst</span>")
        github_label.setAlignment(Qt.AlignLeft)
        github_label.setStyleSheet("font-size: 18px;")
        layout.addWidget(github_label)

        # Discord Server
        discord_label = QLabel(
            "💬 Discord Support Server: <a href='https://discord.com/invite/tgSacvyHqV' "
            "style='color: #5865F2; text-decoration: none;'>OpenZenith Support Server</a>"
        )
        discord_label.setAlignment(Qt.AlignLeft)
        discord_label.setStyleSheet("font-size: 18px;")
        discord_label.setOpenExternalLinks(True)
        layout.addWidget(discord_label)

        # CashApp
        cashapp_label = QLabel(
            "💵 CashApp: <a href='https://cash.app/$anoncatalyst' "
            "style='color: #00d632; text-decoration: none;'>$anoncatalyst</a>"
        )
        cashapp_label.setAlignment(Qt.AlignLeft)
        cashapp_label.setStyleSheet("font-size: 18px;")
        cashapp_label.setOpenExternalLinks(True)
        layout.addWidget(cashapp_label)

        # Linktree
        linktree_label = QLabel(
            "🌐 Linktree: <span style='color: #2cb67d;'>AnonCatalyst</span>"
        )
        linktree_label.setAlignment(Qt.AlignLeft)
        linktree_label.setStyleSheet("font-size: 18px;")
        layout.addWidget(linktree_label)

        self.setLayout(layout)
