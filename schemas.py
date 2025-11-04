
# schemas.py
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class EventoBase(BaseModel):
    nombre: str
    fecha: str  # ISO 8601
    ubicacion: Optional[str] = None
    organizador: Optional[str] = None

class EventoCreate(EventoBase):
    pass

class EventoUpdate(BaseModel):
    nombre: Optional[str] = None
    fecha: Optional[str] = None

class Evento(EventoBase):
    id: int
    class Config:
        from_attributes = True

class Asistente(BaseModel):
    id: int
    nombre: str
    email: str

class Comentario(BaseModel):
    id: int
    usuario: str
    texto: str
    puntuacion: int

class PaginationMeta(BaseModel):
    total: int
    limit: int
    offset: int
    has_more: bool

