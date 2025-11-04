
EventHub API - Actividad Práctica 2do Parcial

API RESTful para gestión de eventos, asistentes y comentarios. =)


Endpoints Implementados

|   | Endpoint | Método | Descripción |
|---|----------|--------|-------------|
| 1 | `/v1/eventos` | GET | Lista con paginación y filtro |
| 2 | `/v1/eventos` | POST | Crear evento |
| 3 | `/v1/eventos/42` | GET | Detalle |
| 4 | `/v1/eventos/42` | PATCH | Actualizar parcial |
| 5 | `/v1/eventos/42` | DELETE | Eliminar |
| 6 | `/v1/eventos/42/asistentes` | GET | Lista con orden |
| 7 | `/v1/eventos/42/comentarios` | GET | Paginación |
| 8 | `/v1/eventos/42/asistentes` | POST | Registrar |
| 9 | `/v1/eventos/42/comentarios` | POST | Comentar |


Errores
- `400`: Campo obligatorio faltante
- `404`: Recurso no encontrado
- `401`: Sin autenticación
 

Cómo ejecutar (en bash)

-- en el caso que salga error probar con pip3 (python 3)

```bash
pip install -r requirements.txt 
uvicorn main:app --reload


Accede a: http://127.0.0.1:8000/docs (Swagger UI)
