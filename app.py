# app.py
# Interfaz de usuario principal del sistema de gestión de biblioteca

import streamlit as st
import pandas as pd
from datetime import datetime
from managers import BookManager, UserManager, LoanManager
from models import Book, User

# Configuración de la página
st.set_page_config(
    page_title="Sistema de Gestión de Biblioteca",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inicializar sesiones de estado si no existen
if 'book_manager' not in st.session_state:
    st.session_state.book_manager = BookManager()
if 'user_manager' not in st.session_state:
    st.session_state.user_manager = UserManager()
if 'loan_manager' not in st.session_state:
    st.session_state.loan_manager = LoanManager(
        st.session_state.book_manager, 
        st.session_state.user_manager
    )

# Función para obtener los managers
def get_managers():
    return (
        st.session_state.book_manager,
        st.session_state.user_manager,
        st.session_state.loan_manager
    )

# Estilos CSS personalizados
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 1rem;
    }
    .section-header {
        font-size: 1.8rem;
        color: #2563EB;
        margin-top: 1rem;
        margin-bottom: 1rem;
    }
    .card {
        background-color: #F8FAFC;
        padding: 1.5rem;
        border-radius: 0.5rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #EFF6FF;
        padding: 1rem;
        border-radius: 0.5rem;
        text-align: center;
        box-shadow: 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    }
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: #1E40AF;
    }
    .metric-label {
        font-size: 1rem;
        color: #4B5563;
    }
    .sidebar-header {
        font-size: 1.5rem;
        color: #1E3A8A;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Funciones auxiliares
def display_books_table(books):
    """Muestra una tabla con los libros."""
    if not books:
        st.info("No hay libros para mostrar.")
        return
    
    # Convertir la lista de libros a un DataFrame
    books_data = []
    for book in books:
        books_data.append({
            "ID": book.id,
            "Título": book.title,
            "Autor": book.author,
            "Género": book.genre,
            "ISBN": book.isbn,
            "Estado": book.status,
            "Fecha de Publicación": book.publication_date
        })
    
    df = pd.DataFrame(books_data)
    st.dataframe(df, use_container_width=True)

def display_users_table(users):
    """Muestra una tabla con los usuarios."""
    if not users:
        st.info("No hay usuarios para mostrar.")
        return
    
    # Convertir la lista de usuarios a un DataFrame
    users_data = []
    for user in users:
        users_data.append({
            "ID": user.id,
            "Nombre": user.name,
            "Email": user.email,
            "Libros Prestados": len(user.borrowed_books),
            "Historial de Préstamos": len(user.loan_history)
        })
    
    df = pd.DataFrame(users_data)
    st.dataframe(df, use_container_width=True)

def display_loans_table(loans):
    """Muestra una tabla con los préstamos."""
    if not loans:
        st.info("No hay préstamos para mostrar.")
        return
    
    book_manager, user_manager, _ = get_managers()
    
    # Convertir la lista de préstamos a un DataFrame
    loans_data = []
    for loan in loans:
        book = book_manager.get_book_by_id(loan.book_id)
        user = user_manager.get_user_by_id(loan.user_id)
        
        book_title = book.title if book else "Desconocido"
        user_name = user.name if user else "Desconocido"
        
        loans_data.append({
            "ID": loan.id,
            "Libro": book_title,
            "Usuario": user_name,
            "Fecha de Préstamo": loan.loan_date,
            "Fecha de Devolución Prevista": loan.due_date,
            "Fecha de Devolución Real": loan.return_date or "Pendiente",
            "Estado": loan.status
        })
    
    df = pd.DataFrame(loans_data)
    st.dataframe(df, use_container_width=True)

def home_page():
    """Página de inicio con estadísticas y resumen del sistema."""
    st.markdown('<h1 class="main-header">Sistema de Gestión de Biblioteca</h1>', unsafe_allow_html=True)
    
    book_manager, user_manager, loan_manager = get_managers()
    
    # Métricas principales
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">{book_manager.books.size}</div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-label">Libros Totales</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        available_books = len([book for book in book_manager.get_all_books() if book.status == "available"])
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">{available_books}</div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-label">Libros Disponibles</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">{user_manager.users.size}</div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-label">Usuarios Registrados</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        active_loans = len(loan_manager.get_active_loans())
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">{active_loans}</div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-label">Préstamos Activos</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Libros recientemente añadidos
    st.markdown('<h2 class="section-header">Libros Recientemente Añadidos</h2>', unsafe_allow_html=True)
    recent_books = book_manager.get_all_books()
    recent_books = recent_books[-5:] if len(recent_books) > 5 else recent_books
    display_books_table(recent_books)
    
    # Préstamos activos
    st.markdown('<h2 class="section-header">Préstamos Activos</h2>', unsafe_allow_html=True)
    active_loans = loan_manager.get_active_loans()
    display_loans_table(active_loans[:5] if len(active_loans) > 5 else active_loans)

def books_page():
    """Página para la gestión de libros."""
    st.markdown('<h1 class="section-header">Gestión de Libros</h1>', unsafe_allow_html=True)
    
    book_manager, _, _ = get_managers()
    
    # Crear pestañas para las diferentes operaciones
    tabs = st.tabs(["Ver Libros", "Agregar Libro", "Buscar Libros", "Editar/Eliminar"])
    
    # Tab 1: Ver todos los libros
    with tabs[0]:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### Todos los Libros")
        display_books_table(book_manager.get_all_books())
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Tab 2: Agregar un nuevo libro
    with tabs[1]:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### Agregar Nuevo Libro")
        
        with st.form("add_book_form"):
            title = st.text_input("Título", key="title")
            author = st.text_input("Autor", key="author")
            genre = st.text_input("Género", key="genre")
            isbn = st.text_input("ISBN", key="isbn")
            publication_date = st.date_input("Fecha de Publicación", datetime.now())
            
            submit_button = st.form_submit_button("Agregar Libro")
            
            if submit_button:
                if title and author and genre and isbn:
                    new_book = Book(
                        title=title,
                        author=author,
                        genre=genre,
                        isbn=isbn,
                        publication_date=publication_date.strftime("%Y-%m-%d")
                    )
                    if book_manager.add_book(new_book):
                        st.success(f"Libro '{title}' agregado correctamente.")
                else:
                    st.error("Todos los campos son obligatorios.")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Tab 3: Buscar libros
    with tabs[2]:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### Buscar Libros")
        
        col1, col2 = st.columns(2)
        with col1:
            search_type = st.selectbox(
                "Buscar por",
                ["Título", "Autor", "Género", "ISBN", "Estado"]
            )
        
        with col2:
            search_term = st.text_input("Término de búsqueda")
        
        if st.button("Buscar"):
            if search_term:
                criteria = {}
                key_map = {
                    "Título": "title",
                    "Autor": "author",
                    "Género": "genre",
                    "ISBN": "isbn",
                    "Estado": "status"
                }
                criteria[key_map[search_type]] = search_term
                
                results = book_manager.search_books(criteria)
                if results.size > 0:
                    st.success(f"Se encontraron {results.size} resultados.")
                    display_books_table(results.display())
                else:
                    st.info("No se encontraron resultados.")
            else:
                st.error("Por favor, ingresa un término de búsqueda.")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Tab 4: Editar/Eliminar libros
    with tabs[3]:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### Editar o Eliminar Libro")
        
        # Obtener todos los libros para seleccionar
        books = book_manager.get_all_books()
        book_options = {f"{book.title} ({book.id})": book.id for book in books}
        
        if book_options:
            selected_book_name = st.selectbox(
                "Selecciona un libro",
                options=list(book_options.keys())
            )
            
            selected_book_id = book_options[selected_book_name]
            selected_book = book_manager.get_book_by_id(selected_book_id)
            
            if selected_book:
                with st.form("edit_book_form"):
                    title = st.text_input("Título", value=selected_book.title)
                    author = st.text_input("Autor", value=selected_book.author)
                    genre = st.text_input("Género", value=selected_book.genre)
                    isbn = st.text_input("ISBN", value=selected_book.isbn)
                    status = st.selectbox(
                        "Estado",
                        options=["available", "borrowed", "reserved"],
                        index=["available", "borrowed", "reserved"].index(selected_book.status)
                    )
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        update_button = st.form_submit_button("Actualizar Libro")
                    
                    with col2:
                        delete_button = st.form_submit_button("Eliminar Libro")
                    
                    if update_button:
                        updated_data = {
                            "title": title,
                            "author": author,
                            "genre": genre,
                            "isbn": isbn,
                            "status": status
                        }
                        if book_manager.update_book(selected_book_id, updated_data):
                            st.success(f"Libro '{title}' actualizado correctamente.")
                    
                    if delete_button:
                        if book_manager.delete_book(selected_book_id):
                            st.success(f"Libro '{title}' eliminado correctamente.")
                            st.experimental_rerun()
        else:
            st.info("No hay libros disponibles para editar o eliminar.")
        
        st.markdown('</div>', unsafe_allow_html=True)

def users_page():
    """Página para la gestión de usuarios."""
    st.markdown('<h1 class="section-header">Gestión de Usuarios</h1>', unsafe_allow_html=True)
    
    _, user_manager, _ = get_managers()
    
    # Crear pestañas para las diferentes operaciones
    tabs = st.tabs(["Ver Usuarios", "Agregar Usuario", "Buscar Usuarios", "Editar/Eliminar"])
    
    # Tab 1: Ver todos los usuarios
    with tabs[0]:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### Todos los Usuarios")
        display_users_table(user_manager.get_all_users())
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Tab 2: Agregar un nuevo usuario
    with tabs[1]:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### Agregar Nuevo Usuario")
        
        with st.form("add_user_form"):
            name = st.text_input("Nombre", key="user_name")
            email = st.text_input("Email", key="user_email")
            
            submit_button = st.form_submit_button("Agregar Usuario")
            
            if submit_button:
                if name and email:
                    new_user = User(name=name, email=email)
                    if user_manager.add_user(new_user):
                        st.success(f"Usuario '{name}' agregado correctamente.")
                else:
                    st.error("Todos los campos son obligatorios.")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Tab 3: Buscar usuarios
    with tabs[2]:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### Buscar Usuarios")
        
        col1, col2 = st.columns(2)
        with col1:
            search_type = st.selectbox(
                "Buscar por",
                ["Nombre", "Email"]
            )
        
        with col2:
            search_term = st.text_input("Término de búsqueda", key="user_search")
        
        if st.button("Buscar Usuarios"):
            if search_term:
                criteria = {}
                key_map = {
                    "Nombre": "name",
                    "Email": "email"
                }
                criteria[key_map[search_type]] = search_term
                
                results = user_manager.search_users(criteria)
                if results.size > 0:
                    st.success(f"Se encontraron {results.size} resultados.")
                    display_users_table(results.display())
                else:
                    st.info("No se encontraron resultados.")
            else:
                st.error("Por favor, ingresa un término de búsqueda.")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Tab 4: Editar/Eliminar usuarios
    with tabs[3]:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### Editar o Eliminar Usuario")
        
        # Obtener todos los usuarios para seleccionar
        users = user_manager.get_all_users()
        user_options = {f"{user.name} ({user.email})": user.id for user in users}
        
        if user_options:
            selected_user_name = st.selectbox(
                "Selecciona un usuario",
                options=list(user_options.keys())
            )
            
            selected_user_id = user_options[selected_user_name]
            selected_user = user_manager.get_user_by_id(selected_user_id)
            
            if selected_user:
                with st.form("edit_user_form"):
                    name = st.text_input("Nombre", value=selected_user.name)
                    email = st.text_input("Email", value=selected_user.email)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        update_button = st.form_submit_button("Actualizar Usuario")
                    
                    with col2:
                        delete_button = st.form_submit_button("Eliminar Usuario")
                    
                    if update_button:
                        updated_data = {
                            "name": name,
                            "email": email
                        }
                        if user_manager.update_user(selected_user_id, updated_data):
                            st.success(f"Usuario '{name}' actualizado correctamente.")
                    
                    if delete_button:
                        if user_manager.delete_user(selected_user_id):
                            st.success(f"Usuario '{name}' eliminado correctamente.")
                            st.experimental_rerun()
        else:
            st.info("No hay usuarios disponibles para editar o eliminar.")
        
        st.markdown('</div>', unsafe_allow_html=True)

def loans_page():
    """Página para la gestión de préstamos."""
    st.markdown('<h1 class="section-header">Gestión de Préstamos</h1>', unsafe_allow_html=True)
    
    book_manager, user_manager, loan_manager = get_managers()
    
    # Crear pestañas para las diferentes operaciones
    tabs = st.tabs(["Préstamos Activos", "Nuevo Préstamo", "Devolver Libro", "Historial"])
    
    # Tab 1: Ver préstamos activos
    with tabs[0]:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### Préstamos Activos")
        
        active_loans = loan_manager.get_active_loans()
        display_loans_table(active_loans)
        
        # Procesar solicitudes pendientes
        if st.button("Procesar Solicitudes Pendientes"):
            loan_manager.process_loan_requests()
            st.success("Solicitudes de préstamo procesadas correctamente.")
            st.experimental_rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Tab 2: Crear un nuevo préstamo
    with tabs[1]:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### Crear Nuevo Préstamo")
        
        # Obtener usuarios y libros disponibles
        users = user_manager.get_all_users()
        available_books = [book for book in book_manager.get_all_books() if book.status == "available"]
        
        user_options = {f"{user.name} ({user.email})": user.id for user in users}
        book_options = {f"{book.title} ({book.author})": book.id for book in available_books}
        
        if user_options and book_options:
            with st.form("new_loan_form"):
                selected_user = st.selectbox(
                    "Selecciona un usuario",
                    options=list(user_options.keys())
                )
                
                selected_book = st.selectbox(
                    "Selecciona un libro",
                    options=list(book_options.keys())
                )
                
                loan_type = st.radio(
                    "Tipo de préstamo",
                    options=["Inmediato", "Solicitud (Cola)"]
                )
                
                submit_button = st.form_submit_button("Crear Préstamo")
                
                if submit_button:
                    user_id = user_options[selected_user]
                    book_id = book_options[selected_book]
                    
                    if loan_type == "Inmediato":
                        if loan_manager.create_loan(book_id, user_id):
                            st.success("Préstamo creado correctamente.")
                            st.experimental_rerun()
                        else:
                            st.error("No se pudo crear el préstamo.")
                    else:
                        if loan_manager.request_loan(book_id, user_id):
                            st.success("Solicitud de préstamo añadida a la cola correctamente.")
                        else:
                            st.error("No se pudo crear la solicitud de préstamo.")
        elif not user_options:
            st.warning("No hay usuarios disponibles. Por favor, agrega algunos usuarios primero.")
        elif not book_options:
            st.warning("No hay libros disponibles para préstamo. Todos los libros están prestados o reservados.")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Tab 3: Devolver un libro
    with tabs[2]:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### Devolver Libro")
        
        active_loans = loan_manager.get_active_loans()
        
        if active_loans:
            # Preparar opciones para el selectbox
            loan_options = {}
            for loan in active_loans:
                book = book_manager.get_book_by_id(loan.book_id)
                user = user_manager.get_user_by_id(loan.user_id)
                
                if book and user:
                    key = f"{book.title} - {user.name} (Préstamo desde: {loan.loan_date})"
                    loan_options[key] = loan.id
            
            selected_loan = st.selectbox(
                "Selecciona un préstamo para devolver",
                options=list(loan_options.keys())
            )
            
            if st.button("Devolver Libro"):
                loan_id = loan_options[selected_loan]
                if loan_manager.return_book(loan_id):
                    st.success("Libro devuelto correctamente.")
                    st.experimental_rerun()
                else:
                    st.error("No se pudo procesar la devolución.")
        else:
            st.info("No hay préstamos activos para devolver.")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Tab 4: Ver historial de préstamos
    with tabs[3]:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### Historial de Préstamos")
        
        loan_history = loan_manager.get_loan_history()
        
        if loan_history:
            history_data = []
            for operation in loan_history:
                history_data.append({
                    "Tipo": operation["type"],
                    "Fecha": operation["timestamp"],
                    "Detalles": str(operation["data"])
                })
            
            df = pd.DataFrame(history_data)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No hay historial de préstamos para mostrar.")
        
        st.markdown('</div>', unsafe_allow_html=True)

def about_page():
    """Página con información sobre el sistema."""
    st.markdown('<h1 class="section-header">Acerca del Sistema</h1>', unsafe_allow_html=True)
    
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("""
    ### Sistema de Gestión de Biblioteca (MVP)
    
    Esta aplicación es un Producto Mínimo Viable (MVP) para un sistema de gestión de biblioteca que permite:
    
    - **Gestionar libros**: Agregar, editar, eliminar y buscar libros.
    - **Gestionar usuarios**: Agregar, editar, eliminar y buscar usuarios.
    - **Gestionar préstamos**: Crear préstamos, procesar devoluciones y seguir el historial.
    
    #### Estructuras de Datos Implementadas
    
    - **Lista Enlazada**: Utilizada para almacenar colecciones de libros, usuarios y préstamos.
    - **Pila**: Utilizada para mantener un historial de operaciones.
    - **Cola**: Utilizada para gestionar solicitudes de préstamo pendientes.
    
    #### Tecnologías Utilizadas
    
    - **Python**: Lenguaje de programación principal.
    - **Streamlit**: Framework para la interfaz de usuario.
    - **Pandas**: Para el procesamiento y visualización de datos tabulares.
    
    #### Desarrollado por
    
    - Equipo de Desarrollo MVP
    """)
    st.markdown('</div>', unsafe_allow_html=True)

# Barra lateral para navegación
st.sidebar.markdown('<div class="sidebar-header">Navegación</div>', unsafe_allow_html=True)
page = st.sidebar.selectbox(
    "Selecciona una página",
    ["Inicio", "Gestión de Libros", "Gestión de Usuarios", "Gestión de Préstamos", "Acerca del Sistema"]
)

# Mostrar la página seleccionada
if page == "Inicio":
    home_page()
elif page == "Gestión de Libros":
    books_page()
elif page == "Gestión de Usuarios":
    users_page()
elif page == "Gestión de Préstamos":
    loans_page()
elif page == "Acerca del Sistema":
    about_page()