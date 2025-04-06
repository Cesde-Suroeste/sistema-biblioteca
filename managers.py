# managers.py
# Clases para gestionar la lógica de negocio y el acceso a datos

import json
from datetime import datetime
from data_structures import LinkedList, Stack, Queue
from models import Book, User, Loan

class BookManager:
    """
    Clase para gestionar la colección de libros.
    Utiliza una Lista Enlazada para almacenar los libros.
    """
    def __init__(self):
        self.books = LinkedList()
        self.load_data()
    
    def add_book(self, book):
        """Agrega un nuevo libro a la colección."""
        self.books.append(book)
        self.save_data()
        return True
    
    def get_book_by_id(self, book_id):
        """Busca un libro por su ID."""
        current = self.books.head
        while current:
            if current.data.id == book_id:
                return current.data
            current = current.next
        return None
    
    def update_book(self, book_id, updated_data):
        """Actualiza la información de un libro."""
        book = self.get_book_by_id(book_id)
        if not book:
            return False
        
        if "title" in updated_data:
            book.title = updated_data["title"]
        if "author" in updated_data:
            book.author = updated_data["author"]
        if "genre" in updated_data:
            book.genre = updated_data["genre"]
        if "isbn" in updated_data:
            book.isbn = updated_data["isbn"]
        if "status" in updated_data:
            book.status = updated_data["status"]
        if "publication_date" in updated_data:
            book.publication_date = updated_data["publication_date"]
        
        self.save_data()
        return True
    
    def delete_book(self, book_id):
        """Elimina un libro de la colección."""
        current = self.books.head
        previous = None
        
        # Si la lista está vacía
        if not current:
            return False
        
        # Si el libro a eliminar es el primero
        if current.data.id == book_id:
            self.books.head = current.next
            self.books._size -= 1
            self.save_data()
            return True
        
        # Buscar el libro en el resto de la lista
        while current and current.data.id != book_id:
            previous = current
            current = current.next
        
        # Si el libro no se encuentra
        if not current:
            return False
        
        # Eliminar el libro
        previous.next = current.next
        self.books._size -= 1
        self.save_data()
        return True
    
    def search_books(self, criteria):
        """
        Busca libros que coincidan con los criterios especificados.
        criteria: diccionario con campos a buscar (title, author, genre, etc.)
        """
        results = LinkedList()
        current = self.books.head
        
        while current:
            book = current.data
            match = True
            
            for key, value in criteria.items():
                if key == "title" and value.lower() not in book.title.lower():
                    match = False
                    break
                elif key == "author" and value.lower() not in book.author.lower():
                    match = False
                    break
                elif key == "genre" and value.lower() not in book.genre.lower():
                    match = False
                    break
                elif key == "isbn" and value != book.isbn:
                    match = False
                    break
                elif key == "status" and value != book.status:
                    match = False
                    break
            
            if match:
                results.append(book)
            
            current = current.next
        
        return results
    
    def get_all_books(self):
        """Devuelve una lista con todos los libros."""
        return self.books.display()
    
    def save_data(self):
        """Guarda los datos de libros en un archivo JSON."""
        books_data = []
        current = self.books.head
        while current:
            books_data.append(current.data.to_dict())
            current = current.next
        
        with open("books.json", "w") as file:
            json.dump(books_data, file, indent=4)
    
    def load_data(self):
        """Carga los datos de libros desde un archivo JSON."""
        try:
            with open("books.json", "r") as file:
                books_data = json.load(file)
                
                for book_data in books_data:
                    book = Book.from_dict(book_data)
                    self.books.append(book)
        except (FileNotFoundError, json.JSONDecodeError):
            # Si el archivo no existe o está vacío, crear uno nuevo
            with open("books.json", "w") as file:
                json.dump([], file)

class UserManager:
    """
    Clase para gestionar los usuarios.
    Utiliza una Lista Enlazada para almacenar los usuarios.
    """
    def __init__(self):
        self.users = LinkedList()
        self.load_data()
    
    def add_user(self, user):
        """Agrega un nuevo usuario."""
        self.users.append(user)
        self.save_data()
        return True
    
    def get_user_by_id(self, user_id):
        """Busca un usuario por su ID."""
        current = self.users.head
        while current:
            if current.data.id == user_id:
                return current.data
            current = current.next
        return None
    
    def update_user(self, user_id, updated_data):
        """Actualiza la información de un usuario."""
        user = self.get_user_by_id(user_id)
        if not user:
            return False
        
        if "name" in updated_data:
            user.name = updated_data["name"]
        if "email" in updated_data:
            user.email = updated_data["email"]
        
        self.save_data()
        return True
    
    def delete_user(self, user_id):
        """Elimina un usuario."""
        current = self.users.head
        previous = None
        
        # Si la lista está vacía
        if not current:
            return False
        
        # Si el usuario a eliminar es el primero
        if current.data.id == user_id:
            self.users.head = current.next
            self.users._size -= 1
            self.save_data()
            return True
        
        # Buscar el usuario en el resto de la lista
        while current and current.data.id != user_id:
            previous = current
            current = current.next
        
        # Si el usuario no se encuentra
        if not current:
            return False
        
        # Eliminar el usuario
        previous.next = current.next
        self.users._size -= 1
        self.save_data()
        return True
    
    def search_users(self, criteria):
        """
        Busca usuarios que coincidan con los criterios especificados.
        criteria: diccionario con campos a buscar (name, email)
        """
        results = LinkedList()
        current = self.users.head
        
        while current:
            user = current.data
            match = True
            
            for key, value in criteria.items():
                if key == "name" and value.lower() not in user.name.lower():
                    match = False
                    break
                elif key == "email" and value.lower() not in user.email.lower():
                    match = False
                    break
            
            if match:
                results.append(user)
            
            current = current.next
        
        return results
    
    def get_all_users(self):
        """Devuelve una lista con todos los usuarios."""
        return self.users.display()
    
    def save_data(self):
        """Guarda los datos de usuarios en un archivo JSON."""
        users_data = []
        current = self.users.head
        while current:
            users_data.append(current.data.to_dict())
            current = current.next
        
        with open("users.json", "w") as file:
            json.dump(users_data, file, indent=4)
    
    def load_data(self):
        """Carga los datos de usuarios desde un archivo JSON."""
        try:
            with open("users.json", "r") as file:
                users_data = json.load(file)
                
                for user_data in users_data:
                    user = User.from_dict(user_data)
                    self.users.append(user)
        except (FileNotFoundError, json.JSONDecodeError):
            # Si el archivo no existe o está vacío, crear uno nuevo
            with open("users.json", "w") as file:
                json.dump([], file)

class LoanManager:
    """
    Clase para gestionar los préstamos.
    Utiliza una Lista Enlazada para almacenar los préstamos activos
    y una Pila para el historial de operaciones.
    """
    def __init__(self, book_manager, user_manager):
        self.loans = LinkedList()
        self.operations_history = Stack()
        self.book_manager = book_manager
        self.user_manager = user_manager
        self.loan_requests = Queue()  # Cola para solicitudes de préstamo
        self.load_data()
    
    def request_loan(self, book_id, user_id):
        """Añade una solicitud de préstamo a la cola."""
        request = {"book_id": book_id, "user_id": user_id, "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        self.loan_requests.enqueue(request)
        return True
    
    def process_loan_requests(self):
        """Procesa las solicitudes de préstamo pendientes."""
        while not self.loan_requests.is_empty():
            request = self.loan_requests.dequeue()
            success = self.create_loan(request["book_id"], request["user_id"])
            # Registrar el resultado de la operación
            operation = {
                "type": "loan_request",
                "data": request,
                "success": success,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            self.operations_history.push(operation)
    
    def create_loan(self, book_id, user_id):
        """Crea un nuevo préstamo."""
        # Verificar que el libro existe y está disponible
        book = self.book_manager.get_book_by_id(book_id)
        if not book or book.status != "available":
            return False
        
        # Verificar que el usuario existe
        user = self.user_manager.get_user_by_id(user_id)
        if not user:
            return False
        
        # Crear el préstamo
        loan = Loan(book_id, user_id)
        self.loans.append(loan)
        
        # Actualizar el estado del libro
        self.book_manager.update_book(book_id, {"status": "borrowed"})
        
        # Actualizar los préstamos del usuario
        user.borrowed_books.append(book_id)
        self.user_manager.save_data()
        
        # Registrar la operación
        operation = {
            "type": "create_loan",
            "data": loan.to_dict(),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.operations_history.push(operation)
        
        self.save_data()
        return True
    
    def return_book(self, loan_id):
        """Registra la devolución de un libro."""
        # Buscar el préstamo
        current = self.loans.head
        loan = None
        
        while current and not loan:
            if current.data.id == loan_id:
                loan = current.data
            current = current.next
        
        if not loan or loan.status != "active":
            return False
        
        # Actualizar el préstamo
        loan.return_date = datetime.now().strftime("%Y-%m-%d")
        loan.status = "returned"
        
        # Actualizar el estado del libro
        book = self.book_manager.get_book_by_id(loan.book_id)
        if book:
            self.book_manager.update_book(loan.book_id, {"status": "available"})
        
        # Actualizar los préstamos del usuario
        user = self.user_manager.get_user_by_id(loan.user_id)
        if user:
            if loan.book_id in user.borrowed_books:
                user.borrowed_books.remove(loan.book_id)
            user.loan_history.append(loan.id)
            self.user_manager.save_data()
        
        # Registrar la operación
        operation = {
            "type": "return_book",
            "data": loan.to_dict(),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.operations_history.push(operation)
        
        self.save_data()
        return True
    
    def get_active_loans(self):
        """Devuelve una lista con todos los préstamos activos."""
        active_loans = LinkedList()
        current = self.loans.head
        
        while current:
            if current.data.status == "active":
                active_loans.append(current.data)
            current = current.next
        
        return active_loans.display()
    
    def get_loan_history(self):
        """Devuelve el historial de operaciones de préstamos."""
        return self.operations_history.display()
    
    def get_pending_requests(self):
        """Devuelve las solicitudes de préstamo pendientes."""
        return self.loan_requests.display()
    
    def save_data(self):
        """Guarda los datos de préstamos en un archivo JSON."""
        loans_data = []
        current = self.loans.head
        while current:
            loans_data.append(current.data.to_dict())
            current = current.next
        
        with open("loans.json", "w") as file:
            json.dump(loans_data, file, indent=4)
        
        # Guardar el historial de operaciones
        operations_data = self.operations_history.display()
        with open("operations_history.json", "w") as file:
            json.dump(operations_data, file, indent=4)
        
        # Guardar las solicitudes pendientes
        requests_data = self.loan_requests.display()
        with open("loan_requests.json", "w") as file:
            json.dump(requests_data, file, indent=4)
    
    def load_data(self):
        """Carga los datos de préstamos desde archivos JSON."""
        # Cargar préstamos
        try:
            with open("loans.json", "r") as file:
                loans_data = json.load(file)
                
                for loan_data in loans_data:
                    loan = Loan.from_dict(loan_data)
                    self.loans.append(loan)
        except (FileNotFoundError, json.JSONDecodeError):
            with open("loans.json", "w") as file:
                json.dump([], file)
        
        # Cargar historial de operaciones
        try:
            with open("operations_history.json", "r") as file:
                operations_data = json.load(file)
                
                for operation in operations_data:
                    self.operations_history.push(operation)
        except (FileNotFoundError, json.JSONDecodeError):
            with open("operations_history.json", "w") as file:
                json.dump([], file)
        
        # Cargar solicitudes pendientes
        try:
            with open("loan_requests.json", "r") as file:
                requests_data = json.load(file)
                
                for request in requests_data:
                    self.loan_requests.enqueue(request)
        except (FileNotFoundError, json.JSONDecodeError):
            with open("loan_requests.json", "w") as file:
                json.dump([], file)