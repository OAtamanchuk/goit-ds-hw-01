import pickle
from handler import AddressBook

FILENAME = "addressbook.pkl"

def save_data(book, filename=FILENAME):
    with open(filename, "wb") as f:
        pickle.dump(book, f) # Сереалізація 


def load_data(filename=FILENAME):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f) # Десереалізація
    except FileNotFoundError:
        return AddressBook()
