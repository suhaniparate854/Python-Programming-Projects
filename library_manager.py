import json
import os
from typing import Dict, List

DATA_FILE = "library_data.json"

class Book:
    def __init__(self, book_id: int, title: str, author: str, issued: bool = False):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.issued = issued

    def to_dict(self) -> dict:
        return {
            "book_id": self.book_id,
            "title": self.title,
            "author": self.author,
            "issued": self.issued,
        }

    @staticmethod
    def from_dict(data: dict) -> "Book":
        return Book(
            book_id=data["book_id"],
            title=data["title"],
            author=data["author"],
            issued=data.get("issued", False),
        )

    def __str__(self) -> str:
        status = "Issued" if self.issued else "Available"
        return f"[{self.book_id}] {self.title} by {self.author} - {status}"


class Library:
    def __init__(self):
        # HashMap-like storage for quick lookup by id
        self.books: Dict[int, Book] = {}
        self.next_id = 1
        self.load()

    # ---------------- Persistence ----------------
    def load(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                for b in data.get("books", []):
                    book = Book.from_dict(b)
                    self.books[book.book_id] = book
                self.next_id = data.get("next_id", 1)

    def save(self):
        data = {
            "next_id": self.next_id,
            "books": [b.to_dict() for b in self.books.values()],
        }
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    # ---------------- Core Operations ----------------
    def add_book(self, title: str, author: str):
        book = Book(self.next_id, title, author)
        self.books[self.next_id] = book
        self.next_id += 1
        self.save()
        print("Book added successfully.")

    def search_by_title(self, keyword: str) -> List[Book]:
        return [
            b for b in self.books.values()
            if keyword.lower() in b.title.lower()
        ]

    def search_by_author(self, keyword: str) -> List[Book]:
        return [
            b for b in self.books.values()
            if keyword.lower() in b.author.lower()
        ]

    def issue_book(self, book_id: int):
        book = self.books.get(book_id)
        if not book:
            print("Book not found.")
            return
        if book.issued:
            print("Book is already issued.")
            return
        book.issued = True
        self.save()
        print("Book issued successfully.")

    def return_book(self, book_id: int):
        book = self.books.get(book_id)
        if not book:
            print("Book not found.")
            return
        if not book.issued:
            print("Book was not issued.")
            return
        book.issued = False
        self.save()
        print("Book returned successfully.")

    # ---------------- Reports ----------------
    def total_books(self) -> int:
        return len(self.books)

    def issued_count(self) -> int:
        return sum(1 for b in self.books.values() if b.issued)

    def list_all(self):
        if not self.books:
            print("No books in library.")
            return
        for b in self.books.values():
            print(b)


# ---------------- CLI Menu ----------------
def main():
    library = Library()

    while True:
        print("\n===== Library Book Inventory Manager =====")
        print("1. Add Book")
        print("2. Search by Title")
        print("3. Search by Author")
        print("4. Issue Book")
        print("5. Return Book")
        print("6. List All Books")
        print("7. Reports")
        print("0. Exit")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            title = input("Enter title: ").strip()
            author = input("Enter author: ").strip()
            library.add_book(title, author)

        elif choice == "2":
            key = input("Enter title keyword: ").strip()
            results = library.search_by_title(key)
            for b in results:
                print(b)
            if not results:
                print("No matching books found.")

        elif choice == "3":
            key = input("Enter author keyword: ").strip()
            results = library.search_by_author(key)
            for b in results:
                print(b)
            if not results:
                print("No matching books found.")

        elif choice == "4":
            book_id = int(input("Enter book id to issue: "))
            library.issue_book(book_id)

        elif choice == "5":
            book_id = int(input("Enter book id to return: "))
            library.return_book(book_id)

        elif choice == "6":
            library.list_all()

        elif choice == "7":
            print(f"Total books: {library.total_books()}")
            print(f"Issued books: {library.issued_count()}")

        elif choice == "0":
            print("Exiting... Data saved.")
            break

        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()
