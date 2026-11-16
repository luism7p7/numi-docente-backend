"""Backend del panel docente de Numi (Flask + MySQL).

Solo expone la API JSON en /api/... que usa js/app.js del repositorio
numi-docente-frontend, más el puente con la app en /api/app/v1/...
Las páginas las entrega Nginx, que pregunta a /api/sesion antes de abrir una privada.
"""

from flask import Flask, request, session
from werkzeug.exceptions import HTTPException

from . import auth, gestion, puente_app, reportes, seguimiento
from .config import Config
from .db import cerrar_db
from .utilidades import ErrorDeDatos, error

# Endpoints de la API que no piden sesión
API_PUBLICA = {"auth.login", "logout"}


def create_app(config_extra=None):
    app = Flask(__name__, static_folder=None)
    app.config.from_object(Config)
    if config_extra:
        app.config.update(config_extra)

    app.teardown_appcontext(cerrar_db)
    for modulo in (auth, seguimiento, reportes, gestion, puente_app):
        app.register_blueprint(modulo.bp)

    @app.before_request
    def exigir_sesion():
        # El puente con la app usa su propia clave (ver puente_app.py)
        if "usuario_id" in session or request.path.startswith("/api/app/"):
            return None
        if request.path.startswith("/api/") and request.endpoint not in API_PUBLICA:
            return error("Tu sesión terminó. Vuelve a iniciar sesión.", 401)
        return None

    @app.errorhandler(ErrorDeDatos)
    def datos_invalidos(e):
        return error(e.mensaje, e.codigo)

    @app.errorhandler(HTTPException)
    def error_http(e):
        if request.path.startswith("/api/"):
            return error(e.description, e.code)
        return e

    @app.get("/api/sesion")
    def sesion():
        # Nginx (auth_request) pregunta aquí antes de entregar una página privada
        return "", 204

    @app.post("/api/logout")
    def logout():
        session.clear()
        return "", 204

    return app
