# Graphiti Memory Chatbot

Backend de un chatbot con memoria temporal persistente, construido con FastAPI,
Graphiti y FalkorDB.

## Estado del proyecto

Fase 1: base modular de FastAPI con configuración tipada, endpoint de salud y
pruebas automatizadas.

## Requisitos

- Python 3.12
- Git
- Docker Desktop (se utilizará desde la Fase 2)

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
- Documentación Swagger: http://localhost:8000/docs

## Ejecutar las pruebas

```powershell
pytest
```

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

