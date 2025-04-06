# Documentación del Sistema de Gestión de Biblioteca (MVP)

## 1. Introducción

Este documento detalla el diseño, la implementación y las pruebas del Producto Mínimo Viable (MVP) de un Sistema de Gestión de Biblioteca. El sistema permite administrar libros, usuarios y préstamos a través de una interfaz gráfica intuitiva, utilizando estructuras de datos lineales para el almacenamiento eficiente de la información.

### 1.1 Objetivo

Desarrollar un prototipo funcional de un sistema de gestión de biblioteca que demuestre la implementación efectiva de estructuras de datos lineales, con una interfaz de usuario intuitiva y operaciones funcionales para la gestión de libros y usuarios.

### 1.2 Alcance

El MVP incluye:
- Gestión completa de libros (agregar, editar, eliminar, buscar)
- Gestión de usuarios (agregar, editar, eliminar, buscar)
- Gestión de préstamos (crear, devolver, historial)
- Implementación de estructuras de datos lineales (listas enlazadas, pilas, colas)
- Interfaz gráfica intuitiva
- Almacenamiento persistente de datos
- Pruebas unitarias exhaustivas

## 2. Arquitectura del Sistema

### 2.1 Visión General

El sistema sigue una arquitectura en capas:

1. **Capa de Estructuras de Datos**: Implementaciones base de las estructuras lineales.
2. **Capa de Modelos**: Definiciones de las entidades principales (libros, usuarios, préstamos).
3. **Capa de Lógica de Negocio**: Gestores que manejan las operaciones sobre los modelos.
4. **Capa de Persistencia**: Funcionalidad para guardar y cargar datos.
5. **Capa de Interfaz de Usuario**: UI desarrollada con Streamlit.

### 2.2 Diagrama de Componentes

```
┌─────────────────────────────────────────────────────┐
│                                                     │
│                  Interfaz de Usuario                 │
│               (Streamlit Application)               │
│                                                     │
└───────────────────────┬─────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────┐
│                                                     │
│                  Lógica de Negocio                  │
│      (BookManager, UserManager, LoanManager)        │
│                                                     │
└───────────────────────┬─────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────┐
│                                                     │
│                       Modelos                       │
│             (Book, User, Loan Classes)              │
│                                                     │
└───────────────────────┬─────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────┐
│                                                     │
│                Estructuras de Datos                 │
│           (LinkedList, Stack, Queue)                │
│                                                     │
└───────────────────────┬─────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────┐
│                                                     │
│                    Persistencia                     │
│        (Archivos JSON para almacenamiento)          │
│                                                     │
└─────────────────────────────────────────────────────┘
```

## 3. Estructuras de Datos Implementadas

### 3.1 Lista Enlazada (LinkedList)

La Lista Enlazada es la estructura principal utilizada para almacenar colecciones de libros, usuarios y préstamos. Se eligió esta estructura por:

- **Eficiencia en inserciones y eliminaciones**: Operaciones de O(1) cuando se conoce la posición.
- **Crecimiento dinámico**: No requiere reasignación de memoria como los arreglos.
- **Facilidad para implementar operaciones específicas**: Búsquedas por atributos, filtrado, etc.

#### Operaciones Implementadas:
- `append(data)`: Agrega un elemento al final - O(n)
- `prepend(data)`: Agrega un elemento al inicio - O(1)
- `delete(key)`: Elimina un elemento por valor - O(n)
- `search(key)`: Busca un elemento por valor - O(n)
- `search_by_attribute(attr_name, attr_value)`: Búsqueda por atributo - O(n)
- `get_by_index(index)`: Obtiene un elemento por índice - O(n)
- `update(index, data)`: Actualiza un elemento por índice - O(n)
- `display()`: Muestra todos los elementos - O(n)

### 3.2 Pila (Stack)

La estructura de Pila se utiliza para mantener un historial de operaciones en el sistema, permitiendo el seguimiento de acciones en orden cronológico inverso (la última acción es la primera en consultarse).

#### Operaciones Implementadas:
- `push(item)`: Añade un elemento a la pila - O(1)
- `pop()`: Elimina y devuelve el elemento superior - O(1)
- `peek()`: Devuelve el elemento superior sin eliminarlo - O(1)
- `is_empty()`: Verifica si la pila está vacía - O(1)
- `size()`: Devuelve el tamaño de la pila - O(1)
- `display()`: Muestra todos los elementos - O(n)

### 3.3 Cola (Queue)

La estructura de Cola se utiliza para gestionar las solicitudes de préstamo pendientes, garantizando que se procesen en el orden de llegada (FIFO - First In, First Out).

#### Operaciones Implementadas:
- `enqueue(item)`: Añade un elemento al final de la cola - O(1)
- `dequeue()`: Elimina y devuelve el primer elemento - O(1)
- `front()`: Devuelve el primer elemento sin eliminarlo - O(1)
- `is_empty()`: Verifica si la cola está vacía - O(1)
- `size()`: Devuelve el tamaño de la cola - O(1)
- `display()`: Muestra todos los elementos - O(n)

## 4. Modelos de Datos

### 4.1 Libro (Book)

Representa un libro en el sistema, con atributos como título, autor, género, estado, etc.

#### Atributos:
- `id`: Identificador único (UUID)
- `title`: Título del libro
- `author`: Autor del libro
- `genre`: Género literario
- `isbn`: Código ISBN
- `status`: Estado del libro (disponible, prestado, reservado)
- `publication_date`: Fecha de publicación

### 4.2 Usuario (User)

Representa un usuario de la biblioteca, con información personal y su historial de préstamos.

#### Atributos:
- `id`: Identificador único (UUID)
- `name`: Nombre del usuario
- `email`: Correo electrónico
- `borrowed_books`: Lista de IDs de libros actualmente prestados
- `loan_history`: Historial de préstamos realizados

### 4.3 Préstamo (Loan)

Representa un préstamo de un libro a un usuario, con fechas y estado.

#### Atributos:
- `id`: Identificador único (UUID)
- `book_id`: ID del libro prestado
- `user_id`: ID del usuario que realiza el préstamo
- `loan_date`: Fecha de préstamo
- `due_date`: Fecha de devolución prevista
- `return_date`: Fecha de devolución real (null si no devuelto)
- `status`: Estado del préstamo (activo, devuelto)

## 5. Gestores (Managers)

Los gestores implementan la lógica de negocio del sistema, utilizando las estructuras de datos para almacenar y manipular los modelos.

### 5.1 Gestor de Libros (BookManager)

Administra la colección de libros utilizando una Lista Enlazada.

#### Funcionalidades:
- Agregar, editar y eliminar libros
- Buscar libros por diversos criterios
- Gestionar el estado de los libros (disponible, prestado, etc.)
- Persistencia de datos en formato JSON

### 5.2 Gestor de Usuarios (UserManager)

Administra los usuarios del sistema utilizando una Lista Enlazada.

#### Funcionalidades:
- Agregar, editar y eliminar usuarios
- Buscar usuarios por nombre o email
- Gestionar los préstamos activos e historial
- Persistencia de datos en formato JSON

### 5.3 Gestor de Préstamos (LoanManager)

Administra los préstamos y devoluciones utilizando una Lista Enlazada para los préstamos activos, una Pila para el historial y una Cola para las solicitudes pendientes.

#### Funcionalidades:
- Crear préstamos inmediatos o por solicitud
- Procesar devoluciones
- Manejar el historial de operaciones
- Gestionar la cola de solicitudes pendientes
- Persistencia de datos en formato JSON

## 6. Interfaz de Usuario

La interfaz de usuario se ha implementado utilizando Streamlit, una biblioteca de Python para crear aplicaciones web interactivas.

### 6.1 Páginas Principales

- **Inicio**: Dashboard con métricas y resúmenes
- **Gestión de Libros**: CRUD de libros
- **Gestión de Usuarios**: CRUD de usuarios
- **Gestión de Préstamos**: Crear y gestionar préstamos
- **Acerca del Sistema**: Información sobre el sistema

### 6.2 Características de la UI

- Diseño responsivo
- Navegación intuitiva mediante barra lateral
- Utilización de pestañas para organizar funcionalidades
- Formularios para entrada de datos
- Tablas para visualización de información
- Mensajes de feedback al usuario
- Estilos personalizados para mejorar la experiencia

## 7. Persistencia de Datos

El sistema utiliza archivos JSON para almacenar los datos de forma persistente.

### 7.1 Archivos Utilizados

- `books.json`: Almacena la información de libros
- `users.json`: Almacena la información de usuarios
- `loans.json`: Almacena los préstamos activos e históricos
- `operations_history.json`: Guarda el historial de operaciones
- `loan_requests.json`: Almacena las solicitudes pendientes

### 7.2 Estrategia de Persistencia

Cada gestor implementa métodos `save_data()` y `load_data()` que:
1. Convierten los objetos a/desde diccionarios JSON
2. Guardan/Cargan los datos en/desde archivos
3. Manejan errores en caso de archivos no existentes o corruptos

## 8. Pruebas Unitarias

Se han implementado pruebas unitarias exhaustivas para garantizar el correcto funcionamiento de todos los componentes del sistema.

### 8.1 Pruebas de Estructuras de Datos

Verifican que las operaciones de las estructuras (Lista Enlazada, Pila, Cola) funcionan correctamente:
- Inserción y eliminación de elementos
- Búsqueda y recuperación
- Manejo de casos límite (estructuras vacías, índices fuera de rango)

### 8.2 Pruebas de Modelos

Verifican la correcta creación y manipulación de los modelos:
- Inicialización con valores correctos
- Conversión a/desde diccionarios
- Consistencia de atributos

### 8.3 Pruebas de Gestores

Verifican la lógica de negocio de los gestores:
- Operaciones CRUD en libros, usuarios y préstamos
- Búsquedas y filtrados
- Manejo de relaciones entre entidades
- Persistencia y recuperación de datos

## 9. Decisiones de Diseño

### 9.1 Elección de Estructuras de Datos

- **Lista Enlazada vs. Array**: Se eligió Lista Enlazada por su flexibilidad para insertar y eliminar elementos sin reordenar toda la estructura.
- **Pila para Historial**: La naturaleza LIFO de las pilas es perfecta para registrar y consultar el historial de operaciones.
- **Cola para Solicitudes**: La naturaleza FIFO de las colas garantiza equidad en el procesamiento de solicitudes.

### 9.2 Arquitectura de Persistencia

- **Archivos JSON vs. Base de Datos**: Para un MVP, los archivos JSON ofrecen simplicidad y facilidad de implementación sin dependencias externas.
- **Archivos Separados por Entidad**: Mejora el rendimiento y facilita la depuración al separar los datos por tipo.

### 9.3 Interfaz de Usuario

- **Streamlit vs. Otras Alternativas**: Streamlit ofrece un desarrollo rápido de UI interactivas con Python puro, ideal para un MVP.
- **Organización por Pestañas**: Mejora la usabilidad al agrupar funcionalidades relacionadas.
- **Validaciones Client-Side**: Reducen errores y mejoran la experiencia del usuario.

## 10. Limitaciones y Mejoras Futuras

### 10.1 Limitaciones Actuales

- **Escalabilidad**: Las estructuras de datos implementadas pueden tener limitaciones de rendimiento con grandes volúmenes de datos.
- **Concurrencia**: El sistema no maneja múltiples usuarios concurrentes de forma robusta.
- **Búsquedas Avanzadas**: No se implementaron algoritmos de búsqueda más eficientes o indexación.

### 10.2 Mejoras Propuestas

- **Base de Datos Relacional**: Migrar a una base de datos para mejorar rendimiento y escalabilidad.
- **Autenticación y Seguridad**: Implementar login, permisos y cifrado de datos sensibles.
- **Búsqueda Avanzada**: Incorporar algoritmos más eficientes (árboles, hashing) para búsquedas.
- **API REST**: Exponer funcionalidades mediante API para integración con otros sistemas.
- **Notificaciones**: Sistema de alertas para vencimientos de préstamos.
- **Reportes y Estadísticas**: Ampliar las capacidades analíticas del sistema.

## 11. Conclusiones

El MVP del Sistema de Gestión de Biblioteca demuestra la implementación efectiva de estructuras de datos lineales en un contexto práctico. Las estructuras elegidas (Lista Enlazada, Pila, Cola) proporcionan la funcionalidad necesaria para gestionar libros, usuarios y préstamos de manera eficiente.

La arquitectura de capas facilita la separación de responsabilidades y permite la evolución del sistema. La interfaz de usuario desarrollada con Streamlit ofrece una experiencia intuitiva y accesible, mientras que las pruebas unitarias garantizan la robustez del sistema.

El proyecto cumple con los requisitos especificados para un MVP, proporcionando una base sólida para desarrollos futuros y mejoras en funcionalidad, rendimiento y escalabilidad.

## 12. Instrucciones de Ejecución

### 12.1 Requisitos

- Python 3.7 o superior
- Bibliotecas: streamlit, pandas

### 12.2 Instalación

```bash
pip install streamlit pandas
```

### 12.3 Ejecución

1. Clonar el repositorio o descargar los archivos del proyecto
2. Navegar al directorio del proyecto
3. Ejecutar el siguiente comando:

```bash
streamlit run app.py
```

### 12.4 Ejecución de Pruebas

```bash
python tests.py
```

## 13. Referencias

- Estructuras de Datos y Algoritmos:
  - Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2009). *Introduction to Algorithms* (3rd ed.). MIT Press.
  - Goodrich, M. T., Tamassia, R., & Goldwasser, M. H. (2014). *Data Structures and Algorithms in Python*. Wiley.

- Desarrollo con Python y Streamlit:
  - Documentation: [Streamlit.io](https://docs.streamlit.io/)
  - Pandas: [pandas.pydata.org](https://pandas.pydata.org/docs/)
