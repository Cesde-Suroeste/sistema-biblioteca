# tests.py
# Pruebas unitarias para el sistema de gestión de biblioteca

import unittest
import os
import json
from data_structures import LinkedList, Stack, Queue
from models import Book, User, Loan
from managers import BookManager, UserManager, LoanManager

class TestDataStructures(unittest.TestCase):
    """Pruebas para las estructuras de datos."""
    
    def test_linked_list(self):
        """Prueba las operaciones básicas de la Lista Enlazada."""
        ll = LinkedList()
        
        # Probar que la lista está vacía inicialmente
        self.assertTrue(ll.is_empty())
        self.assertEqual(ll.size, 0)
        
        # Probar append
        ll.append("Libro 1")
        self.assertFalse(ll.is_empty())
        self.assertEqual(ll.size, 1)
        
        # Probar prepend
        ll.prepend("Libro 0")
        self.assertEqual(ll.size, 2)
        self.assertEqual(ll.get_by_index(0), "Libro 0")
        
        # Probar get_by_index
        self.assertEqual(ll.get_by_index(1), "Libro 1")
        self.assertIsNone(ll.get_by_index(2))  # Fuera de rango
        
        # Probar search
        ll.append("Libro 2")
        node = ll.search("Libro 1")
        self.assertIsNotNone(node)
        self.assertEqual(node.data, "Libro 1")
        self.assertIsNone(ll.search("Libro 3"))  # No existe
        
        # Probar delete
        self.assertTrue(ll.delete("Libro 1"))
        self.assertEqual(ll.size, 2)
        self.assertIsNone(ll.search("Libro 1"))
        
        # Probar display
        self.assertEqual(ll.display(), ["Libro 0", "Libro 2"])
        
        # Probar update
        self.assertTrue(ll.update(1, "Libro 2 - Actualizado"))
        self.assertEqual(ll.get_by_index(1), "Libro 2 - Actualizado")
    
    def test_stack(self):
        """Prueba las operaciones básicas de la Pila."""
        stack = Stack()
        
        # Probar que la pila está vacía inicialmente
        self.assertTrue(stack.is_empty())
        self.assertEqual(stack.size(), 0)
        
        # Probar push
        stack.push("Operación 1")
        self.assertFalse(stack.is_empty())
        self.assertEqual(stack.size(), 1)
        
        # Probar peek
        self.assertEqual(stack.peek(), "Operación 1")
        self.assertEqual(stack.size(), 1)  # El tamaño no cambia con peek
        
        # Probar pop
        stack.push("Operación 2")
        self.assertEqual(stack.pop(), "Operación 2")
        self.assertEqual(stack.size(), 1)
        self.assertEqual(stack.pop(), "Operación 1")
        self.assertTrue(stack.is_empty())
        self.assertIsNone(stack.pop())  # Pop en pila vacía
        
        # Probar display
        stack.push("A")
        stack.push("B")
        stack.push("C")
        self.assertEqual(stack.display(), ["A", "B", "C"])
    
    def test_queue(self):
        """Prueba las operaciones básicas de la Cola."""
        queue = Queue()
        
        # Probar que la cola está vacía inicialmente
        self.assertTrue(queue.is_empty())
        self.assertEqual(queue.size(), 0)
        
        # Probar enqueue
        queue.enqueue("Solicitud 1")
        self.assertFalse(queue.is_empty())
        self.assertEqual(queue.size(), 1)
        
        # Probar front
        self.assertEqual(queue.front(), "Solicitud 1")
        self.assertEqual(queue.size(), 1)  # El tamaño no cambia con front
        
        # Probar dequeue
        queue.enqueue("Solicitud 2")
        self.assertEqual(queue.dequeue(), "Solicitud 1")
        self.assertEqual(queue.size(), 1)
        self.assertEqual(queue.dequeue(), "Solicitud 2")
        self.assertTrue(queue.is_empty())
        self.assertIsNone(queue.dequeue())  # Dequeue en cola vacía
        
        # Probar display
        queue.enqueue("A")
        queue.enqueue("B")
        queue.enqueue("C")
        self.assertEqual(queue.display(), ["A", "B", "C"])

class TestModels(unittest.TestCase):
    """Pruebas para los modelos de datos."""
    
    def test_book_model(self):
        """Prueba el modelo Book."""
        book = Book(
            title="El Quijote",
            author="Miguel de Cervantes",
            genre="Novela",
            isbn="1234567890"
        )
        
        # Probar atributos
        self.assertEqual(book.title, "El Quijote")
        self.assertEqual(book.author, "Miguel de Cervantes")
        self.assertEqual(book.genre, "Novela")
        self.assertEqual(book.isbn, "1234567890")
        self.assertEqual(book.status, "available")
        
        # Probar to_dict
        book_dict = book.to_dict()
        self.assertEqual(book_dict["title"], "El Quijote")
        self.assertEqual(book_dict["status"], "available")
        
        # Probar from_dict
        book2 = Book.from_dict(book_dict)
        self.assertEqual(book2.id, book.id)
        self.assertEqual(book2.title, book.title)
        self.assertEqual(book2.status, book.status)
    
    def test_user_model(self):
        """Prueba el modelo User."""
        user = User(name="John Doe", email="john@example.com")
        
        # Probar atributos
        self.assertEqual(user.name, "John Doe")
        self.assertEqual(user.email, "john@example.com")
        self.assertEqual(len(user.borrowed_books), 0)
        self.assertEqual(len(user.loan_history), 0)
        
        # Probar to_dict
        user_dict = user.to_dict()
        self.assertEqual(user_dict["name"], "John Doe")
        self.assertEqual(user_dict["email"], "john@example.com")
        
        # Probar from_dict
        user2 = User.from_dict(user_dict)
        self.assertEqual(user2.id, user.id)
        self.assertEqual(user2.name, user.name)
        self.assertEqual(user2.email, user.email)
    
    def test_loan_model(self):
        """Prueba el modelo Loan."""
        loan = Loan(book_id="book123", user_id="user456")
        
        # Probar atributos
        self.assertEqual(loan.book_id, "book123")
        self.assertEqual(loan.user_id, "user456")
        self.assertIsNotNone(loan.loan_date)
        self.assertIsNotNone(loan.due_date)
        self.assertIsNone(loan.return_date)
        self.assertEqual(loan.status, "active")
        
        # Probar to_dict
        loan_dict = loan.to_dict()
        self.assertEqual(loan_dict["book_id"], "book123")
        self.assertEqual(loan_dict["user_id"], "user456")
        self.assertEqual(loan_dict["status"], "active")
        
        # Probar from_dict
        loan2 = Loan.from_dict(loan_dict)
        self.assertEqual(loan2.id, loan.id)
        self.assertEqual(loan2.book_id, loan.book_id)
        self.assertEqual(loan2.status, loan.status)

class TestManagers(unittest.TestCase):
    """Pruebas para los gestores de datos."""
    
    def setUp(self):
        """Preparar el entorno para las pruebas."""
        # Eliminar archivos JSON de pruebas anteriores
        if os.path.exists("books_test.json"):
            os.remove("books_test.json")
        if os.path.exists("users_test.json"):
            os.remove("users_test.json")
        if os.path.exists("loans_test.json"):
            os.remove("loans_test.json")
        if os.path.exists("operations_history_test.json"):
            os.remove("operations_history_test.json")
        if os.path.exists("loan_requests_test.json"):
            os.remove("loan_requests_test.json")
    
    def test_book_manager(self):
        """Prueba el gestor de libros."""
        # Modificar el método save_data para usar archivos de prueba
        original_save = BookManager.save_data
        original_load = BookManager.load_data
        
        def mock_save_data(self):
            books_data = []
            current = self.books.head
            while current:
                books_data.append(current.data.to_dict())
                current = current.next
            
            with open("books_test.json", "w") as file:
                json.dump(books_data, file, indent=4)
        
        def mock_load_data(self):
            try:
                with open("books_test.json", "r") as file:
                    books_data = json.load(file)
                    
                    for book_data in books_data:
                        book = Book.from_dict(book_data)
                        self.books.append(book)
            except (FileNotFoundError, json.JSONDecodeError):
                with open("books_test.json", "w") as file:
                    json.dump([], file)
        
        BookManager.save_data = mock_save_data
        BookManager.load_data = mock_load_data
        
        # Crear una instancia del gestor
        book_manager = BookManager()
        
        # Probar add_book
        book1 = Book(
            title="Libro 1",
            author="Autor 1",
            genre="Género 1",
            isbn="1111111111"
        )
        self.assertTrue(book_manager.add_book(book1))
        self.assertEqual(book_manager.books.size, 1)
        
        # Probar get_book_by_id
        book_id = book1.id
        retrieved_book = book_manager.get_book_by_id(book_id)
        self.assertEqual(retrieved_book.title, "Libro 1")
        
        # Probar update_book
        updated_data = {"title": "Libro 1 - Actualizado"}
        self.assertTrue(book_manager.update_book(book_id, updated_data))
        updated_book = book_manager.get_book_by_id(book_id)
        self.assertEqual(updated_book.title, "Libro 1 - Actualizado")
        
        # Probar search_books
        book2 = Book(
            title="Otro libro",
            author="Otro autor",
            genre="Otro género",
            isbn="2222222222"
        )
        book_manager.add_book(book2)
        
        results = book_manager.search_books({"title": "Actualizado"})
        self.assertEqual(results.size, 1)
        self.assertEqual(results.head.data.title, "Libro 1 - Actualizado")
        
        # Probar delete_book
        self.assertTrue(book_manager.delete_book(book_id))
        self.assertEqual(book_manager.books.size, 1)
        self.assertIsNone(book_manager.get_book_by_id(book_id))
        
        # Restaurar los métodos originales
        BookManager.save_data = original_save
        BookManager.load_data = original_load
    
    def test_user_manager(self):
        """Prueba el gestor de usuarios."""
        # Modificar el método save_data para usar archivos de prueba
        original_save = UserManager.save_data
        original_load = UserManager.load_data
        
        def mock_save_data(self):
            users_data = []
            current = self.users.head
            while current:
                users_data.append(current.data.to_dict())
                current = current.next
            
            with open("users_test.json", "w") as file:
                json.dump(users_data, file, indent=4)
        
        def mock_load_data(self):
            try:
                with open("users_test.json", "r") as file:
                    users_data = json.load(file)
                    
                    for user_data in users_data:
                        user = User.from_dict(user_data)
                        self.users.append(user)
            except (FileNotFoundError, json.JSONDecodeError):
                with open("users_test.json", "w") as file:
                    json.dump([], file)
        
        UserManager.save_data = mock_save_data
        UserManager.load_data = mock_load_data
        
        # Crear una instancia del gestor
        user_manager = UserManager()
        
        # Probar add_user
        user1 = User(name="Usuario 1", email="user1@example.com")
        self.assertTrue(user_manager.add_user(user1))
        self.assertEqual(user_manager.users.size, 1)
        
        # Probar get_user_by_id
        user_id = user1.id
        retrieved_user = user_manager.get_user_by_id(user_id)
        self.assertEqual(retrieved_user.name, "Usuario 1")
        
        # Probar update_user
        updated_data = {"name": "Usuario 1 - Actualizado"}
        self.assertTrue(user_manager.update_user(user_id, updated_data))
        updated_user = user_manager.get_user_by_id(user_id)
        self.assertEqual(updated_user.name, "Usuario 1 - Actualizado")
        
        # Probar search_users
        user2 = User(name="Otro usuario", email="user2@example.com")
        user_manager.add_user(user2)
        
        results = user_manager.search_users({"name": "Actualizado"})
        self.assertEqual(results.size, 1)
        self.assertEqual(results.head.data.name, "Usuario 1 - Actualizado")
        
        # Probar delete_user
        self.assertTrue(user_manager.delete_user(user_id))
        self.assertEqual(user_manager.users.size, 1)
        self.assertIsNone(user_manager.get_user_by_id(user_id))
        
        # Restaurar los métodos originales
        UserManager.save_data = original_save
        UserManager.load_data = original_load
    
    def test_loan_manager(self):
        """Prueba el gestor de préstamos."""
        # Modificar los métodos para usar archivos de prueba
        original_loan_save = LoanManager.save_data
        original_loan_load = LoanManager.load_data
        original_book_save = BookManager.save_data
        original_book_load = BookManager.load_data
        original_user_save = UserManager.save_data
        original_user_load = UserManager.load_data
        
        def mock_loan_save_data(self):
            loans_data = []
            current = self.loans.head
            while current:
                loans_data.append(current.data.to_dict())
                current = current.next
            
            with open("loans_test.json", "w") as file:
                json.dump(loans_data, file, indent=4)
            
            # Guardar historial de operaciones
            operations_data = self.operations_history.display()
            with open("operations_history_test.json", "w") as file:
                json.dump(operations_data, file, indent=4)
            
            # Guardar solicitudes pendientes
            requests_data = self.loan_requests.display()
            with open("loan_requests_test.json", "w") as file:
                json.dump(requests_data, file, indent=4)
        
        def mock_loan_load_data(self):
            try:
                with open("loans_test.json", "r") as file:
                    loans_data = json.load(file)
                    
                    for loan_data in loans_data:
                        loan = Loan.from_dict(loan_data)
                        self.loans.append(loan)
            except (FileNotFoundError, json.JSONDecodeError):
                with open("loans_test.json", "w") as file:
                    json.dump([], file)
            
            try:
                with open("operations_history_test.json", "r") as file:
                    operations_data = json.load(file)
                    
                    for operation in operations_data:
                        self.operations_history.push(operation)
            except (FileNotFoundError, json.JSONDecodeError):
                with open("operations_history_test.json", "w") as file:
                    json.dump([], file)
            
            try:
                with open("loan_requests_test.json", "r") as file:
                    requests_data = json.load(file)
                    
                    for request in requests_data:
                        self.loan_requests.enqueue(request)
            except (FileNotFoundError, json.JSONDecodeError):
                with open("loan_requests_test.json", "w") as file:
                    json.dump([], file)
        
        def mock_book_save_data(self):
            books_data = []
            current = self.books.head
            while current:
                books_data.append(current.data.to_dict())
                current = current.next
            
            with open("books_test.json", "w") as file:
                json.dump(books_data, file, indent=4)
        
        def mock_book_load_data(self):
            try:
                with open("books_test.json", "r") as file:
                    books_data = json.load(file)
                    
                    for book_data in books_data:
                        book = Book.from_dict(book_data)
                        self.books.append(book)
            except (FileNotFoundError, json.JSONDecodeError):
                with open("books_test.json", "w") as file:
                    json.dump([], file)
        
        def mock_user_save_data(self):
            users_data = []
            current = self.users.head
            while current:
                users_data.append(current.data.to_dict())
                current = current.next
            
            with open("users_test.json", "w") as file:
                json.dump(users_data, file, indent=4)
        
        def mock_user_load_data(self):
            try:
                with open("users_test.json", "r") as file:
                    users_data = json.load(file)
                    
                    for user_data in users_data:
                        user = User.from_dict(user_data)
                        self.users.append(user)
            except (FileNotFoundError, json.JSONDecodeError):
                with open("users_test.json", "w") as file:
                    json.dump([], file)
        
        # Aplicar los mocks
        LoanManager.save_data = mock_loan_save_data
        LoanManager.load_data = mock_loan_load_data
        BookManager.save_data = mock_book_save_data
        BookManager.load_data = mock_book_load_data
        UserManager.save_data = mock_user_save_data
        UserManager.load_data = mock_user_load_data
        
        # Crear las instancias de los gestores
        book_manager = BookManager()
        user_manager = UserManager()
        loan_manager = LoanManager(book_manager, user_manager)
        
        # Crear datos de prueba
        book = Book(
            title="Libro de Prueba",
            author="Autor de Prueba",
            genre="Género de Prueba",
            isbn="9999999999"
        )
        book_manager.add_book(book)
        
        user = User(name="Usuario de Prueba", email="test@example.com")
        user_manager.add_user(user)
        
        # Probar create_loan
        self.assertTrue(loan_manager.create_loan(book.id, user.id))
        active_loans = loan_manager.get_active_loans()
        self.assertEqual(len(active_loans), 1)
        
        # Verificar que el estado del libro se actualizó
        book = book_manager.get_book_by_id(book.id)
        self.assertEqual(book.status, "borrowed")
        
        # Verificar que el préstamo se agregó al usuario
        user = user_manager.get_user_by_id(user.id)
        self.assertIn(book.id, user.borrowed_books)
        
        # Probar return_book
        loan_id = active_loans[0].id
        self.assertTrue(loan_manager.return_book(loan_id))
        
        # Verificar que el estado del libro se actualizó
        book = book_manager.get_book_by_id(book.id)
        self.assertEqual(book.status, "available")
        
        # Verificar que el préstamo se eliminó del usuario
        user = user_manager.get_user_by_id(user.id)
        self.assertNotIn(book.id, user.borrowed_books)
        self.assertIn(loan_id, user.loan_history)
        
        # Probar request_loan
        self.assertTrue(loan_manager.request_loan(book.id, user.id))
        self.assertEqual(len(loan_manager.get_pending_requests()), 1)
        
        # Probar process_loan_requests
        loan_manager.process_loan_requests()
        self.assertEqual(len(loan_manager.get_pending_requests()), 0)
        self.assertEqual(len(loan_manager.get_active_loans()), 1)
        
        # Restaurar los métodos originales
        LoanManager.save_data = original_loan_save
        LoanManager.load_data = original_loan_load
        BookManager.save_data = original_book_save
        BookManager.load_data = original_book_load
        UserManager.save_data = original_user_save
        UserManager.load_data = original_user_load

# Ejecución de las pruebas
if __name__ == "__main__":
    unittest.main()