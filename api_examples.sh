#!/bin/bash

# Script de ejemplo de uso de la API

BASE_URL="http://localhost:8000/api/tasks"

echo "📚 Ejemplos de uso de la API TODO List"
echo "======================================"
echo ""

# 1. Obtener todas las tareas
echo "1️⃣ Obtener todas las tareas"
echo "GET $BASE_URL/"
echo ""
curl -X GET "$BASE_URL/" \
  -H "Content-Type: application/json" | python3 -m json.tool
echo ""
echo "---"
echo ""

# 2. Crear una nueva tarea
echo "2️⃣ Crear una nueva tarea"
echo "POST $BASE_URL/"
echo ""
curl -X POST "$BASE_URL/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Aprender SOLID",
    "description": "Estudiar los principios SOLID en profundidad",
    "priority": 3,
    "completed": false
  }' | python3 -m json.tool
echo ""
echo "---"
echo ""

# 3. Obtener tareas activas (sin completar)
echo "3️⃣ Obtener tareas activas"
echo "GET $BASE_URL/active/"
echo ""
curl -X GET "$BASE_URL/active/" \
  -H "Content-Type: application/json" | python3 -m json.tool
echo ""
echo "---"
echo ""

# 4. Obtener tareas completadas
echo "4️⃣ Obtener tareas completadas"
echo "GET $BASE_URL/completed/"
echo ""
curl -X GET "$BASE_URL/completed/" \
  -H "Content-Type: application/json" | python3 -m json.tool
echo ""
echo "---"
echo ""

# 5. Obtener tarea específica (asume ID 1)
echo "5️⃣ Obtener tarea específica (ID 1)"
echo "GET $BASE_URL/1/"
echo ""
curl -X GET "$BASE_URL/1/" \
  -H "Content-Type: application/json" | python3 -m json.tool
echo ""
echo "---"
echo ""

# 6. Actualizar tarea (asume ID 1)
echo "6️⃣ Actualizar tarea (ID 1)"
echo "PUT $BASE_URL/1/"
echo ""
curl -X PUT "$BASE_URL/1/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Aprender SOLID - Actualizado",
    "description": "Estudiar y aplicar SOLID en proyectos reales",
    "priority": 2,
    "completed": false
  }' | python3 -m json.tool
echo ""
echo "---"
echo ""

# 7. Actualización parcial (asume ID 1)
echo "7️⃣ Actualización parcial (solo prioridad, ID 1)"
echo "PATCH $BASE_URL/1/"
echo ""
curl -X PATCH "$BASE_URL/1/" \
  -H "Content-Type: application/json" \
  -d '{
    "priority": 1
  }' | python3 -m json.tool
echo ""
echo "---"
echo ""

# 8. Cambiar estado de completación (asume ID 1)
echo "8️⃣ Cambiar estado de completación (ID 1)"
echo "PATCH $BASE_URL/1/toggle_completion/"
echo ""
curl -X PATCH "$BASE_URL/1/toggle_completion/" \
  -H "Content-Type: application/json" | python3 -m json.tool
echo ""
echo "---"
echo ""

# 9. Obtener tareas por prioridad
echo "9️⃣ Obtener tareas de prioridad alta (3)"
echo "GET $BASE_URL/by_priority/?priority=3"
echo ""
curl -X GET "$BASE_URL/by_priority/?priority=3" \
  -H "Content-Type: application/json" | python3 -m json.tool
echo ""
echo "---"
echo ""

# 10. Eliminar tarea (asume ID 1)
echo "🔟 Eliminar tarea (ID 1)"
echo "DELETE $BASE_URL/1/"
echo ""
curl -X DELETE "$BASE_URL/1/" \
  -H "Content-Type: application/json" \
  -w "\nEstado HTTP: %{http_code}\n"
echo ""
