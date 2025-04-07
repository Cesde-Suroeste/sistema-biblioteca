# Sistema de Gestión de Biblioteca (MVP)

Sistema de gestión de biblioteca que implementa estructuras de datos lineales (listas enlazadas, pilas y colas) para administrar libros, usuarios y préstamos.

## Características

- **Gestión completa de libros**: Agregar, editar, eliminar y buscar libros
- **Gestión de usuarios**: Administrar usuarios, historial de préstamos
- **Gestión de préstamos**: Crear préstamos, procesar devoluciones, seguimiento
- **Estructuras de datos eficientes**: Lista Enlazada, Pila y Cola
- **Interfaz intuitiva**: Desarrollada con Streamlit para facilitar la interacción
- **Almacenamiento persistente**: Datos guardados en archivos JSON
- **Pruebas exhaustivas**: Verificación de todas las funcionalidades

## Estructura del Proyecto

```
biblioteca-mvp/
├── app.py                  # Aplicación principal Streamlit
├── data_structures.py      # Implementación de estructuras de datos
├── managers.py             # Gestores de libros, usuarios y préstamos
├── models.py               # Definición de modelos (Book, User, Loan)
├── tests.py                # Pruebas unitarias
├── books.json              # Datos persistentes de libros
├── users.json              # Datos persistentes de usuarios
├── loans.json              # Datos persistentes de préstamos
├── operations_history.json # Historial de operaciones
├── loan_requests.json      # Solicitudes de préstamo pendientes
└── README.md               # Documentación del proyecto
```

## Requisitos

- Python 3.7 o superior
- Streamlit
- Pandas

## Instalación en Linux/macOS

1. Clonar el repositorio o descargar los archivos

2. Crear un entorno virtual (recomendado):
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Instalar las dependencias:
   ```bash
   pip install streamlit pandas
   ```

## Instalación en Windows

1. Clonar el repositorio o descargar los archivos

2. Abrir la línea de comandos (cmd) o PowerShell en la carpeta del proyecto

3. Crear un entorno virtual (recomendado):
   ```
   python -m venv venv
   venv\Scripts\activate
   ```

4. Instalar las dependencias:
   ```
   pip install streamlit pandas
   ```

## Uso en Linux/macOS

1. Activar el entorno virtual si no está activado:
   ```bash
   source venv/bin/activate
   ```

2. Ejecutar la aplicación:
   ```bash
   streamlit run app.py
   ```

3. Navegar a la dirección proporcionada (generalmente `http://localhost:8501`)

## Uso en Windows

1. Activar el entorno virtual si no está activado:
   ```
   venv\Scripts\activate
   ```

2. Ejecutar la aplicación:
   ```
   streamlit run app.py
   ```

3. Navegar a la dirección proporcionada (generalmente `http://localhost:8501`)

4. Utilizar la barra lateral para navegar entre las diferentes secciones:
   - **Inicio**: Dashboard con estadísticas
   - **Gestión de Libros**: Administrar libros
   - **Gestión de Usuarios**: Administrar usuarios
   - **Gestión de Préstamos**: Crear y gestionar préstamos
   - **Acerca del Sistema**: Información sobre el MVP

## Solución de problemas comunes en Windows

1. **Error al activar el entorno virtual**: Si aparece un error relacionado con la política de ejecución en PowerShell, ejecute:
   ```
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

2. **Python no reconocido como comando**: Asegúrese de que Python esté añadido al PATH del sistema. Durante la instalación de Python, marque la opción "Add Python to PATH".

3. **Problemas de permisos**: Ejecute la línea de comandos como administrador si encuentra errores de permisos.

4. **Errores con dependencias**: Si hay problemas con la instalación de paquetes, intente actualizar pip:
   ```
   python -m pip install --upgrade pip
   ```

## Ejecución de Pruebas

Para ejecutar las pruebas unitarias:

```bash
python tests.py
```

## Estructuras de Datos Implementadas

### Lista Enlazada
Utilizada para almacenar colecciones de libros, usuarios y préstamos.

### Pila
Utilizada para mantener un historial de operaciones de préstamos.

### Cola
Utilizada para gestionar solicitudes de préstamo pendientes.

## Contribuciones

Este es un proyecto MVP con fines educativos y de demostración. Si deseas contribuir o extender sus funcionalidades, considera implementar:

- Migración a base de datos para mayor escalabilidad
- Autenticación y control de acceso
- Búsquedas avanzadas y reportes
- Notificaciones para fechas de vencimiento
- API para integración con otros sistemas

## Licencia

[MIT](https://opensource.org/licenses/MIT)
