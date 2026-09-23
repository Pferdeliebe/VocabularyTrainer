from qtpy import QtWidgets
from PyQt6.QtWidgets import QMessageBox
from mongodb import *
from ui.window_delete_selection import Ui_WindowDeleteSelection
from ui.window_delete_folder import Ui_WindowDeleteFolder
from ui.window_vocabulary_delete_folder import Ui_WindowVocabularyDeleteFolder
from ui.window_vocabularies_delete import Ui_WindowVocabulariesDelete
from methods_manager import *

methods_manager = SortFolders()
mongodb_manager = MongoDBManager()

class WindowDeleteSelection(QtWidgets.QMainWindow):
    def __init__(self, controller):
        super().__init__(parent=None)
        self.ui = Ui_WindowDeleteSelection()
        self.ui.setupUi(self)

        self.controller = controller
        self.ui.pb_vocabulary.clicked.connect(self.delete_vocabularies)
        self.ui.pb_folder.clicked.connect(self.delete_folder)
        self.ui.pb_back.clicked.connect(self.controller.back_delete_selection)

    def delete_vocabularies(self) -> None:
        """Gets and sorts folders. Gives ist to the window for deleting vocabularies."""
        folders = mongodb_manager.get_folders()
        folders = methods_manager.sort_folders(folders)
        self.controller.open_delete_vocabularies(folders)


    def delete_folder(self) -> None:
        """Gets and sorts folders. Gives ist to the window for deleting folders."""
        folders = mongodb_manager.get_folders()
        folders = methods_manager.sort_folders(folders)
        self.controller.open_delete_folder(folders)


class WindowDeleteFolder(QtWidgets.QMainWindow):
    def __init__(self, controller, folders):
        super().__init__(parent=None)
        self.ui = Ui_WindowDeleteFolder()
        self.ui.setupUi(self)

        self.controller = controller
        self.folders = sorted(folders, key=str.lower)

        self.ui.listWidget.clear()
        self.ui.listWidget.addItems(self.folders)
        self.ui.listWidget.itemClicked.connect(self.delete_folders)
        self.ui.pb_back.clicked.connect(self.controller.back_delete_folder)


    def show_folders(self) -> None:
        """Show the folders."""
        self.ui.listWidget.clear()
        folders = mongodb_manager.get_folders()
        self.folders = methods_manager.sort_folders(folders)
        self.ui.listWidget.addItems(self.folders)

    def delete_folders(self, item: QtWidgets.QListWidgetItem) -> None:
        """Deletes folder and updates the folder list on the screen."""
        folder_name = item.text().strip("•").strip()
        mongodb_manager.delete_folder_or_vocabulary(folder_name)
        self.show_folders()


class WindowVocabularyDeleteFolder(QtWidgets.QMainWindow):
    def __init__(self, controller, kategorien):
        super().__init__(parent=None)
        self.ui = Ui_WindowVocabularyDeleteFolder()
        self.ui.setupUi(self)

        self.controller = controller
        self.folders = sorted(kategorien, key=str.lower)

        self.ui.listWidget.clear()
        self.ui.listWidget.addItems(self.folders)
        self.ui.listWidget.itemClicked.connect(self.vocabularies_delete)
        self.ui.pb_back.clicked.connect(self.controller.back_delete_vocabularies_selection)


    def vocabularies_delete(self, item: QtWidgets.QListWidgetItem) -> None:
        """Checks if the folder is empty. It shows the vocabularies otherwise the folder is empty."""
        folder = item.text().strip("•").strip()
        folder_content = mongodb_manager.find_vocabularies(folder)
        if mongodb_manager.count_vocabularies(folder, "leer", "leer") == 1:
            show_vocabularies = ["Der Ordner ist leer."]
        else:
            show_vocabularies = [f"• {word['Englisch']} - {word['Deutsch']}" for word in folder_content]
        self.controller.open_show_delete_vocabularies(folder, show_vocabularies, self.folders)


class WindowVocabulariesDelete(QtWidgets.QMainWindow):
    def __init__(self, controller, folder, chosen_folder, folders):
        super().__init__(parent=None)
        self.ui = Ui_WindowVocabulariesDelete()
        self.ui.setupUi(self)

        self.controller = controller
        self.folder = folder
        self.chosen_folder = chosen_folder
        self.folders = folders


        self.ui.listWidget.clear()
        self.ui.listWidget.addItems(chosen_folder)
        self.ui.pb_back.clicked.connect(self.back_update_folders)
        self.ui.listWidget.itemClicked.connect(self.vocabulary_delete)

    def back_update_folders (self) -> None:
        """Updates the folder selection for going back from deleting vocabularies to the folder selection."""
        folders = mongodb_manager.get_folders()
        folders = methods_manager.sort_folders(folders)
        self.controller.back_delete_vocabularies(folders)


    def vocabulary_delete(self, item: QtWidgets.QListWidgetItem) -> None:
        """
        Checks if the folder is empty. If it is empty, you cannot delete.
        Is the folder not empty, you can delete vocabularies.
        If you delete the last vocabulary, there will be appear a question box to ask for delete the folder.
        """
        complete_vocabulary = item.text()
        if complete_vocabulary == "Der Ordner ist leer" or "-" not in complete_vocabulary:
            return

        english_word = complete_vocabulary.split("-")[0].strip("•").strip()

        german_word = complete_vocabulary.split("-")[1].strip()

        mongodb_manager.delete_folder_or_vocabulary(None, english_word, german_word)
        if complete_vocabulary in self.chosen_folder:
            self.chosen_folder.remove(complete_vocabulary)
        self.ui.listWidget.clear()
        self.ui.listWidget.addItems(self.chosen_folder)


        if len(self.chosen_folder) == 0:

            message_box = QMessageBox(self)
            message_box.setWindowTitle("Ordner löschen?")
            message_box.setText(
                "Das war die letzte Vokabel. Möchten Sie den leeren Ordner ebenfalls löschen?"
            )

            message_box.setStandardButtons(
                QMessageBox.StandardButton.Yes |
                QMessageBox.StandardButton.No
            )

            message_box.button(QMessageBox.StandardButton.Yes).setText("Ja")
            message_box.button(QMessageBox.StandardButton.No).setText("Nein")

            answer = message_box.exec()

            if answer == QMessageBox.Yes:
                QMessageBox.information(self, "Ordner gelöscht", "Der Ordner ist gelöscht.")

            else:
                english = "leer"
                german = "leer"
                new_vocabulary = {
                    "Englisch": english,
                    "Deutsch": german,
                    "Kategorie": self.folder,
                    "gewusst": False,
                }
                mongodb_manager.add_one_vocabulary(new_vocabulary)
                if len(self.chosen_folder) == 0:
                    self.ui.listWidget.addItem("Der Ordner ist leer.")
