"""
Serializadores para la API REST.
Implementando principios SOLID para separación de responsabilidades.
"""
from rest_framework import serializers
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    """
    Serializador para convertir instancias de Task a JSON.
    
    Responsabilidad: Convertir entre objetos Python y JSON.
    Principio SRP: Solo se encarga de la serialización.
    """
    priority_display = serializers.CharField(
        source='get_priority_display_name',
        read_only=True
    )
    
    class Meta:
        model = Task
        fields = [
            'id',
            'title',
            'description',
            'completed',
            'priority',
            'priority_display',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['created_at', 'updated_at', 'id']


class TaskCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Serializador especializado para creación y actualización de tareas.
    
    Implementa validación específica para operaciones de escritura.
    """
    
    class Meta:
        model = Task
        fields = ['title', 'description', 'completed', 'priority']
    
    def validate_title(self, value):
        """Valida que el título no esté vacío y tenga longitud mínima."""
        if not value or not value.strip():
            raise serializers.ValidationError("El título no puede estar vacío.")
        if len(value.strip()) < 3:
            raise serializers.ValidationError("El título debe tener al menos 3 caracteres.")
        return value.strip()
    
    def validate_priority(self, value):
        """Valida que la prioridad sea válida."""
        if value not in [1, 2, 3]:
            raise serializers.ValidationError("La prioridad debe ser 1, 2 o 3.")
        return value
