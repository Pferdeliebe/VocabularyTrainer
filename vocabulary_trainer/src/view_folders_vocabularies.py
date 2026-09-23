from mongodb import *
from qtpy import QtWidgets
from ui.window_show_folders import Ui_WindowShowFolders
from ui.window_show_vocabularies import Ui_WindowShowVocabularies

mongodb_manager= MongoDBManager()

class WindowShowFolders(QtWidgets.QMainWindow):
    def __init__(self, controller, folders):
        super().__init__(parent=None)
        self.ui = Ui_WindowShowFolders()
        self.ui.setupUi(self)

        self.controller = controller
        self.folders = folders
        self.folders.sort(key=str.lower)

        self.ui.listWidget.clear()
        self.ui.listWidget.addItems(folders)
        self.ui.listWidget.itemClicked.connect(self.folder_chosen)
        self.ui.pb_back.clicked.connect(self.controller.back_show_folders)

    def folder_chosen(self, item: QtWidgets.QListWidgetItem) -> None:
        """Takes the vocabularies or 'Der Ordner ist leer' and opens the vocabulary window with it."""
        folder = item.text().strip("•").strip()
        folder_contents = mongodb_manager.find_vocabularies(folder)
        if mongodb_manager.count_vocabularies(folder, "leer", "leer") == 1:
            show_vocabularies = ["Der Ordner ist leer."]
        else:
            folder_contents = sorted(folder_contents, key=lambda word: word["Englisch"].casefold())
            show_vocabularies = [f"• {word['Englisch']} - {word['Deutsch']}" for word in folder_contents]
        self.controller.open_vocabularies(show_vocabularies, self.folders)


class WindowShowVocabularies(QtWidgets.QMainWindow):
    def __init__(self, controller, show_vocabularies, folders):
        super().__init__(parent=None)
        self.ui = Ui_WindowShowVocabularies()
        self.ui.setupUi(self)

        self.folders = folders
        self.controller = controller

        self.ui.listWidget.clear()
        self.ui.listWidget.addItems(show_vocabularies)
        self.ui.pb_back.clicked.connect(self.controller.back_show_vocabularies)
