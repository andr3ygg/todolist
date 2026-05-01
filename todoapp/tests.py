"""
Tests para la aplicación TODO List
Ejecutar con: python manage.py test
"""

from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Task


class TaskModelTest(TestCase):
    """Tests para el modelo Task"""
    
    def setUp(self):
        """Crear una tarea para los tests"""
        self.task = Task.objects.create(
            title="Tarea de prueba",
            description="Una descripción",
            priority=2
        )
    
    def test_task_creation(self):
        """Verificar que una tarea se crea correctamente"""
        self.assertEqual(self.task.title, "Tarea de prueba")
        self.assertFalse(self.task.completed)
        self.assertEqual(self.task.priority, 2)
    
    def test_mark_as_completed(self):
        """Verificar que una tarea puede marcarse como completada"""
        self.task.mark_as_completed()
        self.assertTrue(self.task.completed)
    
    def test_mark_as_incomplete(self):
        """Verificar que una tarea puede marcarse como incompleta"""
        self.task.completed = True
        self.task.save()
        self.task.mark_as_incomplete()
        self.assertFalse(self.task.completed)
    
    def test_update_priority(self):
        """Verificar que la prioridad se puede actualizar"""
        self.task.update_priority(3)
        self.assertEqual(self.task.priority, 3)
    
    def test_invalid_priority(self):
        """Verificar que prioridades inválidas no se aceptan"""
        initial_priority = self.task.priority
        self.task.update_priority(5)
        self.task.refresh_from_db()
        self.assertEqual(self.task.priority, initial_priority)


class TaskAPITest(TestCase):
    """Tests para los endpoints de la API"""
    
    def setUp(self):
        """Configurar cliente y datos de prueba"""
        self.client = APIClient()
        self.task_data = {
            'title': 'Nueva tarea',
            'description': 'Descripción de prueba',
            'priority': 2,
            'completed': False
        }
    
    def test_create_task(self):
        """Test: Crear una tarea"""
        response = self.client.post('/api/tasks/', self.task_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)
    
    def test_create_task_invalid(self):
        """Test: Crear tarea con datos inválidos"""
        invalid_data = {'title': ''}  # Título vacío
        response = self.client.post('/api/tasks/', invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_list_tasks(self):
        """Test: Listar todas las tareas"""
        Task.objects.create(**self.task_data)
        response = self.client.get('/api/tasks/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_retrieve_task(self):
        """Test: Obtener una tarea específica"""
        task = Task.objects.create(**self.task_data)
        response = self.client.get(f'/api/tasks/{task.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Nueva tarea')
    
    def test_update_task(self):
        """Test: Actualizar una tarea"""
        task = Task.objects.create(**self.task_data)
        updated_data = {
            'title': 'Tarea actualizada',
            'description': 'Nueva descripción',
            'priority': 3,
            'completed': True
        }
        response = self.client.put(f'/api/tasks/{task.id}/', updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Tarea actualizada')
    
    def test_partial_update_task(self):
        """Test: Actualización parcial de tarea"""
        task = Task.objects.create(**self.task_data)
        updated_data = {'priority': 3}
        response = self.client.patch(f'/api/tasks/{task.id}/', updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['priority'], 3)
    
    def test_delete_task(self):
        """Test: Eliminar una tarea"""
        task = Task.objects.create(**self.task_data)
        response = self.client.delete(f'/api/tasks/{task.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 0)
    
    def test_toggle_completion(self):
        """Test: Cambiar estado de completación"""
        task = Task.objects.create(**self.task_data)
        response = self.client.patch(f'/api/tasks/{task.id}/toggle_completion/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['completed'])
    
    def test_active_tasks(self):
        """Test: Obtener tareas activas"""
        Task.objects.create(**self.task_data, completed=False)
        Task.objects.create(**self.task_data, title='Completada', completed=True)
        response = self.client.get('/api/tasks/active/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_completed_tasks(self):
        """Test: Obtener tareas completadas"""
        Task.objects.create(**self.task_data, completed=False)
        Task.objects.create(**self.task_data, title='Completada', completed=True)
        response = self.client.get('/api/tasks/completed/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_by_priority(self):
        """Test: Obtener tareas por prioridad"""
        Task.objects.create(**self.task_data, priority=1)
        Task.objects.create(**self.task_data, title='Alta', priority=3)
        response = self.client.get('/api/tasks/by_priority/?priority=3')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['priority'], 3)
