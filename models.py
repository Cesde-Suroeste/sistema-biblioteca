# models.py
# Definición de los modelos de datos para el sistema de biblioteca

import uuid
from datetime import datetime, timedelta

class Book:
    """
    Clase que representa un libro en el sistema de biblioteca.
    """
    def __init__(self, title, author, genre, isbn, publication_date=None):
        self.id = str(uuid.uuid4())
        self.title = title
        self.author = author
        self.genre = genre
        self.isbn = isbn
        self.status = "available"  # available, borrowed, reserved
        self.publication_date = publication_date or datetime.now().strftime("%Y-%m-%d")
    
    def to_dict(self):
        """Convierte el objeto a un diccionario para almacenamiento."""
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "genre": self.genre,
            "isbn": self.isbn,
            "status": self.status,
            "publication_date": self.publication_date
        }
    
    @classmethod
    def from_dict(cls, data):
        """Crea un objeto Book a partir de un diccionario."""
        book = cls(
            title=data["title"],
            author=data["author"],
            genre=data["genre"],
            isbn=data["isbn"],
            publication_date=data.get("publication_date")
        )
        book.id = data["id"]
        book.status = data["status"]
        return book

class User:
    """
    Clase que representa un usuario en el sistema de biblioteca.
    """
    def __init__(self, name, email):
        self.id = str(uuid.uuid4())
        self.name = name
        self.email = email
        self.borrowed_books = []
        self.loan_history = []
    
    def to_dict(self):
        """Convierte el objeto a un diccionario para almacenamiento."""
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "borrowed_books": self.borrowed_books,
            "loan_history": self.loan_history
        }
    
    @classmethod
    def from_dict(cls, data):
        """Crea un objeto User a partir de un diccionario."""
        user = cls(
            name=data["name"],
            email=data["email"]
        )
        user.id = data["id"]
        user.borrowed_books = data["borrowed_books"]
        user.loan_history = data["loan_history"]
        return user

class Loan:
    """
    Clase que representa un préstamo en el sistema de biblioteca.
    """
    def __init__(self, book_id, user_id, loan_days=14):
        self.id = str(uuid.uuid4())
        self.book_id = book_id
        self.user_id = user_id
        self.loan_date = datetime.now().strftime("%Y-%m-%d")
        self.due_date = (datetime.now() + timedelta(days=loan_days)).strftime("%Y-%m-%d")
        self.return_date = None
        self.status = "active"  # active, returned
    
    def to_dict(self):
        """Convierte el objeto a un diccionario para almacenamiento."""
        return {
            "id": self.id,
            "book_id": self.book_id,
            "user_id": self.user_id,
            "loan_date": self.loan_date,
            "due_date": self.due_date,
            "return_date": self.return_date,
            "status": self.status
        }
    
    @classmethod
    def from_dict(cls, data):
        """Crea un objeto Loan a partir de un diccionario."""
        loan = cls(
            book_id=data["book_id"],
            user_id=data["user_id"]
        )
        loan.id = data["id"]
        loan.loan_date = data["loan_date"]
        loan.due_date = data["due_date"]
        loan.return_date = data["return_date"]
        loan.status = data["status"]
        return loan