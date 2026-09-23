from qtpy import QtWidgets
from ui.window_add_vocabularies import Ui_WindowAddVocabularies
from mongodb import *
from ui.window_add_vocabularies_folder import Ui_WindowAddVocabulariesFolder
from ui.window_add_vocabularies_name_folder import Ui_WindowAddVocabulariesNameFolder
from methods_manager import *

methods_manager = SortFolders()
mongodb_manager = MongoDBManager()

class WindowAddVocabulariesFolder(QtWidgets.QMainWindow):
    def __init__(self, controller, folders):
        super().__init__(parent=None)
        self.ui = Ui_WindowAddVocabulariesFolder()
        self.ui.setupUi(self)

        self.controller = controller
        self.folders = sorted(folders, key=str.lower)

        self.ui.pb_back.clicked.connect(self.controller.back_add_vocabularies_folder)

        self.ui.listWidget.clear()
        self.ui.listWidget.addItems(self.folders)
        self.ui.listWidget.itemClicked.connect(self.folder_chosen)
        self.ui.pb_new_folder.clicked.connect(self.controller.new_folder)

    def folder_chosen(self, item: QtWidgets.QListWidgetItem) -> None:
        """Takes the clicked folder and opens the folder's vocabularies."""
        folder = item.text().strip("•").strip()
        self.controller.open_folder_chosen(folder)


class WindowAddVocabularies(QtWidgets.QMainWindow):
    def __init__(self, controller, folder, folders):
        super().__init__(parent=None)
        self.ui = Ui_WindowAddVocabularies()
        self.ui.setupUi(self)

        self.controller = controller
        self.folder = folder
        self.folders = folders

        self.ui.pb_confirm.setEnabled(False)
        self.ui.l_vocabulary_german.textChanged.connect(self.check_entries)
        self.ui.l_vocabulary_english.textChanged.connect(self.check_entries)
        self.ui.pb_confirm.clicked.connect(self.add)
        self.ui.pb_back.clicked.connect(self.controller.back_add_vocabularies)

    def check_entries(self) -> None:
        """Checks if labels are filled. If the labels are filled, you can click the push button."""
        if self.ui.l_vocabulary_english.text() and self.ui.l_vocabulary_german.text():
            self.ui.pb_confirm.setEnabled(True)
        else:
            self.ui.pb_confirm.setEnabled(False)

    def add(self) -> None:
        """Adds a new vocabulary, deletes the placeholder vocabulary and clears the labels after confirmation."""
        english = self.ui.l_vocabulary_english.text()
        german = self.ui.l_vocabulary_german.text()
        neue_vokabel = {
            "Englisch": english,
            "Deutsch": german,
            "Kategorie": self.folder,
            "gewusst": False,
        }
        mongodb_manager.add_one_vocabulary(neue_vokabel)
        mongodb_manager.delete_folder_or_vocabulary(self.folder, "leer", "leer")
        folder_content = mongodb_manager.find_vocabularies(self.folder)

        show_vocabularies = [f"• {word['Englisch']} - {word['Deutsch']}" for word in folder_content]
        self.ui.listWidget.clear()
        self.ui.listWidget.addItems(show_vocabularies[::-1])

        self.ui.pb_confirm.setEnabled(False)
        self.ui.l_vocabulary_english.clear()
        self.ui.l_vocabulary_german.clear()


class WindowAddVocabulariesNameFolder(QtWidgets.QMainWindow):
    def __init__(self, controller, folders):
        super().__init__(parent=None)
        self.ui = Ui_WindowAddVocabulariesNameFolder()
        self.ui.setupUi(self)

        self.folders = folders
        self.controller = controller

        self.ui.pb_confirm.setEnabled(False)
        self.ui.pb_back.clicked.connect(self.back_folders)
        self.ui.pb_confirm.clicked.connect(self.enter_folder)
        self.ui.l_folder.textChanged.connect(self.check_entry)

    def sort_folders(self) -> list[str]:
        """Gets the folders und gives the folders mit point back."""
        folders = mongodb_manager.get_folders()
        folders = methods_manager.sort_folders(folders)
        return folders

    def back_folders(self) -> None:
        """Goes back and updates the folders."""
        self.ui.listWidget.clear()
        self.sort_folders()
        self.controller.update_folders()
        self.ui.listWidget.addItems(self.folders)
        self.controller.back_name_folders()

    def check_entry(self) -> None:
        """Checks if you have given the folder a name. If the label is filled, you can click the push button."""
        if self.ui.l_folder.text():
            self.ui.pb_confirm.setEnabled(True)
        else:
            self.ui.pb_confirm.setEnabled(False)

    def enter_folder(self) -> None:
        """
        Creates a placeholder vocabulary and updates the list of folders.
        It takes the new folder at the beginning.
        """
        folder_new = self.ui.l_folder.text()
        english = "leer"
        german = "leer"
        new_vocabulary = {
            "Englisch": english,
            "Deutsch": german,
            "Kategorie": folder_new,
            "gewusst": False,
        }
        mongodb_manager.add_one_vocabulary(new_vocabulary)

        self.ui.l_folder.clear()

        folders = mongodb_manager.get_folders()
        folders = methods_manager.sort_folders(folders)
        for k in folders:
            if k == "• " + folder_new.strip():
                folders.remove(k)
                folders.insert(0, k)

        self.ui.listWidget.clear()
        self.ui.listWidget.addItems(folders)