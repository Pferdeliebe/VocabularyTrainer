from qtpy import QtWidgets
import random
from mongodb import *
from ui.window_folder_query import Ui_WindowFolderQuery
from ui.window_vocabulary_asking import Ui_WindowVocabularyAsking
from methods_manager import *

methods_manager = SortFolders()
training = Training()
mongodb_manager = MongoDBManager()


class WindowFolderQueryAsk(QtWidgets.QMainWindow):
    def __init__(self, controller):
        super().__init__(parent=None)
        self.ui = Ui_WindowFolderQuery()
        self.ui.setupUi(self)

        folders = mongodb_manager.get_folders()
        folders = methods_manager.sort_folders(folders)

        self.controller = controller
        self.ui.pb_back.clicked.connect(self.controller.back_ask_vocabularies_selection)

        self.ui.listWidget.clear()
        self.ui.listWidget.addItems(folders)
        self.ui.listWidget.itemClicked.connect(self.folder_chosen)

    def folder_chosen(self, item: QtWidgets.QListWidgetItem) -> None:
        """Takes the clicked folder and opens the folder's vocabularies for asking."""
        self.folder = item.text().strip("•").strip()
        self.controller.open_ask_vocabularies(self.folder, training.direction(self.ui))


class WindowVocabularyAsking(QtWidgets.QMainWindow):
    def __init__(self, controller, folder, direction, give_number):
        super().__init__(parent=None)
        self.give_number= give_number
        self.ui = Ui_WindowVocabularyAsking()
        self.ui.setupUi(self)

        self.controller = controller
        self.direction = direction
        self.folder = folder
        self.frontside = True


        self.ui.pb_back.clicked.connect(self.controller.back_ask_vocabularies)
        self.ui.pb_card.clicked.connect(self.switch_card)
        self.ui.pb_known.setEnabled(False)
        self.ui.pb_not_known.setEnabled(False)
        self.ui.pb_known.clicked.connect(self.button_known)
        self.ui.pb_not_known.clicked.connect(self.button_not_known)
        self.ui.pb_statistic.hide()

        mongodb_manager.update_known(self.folder, True)

        vocabularies = list(mongodb_manager.find_vocabularies(self.folder))
        random.shuffle(vocabularies)
        self.vocabularylist = vocabularies

        self.check_folder_empty()

        self.ui.pb_statistic.clicked.connect(self.statistic_show)

    def start(self, direction: bool) -> None:
        """Checks if you are finish with your training. Determines the direction in which the card should be asked."""
        if len(self.vocabularylist) == 0:
            self.ui.l_card.clear()
            self.ui.l_card.setText("Ende!\n Sie haben es geschafft!")
            self.ui.pb_card.setEnabled(False)
            self.ui.pb_known.setEnabled(False)
            self.ui.pb_not_known.setEnabled(False)
            self.ui.pb_statistic.show()
        else:
            self.vocabulary = self.vocabularylist[0]
            if direction == True:
                self.english = self.vocabulary["Englisch"]
                self.german = self.vocabulary["Deutsch"]
            else:
                self.english = self.vocabulary["Deutsch"]
                self.german = self.vocabulary["Englisch"]

            self.switch_card()

    def switch_card(self) -> None:
        """Flips the card."""
        if self.frontside:
            self.card_frontside()
        else:
            self.card_backside()

    def card_frontside(self) -> None:
        """Cleans the card and gives it a text. Deactivates the push buttons."""
        self.ui.l_card.clear()
        self.ui.l_card.setText(self.english)
        self.ui.pb_known.setEnabled(False)
        self.ui.pb_not_known.setEnabled(False)
        self.frontside = False


    def card_backside(self) -> None:
        """Gives the card a text and activates the push buttons."""
        self.ui.l_card.setText(self.german)
        self.ui.pb_known.setEnabled(True)
        self.ui.pb_not_known.setEnabled(True)
        self.frontside = True


    def button_known(self) -> None:
        """Takes the know vocabulary from the vocabularies and starts with next vocabulary."""
        self.vocabularylist.pop(0)
        self.start(self.direction)

    def button_not_known(self) -> None:
        """
        Updates 'gewusst' into False for the statistic.
        Takes the vocabulary from the vocabularies and puts it to the end for asking later again.
        Starts asking the next vocabulary.
        """
        mongodb_manager.update_known_id(self.vocabulary, False)
        self.take_vocabulary = self.vocabularylist.pop(0)
        self.vocabularylist.append(self.take_vocabulary)
        self.start(self.direction)

    def check_folder_empty(self) -> None:
        """Checks if the folder is empty, so that there is only the placeholder vocabulary."""
        if mongodb_manager.count_vocabularies(self.folder, "leer", "leer")== 1:
            self.empty_folder = "Der Ordner ist leer. \n Sie können hier nicht lernen."
            self.ui.l_card.setText(self.empty_folder)
            self.ui.pb_card.setEnabled(False)
        else:
            self.start(self.direction)

    def statistic_show(self) -> None:
        """
        Determines the know and not know vocabularies in the first asking round.
        Shows the statistic.
        Gives a number. So the programm knows by going back in the next window, that you come from asking.
        Opens the statistic window.
        """
        plt.close("all")
        vocabularies = list(mongodb_manager.find_vocabularies(self.folder))
        self.number_of_vocabularies = len(vocabularies)
        self.not_known = len(list(mongodb_manager.find_vocabularies(self.folder, False)))
        training.get_statistic(self.number_of_vocabularies, self.not_known)
        self.give_number.number_ask_vocabularies()
        self.controller.open_statistic()




