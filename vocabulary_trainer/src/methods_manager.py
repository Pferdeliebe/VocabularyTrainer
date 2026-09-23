from matplotlib import pyplot as plt

class SortFolders:

    def sort_folders(self, folders: list[str]) -> list[str]:
        """Gives the folder names the point and sorts them."""
        folders = ["• " + k.strip() for k in folders]
        folders.sort(key=str.lower)
        return folders


class Training:

    def direction(self, ui) -> bool:
        """Checks the direction."""
        if ui.rb_eng.isChecked():
            return True
        else:
            return False

    def get_statistic(self, number_of_vocabularies: int, not_known: int) -> None:
        """Determines know and not know vocabularies in the first round. Create diagramm."""
        self.known = number_of_vocabularies - not_known
        self.number = [self.known, not_known]
        self.knownledge = [f"Gewusst: {self.known}", f"Nicht gewusst: {not_known}"]

        plt.pie(self.number, labels=self.knownledge, autopct='%1.1f%%', startangle=90)
        plt.title("Bei der ersten Abfrage gewusst")
        plt.savefig("../statistic/statistic_result.png", dpi=300)

