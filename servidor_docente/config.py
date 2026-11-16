"""Configuración del panel docente, leída de variables de entorno (.env)."""

import os
from pathlib import Path

from dotenv import load_dotenv

# Raíz del repositorio (aquí va el .env cuando se corre sin Docker)
RAIZ = Path(__file__).resolve().parent.parent
load_dotenv(RAIZ / ".env")


class Config:
    SECRET_KEY = os.environ.get("DOCENTE_SECRET_KEY") or "solo-para-desarrollo-docente"

    # Cookie distinta a la del panel administrativo (ver servidor_admin/config.py)
    SESSION_COOKIE_NAME = "numi_docente_session"
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    # En el servidor (HTTPS) la cookie solo viaja cifrada: SESSION_COOKIE_SECURE=1
    SESSION_COOKIE_SECURE = os.environ.get("SESSION_COOKIE_SECURE") == "1"

    DB_HOST = os.environ.get("DB_HOST", "127.0.0.1")
    DB_PORT = int(os.environ.get("DB_PORT", "3306"))
    DB_USER = os.environ.get("DB_USER", "root")
    DB_PASSWORD = os.environ.get("DB_PASSWORD", "")
    DB_NAME = os.environ.get("DB_NAME", "numi")

    # Backend de la app Numi: de aquí sale la versión del paquete de conocimiento
    APP_API_URL = os.environ.get("APP_API_URL", "").rstrip("/")
    # Clave que debe enviar el backend de la app para usar /api/app/v1/...
    APP_API_KEY = os.environ.get("APP_API_KEY", "")

    # Imágenes, audios y videos que sube o importa el panel administrativo (se los entrega a la app)
    CARPETA_UPLOADS = Path(os.environ.get("UPLOADS_DIR") or RAIZ / "uploads")
