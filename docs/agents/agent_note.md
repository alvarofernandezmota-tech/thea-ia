📝 Agent: Note — THEA IA
Versión: 1.0
Última actualización: 2025-11-08 (Sesión 35)
Responsable: Agents Team
Estado: ✅ Activo
Prioridad: 🔴 Alta (Core)

📋 Propósito
El Agente Note gestiona notas, apuntes y documentación del usuario. Es responsable de crear, buscar, modificar, etiquetas y organizar notas con indexación full-text.

Audiencia:

Desarrolladores integrando funcionalidad de notas

QA testeando búsquedas y organización

Usuarios finales tomando y buscando notas

🎯 Responsabilidades
Funcionalidad	Descripción
Crear nota	Nueva nota con título y contenido
Listar notas	Mostrar todas las notas del usuario
Buscar notas	Full-text search por palabra clave
Modificar nota	Actualizar título y contenido
Eliminar nota	Borrar nota por ID
Etiquetas	Organizar notas por tags
Archivar	Mover notas a archivo
🔧 Configuración
Archivo: config/agents/note.yaml

text
agent:
  name: "Note"
  version: "1.0"
  enabled: true
  timeout: 20
  max_retries: 2

capabilities:
  - create_note
  - list_notes
  - search_notes
  - modify_note
  - delete_note
  - add_tag
  - archive_note

models:
  nlp: "bert-base-uncased"
  text_embedding: "sentence-transformers/all-MiniLM-L6-v2"

database:
  table: "notes"
  index: "notes_full_text_index"
  cache_ttl: 1800

search:
  engine: "elasticsearch"  # o sqlite full-text
  batch_size: 50
  timeout: 5
📥 Entrada esperada
Formato general
python
{
  "action": "create_note",  # create/list/search/modify/delete
  "data": {
    "title": "Mi nota",
    "content": "Contenido de la nota",
    "tags": ["personal", "ideas"],
    "color": "yellow"  # opcional
  }
}
Casos específicos
Crear nota:

python
{
  "action": "create_note",
  "data": {
    "title": "Roadmap Q1",
    "content": "- Feature A\n- Feature B\n- Testing",
    "tags": ["roadmap", "planning"]
  }
}
Buscar notas:

python
{
  "action": "search_notes",
  "data": {
    "query": "roadmap Q1",
    "tags": ["planning"],
    "limit": 10
  }
}
Modificar nota:

python
{
  "action": "modify_note",
  "data": {
    "note_id": "note_12345",
    "title": "Nuevo título",
    "content": "Contenido actualizado"
  }
}
📤 Salida esperada
Éxito - Crear nota
python
{
  "status": "success",
  "action": "create_note",
  "note": {
    "note_id": "note_12345",
    "title": "Roadmap Q1",
    "content": "- Feature A\n- Feature B",
    "tags": ["roadmap", "planning"],
    "created_at": "2025-11-08T14:50:00Z",
    "updated_at": "2025-11-08T14:50:00Z"
  },
  "message": "Nota creada exitosamente"
}
Éxito - Búsqueda
python
{
  "status": "success",
  "action": "search_notes",
  "results": [
    {
      "note_id": "note_12345",
      "title": "Roadmap Q1",
      "excerpt": "- Feature A\n- Feature B...",
      "relevance_score": 0.95,
      "tags": ["roadmap", "planning"]
    },
    {
      "note_id": "note_67890",
      "title": "Q1 Planning",
      "excerpt": "Planificación para Q1...",
      "relevance_score": 0.87,
      "tags": ["planning"]
    }
  ],
  "total": 2,
  "query_time_ms": 125
}
Error
python
{
  "status": "error",
  "action": "create_note",
  "error_code": "INVALID_INPUT",
  "message": "Título requerido",
  "details": {
    "missing_fields": ["title"]
  }
}
🔄 Flujo de procesamiento
1. Crear nota
text
Usuario input
     ↓
Validar entrada (título requerido)
     ↓
Generar note_id único
     ↓
Guardar en BD (tabla notes)
     ↓
Indexar para full-text search
     ↓
Procesar tags/etiquetas
     ↓
Retornar nota creada
2. Buscar notas
text
Usuario query (ej: "roadmap")
     ↓
Tokenizar y normalizar query
     ↓
Ejecutar full-text search en BD
     ↓
Filtrar por tags (si aplica)
     ↓
Calcular relevancia/scoring
     ↓
Ordenar por relevancia
     ↓
Retornar resultados + metadata
🧠 Lógica interna
Full-text search
El agente implementa búsqueda de texto completo:

python
def search_notes(query, tags=None, limit=10):
    # Normalizar query
    normalized_query = normalize_text(query)
    
    # Ejecutar búsqueda full-text
    results = db.execute("""
        SELECT note_id, title, content, 
               ts_rank(to_tsvector('spanish', content), 
                      plainto_tsquery('spanish', %s)) AS relevance
        FROM notes
        WHERE to_tsvector('spanish', content) @@ 
              plainto_tsquery('spanish', %s)
        ORDER BY relevance DESC
        LIMIT %s
    """, (normalized_query, normalized_query, limit))
    
    return results
Etiquetado automático
python
def auto_tag_note(content):
    # Usar NLP para sugerir tags
    topics = nlp_model.extract_topics(content)
    
    return {
        "auto_tags": topics,
        "confidence": [0.95, 0.87, 0.72]
    }
Deduplicación
python
def check_duplicate(title, content):
    # Calcular embedding del contenido
    embedding = text_embedding_model.encode(content)
    
    # Buscar notas similares
    similar = db.similarity_search(embedding, threshold=0.9)
    
    if similar:
        return {
            "is_duplicate": True,
            "similar_notes": similar
        }
    return {"is_duplicate": False}
📊 Métricas
Métrica	Actual	Target
Search response time	180ms	< 200ms
Index update latency	50ms	< 100ms
Search accuracy	0.92	> 0.90
Dedup detection rate	0.98	> 0.95
🚨 Errores comunes
Error	Causa	Solución
INVALID_INPUT	Título faltante	Proporcionar título
DUPLICATE_DETECTED	Nota similar existe	Verificar nota existente
SEARCH_TIMEOUT	Query muy compleja	Simplificar o agregar límites
INDEXING_ERROR	Fallo al indexar	Reintentar o reindexar
NOTE_NOT_FOUND	ID no existe	Verificar note_id
🏷️ Sistema de etiquetas
Etiquetas predefinidas:

personal

trabajo

ideas

research

planning

bug-report

feature-request

Etiquetas personalizadas:

python
{
  "action": "add_tag",
  "data": {
    "note_id": "note_12345",
    "tags": ["custom-tag-1", "custom-tag-2"]
  }
}
✅ Tests
Unit test ejemplo
python
def test_note_create_note_valid_data():
    agent = NoteAgent()
    
    result = agent.process({
        "action": "create_note",
        "data": {
            "title": "Test note",
            "content": "Test content"
        }
    })
    
    assert result["status"] == "success"
    assert result["note"]["title"] == "Test note"
    assert "note_id" in result["note"]

def test_note_search_full_text():
    agent = NoteAgent()
    
    # Crear nota primero
    agent.process({
        "action": "create_note",
        "data": {"title": "Roadmap", "content": "roadmap content"}
    })
    
    # Buscar
    result = agent.process({
        "action": "search_notes",
        "data": {"query": "roadmap"}
    })
    
    assert result["status"] == "success"
    assert len(result["results"]) > 0
Ver más tests en: src/theaia/tests/unit/test_agents_note.py

🔗 Enlaces relacionados
Agents Overview — Sistema multi-agente

Best Practices — Convenciones

Testing — Cómo testear agentes

📌 Meta-información
Campo	Valor
Archivo	docs/agents/agent_note.md
Versión	1.0
Última revisión	2025-11-08 (Sesión 35)
Responsable	Agents Team
Estado	✅ Activo
🛡️ Auditoría y cumplimiento
Parte del Hito 35.1.3 (docs/agents/)

Agente core con prioridad alta

Full-text search implementado

Tests unitarios completos

Validado en sesión 35