import threading
import sys
from PyQt5.QtWidgets import QApplication
from injector import DependencyInjector

class FlaskAPIThread:
    """Handles the Flask API thread."""
    def __init__(self, api_app):
        self.api_app = api_app

    def run(self):
        self.api_app.run(debug=True, use_reloader=False)

class PyQtGUIThread:
    "Handles the PyQt5 GUI thread."
    def __init__(self, gui_class):
        self.gui_class = gui_class

    def run(self):
        app = QApplication(sys.argv)
        window = self.gui_class()
        window.show()
        sys.exit(app.exec_())

class ApplicationRunner:
    "Manages and coordinates threads for the Flask API and PyQt5 GUI."
    def __init__(self, api_thread, gui_thread):
        self.api_thread = threading.Thread(target=api_thread.run)
        self.gui_thread = threading.Thread(target=gui_thread.run)

    def start(self):
        self.api_thread.start()
        self.gui_thread.start()

    def join(self):
        self.api_thread.join()
        self.gui_thread.join()

if __name__ == '__main__':
    injector = DependencyInjector()
    api_app = injector.get_api_app()
    gui_class = injector.get_gui_class()

    api_thread = FlaskAPIThread(api_app)
    gui_thread = PyQtGUIThread(gui_class)

    runner = ApplicationRunner(api_thread, gui_thread)
    runner.start()
    runner.join()