# Arquitectura del chatbot con memoria

## Flujo principal

```text
Cliente / Swagger
       |
       v
FastAPI valida user_id y message
       |
       v
GraphitiMemoryService bloquea operaciones del mismo usuario
       |
       +----> Graphiti busca hechos relevantes
       |             |
       |             v
       |         FalkorDB
       |
       v
Gemini recibe pregunta + recuerdos relevantes
       |
       v
FastAPI devuelve la respuesta y los recuerdos utilizados
       |
       v
Graphiti procesa y guarda únicamente el mensaje del usuario
```

## Decisiones importantes

### Memoria aislada por usuario

El `user_id` forma el nombre de un grafo independiente:

```text
graphiti_memory_yussef
graphiti_memory_demo2
```

Esto evita que una consulta de un usuario recupere información de otro. El
identificador solo acepta letras ASCII, números, guiones y guiones bajos para
impedir nombres inseguros.

### Un solo proveedor de IA

Graphiti utiliza Gemini explícitamente en sus tres puntos configurables:

1. `GeminiClient`: extracción y razonamiento.
2. `GeminiEmbedder`: búsqueda por significado.
3. `GeminiRerankerClient`: ordenamiento final por relevancia.

Configurar los tres evita que Graphiti recurra silenciosamente a sus clientes
predeterminados de OpenAI.

### Orden temporal consistente

Cada usuario tiene un `asyncio.Lock`. Si llegan dos mensajes simultáneos del
mismo usuario, se procesan en orden. Es importante porque Graphiti compara un
episodio nuevo con los anteriores para actualizar o invalidar hechos.

Usuarios diferentes conservan locks diferentes y pueden avanzar de manera
independiente.

### Solo el usuario crea memoria

El endpoint `/chat` guarda el mensaje escrito por el usuario, pero no guarda la
respuesta del modelo como fuente de verdad. Una respuesta generada podría
contener un error; almacenarla automáticamente convertiría una alucinación en
un recuerdo persistente.

### Inicialización bajo demanda

Los índices necesarios se crean cuando un usuario utiliza por primera vez su
grafo. Los clientes se mantienen en caché durante la ejecución y se cierran
cuando FastAPI se detiene.

## Responsabilidad por módulo

- `app/api`: HTTP, códigos de estado y conversión a esquemas.
- `app/models`: validación y forma pública de los datos.
- `app/services`: reglas de negocio y proveedores externos.
- `app/core`: configuración compartida.
- `app/main.py`: composición y ciclo de vida de la aplicación.

Esta separación permite probar la API con servicios falsos, sin gastar cuota y
sin levantar una base de datos.
