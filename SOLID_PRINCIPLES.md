# Guía de Principios SOLID Implementados

Esta aplicación TODO List implementa todos los principios SOLID de manera práctica. Este documento explica cómo cada principio se ha aplicado en el código.

## 1. Single Responsibility Principle (SRP)

**Definición**: Una clase debe tener una única razón para cambiar.

### Implementación en el Backend

#### `models.py` - Clase `Task`
```python
class Task(models.Model):
    # Solo se encarga de representar una tarea
    # Responsabilidades:
    # - Definir campos de la tarea
    # - Métodos de negocio de la tarea (mark_as_completed, update_priority)
    # - Representación en string
```

**Beneficio**: Si necesitamos cambiar la lógica de una tarea, solo modificamos esta clase.

#### `serializers.py` - Clases `TaskSerializer` y `TaskCreateUpdateSerializer`
```python
class TaskSerializer(serializers.ModelSerializer):
    # Solo se encarga de serializar para lectura
    
class TaskCreateUpdateSerializer(serializers.ModelSerializer):
    # Solo se encarga de validar y serializar para escritura
```

**Beneficio**: Tenemos serializadores especializados, no un único serializador que hace todo.

#### `views.py` - Clase `TaskViewSet`
```python
class TaskViewSet(viewsets.ModelViewSet):
    # Solo se encarga de manejar HTTP requests/responses
    # No valida directamente (eso es del serializador)
    # No accede a la BD directamente (usa QuerySet/ORM)
```

**Beneficio**: Las vistas solo orquestan, no implementan lógica de negocio.

### Implementación en el Frontend

#### `script.js` - Clase `TaskAPI`
```javascript
class TaskAPI {
    // Solo se encarga de comunicación con la API
    // Métodos: GET, POST, PUT, DELETE, etc.
}
```

**Beneficio**: Cambios en la API solo afectan a esta clase.

#### `script.js` - Clase `TaskUI`
```javascript
class TaskUI {
    // Solo se encarga de manipular el DOM
    // Métodos: renderTasks, showModal, showToast, etc.
}
```

**Beneficio**: Si cambias la interfaz, solo modificas esta clase.

#### `script.js` - Clase `TaskManager`
```javascript
class TaskManager {
    // Orquesta API y UI
    // Maneja eventos y lógica de la aplicación
}
```

**Beneficio**: Separación clara entre presentación y lógica.

---

## 2. Open/Closed Principle (OCP)

**Definición**: Las clases deben estar abiertas a extensión pero cerradas a modificación.

### Implementación

#### Uso de Django ViewSet
```python
class TaskViewSet(viewsets.ModelViewSet):
    # Extiende ModelViewSet, heredando todas sus funcionalidades
    # Extensión: añadimos métodos custom como toggle_completion
    # Sin modificar la clase base
    
    @action(detail=True, methods=['patch'])
    def toggle_completion(self, request, pk=None):
        # Nuevo comportamiento sin modificar ModelViewSet
```

**Beneficio**: Podemos agregar nuevos endpoints sin modificar la clase base.

#### Serializadores extensibles
```python
class TaskCreateUpdateSerializer(TaskSerializer):
    # Hereda de TaskSerializer
    # Añade validación custom
    # Puede ser extendida sin modificar TaskSerializer
```

**Beneficio**: Nueva validación = nueva clase, no modificar la existente.

#### Frontend - Métodos de acción
```javascript
class TaskManager {
    async handleAddTask(e) { }
    async handleEditTask(task, taskId) { }
    async handleDeleteTask(taskId) { }
    
    // Podemos añadir más métodos sin modificar los existentes
}
```

---

## 3. Liskov Substitution Principle (LSP)

**Definición**: Los objetos de subclases deben poder sustituir objetos de sus clases base.

### Implementación

#### ViewSet en Django
```python
class TaskViewSet(viewsets.ModelViewSet):
    # Puede usarse en lugar de ModelViewSet
    # Proporciona todas las operaciones CRUD esperadas
    # Más específicamente, TaskViewSet para tareas
```

**Beneficio**: Podríamos reemplazar TaskViewSet con otra implementación sin romper el código.

#### Serializadores
```python
# Ambos pueden usarse donde se espera un serializador
serializer = TaskSerializer(task)
serializer = TaskCreateUpdateSerializer(task_data)
```

**Beneficio**: Consistencia en la interfaz de serialización.

---

## 4. Interface Segregation Principle (ISP)

**Definición**: No se debe forzar a un cliente a usar interfaces que no necesita.

### Implementación

#### Serializadores separados
```python
# TaskSerializer - para lectura (tiene campos adicionales como priority_display)
class TaskSerializer(serializers.ModelSerializer):
    priority_display = serializers.CharField(source='get_priority_display_name', read_only=True)

# TaskCreateUpdateSerializer - para escritura (validación específica)
class TaskCreateUpdateSerializer(serializers.ModelSerializer):
    def validate_title(self, value):
        # Validación que solo hace sentido en creación/actualización
```

**Beneficio**: 
- El cliente que solo lee no hereda validación de escritura
- El que escribe tiene validación especializada

#### JavaScript - Métodos especializados
```javascript
class TaskAPI {
    async getTasks() { }           // Solo lectura
    async createTask(taskData) { } // Escritura
    async getActiveTasks() { }     // Lectura filtrada
}
```

**Beneficio**: Cada método tiene una responsabilidad clara.

---

## 5. Dependency Inversion Principle (DIP)

**Definición**: Las clases de alto nivel no deben depender de las de bajo nivel. Ambas deben depender de abstracciones.

### Implementación

#### Backend - ViewSet y ORM
```python
class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()  # Abstracción de la BD
    serializer_class = TaskSerializer
    
    # No crea conexiones a BD directamente
    # Usa Django ORM como abstracción
```

**Beneficio**: Si cambias de SQLite a PostgreSQL, el ViewSet no se modifica.

#### Frontend - Inyección de dependencias
```javascript
class TaskManager {
    constructor() {
        this.api = new TaskAPI();      // Inyección
        this.ui = new TaskUI();        // Inyección
    }
    
    // TaskManager depende de abstracciones (API, UI)
    // No directamente de xhr o DOM
}
```

**Beneficio**: Podríamos reemplazar TaskAPI con una versión que use WebSockets sin cambiar TaskManager.

#### Uso de interfaces implícitas
```javascript
class TaskAPI {
    async getTasks() { }           // Interface que TaskManager espera
    async createTask(data) { }
    async updateTask(id, data) { }
}

// Otra implementación podría usarse si implementa la misma interfaz
class TaskAPIAlternativa {
    async getTasks() { }           // Misma interface
    async createTask(data) { }
    async updateTask(id, data) { }
}
```

---

## 📊 Diagrama de Dependencias

### Backend
```
HTTP Request
    ↓
TaskViewSet (View)
    ↓
TaskSerializer/TaskCreateUpdateSerializer (Presentation)
    ↓
Task (Model - Lógica de negocio)
    ↓
Base de Datos (SQLite)
```

Cada capa depende de la anterior, no de la siguiente.

### Frontend
```
usuario
    ↓
TaskManager (Lógica)
    ↓
TaskUI (Presentación)
    ↓
DOM
    
TaskManager también depende de:
    ↓
TaskAPI (Comunicación)
    ↓
API REST
```

---

## 🎯 Ventajas de esta Arquitectura

1. **Mantenibilidad**: Código organizado y fácil de entender
2. **Escalabilidad**: Fácil agregar nuevas features sin romper código existente
3. **Testabilidad**: Cada componente se puede probar independientemente
4. **Reutilización**: Las clases tienen un propósito claro y pueden reutilizarse
5. **Flexibilidad**: Cambios en una capa no afectan a otras

---

## 💡 Ejemplos Prácticos

### Ejemplo 1: Agregar un nuevo tipo de tarea

**Antes (sin SOLID)**: Modificarías Task, Serializer, ViewSet, UI
**Después (con SOLID)**: 
```python
# Extiendes Task para crear SubTask (OCP)
class SubTask(Task):
    parent_task = models.ForeignKey(Task, ...)

# Creas un nuevo serializador si necesitas (ISP)
class SubTaskSerializer(TaskSerializer):
    pass

# Creas un nuevo ViewSet si necesitas (OCP)
class SubTaskViewSet(TaskViewSet):
    queryset = SubTask.objects.all()
```

### Ejemplo 2: Cambiar validación

**Antes**: Modificarías TaskSerializer
**Después**: Creas TaskCreateUpdateSerializer con validación nueva (SRP, OCP)

### Ejemplo 3: Usar otra API

**Antes**: Modificarías TaskManager para acceder a otra API
**Después**: Creas TaskAPIAlternativa que implemente la misma interface (DIP)

---

## 📖 Referencias

- [SOLID Principles](https://en.wikipedia.org/wiki/SOLID)
- [Clean Code](https://www.oreilly.com/library/view/clean-code-a/9780136083238/)
- [Design Patterns](https://refactoring.guru/design-patterns)
