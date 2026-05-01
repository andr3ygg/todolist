"""
Archivo apps.py para la configuración de la aplicación.
"""
from django.apps import AppConfig


class TodoappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'todoapp'
    verbose_name = 'Aplicación de Tareas'
