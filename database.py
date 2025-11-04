
# database.py
from typing import List, Dict

# Simulación de DB
eventos_db = {}
asistentes_db = {}  # {evento_id: [asistentes]}
comentarios_db = {}  # {evento_id: [comentarios]}

# Datos de ejemplo
eventos_db[42] = {
    "id": 42,
    "nombre": "Conferencia de IA 2025",
    "fecha": "2025-06-15T09:00:00Z",
    "ubicacion": "Buenos Aires",
    "organizador": "TechCorp"
}

asistentes_db[42] = [
    {"id": 1, "nombre": "Ana Gómez", "email": "ana@example.com"},
    {"id": 2, "nombre": "Luis Pérez", "email": "luis@example.com"}
]

comentarios_db[42] = [
    {"id": 1, "usuario": "Ana", "texto": "¡Excelente evento!", "puntuacion": 5},
    {"id": 2, "usuario": "Luis", "texto": "Muy buen contenido.", "puntuacion": 4}
]
