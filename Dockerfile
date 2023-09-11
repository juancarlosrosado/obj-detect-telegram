# syntax=docker/dockerfile:1

# Utilizamos la imagen base de Python
ARG PYTHON_VERSION=3.10.12
FROM python:${PYTHON_VERSION}-slim as base

# Prevenimos que Python escriba archivos pyc
ENV PYTHONDONTWRITEBYTECODE=1

# Evitamos el almacenamiento en búfer de la salida estándar y de error de Python
ENV PYTHONUNBUFFERED=1

# Establecemos el directorio de trabajo en /app
WORKDIR /app

# Creamos un usuario no privilegiado que ejecutará la aplicación
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

# Descargamos las dependencias como un paso separado para aprovechar la caché de Docker
# Usamos un montaje de caché a /root/.cache/pip para acelerar las compilaciones posteriores
# Usamos un montaje de enlace a requirements.txt para evitar tener que copiarlos en esta capa
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install -r requirements.txt

# Instalamos libgl1-mesa-glx y libglib2.0-0
RUN apt-get update && apt-get install -y libgl1-mesa-glx libglib2.0-0

# Creamos el directorio para las fotos y establecemos los permisos
RUN mkdir -p /app/telegram_photos && chown -R appuser:appuser /app/telegram_photos
RUN mkdir /app/predictions && chown -R appuser:appuser /app/predictions

# Copiamos el código fuente dentro del contenedor
COPY src/ /app/
COPY .env /app/.env
COPY runs/ /app/runs/

# Concedemos permisos de ejecución al archivo main.py
RUN chmod +x /app/main.py

# Cambiamos al usuario no privilegiado para ejecutar la aplicación
USER appuser

# Ejecutamos la aplicación
ENTRYPOINT ["python", "/app/main.py"]
