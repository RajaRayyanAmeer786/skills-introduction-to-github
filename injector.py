from gui import CodeEditor
from api import create_app

class DependencyInjector:
    "Resolves dependencies for GUI and API."
    @staticmethod
    def get_gui_class():
        return CodeEditor

    @staticmethod
    def get_api_app():
        return create_app()