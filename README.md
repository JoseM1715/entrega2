# Simulador de Ahorro Programado (Entrega 2)

Aplicación web de tres capas: **frontend**, **backend** y **base de datos**, orquestadas con Docker Compose.
Calcula la cuota mensual que se debe ahorrar para llegar a una meta (interés compuesto 0,75 % mensual, con abono extra opcional) y la guarda en PostgreSQL.

## Integrantes
| Nombre | Rol |
|---|---|
| Jose Angel Sanchez | Backend |
| Valentina Mesa| Frontend |
| Francisco Gomez | Base de datos / DevOps |

## Tipo de aplicación y tecnologías

| Componente | Tipo | Tecnología | Versión |
|---|---|---|---|
| frontend | Aplicación web estática (HTML + CSS + JavaScript) | nginx | 1.27 |
| backend | API REST con Swagger/OpenAPI | Python / Flask / gunicorn | 3.12 / 3.x / 22+ |
| backend | Driver de BD | psycopg2-binary | 2.9.x |
| base de datos | Relacional | PostgreSQL | 16 |
| orquestación | Contenedores | Docker + Docker Compose | Docker Desktop reciente |
| pruebas | Unitarias / E2E | unittest y pytest / Playwright | pytest 9.1.1 / Playwright 1.56.0 |

## Repositorios
- Monorepo (este): https://github.com/JoseM1715/entrega2
- Backend: https://github.com/JoseM1715/entrega2-backend
- Frontend: https://github.com/ValenMJ-02/entrega2-frontend.git

## Imágenes en DockerHub
- https://hub.docker.com/r/USUARIO_DOCKERHUB/entrega2-backend
- https://hub.docker.com/r/USUARIO_DOCKERHUB/entrega2-frontend

## Requisitos
- Git
- Docker Desktop (abierto y corriendo)
- Puertos libres: 8080 (frontend) y 5000 (backend)
- Solo para las pruebas: Python 3.12+

## Cómo descargar

**Opción A: clonar con git** (frontend y backend son submódulos, por eso `--recurse-submodules`):
```
git clone --recurse-submodules https://github.com/JoseM1715/entrega2.git
cd entrega2
```
Si ya clonó sin esa opción: `git submodule update --init --recursive`

**Opción B: imágenes de DockerHub** (sin código fuente): descargue solo `docker-compose.yml` y `.env.example` y use `docker compose pull`.

## Cómo instalar y ejecutar
1. Copie las variables de entorno y edítelas (contraseñas y su usuario de DockerHub):
   ```
   copy .env.example .env
   ```
   (Linux/Mac: `cp .env.example .env`)
2. Construya y levante todo:
   ```
   docker compose up --build
   ```
   O con las imágenes de DockerHub: `docker compose pull` y luego `docker compose up --no-build`.
3. Abra:
   - Aplicación: http://localhost:8080
   - Swagger (documentación de la API): http://localhost:5000/docs
4. Para apagar: `docker compose down` (agregue `-v` para borrar también la base de datos).

El servicio `seed` crea las tablas y carga el usuario admin, la tabla maestra de parámetros y datos de ejemplo (se puede repetir sin duplicar).

## Pruebas
**Unitarias del backend** (las de `test_db.py` necesitan PostgreSQL; las demás no):
```
cd backend
pip install -r requirements-dev.txt
python -m pytest src/tests
```
**Playwright (end-to-end)**, con el sistema corriendo (`docker compose up -d --build`):
```
pip install -r e2e/requirements.txt
playwright install chromium
pytest e2e
```

## Estructura
```
entrega2/
├── docker-compose.yml
├── .env.example
├── README.md
├── docs/historias_de_usuario.md
├── e2e/                 pruebas Playwright
├── frontend/            (submódulo) Dockerfile, .dockerignore, src/
└── backend/             (submódulo) Dockerfile, .dockerignore, src/, sql/
```

## Historias de usuario
Ver [docs/historias_de_usuario.md](docs/historias_de_usuario.md).
