import random
from ui.window_write_vocabularies import Ui_WindowWriteVocabularies
from ui.window_folder_query import Ui_WindowFolderQuery
from qtpy import QtWidgets
from mongodb import *
from methods_manager import *

sort_folders = SortFolders()
training = Training()
mongodb_manager = MongoDBManager()


class WindowFolderQueryWrite(QtWidgets.QMainWindow):
    def __init__(self, controller):
        super().__init__(parent=None)
        self.ui = Ui_WindowFolderQuery()
        self.ui.setupUi(self)

        folders = mongodb_manager.get_folders()
        folders = sort_folders.sort_folders(folders)

        self.controller = controller
        self.ui.pb_back.clicked.connect(self.controller.back_write_vocabularies_selection)

        self.ui.listWidget.clear()
        self.ui.listWidget.addItems(folders)
        self.ui.listWidget.itemClicked.connect(self.folder_chosen)


    def folder_chosen(self, item: QtWidgets.QListWidgetItem) -> None:
        """Gets the folder and gives it to the controller."""
        self.folder = item.text().strip("•").strip()
        self.controller.open_write_vocabularies(self.folder, training.direction(self.ui))


class WindowWritesVocabularies(QtWidgets.QMainWindow):
    def __init__(self, controller, folder, direction, give_number):
        super().__init__(parent=None)
        self.ui = Ui_WindowWriteVocabularies()
        self.ui.setupUi(self)

        self.give_number = give_number
        self.controller = controller
        self.direction = direction
        self.folder = folder


        self.ui.pb_back.clicked.connect(self.controller.back_write_vocabularies)
        self.ui.pb_check.clicked.connect(self.check_translation)
        self.ui.l_input.textChanged.connect(self.check_entry)
        self.ui.pb_card.clicked.connect(self.card)
        self.ui.pb_check.setEnabled(False)
        self.ui.pb_card.setEnabled(False)
        self.ui.pb_statistic.hide()

        mongodb_manager.update_known(self.folder, True)

        vocabularies = list(mongodb_manager.find_vocabularies(self.folder))
        random.shuffle(vocabularies)
        self.vocabulary_list = vocabularies

        self.check_folder_empty()

        self.ui.pb_statistic.clicked.connect(self.show_statistic)

    def start(self, direction: bool) -> None:
        """Checks if you are finished with you training and sets the direction for writing."""
        if len(self.vocabulary_list) == 0:
            self.ui.l_card.clear()
            self.ui.l_text.clear()
            self.ui.l_input.clear()
            self.ui.l_card.setText("Ende!\n Sie haben es geschafft!")
            self.ui.pb_check.setEnabled(False)
            self.ui.pb_card.setEnabled(False)
            self.ui.l_input.setEnabled(False)
            self.ui.pb_statistic.show()


        else:
            self.ui.pb_card.setEnabled(True)
            self.vocabulary = self.vocabulary_list[0]
            if direction == True:
                self.english = self.vocabulary["Englisch"]
                self.german = self.vocabulary["Deutsch"]
            else:
                self.english = self.vocabulary["Deutsch"]
                self.german = self.vocabulary["Englisch"]



    def card(self) -> None:
        """Clears and gives the text on the card. Activates the statistic push button."""
        self.ui.l_card.clear()
        self.ui.l_card.setText(self.english)
        self.ui.l_input.clear()
        self.ui.l_text.clear()
        self.ui.pb_statistic.setEnabled(True)


    def check_folder_empty(self) -> None:
        """Checks if the folder is empty. If the folder is not empty, it starts."""
        if mongodb_manager.count_vocabularies(self.folder, "leer", "leer") == 1:
            self.empty_folder = "Der Ordner ist leer. \n Sie können hier nicht lernen."
            self.ui.l_card.setText(self.empty_folder)
            self.ui.l_input.setEnabled(False)
            self.ui.l_text.clear()

        else:
            self.start(self.direction)
            self.card()

    def check_translation(self) -> None:
        """Checks if the translation word is in the vocabulary."""
        if self.ui.l_input.text() == self.german:
            self.ui.l_text.clear()
            self.ui.l_text.setText("Richtig!")
            self.ui.l_card.clear()
            self.ui.l_card.setText(self.german)
            self.vocabulary_list.pop(0)
            self.start(self.direction)
        else:
            mongodb_manager.update_known_id(self.vocabulary, False)
            self.ui.l_text.clear()
            self.ui.l_text.setText("Falsch!")
            self.ui.l_card.clear()
            self.ui.l_card.setText(self.german)
            self.take_vocabulary = self.vocabulary_list.pop(0)
            self.vocabulary_list.append(self.take_vocabulary)
            self.start(self.direction)
        self.ui.pb_check.setEnabled(False)

    def check_entry(self) -> None:
        """Checks if there is an entry and activates or deactivates the push button."""
        if self.ui.l_input.text():
            self.ui.pb_check.setEnabled(True)
        else:
            self.ui.pb_check.setEnabled(False)

    def show_statistic(self) -> None:
        """
        Gives the number of not known and number of all trained vocabularies to the statistic.
        Opens the statistic.
        Changes the number of the GiveNumber class.
        """
        plt.close("all")
        vocabularies = list(mongodb_manager.find_vocabularies(self.folder))
        self.number_of_vocabularies = len(vocabularies)
        self.not_known = len(list(mongodb_manager.find_vocabularies(self.folder, False)))
        training.get_statistic(self.number_of_vocabularies, self.not_known)
        self.give_number.number_write_vocabularies()
        self.controller.open_statistic()













