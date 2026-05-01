/**
 * TaskManager - Gestor de Tareas
 * Implementa el patrón MVC y principios SOLID
 */

/**
 * Clase para interactuar con la API REST
 */
class TaskAPI {
    constructor(baseURL = '/api') {
        this.baseURL = baseURL;
        this.tasksEndpoint = `${baseURL}/tasks/`;
    }

    async getTasks() {
        try {
            const response = await fetch(this.tasksEndpoint);
            if (!response.ok) throw new Error('Error al obtener tareas');
            const data = await response.json();
            if (Array.isArray(data)) return data;
            if (data && Array.isArray(data.results)) return data.results;
            throw new Error('Formato de respuesta inesperado al obtener tareas');
        } catch (error) {
            console.error('Error:', error);
            throw error;
        }
    }

    async getActiveTasks() {
        try {
            const response = await fetch(`${this.tasksEndpoint}active/`);
            if (!response.ok) throw new Error('Error al obtener tareas activas');
            const data = await response.json();
            if (Array.isArray(data)) return data;
            if (data && Array.isArray(data.results)) return data.results;
            throw new Error('Formato de respuesta inesperado al obtener tareas activas');
        } catch (error) {
            console.error('Error:', error);
            throw error;
        }
    }

    async getCompletedTasks() {
        try {
            const response = await fetch(`${this.tasksEndpoint}completed/`);
            if (!response.ok) throw new Error('Error al obtener tareas completadas');
            const data = await response.json();
            if (Array.isArray(data)) return data;
            if (data && Array.isArray(data.results)) return data.results;
            throw new Error('Formato de respuesta inesperado al obtener tareas completadas');
        } catch (error) {
            console.error('Error:', error);
            throw error;
        }
    }

    async createTask(taskData) {
        try {
            const response = await fetch(this.tasksEndpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(taskData)
            });
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(JSON.stringify(errorData));
            }
            return await response.json();
        } catch (error) {
            console.error('Error:', error);
            throw error;
        }
    }

    async updateTask(id, taskData) {
        try {
            const response = await fetch(`${this.tasksEndpoint}${id}/`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(taskData)
            });
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(JSON.stringify(errorData));
            }
            return await response.json();
        } catch (error) {
            console.error('Error:', error);
            throw error;
        }
    }

    async deleteTask(id) {
        try {
            const response = await fetch(`${this.tasksEndpoint}${id}/`, {
                method: 'DELETE'
            });
            if (!response.ok) throw new Error('Error al eliminar la tarea');
            return true;
        } catch (error) {
            console.error('Error:', error);
            throw error;
        }
    }

    async toggleTaskCompletion(id) {
        try {
            const response = await fetch(`${this.tasksEndpoint}${id}/toggle_completion/`, {
                method: 'PATCH',
                headers: {
                    'Content-Type': 'application/json',
                }
            });
            if (!response.ok) throw new Error('Error al cambiar estado de tarea');
            return await response.json();
        } catch (error) {
            console.error('Error:', error);
            throw error;
        }
    }
}

/**
 * Clase para manejar la interfaz del usuario
 */
class TaskUI {
    constructor() {
        this.taskForm = document.getElementById('taskForm');
        this.taskTitle = document.getElementById('taskTitle');
        this.taskDescription = document.getElementById('taskDescription');
        this.taskPriority = document.getElementById('taskPriority');
        this.tasksList = document.getElementById('tasksList');
        this.filterButtons = document.querySelectorAll('.filter-btn');
        this.loadingMessage = document.getElementById('loadingMessage');
        this.emptyMessage = document.getElementById('emptyMessage');
        this.editModal = document.getElementById('editModal');
        this.editForm = document.getElementById('editForm');
        this.editTitle = document.getElementById('editTitle');
        this.editDescription = document.getElementById('editDescription');
        this.editPriority = document.getElementById('editPriority');
        this.cancelEditBtn = document.getElementById('cancelEdit');
        this.modalCloseBtn = document.querySelector('.modal-close');
        this.toast = document.getElementById('toast');
    }

    /**
     * Renderiza la lista de tareas
     */
    renderTasks(tasks) {
        this.tasksList.innerHTML = '';
        
        if (tasks.length === 0) {
            this.showEmptyMessage();
            return;
        }

        this.hideEmptyMessage();
        tasks.forEach(task => {
            const taskElement = this.createTaskElement(task);
            this.tasksList.appendChild(taskElement);
        });
    }

    /**
     * Crea un elemento de tarea
     */
    createTaskElement(task) {
        const li = document.createElement('li');
        li.className = `task-item ${task.completed ? 'completed' : ''}`;
        li.dataset.taskId = task.id;

        const priorityMap = { 1: 'low', 2: 'medium', 3: 'high' };
        const priorityClass = priorityMap[task.priority];

        const createdDate = new Date(task.created_at).toLocaleDateString('es-ES', {
            year: 'numeric',
            month: 'short',
            day: 'numeric'
        });

        li.innerHTML = `
            <input type="checkbox" class="task-checkbox" ${task.completed ? 'checked' : ''} 
                   aria-label="Marcar tarea como completada">
            <div class="task-priority ${priorityClass}" title="Prioridad: ${task.priority_display}"></div>
            <div class="task-content">
                <h3 class="task-title">${this.escapeHTML(task.title)}</h3>
                ${task.description ? `<p class="task-description">${this.escapeHTML(task.description)}</p>` : ''}
                <div class="task-meta">
                    <span class="task-date">📅 ${createdDate}</span>
                    <span class="task-priority-label ${priorityClass}">${task.priority_display}</span>
                </div>
            </div>
            <div class="task-actions">
                <button class="task-btn task-btn-edit" aria-label="Editar tarea">✏️ Editar</button>
                <button class="task-btn task-btn-delete" aria-label="Eliminar tarea">🗑️ Eliminar</button>
            </div>
        `;

        return li;
    }

    /**
     * Escapa caracteres HTML para prevenir XSS
     */
    escapeHTML(text) {
        const map = {
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            "'": '&#039;'
        };
        return text.replace(/[&<>"']/g, m => map[m]);
    }

    /**
     * Muestra el modal de edición
     */
    showEditModal(task, onSubmit, onCancel) {
        this.editTitle.value = task.title;
        this.editDescription.value = task.description;
        this.editPriority.value = task.priority;

        this.editModal.classList.remove('hidden');

        // Resetea listeners anteriores
        this.editForm.onsubmit = (e) => {
            e.preventDefault();
            const updatedData = {
                title: this.editTitle.value,
                description: this.editDescription.value,
                priority: parseInt(this.editPriority.value),
                completed: task.completed
            };
            onSubmit(updatedData);
            this.hideEditModal();
        };

        this.cancelEditBtn.onclick = () => {
            this.hideEditModal();
            onCancel();
        };

        this.modalCloseBtn.onclick = () => {
            this.hideEditModal();
            onCancel();
        };

        this.editTitle.focus();
    }

    /**
     * Oculta el modal de edición
     */
    hideEditModal() {
        this.editModal.classList.add('hidden');
        this.editForm.reset();
    }

    /**
     * Muestra mensaje de carga
     */
    showLoadingMessage() {
        this.loadingMessage.classList.remove('hidden');
        this.emptyMessage.classList.add('hidden');
    }

    /**
     * Oculta mensaje de carga
     */
    hideLoadingMessage() {
        this.loadingMessage.classList.add('hidden');
    }

    /**
     * Muestra mensaje de lista vacía
     */
    showEmptyMessage() {
        this.emptyMessage.classList.remove('hidden');
    }

    /**
     * Oculta mensaje de lista vacía
     */
    hideEmptyMessage() {
        this.emptyMessage.classList.add('hidden');
    }

    /**
     * Limpia el formulario
     */
    clearForm() {
        this.taskForm.reset();
        this.taskTitle.focus();
    }

    /**
     * Muestra notificación
     */
    showToast(message, type = 'success') {
        this.toast.textContent = message;
        this.toast.className = `toast ${type}`;
        this.toast.classList.remove('hidden');

        setTimeout(() => {
            this.toast.classList.add('hidden');
        }, 3000);
    }

    /**
     * Actualiza contadores de filtros
     */
    updateFilterCounts(allCount, activeCount, completedCount) {
        const filterBtns = {
            'all': allCount,
            'active': activeCount,
            'completed': completedCount
        };

        this.filterButtons.forEach(btn => {
            const filter = btn.dataset.filter;
            btn.textContent = `${filter.charAt(0).toUpperCase() + filter.slice(1)} (${filterBtns[filter]})`;
        });
    }

    /**
     * Obtiene los datos del formulario
     */
    getFormData() {
        return {
            title: this.taskTitle.value.trim(),
            description: this.taskDescription.value.trim(),
            priority: parseInt(this.taskPriority.value),
            completed: false
        };
    }
}

/**
 * Clase principal para gestionar la aplicación
 */
class TaskManager {
    constructor() {
        this.api = new TaskAPI();
        this.ui = new TaskUI();
        this.currentFilter = 'all';
        this.allTasks = [];
        this.filteredTasks = [];
        this.editingTaskId = null;

        this.init();
    }

    /**
     * Inicializa la aplicación
     */
    async init() {
        this.setupEventListeners();
        await this.loadTasks();
    }

    /**
     * Configura los event listeners
     */
    setupEventListeners() {
        // Formulario
        this.ui.taskForm.addEventListener('submit', (e) => this.handleAddTask(e));

        // Filtros
        this.ui.filterButtons.forEach(btn => {
            btn.addEventListener('click', () => this.handleFilterChange(btn));
        });

        // Delegación de eventos para tareas (editar, eliminar, checkbox)
        this.ui.tasksList.addEventListener('click', (e) => this.handleTaskAction(e));
        this.ui.tasksList.addEventListener('change', (e) => this.handleTaskCheckbox(e));
    }

    /**
     * Carga las tareas desde la API
     */
    async loadTasks() {
        try {
            this.ui.showLoadingMessage();
            this.allTasks = await this.api.getTasks();
            this.applyFilter(this.currentFilter);
            this.updateFilterCounts();
        } catch (error) {
            this.ui.showToast('Error al cargar las tareas', 'error');
            console.error(error);
        }
    }

    /**
     * Maneja la adición de una nueva tarea
     */
    async handleAddTask(e) {
        e.preventDefault();

        try {
            const formData = this.ui.getFormData();

            if (!formData.title) {
                this.ui.showToast('Por favor ingresa un título para la tarea', 'warning');
                return;
            }

            const newTask = await this.api.createTask(formData);
            this.allTasks.unshift(newTask);
            this.applyFilter(this.currentFilter);
            this.updateFilterCounts();
            this.ui.clearForm();
            this.ui.showToast('✅ Tarea añadida exitosamente', 'success');
        } catch (error) {
            let errorMessage = 'Error al añadir la tarea';
            try {
                const errorData = JSON.parse(error.message);
                if (errorData.title) {
                    errorMessage = errorData.title[0];
                }
            } catch (e) {
                // error.message no es JSON
            }
            this.ui.showToast(errorMessage, 'error');
            console.error(error);
        }
    }

    /**
     * Maneja el cambio de filtro
     */
    handleFilterChange(btn) {
        this.ui.filterButtons.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');

        this.currentFilter = btn.dataset.filter;
        this.applyFilter(this.currentFilter);
    }

    /**
     * Aplica filtro a las tareas
     */
    applyFilter(filter) {
        switch (filter) {
            case 'active':
                this.filteredTasks = this.allTasks.filter(task => !task.completed);
                break;
            case 'completed':
                this.filteredTasks = this.allTasks.filter(task => task.completed);
                break;
            default:
                this.filteredTasks = this.allTasks;
        }

        this.ui.renderTasks(this.filteredTasks);
    }

    /**
     * Actualiza los contadores de filtros
     */
    updateFilterCounts() {
        const activeCount = this.allTasks.filter(t => !t.completed).length;
        const completedCount = this.allTasks.filter(t => t.completed).length;

        this.ui.updateFilterCounts(this.allTasks.length, activeCount, completedCount);
    }

    /**
     * Maneja acciones en tareas (editar, eliminar)
     */
    handleTaskAction(e) {
        const taskElement = e.target.closest('.task-item');
        if (!taskElement) return;

        const taskId = parseInt(taskElement.dataset.taskId);
        const task = this.allTasks.find(t => t.id === taskId);

        if (e.target.closest('.task-btn-edit')) {
            this.handleEditTask(task, taskId);
        } else if (e.target.closest('.task-btn-delete')) {
            this.handleDeleteTask(taskId);
        }
    }

    /**
     * Maneja la edición de una tarea
     */
    handleEditTask(task, taskId) {
        this.editingTaskId = taskId;

        this.ui.showEditModal(
            task,
            (updatedData) => this.submitEditTask(taskId, updatedData),
            () => { this.editingTaskId = null; }
        );
    }

    /**
     * Envía la actualización de la tarea
     */
    async submitEditTask(taskId, updatedData) {
        try {
            const updatedTask = await this.api.updateTask(taskId, updatedData);
            const index = this.allTasks.findIndex(t => t.id === taskId);
            if (index !== -1) {
                this.allTasks[index] = updatedTask;
            }
            this.applyFilter(this.currentFilter);
            this.ui.showToast('✏️ Tarea actualizada exitosamente', 'success');
        } catch (error) {
            this.ui.showToast('Error al actualizar la tarea', 'error');
            console.error(error);
        }
    }

    /**
     * Maneja la eliminación de una tarea
     */
    async handleDeleteTask(taskId) {
        const confirmed = confirm('¿Está seguro de que desea eliminar esta tarea?');
        if (!confirmed) return;

        try {
            await this.api.deleteTask(taskId);
            this.allTasks = this.allTasks.filter(t => t.id !== taskId);
            this.applyFilter(this.currentFilter);
            this.updateFilterCounts();
            this.ui.showToast('🗑️ Tarea eliminada exitosamente', 'success');
        } catch (error) {
            this.ui.showToast('Error al eliminar la tarea', 'error');
            console.error(error);
        }
    }

    /**
     * Maneja el checkbox de completación
     */
    async handleTaskCheckbox(e) {
        if (!e.target.classList.contains('task-checkbox')) return;

        const taskElement = e.target.closest('.task-item');
        const taskId = parseInt(taskElement.dataset.taskId);

        try {
            const updatedTask = await this.api.toggleTaskCompletion(taskId);
            const index = this.allTasks.findIndex(t => t.id === taskId);
            if (index !== -1) {
                this.allTasks[index] = updatedTask;
            }
            this.applyFilter(this.currentFilter);
            this.updateFilterCounts();

            const message = updatedTask.completed ? '✅ Tarea completada' : '↩️ Tarea reactivada';
            this.ui.showToast(message, 'success');
        } catch (error) {
            e.target.checked = !e.target.checked; // Revierte el cambio
            this.ui.showToast('Error al cambiar estado de la tarea', 'error');
            console.error(error);
        }
    }
}

/**
 * Inicializa la aplicación cuando el DOM está listo
 */
document.addEventListener('DOMContentLoaded', () => {
    new TaskManager();
});
