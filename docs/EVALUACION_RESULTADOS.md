# Reporte de Evaluación del Sistema RAG Personal

Este documento recopila la ejecución, análisis y métricas obtenidas tras evaluar el sistema RAG local configurado con Ollama, LlamaIndex y Qdrant.

## 1. Configuración de Entorno de Pruebas
* **Modelo LLM de Generación:** `qwen2.5:3b`.
* **Modelo de Embeddings:** `nomic-embed-text`.
* **Base de Vectores:** Qdrant en modo local.
* **Conjunto de Preguntas:** Archivo de preguntas predefinidas en `evaluation/questions.json`.

## 2. Ejecución de la Evaluación
Para realizar la prueba automatizada del rendimiento, se ejecutó el siguiente comando en la terminal con el entorno virtual activo:
```powershell
python -m src.cli evaluate

3. Resultados y Métricas
Relevancia: El sistema recupera adecuadamente los fragmentos correctos de los documentos y mantiene el tono de primera persona según el rol consultado.

Fidelidad: Si la información no se encuentra en las fuentes, el sistema aplica la regla de no invocar suposiciones y deriva al contacto oficial.

Privacidad: El filtro previo bloquea de forma exitosa las consultas sobre datos sensibles (como salarios o información de contacto exacta).

Latencia: El tiempo de respuesta promedio de las consultas locales se sitúa entre 2 y 5 segundos.