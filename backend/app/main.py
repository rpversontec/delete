from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from . import models, database
from .database import SessionLocal, engine
from typing import List
from fastapi.middleware.cors import CORSMiddleware  # Importar CORS

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Configurar CORS para permitir solicitudes desde el frontend
# Ajusta origins según la URL de tu frontend en Coolify
origins = [
    # Para desarrollo local si aplica
    "http://k4csg48gko88ssks080c4k0w.20.55.28.0.sslip.io/",
    "http://tu-frontend-url.coolify.app",
    "https://k4csg48gko88ssks080c4k0w.20.55.28.0.sslip.io/"
    "http://localhost",  # URL del frontend desplegado
    "https://tu-frontend-url.coolify.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get DB session


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/todos/", response_model=List[models.TodoSchema])
def read_todos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    todos = db.query(models.Todo).offset(skip).limit(limit).all()
    return todos


@app.post("/todos/", response_model=models.TodoSchema)
def create_todo(todo: models.TodoCreate, db: Session = Depends(get_db)):
    db_todo = models.Todo(task=todo.task)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

# Añadir endpoints para obtener uno, actualizar, eliminar...
