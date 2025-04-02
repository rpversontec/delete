# backend/app/database.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
# Útil para desarrollo local, opcional en producción si la variable ya está
from dotenv import load_dotenv

# Cargar variables de entorno desde un archivo .env (útil para desarrollo local)
# En producción con Coolify, la variable DATABASE_URL ya debería estar disponible
load_dotenv()

# Obtener la URL de la base de datos desde la variable de entorno
DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL is None:
    # Si no se encuentra la variable, puedes poner un valor por defecto o lanzar un error
    # Para PostgreSQL, la URL suele ser "postgresql://user:password@host:port/database"
    print("Advertencia: Variable de entorno DATABASE_URL no encontrada.")
    # Podrías asignar una URL de fallback para desarrollo local si no usas .env
    # DATABASE_URL = "postgresql://user:password@localhost/db_name"
    # O simplemente dejar que falle si es requerida:
    raise ValueError("La variable de entorno DATABASE_URL es requerida.")
elif DATABASE_URL.startswith("postgres://"):
    # SQLAlchemy 1.4+ recomienda usar "postgresql://" en lugar de "postgres://"
    # Heroku y otros a veces dan "postgres://", hacemos el reemplazo por si acaso.
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)


# Crear el motor de SQLAlchemy
# pool_pre_ping es bueno para verificar conexiones antes de usarlas
# echo=True es útil para debugging, muestra las queries SQL generadas (quítalo en prod)
engine = create_engine(DATABASE_URL, pool_pre_ping=True)  # , echo=True)


# Crear una fábrica de sesiones (SessionLocal)
# Esta es la línea clave que define SessionLocal
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Crear una clase Base para que tus modelos la hereden
Base = declarative_base()
