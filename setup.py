"""
Script para inicializar y configurar la aplicación
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'todoproject.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

django.setup()

if __name__ == '__main__':
    print("✅ Django está configurado correctamente")
    print("\n📋 Próximos pasos:")
    print("1. Ejecutar migraciones: python manage.py migrate")
    print("2. Crear superusuario: python manage.py createsuperuser")
    print("3. Iniciar servidor: python manage.py runserver")
    print("\n🌐 La aplicación estará disponible en: http://localhost:8000")
