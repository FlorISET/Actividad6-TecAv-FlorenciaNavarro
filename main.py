# main.py
from fastapi import FastAPI, HTTPException, Query, Depends
from fastapi.responses import JSONResponse
from typing import List, Optional
import uvicorn
from database import eventos_db, asistentes_db, comentarios_db
from schemas import (
    Evento, EventoCreate, EventoUpdate, Asistente, Comentario,
    PaginationMeta, EventoBase
)

app = FastAPI(
    title="EventHub API",
    version="1.0.0",
    description="API RESTful para gestión de eventos"
)

# Simulación de autenticación
def require_auth():
    raise HTTPException(status_code=401, detail={"error": {"code": "UNAUTHORIZED", "message": "Token de autenticación requerido"}})

# --- ENDPOINTS ---

@app.get("/v1/eventos", response_model=dict, tags=["Eventos"])
def listar_eventos(
    ubicacion: Optional[str] = Query(None),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    auth: None = Depends(require_auth)
):
    eventos = list(eventos_db.values())
    if ubicacion:
        eventos = [e for e in eventos if e["ubicacion"] == ubicacion]
    
    total = len(eventos)
    eventos_paginados = eventos[offset:offset + limit]
    has_more = (offset + limit) < total

    return {
        "meta": {"total": total, "limit": limit, "offset": offset, "has_more": has_more},
        "data": eventos_paginados
    }

@app.post("/v1/eventos", status_code=201, response_model=Evento, tags=["Eventos"])
def crear_evento(evento: EventoCreate, auth: None = Depends(require_auth)):
    if not evento.fecha:
        raise HTTPException(status_code=400, detail={"error": {"code": "BAD_REQUEST", "message": "El campo 'fecha' es obligatorio"}})
    
    nuevo_id = max(eventos_db.keys(), default=0) + 1
    nuevo_evento = evento.dict()
    nuevo_evento["id"] = nuevo_id
    eventos_db[nuevo_id] = nuevo_evento
    return nuevo_evento

@app.get("/v1/eventos/{evento_id}", response_model=Evento, tags=["Eventos"])
def obtener_evento(evento_id: int, auth: None = Depends(require_auth)):
    if evento_id not in eventos_db:
        raise HTTPException(status_code=404, detail="Evento no encontrado")
    return eventos_db[evento_id]

@app.patch("/v1/eventos/{evento_id}", response_model=Evento, tags=["Eventos"])
def actualizar_evento(evento_id: int, update: EventoUpdate, auth: None = Depends(require_auth)):
    if evento_id not in eventos_db:
        raise HTTPException(status_code=404, detail="Evento no encontrado")
    datos = update.dict(exclude_unset=True)
    eventos_db[evento_id].update(datos)
    return eventos_db[evento_id]

@app.delete("/v1/eventos/{evento_id}", status_code=204, tags=["Eventos"])
def eliminar_evento(evento_id: int, auth: None = Depends(require_auth)):
    if evento_id not in eventos_db:
        raise HTTPException(status_code=404, detail="Evento no encontrado")
    del eventos_db[evento_id]
    asistentes_db.pop(evento_id, None)
    comentarios_db.pop(evento_id, None)
    return JSONResponse(status_code=204, content=None)

# --- ASISTENTES ---
@app.get("/v1/eventos/{evento_id}/asistentes", response_model=List[Asistente], tags=["Asistentes"])
def listar_asistentes(evento_id: int, limit: int = 10, offset: int = 0, order: str = "nombre", auth: None = Depends(require_auth)):
    if evento_id not in eventos_db:
        raise HTTPException(status_code=404, detail="Evento no encontrado")
    asistentes = asistentes_db.get(evento_id, [])
    if order == "nombre":
        asistentes = sorted(asistentes, key=lambda x: x["nombre"])
    return asistentes[offset:offset + limit]

@app.post("/v1/eventos/{evento_id}/asistentes", response_model=Asistente, tags=["Asistentes"])
def registrar_asistente(evento_id: int, asistente: dict, auth: None = Depends(require_auth)):
    if evento_id not in eventos_db:
        raise HTTPException(status_code=404, detail="Evento no encontrado")
    nuevo_id = max((a["id"] for a in asistentes_db.get(evento_id, [])), default=0) + 1
    nuevo = {"id": nuevo_id, **asistente}
    asistentes_db.setdefault(evento_id, []).append(nuevo)
    return nuevo

# --- COMENTARIOS ---
@app.get("/v1/eventos/{evento_id}/comentarios", response_model=List[Comentario], tags=["Comentarios"])
def listar_comentarios(evento_id: int, limit: int = 10, offset: int = 0, auth: None = Depends(require_auth)):
    if evento_id not in eventos_db:
        raise HTTPException(status_code=404, detail="Evento no encontrado")
    comentarios = comentarios_db.get(evento_id, [])
    return comentarios[offset:offset + limit]

@app.post("/v1/eventos/{evento_id}/comentarios", response_model=Comentario, tags=["Comentarios"])
def crear_comentario(evento_id: int, comentario: dict, auth: None = Depends(require_auth)):
    if evento_id not in eventos_db:
        raise HTTPException(status_code=404, detail="Evento no encontrado")
    nuevo_id = max((c["id"] for c in comentarios_db.get(evento_id, [])), default=0) + 1
    nuevo = {"id": nuevo_id, **comentario}
    comentarios_db.setdefault(evento_id, []).append(nuevo)
    return nuevo

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
