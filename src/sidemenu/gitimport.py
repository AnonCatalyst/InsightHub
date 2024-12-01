import sys
import subprocess
from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QFileDialog, QLabel, QTextEdit
import os


class ToolExecutor(QThread):
    output_signal = pyqtSignal(str)
    status_signal = pyqtSignal(str)
    completion_signal = pyqtSignal(str)  # New signal to indicate completion

    def __init__(self, repo_path, runfile, arguments, requirements_file=None):
        super().__init__()
        self.repo_path = repo_path
        self.runfile = runfile
        self.arguments = arguments
        self.requirements_file = requirements_file

    def run(self):
        # Install requirements if a requirements file is provided
        if self.requirements_file:
            self.status_signal.emit("Installing dependencies...")
            try:
                subprocess.run([sys.executable, "-m", "pip", "install", "-r", self.requirements_file],
                               check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                self.output_signal.emit("Dependencies installed successfully!")
            except subprocess.CalledProcessError as e:
                self.output_signal.emit(f"Error installing dependencies: {e.stderr.decode()}")

        # Run the script with optional arguments
        self.status_signal.emit("Running the script...")
        try:
            if self.runfile.endswith(".py"):
                process = subprocess.Popen([sys.executable, self.runfile] + self.arguments, 
                                           stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            elif self.runfile.endswith(".sh"):
                process = subprocess.Popen(["bash", self.runfile] + self.arguments, 
                                           stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            else:
                self.output_signal.emit("Error: Unsupported script format")
                return

            # Stream output in real-time
            for stdout_line in process.stdout:
                self.output_signal.emit(stdout_line.strip())  # Emit each line of output as it's received
            for stderr_line in process.stderr:
                self.output_signal.emit(stderr_line.strip())  # Emit error output as well

            process.stdout.close()
            process.stderr.close()
            process.wait()  # Wait for the process to finish

            self.output_signal.emit("Tool executed successfully!")
            self.completion_signal.emit("Execution Complete")  # Emit completion signal

        except subprocess.CalledProcessError as e:
            self.output_signal.emit(f"Error running script: {e.stderr.decode()}")

        except Exception as e:
            self.output_signal.emit(f"Error: {str(e)}")


class GitHubImporter(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("GitHub Tool Importer")
        self.setGeometry(100, 100, 700, 600)  # Adjusted window size (wider)

        self.layout = QVBoxLayout()

        # Repository URL Section
        self.repo_layout = QHBoxLayout()
        self.repo_url_input = QLineEdit(self)
        self.repo_url_input.setPlaceholderText("Enter GitHub Repository URL")
        self.repo_layout.addWidget(self.repo_url_input)

        self.clone_button = QPushButton("Clone Repository", self)
        self.clone_button.clicked.connect(self.clone_repository)
        self.repo_layout.addWidget(self.clone_button)

        self.layout.addLayout(self.repo_layout)

        # Requirements File Section
        self.requirements_layout = QHBoxLayout()
        self.select_requirements_button = QPushButton("Select Requirements File (Optional)", self)
        self.select_requirements_button.clicked.connect(self.select_requirements_file)
        self.requirements_layout.addWidget(self.select_requirements_button)

        self.layout.addLayout(self.requirements_layout)

        # Run Script Section
        self.runfile_layout = QHBoxLayout()
        self.select_runfile_button = QPushButton("Select Run Script", self)
        self.select_runfile_button.clicked.connect(self.select_runfile)
        self.runfile_layout.addWidget(self.select_runfile_button)

        self.layout.addLayout(self.runfile_layout)

        # Arguments Input Section
        self.arguments_input = QLineEdit(self)
        self.arguments_input.setPlaceholderText("Enter arguments for the script (Optional)")
        self.layout.addWidget(self.arguments_input)

        # Execute Button
        self.execute_button = QPushButton("Execute Tool", self)
        self.execute_button.clicked.connect(self.execute_tool)
        self.layout.addWidget(self.execute_button)

        # Output Section
        self.output_label = QLabel("Status: Waiting for input", self)
        self.layout.addWidget(self.output_label)

        # Completion Status Indicator (New Label)
        self.completion_label = QLabel("", self)
        self.layout.addWidget(self.completion_label)

        # Live Output Box
        self.output_box = QTextEdit(self)
        self.output_box.setReadOnly(True)  # Make it read-only
        self.layout.addWidget(self.output_box)

        # Set layout
        self.setLayout(self.layout)

    def clone_repository(self):
        repo_url = self.repo_url_input.text()
        if not repo_url:
            self.output_label.setText("Error: Please provide a valid GitHub repository URL")
            return

        # Extract the repo name from the URL
        repo_name = repo_url.split("/")[-1].replace(".git", "")
        
        # Define the path where the repository will be cloned
        imports_dir = os.path.join(os.getcwd(), "../", "src", "sidemenu", "imports", repo_name)
        
        # Ensure the imports directory exists
        if not os.path.exists(imports_dir):
            os.makedirs(imports_dir)

        self.output_label.setText(f"Cloning the repository into {repo_name}...")
        self.append_to_output_box(f"Cloning the repository into {repo_name}...\n")
        
        try:
            # Clone the repository into the newly created folder under imports
            subprocess.run(["git", "clone", repo_url, imports_dir], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.output_label.setText(f"Repository cloned successfully into {repo_name}!")
            self.append_to_output_box(f"Repository cloned successfully into {repo_name}!\n")
        except subprocess.CalledProcessError as e:
            self.output_label.setText("Error: Failed to clone repository")
            self.append_to_output_box(f"Error cloning repository: {e.stderr.decode()}\n")

    def select_requirements_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Requirements File", "", "Text Files (*.txt);;All Files (*)")
        if file_path:
            self.requirements_file = file_path
            self.output_label.setText(f"Selected requirements: {os.path.basename(file_path)}")
            self.append_to_output_box(f"Selected requirements: {os.path.basename(file_path)}\n")

    def select_runfile(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Run Script", "", "All Files (*)")
        if file_path:
            self.runfile = file_path
            self.append_to_output_box(f"Selected run script: {os.path.basename(file_path)}\n")

    def execute_tool(self):
        if not hasattr(self, 'runfile'):
            self.output_label.setText("Error: Please select a run script")
            self.append_to_output_box("Error: Please select a run script\n")
            return

        # Clone repository if it hasn't been cloned yet
        repo_name = self.repo_url_input.text().split("/")[-1].replace(".git", "")
        repo_path = os.path.join(os.getcwd(), "../", "src", "sidemenu", "imports", repo_name)

        if not os.path.exists(repo_path):
            self.output_label.setText("Error: Repository is not cloned yet.")
            self.append_to_output_box("Error: Repository is not cloned yet.\n")
            return

        # Get the arguments from the input box
        arguments = self.arguments_input.text().strip().split()

        # Start the tool executor in a separate thread
        self.tool_executor = ToolExecutor(repo_path, self.runfile, arguments, self.requirements_file if hasattr(self, 'requirements_file') else None)
        self.tool_executor.output_signal.connect(self.append_to_output_box)
        self.tool_executor.status_signal.connect(self.update_status_label)
        self.tool_executor.completion_signal.connect(self.update_completion_label)  # Connect completion signal
        self.tool_executor.start()

    def update_status_label(self, text):
        """Update status label with the current status."""
        self.output_label.setText(text)

    def update_completion_label(self, text):
        """Update the completion label when execution finishes."""
        self.completion_label.setText(text)

    def append_to_output_box(self, text):
        """Helper function to append text to the output box"""
        self.output_box.append(text)
        # Scroll to the end of the output box to show the latest output
        cursor = self.output_box.textCursor()
        cursor.movePosition(cursor.MoveOperation.End)  # Correctly move to the end of the text
        self.output_box.setTextCursor(cursor)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GitHubImporter()
    window.show()
    sys.exit(app.exec())
