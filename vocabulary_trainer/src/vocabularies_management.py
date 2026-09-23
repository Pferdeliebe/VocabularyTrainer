from qtpy import QtWidgets
from mongodb import MongoDBManager
from ui.window_vocabulary_management import Ui_WindowVocabularyManagement
from methods_manager import *

methods_manager = SortFolders()
mongodb_manager = MongoDBManager()

class WindowVocabularyManagement(QtWidgets.QMainWindow):
    def __init__(self, controller):
        super().__init__(parent=None)
        self.controller = controller
        self.ui = Ui_WindowVocabularyManagement()
        self.ui.setupUi(self)


        self.ui.pb_show_vocabularies.clicked.connect(self.get_show_folders)
        self.ui.pb_back.clicked.connect(self.controller.back_manage_vocabularies)
        self.ui.pb_add_vocabularies.clicked.connect(self.controller.add_vocabularies_folder)
        self.ui.pb_delete_vocabularies.clicked.connect(self.controller.selection_delete)


    def get_show_folders(self) -> None:
        """Gives the sorted folders to the controller."""
        self.controller.show_folders(self.get_folders())

    def get_folders(self) -> list[str]:
        """Takes the folders and sorts them."""
        folders = mongodb_manager.get_folders()
        folders = methods_manager.sort_folders(folders)
        return folders