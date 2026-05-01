"""
Vistas de la API REST.
Implementando principios SOLID y buenas prácticas.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Task
from .serializers import TaskSerializer, TaskCreateUpdateSerializer


class TaskViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar las operaciones CRUD de Tareas.
    
    Endpoints:
        GET /api/tasks/ - Listar todas las tareas
        POST /api/tasks/ - Crear una nueva tarea
        GET /api/tasks/{id}/ - Obtener una tarea específica
        PUT /api/tasks/{id}/ - Actualizar una tarea
        PATCH /api/tasks/{id}/ - Actualización parcial
        DELETE /api/tasks/{id}/ - Eliminar una tarea
        PATCH /api/tasks/{id}/toggle_completion/ - Cambiar estado
    """
    
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    
    def get_serializer_class(self):
        """
        Retorna el serializador apropiado según la acción.
        
        Principio: Usar serializadores específicos para cada operación.
        """
        if self.action in ['create', 'update', 'partial_update']:
            return TaskCreateUpdateSerializer
        return TaskSerializer
    
    def create(self, request, *args, **kwargs):
        """
        Crea una nueva tarea.
        
        Principio OCP: Extendido con lógica personalizada.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        # Retornar el objeto completo con el serializador de lectura
        task = Task.objects.get(pk=serializer.instance.pk)
        read_serializer = TaskSerializer(task)
        return Response(read_serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        """
        Actualiza una tarea existente.
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=partial
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        # Retornar el objeto completo con el serializador de lectura
        task = Task.objects.get(pk=instance.pk)
        read_serializer = TaskSerializer(task)
        return Response(read_serializer.data)
    
    @action(detail=True, methods=['patch'])
    def toggle_completion(self, request, pk=None):
        """
        Alterna el estado de completación de una tarea.
        
        Endpoint: PATCH /api/tasks/{id}/toggle_completion/
        """
        task = self.get_object()
        
        if task.completed:
            task.mark_as_incomplete()
        else:
            task.mark_as_completed()
        
        serializer = TaskSerializer(task)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        """
        Retorna solo las tareas incompletas.
        
        Endpoint: GET /api/tasks/active/
        """
        tasks = self.queryset.filter(completed=False)
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def completed(self, request):
        """
        Retorna solo las tareas completadas.
        
        Endpoint: GET /api/tasks/completed/
        """
        tasks = self.queryset.filter(completed=True)
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_priority(self, request):
        """
        Retorna tareas ordenadas por prioridad.
        
        Endpoint: GET /api/tasks/by_priority/?priority=1,2,3
        """
        priority = request.query_params.get('priority')
        if priority:
            try:
                priorities = [int(p) for p in priority.split(',')]
                tasks = self.queryset.filter(priority__in=priorities).order_by('-priority')
                serializer = self.get_serializer(tasks, many=True)
                return Response(serializer.data)
            except ValueError:
                return Response(
                    {'error': 'Prioridades inválidas'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        return Response(
            {'error': 'El parámetro priority es requerido'},
            status=status.HTTP_400_BAD_REQUEST
        )
