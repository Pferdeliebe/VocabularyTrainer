from bson import ObjectId
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from pymongo.synchronous.cursor import Cursor

class MongoDBManager:
    def __init__(self):
        try:
            self.client = MongoClient("mongodb://localhost:27017/")
            self.client.admin.command("ping")
            self.database = self.client["Vokabeltrainer"]
            self.collection = self.database["Vokabeln"]

        except ConnectionFailure:
            print("There is no connection to MongoDB possible.")

    def get_folders(self) -> list[str]:
        """Takes the folders."""
        folders = self.collection.distinct("Kategorie")
        return folders

    def find_vocabularies(self, folder: str, know: bool | None = None) -> Cursor:
        """Gets the searched vocabularies."""
        query: dict[str, str | bool] = {"Kategorie": folder}

        if know is not None:
            query["gewusst"] = know
        return self.collection.find(query)

    def add_one_vocabulary(self, vocabulary: dict[str, str | bool]):
        """Adds one vocabulary."""
        self.collection.insert_one(vocabulary)

    def delete_folder_or_vocabulary (
                                    self,
                                    folder: str | None = None,
                                    english: str | None = None,
                                    german: str | None = None
    ) -> None:
        """Deletes a folder or vocabulary."""
        query = {}
        if folder is not None:
            query["Kategorie"] = folder

        if english is not None and german is not None:
            query["Englisch"] = english
            query["Deutsch"] = german

        self.collection.delete_many(query)

    def count_vocabularies(self, folder: str, english: str, german: str) -> int:
        """Counts vocabularies."""
        return self.collection.count_documents({"Kategorie": folder, "Englisch": english, "Deutsch": german})

    def update_known(self, folder: str, on_off_known: bool) -> None:
        """Updates 'gewusst' from a specific folder."""
        self.collection.update_many({"Kategorie": folder}, {"$set": {"gewusst": on_off_known}})

    def update_known_id(self,vokabel: dict[str, str | bool | ObjectId], on_off_known):
        """Updates 'gewusst' from a specific vocabulary."""
        self.collection.update_one({"_id": vokabel["_id"]}, {"$set": {"gewusst": on_off_known}})