🔍 Agent: Query — THEA IA
Versión: 1.0
Última actualización: 2025-11-08 (Sesión 35)
Responsable: Agents Team
Estado: ✅ Activo
Prioridad: 🔴 Alta (Core)

📋 Propósito
El Agente Query realiza búsquedas inteligentes usando NLP: consultas en lenguaje natural, búsqueda semántica, extracción de información y respuesta a preguntas.

Audiencia:

Desarrolladores integrando búsquedas NLP

Data scientists optimizando modelos

Usuarios finales consultando información

🎯 Responsabilidades
Funcionalidad	Descripción
Búsqueda semántica	Buscar por significado no solo palabras
Question answering	Responder preguntas directamente
Extracción info	Extraer entidades y datos clave
Búsqueda multi-fuente	Buscar en notas, eventos, docs
Ranking relevancia	Ordenar resultados por relevancia
🔧 Configuración
text
agent:
  name: "Query"
  version: "1.0"
  enabled: true
  timeout: 25

models:
  embedding: "sentence-transformers/all-MiniLM-L6-v2"
  qa_model: "deepset/roberta-base-squad2"
  
search:
  max_results: 20
  min_relevance: 0.7
📥 Entrada
python
{
  "action": "semantic_search",
  "data": {
    "query": "¿Cuándo es la próxima reunión de equipo?",
    "sources": ["events", "notes"],
    "limit": 10
  }
}
📊 Métricas
Métrica	Actual	Target
Search accuracy	0.89	> 0.85
Response time	350ms	< 500ms
QA precision	0.91	> 0.90
📌 Meta
Campo	Valor
Archivo	docs/agents/agent_query.md
Estado	✅ Activo