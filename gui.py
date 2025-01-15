from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTextEdit, QVBoxLayout, QPushButton, QLabel, QWidget,
    QLineEdit, QSplitter, QFileDialog, QAction
)
from PyQt5.QtCore import Qt
import sys
import requests

class FileHandler:
    "Handles file-related operations such as saving and loading files."

    @staticmethod
    def open_file():
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(None, "Open File", "", "Python Files (*.py);;All Files (*)", options=options)
        if file_name:
            with open(file_name, 'r') as file:
                return file_name, file.read()
        return None, None

    @staticmethod
    def save_file_as(content):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(None, "Save File As", "", "Python Files (*.py);;All Files (*)", options=options)
        if file_name:
            with open(file_name, 'w') as file:
                file.write(content)
            return file_name
        return None

    @staticmethod
    def save_file(content, file_name):
        with open(file_name, 'w') as file:
            file.write(content)

class SyntaxChecker:
    "Handles API interaction for syntax checking."

    def __init__(self, api_key, api_url):
        self.api_key = api_key
        self.api_url = api_url

    def check_syntax(self, code):
        json_payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": code
                        }
                    ]
                }
            ]
        }
        try:
            response = requests.post(self.api_url, headers={"Authorization": f"Bearer {self.api_key}"}, json=json_payload)
            return response.json().get("errors", "No errors found!")
        except requests.exceptions.RequestException as e:
            return f"Error contacting the syntax check API: {str(e)}"

class CodeEditor(QMainWindow):
    def __init__(self, syntax_checker):
        super().__init__()
        self.setWindowTitle("Code Assistant")
        self.resize(800, 600)
        self.syntax_checker = syntax_checker
        self.current_file = None
        self._init_ui()

    def _init_ui(self):
        self._init_menu()
        self._init_workspace()

    def _init_menu(self):
        self.menu_bar = self.menuBar()
        self.file_menu = self.menu_bar.addMenu("File")
        actions = {
            "New Project": self.new_project,
            "Open Project": self.open_project,
            "Save": self.save_project,
            "Save As": self.save_as_project,
            "Exit": self.close
        }
        for action_name, action_handler in actions.items():
            action = QAction(action_name, self)
            self.file_menu.addAction(action)
            action.triggered.connect(action_handler)

    def _init_workspace(self):
        self.logic_input = QLineEdit()
        self.logic_input.setPlaceholderText("Enter the logic of your program...")
        self.editor = QTextEdit()
        self.error_display = QLabel("Errors will be displayed here.")
        self.check_button = QPushButton("Check Syntax")
        self.check_button.clicked.connect(self.check_syntax)

        splitter = QSplitter(Qt.Vertical)
        splitter.addWidget(self.logic_input)
        splitter.addWidget(self.editor)

        layout = QVBoxLayout()
        layout.addWidget(splitter)
        layout.addWidget(self.check_button)
        layout.addWidget(self.error_display)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def new_project(self):
        self.editor.clear()
        self.logic_input.clear()
        self.current_file = None

    def open_project(self):
        file_name, content = FileHandler.open_file()
        if content is not None:
            self.editor.setText(content)
            self.current_file = file_name

    def save_project(self):
        if self.current_file:
            FileHandler.save_file(self.editor.toPlainText(), self.current_file)
        else:
            self.save_as_project()

    def save_as_project(self):
        self.current_file = FileHandler.save_file_as(self.editor.toPlainText())

    def check_syntax(self):
        code = self.editor.toPlainText()
        errors = self.syntax_checker.check_syntax(code)
        # Display errors in a user-friendly way
        if isinstance(errors, dict) and "error" in errors:
            self.error_display.setText(errors["error"])
        else:
            self.error_display.setText(str(errors))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    api_key = 'AlzaSyDZus0NaKoJnKUNt-hhrKtdY9bd2-yzpqw'  # Add your Gemini API key here
    api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"  # Updated endpoint
    syntax_checker = SyntaxChecker(api_key, api_url)
    window = CodeEditor(syntax_checker)
    window.show()
    sys.exit(app.exec_())