FROM python:3.9-slim

WORKDIR /code

# Cambia esta línea para apuntar a la ruta correcta desde la raíz del repo
COPY ./backend/requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Cambia esta línea para apuntar a la ruta correcta desde la raíz del repo
COPY ./backend/app /code/app

# Puerto que FastAPI usará (uvicorn)
EXPOSE 8000

# Comando para ejecutar la aplicación
# Escucha en 0.0.0.0 para ser accesible desde fuera del contenedor
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]