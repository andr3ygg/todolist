# Mi Lista de Tareas - TODO List App

Una aplicación web moderna de gestión de tareas construida con Django, Django REST Framework, HTML5, CSS3 y JavaScript vanilla. La aplicación implementa principios SOLID, programación orientada a objetos y proporciona una interfaz intuitiva y responsiva.

## 🚀 Características

- ✅ **Añadir tareas** con título, descripción y prioridad
- ✏️ **Editar tareas** en cualquier momento
- 🗑️ **Eliminar tareas** con confirmación
- ☑️ **Marcar tareas como completadas**
- 🔍 **Filtrar tareas** (Todas, Activas, Completadas)
- 📊 **Contadores de tareas** en cada filtro
- 🎨 **Interfaz moderna y responsiva**
- 🔐 **Validación en cliente y servidor**
- ⚡ **API RESTful** con Django REST Framework
- 🏗️ **Arquitectura escalable** con principios SOLID

## 📋 Requisitos

- Python 3.8+
- pip
- Un navegador web moderno

## 🔧 Instalación

### 1. Crear un entorno virtual

```bash
# En Linux/macOS
python3 -m venv venv
source venv/bin/activate

# En Windows
python -m venv venv
venv\Scripts\activate
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Realizar migraciones de base de datos

```bash
python manage.py migrate
```

## 🎯 Uso

### Iniciar el servidor

```bash
python manage.py runserver
```

El servidor estará disponible en: `http://localhost:8000`

## 📱 Interfaz de Usuario

### Vista Principal

La aplicación tiene una interfaz intuitiva dividida en las siguientes secciones:

1. **Header**: Título y subtítulo de la aplicación
2. **Formulario de entrada**: Añade nuevas tareas
   - Campo de título (requerido)
   - Campo de descripción (opcional)
   - Selector de prioridad
3. **Filtros**: Muestra tareas por estado
   - Todas (contador total)
   - Activas (no completadas)
   - Completadas
4. **Lista de tareas**: Muestra las tareas según el filtro
   - Checkbox para marcar como completada
   - Indicador visual de prioridad
   - Botones de editar y eliminar
   - Fecha de creación y prioridad

### Modal de Edición

Al hacer clic en "Editar", se abre un modal que permite:
- Modificar título
- Cambiar descripción
- Ajustar prioridad
- Guardar o cancelar cambios

## 🛠️ Arquitectura

### Backend (Django)

**Principios SOLID implementados:**

1. **Single Responsibility Principle (SRP)**
   - `Task`: Modelo que solo representa una tarea
   - `TaskSerializer`: Solo serialización
   - `TaskViewSet`: Solo gestiona HTTP requests/responses

2. **Open/Closed Principle (OCP)**
   - Las clases están abiertas a extensión (herencia)
   - Cerradas a modificación (métodos bien definidos)

3. **Liskov Substitution Principle (LSP)**
   - `TaskViewSet` extiende `ModelViewSet` correctamente
   - Los serializadores implementan correctamente la interfaz DRF

4. **Interface Segregation Principle (ISP)**
   - Serializadores separados para lectura y escritura
   - Métodos específicos para acciones específicas

5. **Dependency Inversion Principle (DIP)**
   - Uso de inyección de dependencias a través de ViewSet
   - Las vistas no dependen de la base de datos directamente

### Estructura de archivos

```
todoproject/
├── manage.py                 # Entrada principal de Django
├── requirements.txt          # Dependencias del proyecto
├── db.sqlite3               # Base de datos SQLite
├── todoproject/             # Configuración del proyecto
│   ├── __init__.py
│   ├── settings.py          # Configuración de Django
│   ├── urls.py              # URLs principales
│   ├── asgi.py
│   └── wsgi.py
├── todoapp/                 # Aplicación Django
│   ├── __init__.py
│   ├── apps.py              # Configuración de la app
│   ├── models.py            # Modelos (Task)
│   ├── serializers.py       # Serializadores
│   ├── views.py             # Vistas (TaskViewSet)
│   └── urls.py              # URLs de la app
└── frontend/                # Interfaz web
    ├── index.html           # HTML
    ├── style.css            # Estilos
    └── script.js            # Lógica del cliente
```

### Frontend (JavaScript)

**Clases implementadas:**

1. **TaskAPI**: Maneja comunicación con la API
   - Métodos para GET, POST, PUT, DELETE
   - Manejo de errores

2. **TaskUI**: Gestiona la interfaz de usuario
   - Renderizado de tareas
   - Modales
   - Notificaciones

3. **TaskManager**: Controlador principal
   - Coordina API y UI
   - Maneja eventos del usuario
   - Gestiona estado de la aplicación

## 🌐 API Endpoints

Todos los endpoints están bajo `/api/tasks/`

### Listar tareas
```
GET /api/tasks/
```

### Crear tarea
```
POST /api/tasks/
Content-Type: application/json

{
    "title": "Mi tarea",
    "description": "Descripción opcional",
    "priority": 2,
    "completed": false
}
```

### Obtener tarea específica
```
GET /api/tasks/{id}/
```

### Actualizar tarea
```
PUT /api/tasks/{id}/
```

### Actualización parcial
```
PATCH /api/tasks/{id}/
```

### Eliminar tarea
```
DELETE /api/tasks/{id}/
```

### Cambiar estado de completación
```
PATCH /api/tasks/{id}/toggle_completion/
```

### Tareas activas (no completadas)
```
GET /api/tasks/active/
```

### Tareas completadas
```
GET /api/tasks/completed/
```

### Tareas por prioridad
```
GET /api/tasks/by_priority/?priority=1,2,3
```

## 🎨 Personalización

### Colores principales
Edita las variables CSS en `frontend/style.css`:
```css
:root {
    --primary-color: #3498db;      /* Azul principal */
    --success-color: #27ae60;      /* Verde para éxito */
    --danger-color: #e74c3c;       /* Rojo para peligro */
    --warning-color: #f39c12;      /* Naranja para advertencia */
}
```

### Prioridades
En `todoapp/models.py`:
```python
PRIORITY_CHOICES = [
    (1, 'Baja'),
    (2, 'Media'),
    (3, 'Alta'),
]
```

## 📱 Responsividad

La aplicación está optimizada para:
- 📱 Móviles (480px y menos)
- 📱 Tablets (768px y menos)
- 🖥️ Escritorio (1200px+)

## 🔒 Validación

### Del lado del cliente
- Título requerido
- Validación de longitud mínima (3 caracteres)
- Valores de prioridad válidos

### Del lado del servidor
- Validación en modelos
- Validación en serializadores
- Manejo de errores con mensajes descriptivos

## 🐛 Troubleshooting

### "No se puede conectar al servidor"
```bash
# Asegúrate que Django está corriendo
python manage.py runserver
```

### "Error de base de datos"
```bash
# Recrear la base de datos
rm db.sqlite3
python manage.py migrate
```

### "CORS error"
La configuración CORS ya está incluida en `settings.py`

## 📚 Tecnologías utilizadas

- **Backend**:
  - Django 4.2
  - Django REST Framework 3.14
  - SQLite (base de datos)

- **Frontend**:
  - HTML5
  - CSS3 (con variables CSS)
  - JavaScript ES6 (vanilla, sin frameworks)

- **Arquitectura**:
  - MVC (Model-View-Controller)
  - API RESTful
  - Principios SOLID
  - OOP (Programación Orientada a Objetos)

## 📄 Licencia

Este proyecto está bajo licencia MIT. Ver archivo LICENSE para más detalles.

## 👨‍💻 Autor

Creado por Andrey
