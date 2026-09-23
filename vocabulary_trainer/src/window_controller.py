from write_vocabularies import *
from main_menue import *
from vocabularies_management import *
from view_folders_vocabularies import *
from add_vocabularies_folder import *
from delete import *
from ask_vocabularies import *
from manager import Manager
from get_numbers import *
from statistic import *


manager = Manager()


class Controller:
    def __init__(self):
        self.get_number = GetNumbers()

        self.window_main = WindowMain(self)

        self.window_manage_vocabularies = WindowVocabularyManagement(self)
        self.folders_mv = self.window_manage_vocabularies.get_folders()

        self.window_name_folders = WindowAddVocabulariesNameFolder(self, self.folders_mv)
        self.window_selection_delete = WindowDeleteSelection(self)

    def start(self) -> None:
        """Opens the main menu."""
        self.window_main.show()

    def manage_vocabularies(self):
        """Closes the main menu and opens the vocabulary management."""
        manager.open_window(self.window_main, self.window_manage_vocabularies)

    def ask_vocabularies(self) -> None:
        """Closes the main menu and opens the folder selection of asking vocabularies."""
        self.window_ask_vocabularies_choose_folder = WindowFolderQueryAsk(self)
        manager.open_window(self.window_main, self.window_ask_vocabularies_choose_folder)

    def write_vocabularies(self) -> None:
        """Closes the main menu and opens the folder selection of writing vocabularies."""
        self.window_choose_folder_write_vocabularies = WindowFolderQueryWrite(self)
        manager.open_window(self.window_main, self.window_choose_folder_write_vocabularies)

    def show_folders(self, folders: list[str]) -> None:
        """Closes the vocabulary management and opens the folder selection for showing."""
        self.window_show_folders = WindowShowFolders(self, folders)
        manager.open_window(self.window_manage_vocabularies, self.window_show_folders)

    def back_manage_vocabularies(self) -> None:
        """Closes the vocabulary management and opens the main menu."""
        manager.open_window(self.window_manage_vocabularies, self.window_main)

    def add_vocabularies_folder(self) -> None:
        """Closes the vocabulary management and opens the folder selection for adding vocabularies."""
        self.current_folders = self.window_manage_vocabularies.get_folders()
        self.window_add_vocabularies_folder = WindowAddVocabulariesFolder(self, self.current_folders)
        manager.open_window(self.window_manage_vocabularies, self.window_add_vocabularies_folder)

    def selection_delete(self) -> None:
        """Closes the vocabulary management and opens the selection to delete vocabularies or folders."""
        manager.open_window(self.window_manage_vocabularies, self.window_selection_delete)

    def open_vocabularies(self, show_vocabularies: list[str], folders: list[str]) -> None:
        """Closes the showing of the folders and opens the vocabularies of the clicked folder."""
        self.window_vokabeln = WindowShowVocabularies(self, show_vocabularies, folders)
        manager.open_window(self.window_show_folders, self.window_vokabeln)

    def back_show_folders(self) -> None:
        """Closes the showing of the folders and opens the vocabulary management menu."""
        manager.open_window(self.window_show_folders, self.window_manage_vocabularies)

    def back_show_vocabularies(self) -> None:
        """Closes the showing of the vocabularies and opens the showing of the folders."""
        manager.open_window(self.window_vokabeln, self.window_show_folders)

    def new_folder(self) -> None:
        """Closes the folder selection of adding vocabularies and opens the naming of folders."""
        manager.open_window(self.window_add_vocabularies_folder, self.window_name_folders)

    def open_folder_chosen(self, folder: str) -> None:
        """Closes the folder selection of adding vocabularies and opens the adding of vocabularies."""
        self.window_add_vocabularies = WindowAddVocabularies(self, folder, self.folders_mv)
        manager.open_window(self.window_add_vocabularies_folder, self.window_add_vocabularies)

    def back_add_vocabularies_folder(self) -> None:
        """Closes the folder selection of adding vocabularies and opens the vocabulary management."""
        manager.open_window(self.window_add_vocabularies_folder, self.window_manage_vocabularies)

    def back_add_vocabularies(self) -> None:
        """Closes adding the vocabularies and opens the folder selection of adding vocabularies."""
        manager.open_window(self.window_add_vocabularies, self.window_add_vocabularies_folder)

    def back_name_folders(self) -> None:
        """Closes for naming folders and opens the folder selection of adding vocabularies."""
        manager.open_window(self.window_name_folders, self.window_add_vocabularies_folder)

    def update_folders(self) -> None:
        """Updates the folders in the window of the folder selection of adding vocabularies."""
        self.folders_mv = self.window_name_folders.sort_folders()
        self.window_add_vocabularies_folder = WindowAddVocabulariesFolder(self, self.folders_mv)

    def open_delete_vocabularies(self, folders: list[str]) -> None:
        """Closes the selection of deleting vocabularies and opens the folder selection of deleting the vocabularies."""
        self.window_delete_vocabularies_selection = WindowVocabularyDeleteFolder(self, folders)
        manager.open_window(self.window_selection_delete, self.window_delete_vocabularies_selection)

    def open_delete_folder(self, folders: list[str]) -> None:
        """Closes the selection of deleting vocabularies and opens deleting folders."""
        self.window_delete_folders = WindowDeleteFolder(self, folders)
        manager.open_window(self.window_selection_delete, self.window_delete_folders)

    def back_delete_selection(self) -> None:
        """Closes the selection of deleting and opens the vocabulary management."""
        manager.open_window(self.window_selection_delete, self.window_manage_vocabularies)

    def back_delete_folder(self) -> None:
        """Closes deleting folders and opens the selection von deleting."""
        manager.open_window(self.window_delete_folders, self.window_selection_delete)

    def open_show_delete_vocabularies(self, folder: str, show_vocabularies: list[str], folders: list[str]) -> None:
        """Closes the folder selection of deleting vocabularies and opens deleting vocabularies."""
        self.window_show_vocabularies_delete = WindowVocabulariesDelete(self, folder, show_vocabularies, folders)
        manager.open_window(self.window_delete_vocabularies_selection , self.window_show_vocabularies_delete)

    def back_delete_vocabularies_selection(self) -> None:
        """Closes the folder selection of deleting vocabularies and opens the selection of deleting."""
        manager.open_window(self.window_delete_vocabularies_selection, self.window_selection_delete)

    def back_delete_vocabularies(self, folders) -> None:
        """Closes deleting vocabularies and opens the folder selection of deleting."""
        self.window_delete_vocabularies_selection = WindowVocabularyDeleteFolder(self, folders)
        manager.open_window(self.window_show_vocabularies_delete, self.window_delete_vocabularies_selection)

    def back_ask_vocabularies_selection(self) -> None:
        """Closes the folder selection of asking vocabularies and opens the main menu."""
        manager.open_window(self.window_ask_vocabularies_choose_folder, self.window_main)

    def open_ask_vocabularies(self, folder: str, direction: bool) -> None:
        """Closes the folder selection of asking vocabularies and opens asking vocabularies."""
        self.window_ask_vocabularies = WindowVocabularyAsking(self, folder, direction, self.get_number)
        manager.open_window(self.window_ask_vocabularies_choose_folder, self.window_ask_vocabularies)

    def open_write_vocabularies(self, folder: str, direction: bool) -> None:
        """Closes the folder selection of writing vocabularies and opens writing vocabularies."""
        self.window_write_vocabularies = WindowWritesVocabularies(
            self,
            folder,
            direction,
            self.get_number
        )
        manager.open_window(self.window_choose_folder_write_vocabularies, self.window_write_vocabularies)

    def back_write_vocabularies_selection(self) -> None:
        """Closes the folder selection of writing vocabularies and opens the main menu."""
        manager.open_window(self.window_choose_folder_write_vocabularies, self.window_main)

    def back_write_vocabularies(self) -> None:
        """Closes writing vocabularies and opens the folder selection of wring vocabularies."""
        manager.open_window(self.window_write_vocabularies, self.window_choose_folder_write_vocabularies)

    def back_ask_vocabularies(self) -> None:
        """Closes asking vocabularies and opens the selection of asking vocabularies."""
        manager.open_window(self.window_ask_vocabularies, self.window_ask_vocabularies_choose_folder)

    def open_statistic(self) -> None:
        """Checks the number and concludes the current window. Closes the current window and opens the statistic. """
        self.window_statistic = WindowStatistic(self)
        if self.get_number.number == 1:
            manager.open_window(self.window_ask_vocabularies, self.window_statistic)
        elif self.get_number.number == 2:
            manager.open_window(self.window_write_vocabularies, self.window_statistic)

    def back_statistic(self) -> None:
        """Closes the statistic. Checks the number and concludes the current window and opens the current window."""
        if self.get_number.number == 1:
            manager.open_window(self.window_statistic, self.window_ask_vocabularies_choose_folder)
        elif self.get_number.number == 2:
            manager.open_window(self.window_statistic, self.window_choose_folder_write_vocabularies)

