# Trade-offs técnicos

## Graphiti + FalkorDB frente a PostgreSQL + embeddings tradicionales

| Criterio | Graphiti + FalkorDB | PostgreSQL + vector tradicional |
|---|---|---|
| Modelo mental | Entidades conectadas por relaciones | Filas, columnas y fragmentos de texto |
| Cambios en el tiempo | Validez e invalidación temporal de hechos | Hay que diseñar historial y vigencias manualmente |
| Relaciones de varios saltos | Naturales mediante recorridos de grafo | Requieren joins o lógica adicional |
| Recuperación | Semántica, palabras clave y estructura del grafo | Normalmente similitud vectorial y filtros SQL |
| Trazabilidad | Hechos vinculados con episodios de origen | Debe implementarse con tablas y metadatos |
| Simplicidad operativa | Más componentes y aprendizaje | PostgreSQL suele ser más conocido y consolidado |
| Datos transaccionales | No es su principal fortaleza | Excelente para consistencia, reportes y transacciones |
| Costo de ingestión | Varias llamadas al LLM para estructurar conocimiento | Embedding por fragmento, normalmente más barato |
| Flexibilidad del esquema | Relaciones emergentes y conocimiento conectado | Esquema explícito, controlado y predecible |

## Cuándo conviene este stack

Graphiti y FalkorDB son apropiados cuando la aplicación necesita recordar cómo
cambian personas, preferencias, organizaciones y relaciones. Ejemplos:

- Asistentes personales de larga duración.
- CRM conversacional con cambios de cargo o empresa.
- Soporte donde políticas y estados cambian con el tiempo.
- Agentes que necesitan explicar de qué conversación salió un hecho.
- Preguntas que conectan varias entidades y no solo buscan un texto parecido.

## Cuándo elegir PostgreSQL y embeddings

PostgreSQL con `pgvector` suele ser mejor cuando:

- La información principal son documentos relativamente estáticos.
- Solo se necesita encontrar fragmentos semánticamente parecidos.
- El equipo ya opera PostgreSQL y quiere minimizar infraestructura.
- Son prioritarias las transacciones, agregaciones y consultas tabulares.
- El presupuesto o la latencia no permiten varias llamadas al LLM por mensaje.

## Costos y limitaciones de nuestra solución

1. **Ingestión más lenta:** Graphiti extrae, deduplica y valida entidades y
   relaciones; guardar un mensaje tarda más que insertar una fila.
2. **Consumo del proveedor:** una sola conversación puede generar varias
   solicitudes a Gemini. El nivel gratuito tiene límites.
3. **Complejidad operativa:** hay que monitorear FastAPI, FalkorDB, Graphiti y el
   proveedor de IA.
4. **Extracción probabilística:** un LLM puede interpretar mal una relación. La
   trazabilidad reduce el riesgo, pero no lo elimina.
5. **Consistencia eventual en producción:** para reducir la latencia, una
   versión de producción probablemente movería la ingestión a una cola. El
   prototipo espera a que termine para ofrecer consistencia inmediata.
6. **Privacidad:** los mensajes se envían al proveedor de IA. En el nivel
   gratuito deben utilizarse datos ficticios o no sensibles.

## Decisión para esta prueba técnica

Elegimos Graphiti + FalkorDB porque la prueba busca demostrar memoria de
conversación conectada y temporal. PostgreSQL con embeddings resolvería una
búsqueda semántica convencional, pero obligaría a construir manualmente la
extracción de entidades, el historial, la invalidación de hechos, la
trazabilidad y los recorridos de relaciones.

La contrapartida aceptada es mayor complejidad y costo de ingestión a cambio de
una memoria más expresiva, explicable y adecuada para información que cambia.
