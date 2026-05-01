"""
Models para la aplicación TODO.
Utilizando OOP y principios SOLID.
"""
from django.db import models
from django.utils import timezone


class Task(models.Model):
    """
    Modelo que representa una tarea.
    
    Atributos:
        title: Título de la tarea
        description: Descripción detallada de la tarea
        completed: Estado de completación
        created_at: Fecha de creación
        updated_at: Fecha de última actualización
        priority: Prioridad de la tarea (1-3)
    """
    
    PRIORITY_CHOICES = [
        (1, 'Baja'),
        (2, 'Media'),
        (3, 'Alta'),
    ]
    
    title = models.CharField(
        max_length=255,
        verbose_name="Título"
    )
    description = models.TextField(
        blank=True,
        default='',
        verbose_name="Descripción"
    )
    completed = models.BooleanField(
        default=False,
        verbose_name="Completada"
    )
    priority = models.IntegerField(
        choices=PRIORITY_CHOICES,
        default=2,
        verbose_name="Prioridad"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de creación"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Fecha de actualización"
    )
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Tarea"
        verbose_name_plural = "Tareas"
    
    def __str__(self):
        return self.title
    
    def mark_as_completed(self):
        """Marca la tarea como completada."""
        self.completed = True
        self.save()
    
    def mark_as_incomplete(self):
        """Marca la tarea como incompleta."""
        self.completed = False
        self.save()
    
    def update_priority(self, priority):
        """
        Actualiza la prioridad de la tarea.
        
        Args:
            priority: Valor de prioridad (1-3)
        """
        if priority in dict(self.PRIORITY_CHOICES):
            self.priority = priority
            self.save()
    
    def get_priority_display_name(self):
        """Retorna el nombre legible de la prioridad."""
        return dict(self.PRIORITY_CHOICES).get(self.priority, 'Desconocida')
