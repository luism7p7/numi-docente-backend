# Numi · Panel docente · Backend

API del panel docente de **Numi** (Python 3.12, Flask 3, MySQL 8 con PyMySQL, openpyxl y fpdf2) y puente con
el backend de la app.

- **Frontend:** [numi-docente-frontend](https://github.com/luism7p7/numi-docente-frontend)
- **Base de datos y despliegue:** [numi-admin-backend](https://github.com/luism7p7/numi-admin-backend) (`database/` y `despliegue/`)
- **En producción:** https://numi-g01.northcentralus.cloudapp.azure.com:8443

## Estructura

```
├── servidor_docente/   # blueprints: auth, seguimiento, reportes, gestion, puente_app
├── tests/              # pytest (usan database/ de numi-admin-backend clonado al lado)
├── app.py              # python app.py -> http://localhost:5001 (solo la API)
├── Dockerfile          # imagen con Gunicorn
└── .env.example
```

## Despliegue

En la VM de Azure este backend corre como el servicio `docente-backend` de
`numi-admin-backend/despliegue/compose.yaml`: Gunicorn en el puerto 5001, sin puertos publicados. Nginx lo
alcanza por la red interna de Docker y lo expone solo en https://numi-g01.northcentralus.cloudapp.azure.com:8443/api/.

## Probarlo en local (sin Docker)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env        # misma base que numi-admin-backend
python app.py                      # API en http://localhost:5001/api/...
```

Cuenta de ejemplo: `luisa.munoz@ielaaldea.edu.co` (docente de 3° A, 4° B y 5° A).

## API

| Método | URL | Qué hace |
|--------|-----|----------|
| GET | `/api/sesion` | 204 si hay sesión, 401 si no (lo usa Nginx con auth_request) |
| POST | `/api/logout` | Cierra la sesión |


| Pantalla | Endpoints |
|----------|-----------|
| Login, perfil, Mis datos | `POST /api/login`, `GET /api/me`, `POST /api/grupo-activo` |
| Panel | `GET /api/panel` |
| Estudiantes | `GET /api/estudiantes`, `GET /api/estudiantes/<id>`, `PUT /api/estudiantes/<id>/nota`, `GET /api/estudiantes/exportar`, `GET /api/estudiantes/<id>/informe` |
| Actividades | `GET /api/actividades`, `PATCH /api/actividades/<id>` |
| Reportes | `GET /api/reportes?periodo=`, `GET /api/reportes/descargar` |
| Gestión | `GET /api/gestion`, `POST /api/gestion/codigo`, `PATCH /api/gestion/ia`, `POST /api/gestion/paquete` |

**Puente con la app** (cabecera `X-Api-Key: <APP_API_KEY>`, lo llama el backend de la app, nunca el celular)

| Método | URL | Qué hace |
|--------|-----|----------|
| POST | `/api/app/v1/unirse` | `{uid, nombre, codigo}`: el niño entra al grupo con el código del docente |
| GET | `/api/app/v1/actividades?uid=` | Actividades publicadas y activas para el grupo del niño |
| PUT | `/api/app/v1/progreso` | `{uid, version_app, racha_dias, items[]}`: mismo formato que `/api/v1/me/progreso` de la app |
## Equipo

- Luis Miguel Muñoz Rendón
- Alexander Mejía Ospina
- Santiago Mayorga Hueso
- Santiago Rodríguez Jiménez

Proyecto Numi · Universidad Cooperativa de Colombia, sede Medellín.
