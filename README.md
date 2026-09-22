# Vocabulary Trainer

Do you want to learn new English vocabulary without having to store piles of paper flashcards in your cupboard?
Then I have the right solution for you!
This is a desktop application for learning with digital flashcards. 
You can quiz yourself on your vocabulary, organize your vocabulary into folders, and manage your vocabulary collections easily.

It is an application using MongoDB and Qt that was developed using object-oriented programming.


## View Application

### Main Menu
![Main Menu](screenshots/main_menu.png)

### Vocabulary Management
![Vocabulary Management](screenshots/vocabulary_management.png)

### Learning Mode
![Learning Mode](screenshots/learning_mode.png)


## Setup

1. Create a virtual environment (using Python 3.12) (Windows):
   
   python -m venv .venv

1. Create a virtual environment (using Python 3.12) (Ubuntu):
   
   python3.12 -m venv .venv
   
2. Activate the environment (Windows):

       .venv\Scripts\activate

2. Activate the environment (Ubuntu):

  source .venv/bin/activate

3. Install the dependencies:
   
      pip install -r requirements.txt

4. Set up MongoDB locally (required for `vocabulary_trainer/main.py`)

   - MongoDB must be running locally on `mongodb://localhost:27017/`
   - Expected database: `Vokabeltrainer`
   - Expected collection: `Vokabeln`
   - Expected fields for each entry:`Englisch`, `Deutsch`, `Kategorie`, `gewusst`

    Example using `mongosh`:
   
    use Vokabeltrainer
    db.createCollection("Vokabeln")
    db.Vokabeln.insertOne({ Englisch: "apple", Deutsch: "Apfel", Kategorie: "Obst" })


   Done! You can start the project now.





   





   


   





