"""
Configuración de admin para la aplicación de tareas.
"""
from django.contrib import admin
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """
    Administrador de tareas con interfaz personalizada.
    """
    list_display = ('title', 'completed', 'priority', 'created_at')
    list_filter = ('completed', 'priority', 'created_at')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Información General', {
            'fields': ('title', 'description', 'priority')
        }),
        ('Estado', {
            'fields': ('completed',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['mark_as_completed', 'mark_as_incomplete']
    
    def mark_as_completed(self, request, queryset):
        """Acción para marcar tareas como completadas."""
        updated = queryset.update(completed=True)
        self.message_user(request, f'{updated} tarea(s) marcada(s) como completada(s).')
    mark_as_completed.short_description = "Marcar como completada"
    
    def mark_as_incomplete(self, request, queryset):
        """Acción para marcar tareas como incompletas."""
        updated = queryset.update(completed=False)
        self.message_user(request, f'{updated} tarea(s) marcada(s) como incompleta(s).')
    mark_as_incomplete.short_description = "Marcar como incompleta"
