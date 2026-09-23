from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QMainWindow

from mongodb import MongoDBManager


mongodb_manager = MongoDBManager()

class Manager:

    def open_window(self, current_window: QMainWindow, new_window: QMainWindow) -> None:
        """Opens and closes windows and let the window slower open."""
        new_window.show()
        QTimer.singleShot(100, current_window.close)





