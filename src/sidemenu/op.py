from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem, QPushButton, QHBoxLayout, QLabel, QComboBox, QGroupBox, QScrollArea, QLineEdit
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QMutex
from PyQt6.QtWidgets import QHeaderView
import sys
import json

class SaveDataThread(QThread):
    finished_signal = pyqtSignal()

    def __init__(self, data, parent=None):
        super().__init__(parent)
        self.data = data
        self.mutex = QMutex()

    def run(self):
        try:
            self.mutex.lock()  # Lock the mutex to ensure thread-safe access
            with open("investigations_data.json", "w") as f:
                json.dump(self.data, f)
        except Exception as e:
            print(f"Error saving data: {e}")
        finally:
            self.mutex.unlock()  # Unlock the mutex
        self.finished_signal.emit()



class LoadDataThread(QThread):
    loaded_signal = pyqtSignal(list)

    def __init__(self, parent=None):
        super().__init__(parent)

    def run(self):
        data = []
        try:
            with open("investigations_data.json", "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            print("No saved data found.")
        except json.JSONDecodeError:
            print("Error loading data.")
        self.loaded_signal.emit(data)


class OSINTDashboard(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("InsightHub Operations Dashboard")
        self.active_investigations = []  # List to store active investigations
        self.completed_reports = []  # List to store completed reports
        self.save_thread = None  # Reuse save thread
        self.init_ui()

        # Start loading data in a separate thread
        self.load_data_thread = LoadDataThread()
        self.load_data_thread.loaded_signal.connect(self.populate_table)
        self.load_data_thread.start()

    def init_ui(self):
        central_widget = QWidget(self)
        layout = QVBoxLayout()

        # Title
        title_label = QLabel("InsightHub Operations Dashboard", self)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 22px; font-weight: bold; margin-bottom: 20px;")
        layout.addWidget(title_label)

        # Active Investigations Table
        self.investigations_table = self.create_investigations_table()

        # Scroll Area for Table
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.investigations_table)
        layout.addWidget(scroll_area)

        # Input and Button Section
        self.new_investigation_name = QLineEdit(self)
        self.new_investigation_name.setPlaceholderText("Enter investigation name")
        layout.addWidget(self.new_investigation_name)

        button_layout = self.create_buttons_layout()
        layout.addLayout(button_layout)

        # Completed Reports Section
        self.completed_reports_box = self.create_completed_reports_section()
        layout.addWidget(self.completed_reports_box)

        # Save Button
        save_button = QPushButton("Save Operations", self)
        save_button.setStyleSheet("font-size: 12px; padding: 5px; border: 1px solid black;")
        save_button.clicked.connect(self.save_data)
        layout.addWidget(save_button)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Set minimum and maximum size for the window
        self.setMinimumSize(800, 600)
        self.setMaximumSize(1600, 1200)

    def create_investigations_table(self):
        table = QTableWidget(self)
        table.setColumnCount(3)  # Reduced to 3 columns (Operations, Status, Actions)
        table.setHorizontalHeaderLabels(["Operations", "Status", "Actions"])
        table.horizontalHeader().setStretchLastSection(True)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        table.setSizeAdjustPolicy(QTableWidget.SizeAdjustPolicy.AdjustToContents)
        table.setMinimumHeight(200)
        return table

    def create_buttons_layout(self):
        button_layout = QHBoxLayout()
        create_button = QPushButton("Create New Operation", self)
        create_button.setStyleSheet("font-size: 12px; padding: 5px; border: 1px solid black;")
        create_button.clicked.connect(self.create_new_investigation)

        remove_button = QPushButton("Remove Selected Operation", self)
        remove_button.setStyleSheet("font-size: 12px; padding: 5px; border: 1px solid black;")
        remove_button.clicked.connect(self.remove_investigation)

        button_layout.addWidget(create_button)
        button_layout.addWidget(remove_button)
        return button_layout

    def create_completed_reports_section(self):
        completed_box = QGroupBox("Completed Reports", self)
        completed_layout = QVBoxLayout()
        self.completed_reports_combo = QComboBox(self)
        self.completed_reports_combo.addItems([report["name"] for report in self.completed_reports])
        self.restore_button = QPushButton("Restore to Active", self)
        self.restore_button.setStyleSheet("font-size: 12px; padding: 5px; border: 1px solid black;")
        self.restore_button.clicked.connect(self.restore_completed_report)

        completed_layout.addWidget(self.completed_reports_combo)
        completed_layout.addWidget(self.restore_button)
        completed_box.setLayout(completed_layout)
        return completed_box

    def create_new_investigation(self):
        investigation_name = self.new_investigation_name.text().strip()
        if not investigation_name:
            return

        # Add the new investigation to the table and list of active investigations
        self.add_investigation_row(investigation_name, "Inactive")
        self.active_investigations.append({"name": investigation_name, "status": "Inactive"})
        self.new_investigation_name.clear()

        # Save the data to the file after creating a new investigation
        self.save_data()

    def remove_investigation(self):
        selected_row = self.investigations_table.currentRow()
        if selected_row != -1:
            investigation_name = self.investigations_table.item(selected_row, 0).text()
            self.active_investigations = [inv for inv in self.active_investigations if inv["name"] != investigation_name]
            self.investigations_table.removeRow(selected_row)

        # Check if the table is empty and add the placeholder row
        self.update_placeholder()

        # Save data after removing an investigation
        self.save_data()

    def move_to_completed(self):
        selected_row = self.investigations_table.currentRow()
        if selected_row != -1:
            status_widget = self.investigations_table.cellWidget(selected_row, 1)
            if status_widget and status_widget.currentText() == "Completed":
                investigation_name = self.investigations_table.item(selected_row, 0).text()
                completed_report = {"name": investigation_name}
                self.completed_reports.append(completed_report)

                # Remove from active investigations
                self.active_investigations = [inv for inv in self.active_investigations if inv["name"] != investigation_name]

                # Update the completed reports combo box
                self.completed_reports_combo.clear()
                self.completed_reports_combo.addItems([report["name"] for report in self.completed_reports])

                # Remove from the table
                self.investigations_table.removeRow(selected_row)

        # Save the data after moving to completed
        self.save_data()

    def restore_completed_report(self):
        selected_report = self.completed_reports_combo.currentText()
        if selected_report:
            completed_report = next((report for report in self.completed_reports if report["name"] == selected_report), None)
            if completed_report:
                self.active_investigations.append(completed_report)
                self.completed_reports = [report for report in self.completed_reports if report["name"] != selected_report]

                self.completed_reports_combo.clear()
                self.completed_reports_combo.addItems([report["name"] for report in self.completed_reports])

                self.add_investigation_row(selected_report, "Inactive")

                # Save the data after restoring a completed report
                self.save_data()

    def add_investigation_row(self, name, status):
        row_position = self.investigations_table.rowCount()
        self.investigations_table.insertRow(row_position)
        self.investigations_table.setItem(row_position, 0, QTableWidgetItem(name))

        # Add status combobox
        status_combobox = QComboBox(self)
        status_combobox.addItems(["Inactive", "In Progress", "Completed"])
        status_combobox.setCurrentText(status)
        status_combobox.currentTextChanged.connect(lambda: self.update_status_and_button(row_position))
        self.investigations_table.setCellWidget(row_position, 1, status_combobox)

        # Add Save to Completed button
        save_button = QPushButton("Save to Completed Reports", self)
        save_button.setStyleSheet("background-color: black; color: grey;")  # Initially greyed out
        save_button.setEnabled(False)  # Disable button by default
        save_button.clicked.connect(self.move_to_completed)
        self.investigations_table.setCellWidget(row_position, 2, save_button)

    def update_status_and_button(self, row_position):
        status_widget = self.investigations_table.cellWidget(row_position, 1)
        save_button = self.investigations_table.cellWidget(row_position, 2)

        if status_widget and save_button:
            if status_widget.currentText() == "Completed":
                save_button.setEnabled(True)
                save_button.setStyleSheet("background-color: green; color: white;")
            else:
                save_button.setEnabled(False)
                save_button.setStyleSheet("background-color: black; color: grey;")

    def populate_table(self, data):
        for investigation in data:
            self.add_investigation_row(investigation["name"], investigation["status"])

    def save_data(self):
        if self.save_thread and self.save_thread.isRunning():
            return  # If the save thread is already running, don't start another
        self.save_thread = SaveDataThread(self.active_investigations)
        self.save_thread.finished_signal.connect(self.on_save_finished)
        self.save_thread.start()

    def on_save_finished(self):
        print("Data saved successfully.")

    def update_placeholder(self):
        if self.investigations_table.rowCount() == 0:
            self.add_investigation_row("No investigations yet", "Inactive")

    def closeEvent(self, event):
        self.save_data()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = OSINTDashboard()
    window.show()
    sys.exit(app.exec())
