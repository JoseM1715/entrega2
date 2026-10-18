# Simulador de Ahorro Programado (Entrega 2)

Aplicación web de tres capas (**frontend**, **backend** y **base de datos**) que corre con **Docker Compose**.
Calcula la cuota mensual que hay que ahorrar para llegar a una meta (interés compuesto de 0,75 % mensual, con un abono extra opcional) y guarda cada meta en PostgreSQL.

## Contenido
1. [Integrantes](#integrantes)
2. [Cómo funciona](#cómo-funciona)
3. [Tecnologías y versiones](#tecnologías-y-versiones)
4. [Repositorios e imágenes de DockerHub](#repositorios-e-imágenes-de-dockerhub)
5. [Requisitos](#requisitos)
6. [Cómo descargar](#cómo-descargar)
7. [Cómo instalar y ejecutar](#cómo-instalar-y-ejecutar)
8. [Docker explicado](#docker-explicado)
9. [Datos iniciales (seeding)](#datos-iniciales-seeding)
10. [API y Swagger](#api-y-swagger)
11. [Pruebas](#pruebas)
12. [Publicar las imágenes en DockerHub](#publicar-las-imágenes-en-dockerhub)
13. [Problemas frecuentes](#problemas-frecuentes)
14. [Estructura del proyecto](#estructura-del-proyecto)
15. [Historias de usuario](#historias-de-usuario)

## Integrantes
| Nombre | Rol |
|---|---|
| Jose Angel Sanchez | Backend (API, Swagger, seeding) |
| Valentina Mesa | Frontend (página web y nginx) |
| Francisco Gomez | Base de datos, Docker Compose y DockerHub |

## Cómo funciona

```
 Navegador ──► frontend (nginx, :8080) ──/api/──► backend (Flask, :5000) ──► db (PostgreSQL, :5432)
                  página web                      calcula y guarda          guarda usuarios y metas
```

1. El usuario abre la página (http://localhost:8080), elige un usuario e ingresa meta, plazo y abono extra.
2. El **frontend** envía los datos a `/api/metas`. nginx reenvía todo lo que empiece por `/api/` al **backend**.
3. El **backend** valida los datos, calcula la cuota con la fórmula de anualidad de valor futuro y la guarda en la **base de datos**.
4. La página muestra la cuota y el ID de la meta, que luego se puede buscar.

## Tecnologías y versiones

| Componente | Tipo | Tecnología | Versión |
|---|---|---|---|
| frontend | Aplicación web estática (HTML + CSS + JavaScript) | nginx (imagen `nginx:1.27-alpine`) | 1.27 |
| backend | API REST con Swagger/OpenAPI | Python / Flask / gunicorn | 3.12 / 3.1.3 / 26.2.0 |
| backend | Driver de BD | psycopg2-binary | 2.9.13 |
| base de datos | Relacional | PostgreSQL (imagen `postgres:16-alpine`) | 16 |
| orquestación | Contenedores | Docker + Docker Compose | Docker Desktop reciente |
| pruebas | Unitarias / E2E | unittest y pytest / Playwright | pytest 9.1.1 / Playwright 1.56.0 |

## Repositorios e imágenes de DockerHub

Este es el **monorepo**: no contiene el código de la aplicación, solo enlaza (como *submódulos* de git) a los repositorios del backend y del frontend, y agrega el `docker-compose.yml`, las pruebas E2E y la documentación.

| Parte | Repositorio de GitHub | Imagen en DockerHub |
|---|---|---|
| Monorepo (este) | https://github.com/JoseM1715/entrega2 | |
| Backend | https://github.com/JoseM1715/entrega2-backend | https://hub.docker.com/r/josem1715/entrega2-backend (`josem1715/entrega2-backend:1.0.0`) |
| Frontend | https://github.com/ValenMJ-02/entrega2-frontend | https://hub.docker.com/r/josem1715/entrega2-frontend (`josem1715/entrega2-frontend:1.0.0`) |

## Requisitos
- **Git**
- **Docker Desktop**, abierto y corriendo (ícono verde)
- Puertos libres: **8080** (frontend) y **5000** (backend)
- Solo para las pruebas: **Python 3.11 o superior**

## Cómo descargar

**Opción A: clonar con git.** Frontend y backend son submódulos, por eso se usa `--recurse-submodules`:
```
git clone --recurse-submodules https://github.com/JoseM1715/entrega2.git
cd entrega2
```
Si ya clonó sin esa opción y las carpetas `backend` y `frontend` salen vacías:
```
git submodule update --init --recursive
```

**Opción B: imágenes de DockerHub** (sin código fuente):
```
docker pull josem1715/entrega2-backend:1.0.0
docker pull josem1715/entrega2-frontend:1.0.0
```
Para correr todo con esas imágenes descargue solo `docker-compose.yml` y `.env.example`, cree el `.env` (paso 1 de la siguiente sección) y use `docker compose pull` y `docker compose up --no-build`.

## Cómo instalar y ejecutar

1. **Cree el archivo `.env`** a partir del ejemplo (guarda las contraseñas y el usuario de DockerHub; no se sube a git):
   ```
   copy .env.example .env        (Windows)
   cp .env.example .env          (Linux / Mac)
   ```
   Ábralo (`notepad .env`) y revise estas variables:

   | Variable | Para qué sirve |
   |---|---|
   | `PG_DATABASE` | Nombre de la base de datos |
   | `PG_USER` | Usuario de PostgreSQL |
   | `PG_PASSWORD` | Contraseña de PostgreSQL |
   | `ADMIN_PASSWORD` | Contraseña del usuario `admin` que crea el seeding |
   | `DOCKERHUB_USER` | Su usuario de DockerHub (en minúsculas, **solo el nombre**, sin repetir `DOCKERHUB_USER=`) |
   | `VERSION` | Versión de las imágenes (`1.0.0`) |

2. **Construya y levante todo:**
   ```
   docker compose up --build
   ```
   La primera vez tarda unos minutos porque descarga imágenes. Para dejarlo corriendo en segundo plano use `docker compose up -d --build`.

3. **Abra:**
   - Aplicación: http://localhost:8080
   - Swagger (documentación de la API): http://localhost:5000/docs

4. **Para apagar:**
   ```
   docker compose down          (conserva los datos)
   docker compose down -v       (borra también la base de datos)
   ```

## Docker explicado

### Los servicios de `docker-compose.yml`

| Servicio | Imagen | Qué hace | Puerto |
|---|---|---|---|
| `db` | `postgres:16-alpine` | Base de datos PostgreSQL. Guarda los datos en el volumen `pgdata` para que no se pierdan al apagar. | interno (5432) |
| `seed` | la del backend | Crea las tablas y carga los datos iniciales. **Corre una vez y termina** (`Exited (0)` es lo normal). | — |
| `backend` | `josem1715/entrega2-backend` | API en Flask servida con gunicorn. | 5000 |
| `frontend` | `josem1715/entrega2-frontend` | nginx que sirve la página y reenvía `/api/` al backend. | 8080 (hacia el 80 del contenedor) |

### Orden de arranque
Compose espera a que cada servicio esté listo antes de iniciar el siguiente (usa *healthchecks*):

`db` (sano) → `seed` (terminado con éxito) → `backend` (sano) → `frontend`

Por eso, si algo falla al inicio, el servicio siguiente no arranca.

### Dockerfile del backend
Parte de `python:3.12-slim`, instala las dependencias primero (así Docker reutiliza esa capa si el código cambia), copia el código, corre como usuario no root y arranca `gunicorn` en el puerto 5000.

### Dockerfile del frontend
Parte de `nginx:1.27-alpine`, copia `nginx.conf` y la carpeta `src/` (la página). En `nginx.conf`, la regla `location /api/` envía las peticiones al servicio `backend:5000` (dentro de la red de Docker, los servicios se encuentran por su nombre).

### Comandos de Docker más útiles
| Comando | Qué hace |
|---|---|
| `docker compose up -d --build` | Construye y levanta todo en segundo plano |
| `docker compose ps -a` | Muestra el estado de cada servicio |
| `docker compose logs backend` | Muestra los mensajes del backend (cambie el nombre por `db`, `seed` o `frontend`) |
| `docker compose logs -f` | Sigue todos los mensajes en vivo (Ctrl+C para salir) |
| `docker compose restart backend` | Reinicia un servicio |
| `docker compose down` | Apaga y elimina los contenedores (conserva la base de datos) |
| `docker compose down -v` | Apaga y borra también la base de datos |

## Datos iniciales (seeding)
El servicio `seed` ejecuta `poblar_db.py`. Se puede repetir sin duplicar datos. Carga:
- **Usuario administrador** `admin` (admin@ahorro.local, rol `admin`). Su contraseña sale de `ADMIN_PASSWORD` y se guarda con hash. La web todavía no tiene pantalla de inicio de sesión.
- **Tabla maestra `parametros`** con la `tasa_mensual` (0,0075).
- **Datos de ejemplo:** dos usuarios (Miguel Angel y Jose Angel) y una meta de ahorro para cada uno.

## API y Swagger
Documentación interactiva: http://localhost:5000/docs (la especificación está en `/openapi.json`; necesita internet para cargar el diseño de Swagger).

| Método | Ruta | Descripción |
|---|---|---|
| GET | `/health` | Comprueba que el backend está vivo |
| GET | `/api/usuarios` | Lista los usuarios |
| POST | `/api/metas` | Calcula la cuota mensual y guarda la meta (201). Errores: 404 si el usuario no existe, 422 si los datos son inválidos |
| GET | `/api/metas/{id_meta}` | Busca una meta por su ID (404 si no existe) |

Ejemplo de cuerpo para `POST /api/metas`:
```json
{ "id_usuario": 2, "meta": 2500000, "plazo": 12, "extra": 100000, "mes_extra": 6 }
```
Respuesta esperada: cuota mensual de `191516.95`.

## Pruebas

**Unitarias del backend** (las de `test_db.py` necesitan una base PostgreSQL con las variables `PG_*`; las demás no):
```
cd backend
pip install -r requirements-dev.txt
python -m pytest src/tests
```

**Playwright (extremo a extremo).** Prueban la página real: cargar usuarios, calcular y guardar una meta, buscarla, ver errores y comprobar Swagger. Con el sistema corriendo (`docker compose up -d --build`):
```
pip install -r e2e/requirements.txt
python -m playwright install chromium
python -m pytest e2e
```
Resultado esperado: `5 passed`.

## Publicar las imágenes en DockerHub
Con `DOCKERHUB_USER` bien escrito en el `.env`:
```
docker login
docker compose build
docker compose push
```
Esto sube `entrega2-backend` y `entrega2-frontend` con la etiqueta de `VERSION`. En DockerHub los repositorios deben estar en **Public**.

## Problemas frecuentes

| Síntoma | Causa y solución |
|---|---|
| `port is already allocated` | Otro programa (u otro `docker compose`) usa el puerto 8080 o 5000. Apáguelo con `docker compose down` o ciérrelo. |
| El `seed` falla con `password authentication failed` | La contraseña del `.env` no coincide con la que Postgres guardó al crear la base. Ejecute `docker compose down -v` y vuelva a levantar. |
| Las carpetas `backend` o `frontend` están vacías | Se clonó sin `--recurse-submodules`. Ejecute `git submodule update --init --recursive`. |
| `variable is not set` o `invalid reference format` | Falta el `.env` o `DOCKERHUB_USER` está mal escrito (debe ser solo su usuario). |
| La página no carga la lista de usuarios | El backend aún no está listo. Revise `docker compose ps -a` y `docker compose logs backend`. |
| `denied` al hacer `docker compose push` | `DOCKERHUB_USER` no coincide con su cuenta, o falta `docker login`. |
| Las pruebas dicen `connection refused` | El sistema no está corriendo. Ejecute `docker compose up -d` y espere unos segundos. |

## Estructura del proyecto
```
entrega2/
├── docker-compose.yml        define los servicios db, seed, backend y frontend
├── .env.example              plantilla de variables (copiar como .env)
├── README.md
├── docs/historias_de_usuario.md
├── e2e/                      pruebas Playwright
├── frontend/                 (submódulo) Dockerfile, .dockerignore, nginx.conf, src/
└── backend/                  (submódulo) Dockerfile, .dockerignore, app.py, poblar_db.py, sql/, src/
```

## Historias de usuario
Ver [docs/historias_de_usuario.md](docs/historias_de_usuario.md), con el responsable de cada una.
