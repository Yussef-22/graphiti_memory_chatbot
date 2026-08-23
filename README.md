# Graphiti Memory Chatbot

Backend de un chatbot con memoria temporal persistente, construido con FastAPI,
Graphiti, Google Gemini y FalkorDB.

## Estado del proyecto

La fase de memoria funcional está completa:

- API modular con FastAPI y documentación Swagger.
- FalkorDB persistente mediante Docker Compose.
- Gemini como LLM, modelo de embeddings y reranker de Graphiti.
- Memoria aislada por usuario.
- Endpoints para guardar, buscar y utilizar recuerdos en un chat.
- Pruebas automatizadas sin llamadas reales a servicios externos.

## Qué hace cada componente

- **FastAPI:** recibe las peticiones HTTP y valida sus datos.
- **Gemini:** interpreta texto, genera respuestas y ayuda a ordenar recuerdos.
- **Graphiti:** extrae entidades y relaciones, conserva su temporalidad y realiza
  recuperación híbrida.
- **FalkorDB:** persiste nodos, relaciones, episodios e índices del grafo.
- **Docker Compose:** levanta FalkorDB de forma reproducible y conserva sus datos
  en un volumen.

Consulta [la arquitectura completa](docs/ARCHITECTURE.md) y el documento de
[trade-offs técnicos](docs/TRADE_OFFS.md).

## Requisitos

- Python 3.11 o superior
- Git
- Docker Desktop con WSL 2
- Una API key gratuita de Google AI Studio

## Instalación en Windows PowerShell

Desde la carpeta raíz del proyecto:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements-dev.txt
Copy-Item .env.example .env
```

Si el entorno virtual ya existe, solo actívalo. Si PowerShell bloquea la
activación, ejecuta una vez en esa terminal:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Completa en `.env`:

```env
GEMINI_API_KEY=tu_clave_real
GEMINI_MODEL=gemini-3.5-flash-lite
GEMINI_EMBEDDING_MODEL=gemini-embedding-001
SEMAPHORE_LIMIT=1
```

Nunca subas `.env` a GitHub. Puedes comprobar su exclusión con:

```powershell
git check-ignore .env
```

## Ejecutar FalkorDB

Con Docker Desktop abierto:

```powershell
docker compose up -d
docker compose ps
```

El contenedor `graphiti-falkordb` debe aparecer como `healthy`. FalkorDB Browser
queda disponible en http://localhost:3000.

## Ejecutar la API

En otra terminal, dentro de la misma carpeta y con `(.venv)` visible:

```powershell
uvicorn app.main:app --reload
```

Abre:

- API: http://localhost:8000
- Documentación interactiva: http://localhost:8000/docs
- Liveness: http://localhost:8000/health
- Readiness de FalkorDB: http://localhost:8000/ready

## Endpoints de memoria

### `POST /memory/episodes`

Guarda una declaración del usuario. Graphiti la convierte en entidades y hechos
temporales.

```json
{
  "user_id": "yussef",
  "content": "Practico natación cinco días por semana."
}
```

### `POST /memory/search`

Busca hechos relevantes solamente dentro de la memoria del usuario indicado.

```json
{
  "user_id": "yussef",
  "query": "¿Qué deporte practico?",
  "limit": 5
}
```

### `POST /chat`

Busca recuerdos, se los proporciona a Gemini, genera una respuesta y después
guarda el nuevo mensaje del usuario.

```json
{
  "user_id": "yussef",
  "message": "¿Qué actividad me recomendarías para hoy?"
}
```

La respuesta incluye `memories_used` para demostrar qué hechos influyeron en la
respuesta y `episode_uuid` para comprobar que el mensaje fue persistido.

## Demostración recomendada

1. Abre `/docs` y guarda dos declaraciones mediante `/memory/episodes`.
2. Consulta una de ellas mediante `/memory/search`.
3. Haz una pregunta relacionada en `/chat` y revisa `memories_used`.
4. Cambia un hecho, por ejemplo de “trabajo en Atlas” a “ya no trabajo en Atlas”.
5. Busca nuevamente y observa la información temporal en FalkorDB Browser.

Cada `user_id` se transforma en un grafo como `graphiti_memory_yussef`. De esta
manera, las búsquedas de un usuario no recuperan recuerdos de otro.

También hay una demostración automatizada. Con Docker y Uvicorn ejecutándose,
abre una tercera terminal y utiliza:

```powershell
.\scripts\demo.ps1
```

El script usa información ficticia, guarda un recuerdo, lo busca y después hace
una pregunta al chatbot.

## Ejecutar las pruebas

```powershell
pytest
```

Las pruebas usan servicios falsos controlados. Por eso no consumen cuota de
Gemini ni requieren que Docker esté funcionando.

## Detener el proyecto

Detén Uvicorn con `Ctrl + C`. Después:

```powershell
docker compose down
```

El volumen permanece. No uses `docker compose down -v` salvo que quieras borrar
todos los grafos y recuerdos.

## Estructura

```text
app/
├── api/
│   ├── chat.py       # Endpoint del chatbot
│   ├── health.py     # Liveness y readiness
│   └── memory.py     # Guardado y búsqueda de recuerdos
├── core/config.py    # Configuración tipada desde .env
├── models/schemas.py # Contratos de entrada y salida
├── services/
│   ├── falkordb.py   # Comprobación ligera de infraestructura
│   └── memory.py     # Orquestación Graphiti–Gemini–FalkorDB
└── main.py           # Creación y ciclo de vida de FastAPI
docs/                 # Arquitectura, notas y trade-offs
scripts/demo.ps1      # Demostración automatizada de punta a punta
tests/                # Pruebas automatizadas
```
