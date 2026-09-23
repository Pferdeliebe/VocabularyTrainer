import sys
from qtpy import QtWidgets
from ui.window_main_menu import Ui_WindowMain

class WindowMain(QtWidgets.QMainWindow):
    def __init__(self, controller):
        super().__init__(parent=None)
        self.controller = controller
        self.ui = Ui_WindowMain()
        self.ui.setupUi(self)

        self.ui.pb_exit.clicked.connect(self.exit_app)
        self.ui.pb_manage_vocabularies.clicked.connect(self.controller.manage_vocabularies)
        self.ui.pb_ask_vocabularies.clicked.connect(self.controller.ask_vocabularies)
        self.ui.pb_write_vocabularies.clicked.connect(self.controller.write_vocabularies)

    def exit_app(self) -> None:
        """Exits the program."""
        sys.exit(0)