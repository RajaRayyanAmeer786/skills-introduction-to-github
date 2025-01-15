from injector import DependencyInjector
from threading import Thread
from PyQt5.QtWidgets import QApplication
import sys

class FlaskAPIThread(Thread):
    def __init__(self, app):
        super().__init__()
        self.app = app

    def run(self):
        self.app.run(debug=True, use_reloader=False)

class PyQtGUIThread(Thread):
    def __init__(self, gui_class):
        super().__init__()
        self.gui_class = gui_class

    def run(self):
        app = QApplication(sys.argv)
        window = self.gui_class()
        window.show()
        sys.exit(app.exec_())

if __name__ == '__main__':
    injector = DependencyInjector()
    api_app = injector.get_api_app()
    gui_class = injector.get_gui_class()

    api_thread = FlaskAPIThread(api_app)
    gui_thread = PyQtGUIThread(gui_class)

    api_thread.start()
    gui_thread.start()

    api_thread.join()
    gui_thread.join()