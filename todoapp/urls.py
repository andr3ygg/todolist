"""
URLs para la aplicación todoapp.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet

# Router para los ViewSets
router = DefaultRouter()
router.register(r'tasks', TaskViewSet)

app_name = 'todoapp'

urlpatterns = [
    path('', include(router.urls)),
]
