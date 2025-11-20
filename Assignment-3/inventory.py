# inventory.py
import json
import logging
from pathlib import Path
from .book import Book

logging.basicConfig(level=logging.INFO)

class LibraryInventory:
    def __init__(self, filepath="data/catalog.json"):
        self.filepath = Path(filepath)
        self.books = []
        self.load_books()

    def load_books(self):
        try:
            if not self.filepath.exists():
                self.filepath.parent.mkdir(parents=True, exist_ok=True)
                self.filepath.write_text("[]")

            with open(self.filepath, "r") as f:
                data = json.load(f)
                self.books = [Book(**book) for book in data]

        except Exception as e:
            logging.error("Error loading book file: %s", e)
            self.books = []

    def save_books(self):
        try:
            with open(self.filepath, "w") as f:
                json.dump([b.to_dict() for b in self.books], f, indent=4)
        except Exception as e:
            logging.error("Error saving book file: %s", e)

    def add_book(self, book):
        for b in self.books:
            if b.isbn == book.isbn:
                return False
        self.books.append(book)
        self.save_books()
        return True

    def search_by_title(self, title):
        return [b for b in self.books if title.lower() in b.title.lower()]

    def search_by_isbn(self, isbn):
        for book in self.books:
            if book.isbn == isbn:
                return book
        return None

    def display_all(self):
        return [str(b) for b in self.books]

    def issue_book(self, isbn):
        book = self.search_by_isbn(isbn)
        if book and book.issue():
            self.save_books()
            return True
        return False

    def return_book(self, isbn):
        book = self.search_by_isbn(isbn)
        if book and book.return_book():
            self.save_books()
            return True
        return False
