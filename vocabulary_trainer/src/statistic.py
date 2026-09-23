from qtpy import QtWidgets
from ui.statistic import Ui_WindowStatistic


class WindowStatistic(QtWidgets.QMainWindow):
    def __init__(self, controller):
        super().__init__(parent=None)
        self.ui = Ui_WindowStatistic()
        self.ui.setupUi(self)

        self.controller = controller
        self.ui.pb_back.clicked.connect(self.controller.back_statistic)
