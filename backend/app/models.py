# backend/app/models.py

from typing import Optional  # Para campos opcionales en la actualización
from datetime import datetime  # Para los tipos de fecha/hora en los esquemas
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, text
from sqlalchemy.sql import func  # Para usar funciones SQL como CURRENT_TIMESTAMP
from .database import Base  # Importamos la Base declarativa desde database.py

# --- Modelo SQLAlchemy ---
# Esta clase representa la tabla 'todos' en tu base de datos


class Todo(Base):
    __tablename__ = "todos"  # Nombre exacto de la tabla en la BD

    # Mapeo de las columnas de la tabla a atributos de la clase
    # Llave primaria, indexada
    id = Column(Integer, primary_key=True, index=True)
    # Texto de la tarea, no puede ser nulo
    task = Column(String, nullable=False)
    # Estado, default false, no nulo
    is_completed = Column(Boolean, server_default='false', nullable=False)

    # Usamos server_default con text() para definir valores por defecto a nivel de base de datos
    # TIMESTAMP(timezone=True) es bueno para PostgreSQL
    created_at = Column(TIMESTAMP(timezone=True),
                        server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(
    ), onupdate=func.now(), nullable=False)
    # Nota sobre onupdate: SQLAlchemy intenta manejar esto, pero para PostgreSQL
    # la actualización automática de 'updated_at' a menudo requiere un TRIGGER en la BD
    # o manejarlo explícitamente en la lógica de tu API al actualizar un registro.
    # Para empezar, la lógica de la API es más simple.


# --- Modelos Pydantic (Esquemas) ---
# Estos modelos son usados por FastAPI para validar datos de entrada (request body)
# y para dar formato a los datos de salida (response body).


# Esquema base con campos comunes (opcional, pero buena práctica)

class TodoBase(BaseModel):
    task: str
    # Default a False si no se provee al crear
    is_completed: Optional[bool] = False

# Esquema para crear un nuevo Todo (lo que se espera en el body de un POST)


class TodoCreate(TodoBase):
    pass  # Hereda 'task' y 'is_completed' de TodoBase

# Esquema para actualizar un Todo (lo que se espera en el body de un PUT/PATCH)
# Todos los campos son opcionales en la actualización


class TodoUpdate(BaseModel):
    task: Optional[str] = None
    is_completed: Optional[bool] = None

# Esquema para leer/devolver un Todo desde la API (lo que se envía en el response body)
# Incluye campos que genera la base de datos como 'id' y timestamps


class TodoSchema(TodoBase):
    id: int
    created_at: datetime
    updated_at: datetime

    # Configuración para decirle a Pydantic que lea datos
    # incluso si no son un diccionario, sino un objeto ORM (como nuestro modelo Todo)
    class Config:
        orm_mode = True  # En Pydantic V2 se llama: from_attributes = True
