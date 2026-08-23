# Notas de presentación — Fase de memoria

## Qué se construyó

Se conectó el servidor FastAPI con Graphiti, Google Gemini y FalkorDB. El sistema
ya puede guardar afirmaciones como episodios, convertirlas en entidades y
relaciones, recuperarlas por significado y utilizarlas para responder.

## Cómo explicarlo de forma sencilla

- FastAPI es la recepción: recibe y revisa cada petición.
- Gemini es quien comprende el lenguaje.
- Graphiti es quien organiza lo comprendido como memoria temporal.
- FalkorDB es el almacén persistente donde queda el grafo.
- Docker mantiene ese almacén aislado y reproducible.

## Por qué hay tres clientes de Gemini

Graphiti necesita una IA para interpretar, un modelo para producir embeddings y
un reranker para ordenar resultados. Configuramos Gemini en los tres lugares
para que ninguna operación dependa accidentalmente de OpenAI.

## Conclusión del paso

> El proyecto dejó de ser únicamente una API conectada a una base disponible.
> Ahora tiene un ciclo completo de memoria: recibe una experiencia, extrae
> conocimiento, lo persiste, recupera hechos relevantes y los utiliza para
> producir una respuesta personalizada. La memoria está aislada por usuario y
> conserva información temporal y trazabilidad hacia el mensaje original.
