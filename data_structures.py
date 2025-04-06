# data_structures.py
# Implementación de estructuras de datos lineales para el sistema de biblioteca

class Node:
    """
    Clase Nodo para Lista Enlazada.
    Cada nodo contiene un valor y una referencia al siguiente nodo.
    """
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    """
    Implementación de Lista Enlazada para almacenar colecciones de elementos.
    Permite operaciones como inserción, eliminación y búsqueda.
    """
    def __init__(self):
        self.head = None
        self._size = 0
    
    def is_empty(self):
        """Verifica si la lista está vacía."""
        return self.head is None
    
    def append(self, data):
        """Agrega un elemento al final de la lista."""
        new_node = Node(data)
        if self.is_empty():
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node
        self._size += 1
    
    def prepend(self, data):
        """Agrega un elemento al inicio de la lista."""
        new_node = Node(data)
        if not self.is_empty():
            new_node.next = self.head
        self.head = new_node
        self._size += 1
    
    def delete(self, key):
        """Elimina un elemento por valor."""
        current = self.head
        previous = None
        
        # Si la lista está vacía
        if not current:
            return False
        
        # Si el elemento a eliminar es el primero
        if current.data == key:
            self.head = current.next
            self._size -= 1
            return True
        
        # Buscar el elemento en el resto de la lista
        while current and current.data != key:
            previous = current
            current = current.next
        
        # Si el elemento no se encuentra
        if not current:
            return False
        
        # Eliminar el elemento
        previous.next = current.next
        self._size -= 1
        return True
    
    def search(self, key):
        """Busca un elemento por valor y devuelve el nodo si se encuentra."""
        current = self.head
        while current:
            if current.data == key:
                return current
            current = current.next
        return None
    
    def search_by_attribute(self, attr_name, attr_value):
        """Busca elementos que tienen un atributo con el valor especificado."""
        results = LinkedList()
        current = self.head
        
        while current:
            if hasattr(current.data, attr_name):
                current_value = getattr(current.data, attr_name)
                # Si el valor del atributo contiene el valor buscado
                if isinstance(current_value, str) and isinstance(attr_value, str):
                    if attr_value.lower() in current_value.lower():
                        results.append(current.data)
                # Si el valor del atributo es igual al valor buscado
                elif current_value == attr_value:
                    results.append(current.data)
            current = current.next
        
        return results
    
    def get_by_index(self, index):
        """Obtiene un elemento por su índice (0-based)."""
        if index < 0 or index >= self._size:
            return None
        
        current = self.head
        for _ in range(index):
            current = current.next
        return current.data
    
    def update(self, index, data):
        """Actualiza el valor de un elemento por su índice."""
        if index < 0 or index >= self._size:
            return False
        
        current = self.head
        for _ in range(index):
            current = current.next
        current.data = data
        return True
    
    def display(self):
        """Muestra todos los elementos de la lista."""
        elements = []
        current = self.head
        while current:
            elements.append(current.data)
            current = current.next
        return elements
    
    @property
    def size(self):
        """Devuelve el tamaño de la lista."""
        return self._size

class Stack:
    """
    Implementación de una Pila (LIFO - Last In, First Out).
    Útil para seguimiento de operaciones recientes e historial.
    """
    def __init__(self):
        self.items = []
    
    def is_empty(self):
        """Verifica si la pila está vacía."""
        return len(self.items) == 0
    
    def push(self, item):
        """Agrega un elemento a la pila."""
        self.items.append(item)
    
    def pop(self):
        """Elimina y devuelve el elemento superior de la pila."""
        if self.is_empty():
            return None
        return self.items.pop()
    
    def peek(self):
        """Devuelve el elemento superior sin eliminarlo."""
        if self.is_empty():
            return None
        return self.items[-1]
    
    def size(self):
        """Devuelve el tamaño de la pila."""
        return len(self.items)
    
    def display(self):
        """Muestra todos los elementos de la pila."""
        return self.items.copy()

class Queue:
    """
    Implementación de una Cola (FIFO - First In, First Out).
    Útil para gestionar solicitudes en orden de llegada.
    """
    def __init__(self):
        self.items = []
    
    def is_empty(self):
        """Verifica si la cola está vacía."""
        return len(self.items) == 0
    
    def enqueue(self, item):
        """Agrega un elemento al final de la cola."""
        self.items.append(item)
    
    def dequeue(self):
        """Elimina y devuelve el primer elemento de la cola."""
        if self.is_empty():
            return None
        return self.items.pop(0)
    
    def front(self):
        """Devuelve el primer elemento sin eliminarlo."""
        if self.is_empty():
            return None
        return self.items[0]
    
    def size(self):
        """Devuelve el tamaño de la cola."""
        return len(self.items)
    
    def display(self):
        """Muestra todos los elementos de la cola."""
        return self.items.copy()