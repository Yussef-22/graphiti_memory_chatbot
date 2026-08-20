# Graphiti Memory Chatbot

Backend de un chatbot con memoria temporal persistente, construido con FastAPI,
Graphiti y FalkorDB.

## Estado del proyecto

Fase 2 en progreso: base modular de FastAPI, FalkorDB persistente mediante
Docker Compose y comprobación de disponibilidad de la base desde la API.

## Requisitos

- Python 3.11 o superior
- Git
- Docker Desktop con WSL 2

## Instalación en Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements-dev.txt
Copy-Item .env.example .env
```

Si PowerShell impide activar el entorno virtual, ejecuta una sola vez en esa
terminal:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

## Ejecutar la API

```powershell
uvicorn app.main:app --reload
```

Después abre:

- API: http://localhost:8000
- Health check: http://localhost:8000/health
- Readiness check: http://localhost:8000/ready
- Documentación Swagger: http://localhost:8000/docs

## Ejecutar las pruebas

```powershell
pytest
```

## Ejecutar FalkorDB

Con Docker Desktop abierto y su motor en ejecución:

```powershell
docker compose config
docker compose up -d
docker compose ps
```

Después abre FalkorDB Browser en http://localhost:3000.

La API distingue dos verificaciones:

- `/health`: confirma que el proceso de FastAPI está vivo.
- `/ready`: confirma que FastAPI también puede comunicarse con FalkorDB.

Para detener el contenedor sin eliminar los datos:

```powershell
docker compose down
```

> No uses `docker compose down -v` salvo que quieras eliminar también el
> volumen y todos los datos almacenados en FalkorDB.

## Estructura actual

```text
app/
├── api/        # Endpoints HTTP
├── core/       # Configuración e infraestructura compartida
├── models/     # Esquemas de entrada y salida
├── services/   # Lógica de negocio e integraciones
└── main.py     # Punto de entrada de FastAPI
tests/          # Pruebas automatizadas
```

## Próximas fases

1. Levantar FalkorDB mediante Docker Compose.
2. Verificar persistencia y conectividad.
3. Integrar Graphiti y crear sus índices.
4. Implementar `/chat` y la memoria por usuario.
5. Construir la demostración temporal y documentar trade-offs.
