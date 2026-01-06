# 🔍 QueryAgent — THEA IA

**Version:** 2.0  
**Last Updated:** 06 January 2026  
**Status:** ⏳ Planned (H10)  
**Priority:** HIGH  
**Milestone:** H10 (February 2026)

---

## 🎯 Purpose

The **QueryAgent** performs intelligent semantic searches and answers questions across multiple data sources (notes, appointments, documents). It uses NLP and vector embeddings to understand meaning, not just keywords.

**This is the SEARCH & QA specialist** - it doesn't create or modify data, only searches and answers questions about existing data.

---

## 📋 Core Responsibilities

| Responsibility | Description | Status |
|----------------|-------------|--------|
| **Semantic Search** | Meaning-based search using vector embeddings | ⏳ H10 |
| **Question Answering** | Extract direct answers from context | ⏳ H10 |
| **Multi-Source Search** | Search across notes, events, documents | ⏳ H10 |
| **Entity Extraction** | Extract dates, names, concepts from text | ⏳ H10 |
| **Contextual Understanding** | Understand user intent and context | ⏳ H10 |
| **Citation Support** | Show sources for answers | ⏳ H10 |
| **Multi-Language** | Support Spanish and English | ⏳ H10 |

---

## 🏗️ Architecture

### Technology Stack

```yaml
# NLP Models
- Embedding Model: sentence-transformers/all-MiniLM-L6-v2
- QA Model: deepset/roberta-base-squad2
- Search Engine: PostgreSQL full-text + vector search

# Database
- Vector embeddings table (pgvector extension)
- Full-text search indexes (ts_vector)
- Relevance scoring cache

# Services
- SemanticSearchService: Vector similarity search
- QuestionAnsweringService: Extract answers from context
- EntityExtractor: Named Entity Recognition (NER)
- MultiSourceAggregator: Combine results from different sources
Search Process Flow
text
User Query: "¿Cuándo es mi próxima reunión?"
    ↓
1. Entity Extraction
   → entities: ["reunión"]
   → intent: FIND_NEXT_EVENT
   → time_reference: FUTURE
    ↓
2. Source Selection
   → sources: [appointments, calendar_events]
    ↓
3. Semantic Search
   → vector_similarity(query, appointments)
   → results: [appointment_1, appointment_2, ...]
    ↓
4. Answer Extraction
   → "Tu próxima reunión es mañana a las 15:00"
   → citation: [appointment_1]
🔧 Implementation Plan (H10)
Phase 1: Infrastructure ⏳
⏳ Install pgvector extension

⏳ Create embeddings table

⏳ Setup full-text search indexes

Phase 2: Semantic Search ⏳
⏳ Implement embedding generation

⏳ Vector similarity search

⏳ Relevance ranking

Phase 3: Question Answering ⏳
⏳ QA model integration

⏳ Answer extraction pipeline

⏳ Citation tracking

Phase 4: Multi-Source Integration ⏳
⏳ Search across notes

⏳ Search across appointments

⏳ Search across documents

⏳ Result aggregation

📊 Testing Strategy
Test Coverage Target: 85%+
Test Type	Count	Status
Unit Tests	25	⏳ H10
Integration Tests	10	⏳ H10
E2E Tests	5	⏳ H10
Total	40	⏳ H10
🌐 API Examples
Semantic Search
text
POST /api/v1/query/search
Content-Type: application/json

{
  "query": "roadmap planning meetings",
  "sources": ["notes", "events"],
  "limit": 10
}

Response:
{
  "results": [
    {
      "id": "note_123",
      "type": "note",
      "title": "Roadmap Q1 Planning",
      "relevance": 0.92,
      "excerpt": "Q1 roadmap planning meeting scheduled for..."
    }
  ]
}
Question Answering
text
POST /api/v1/query/ask
Content-Type: application/json

{
  "question": "¿Cuándo es mi próxima reunión?",
  "context": ["events", "appointments"]
}

Response:
{
  "answer": "Tu próxima reunión es mañana a las 15:00",
  "confidence": 0.95,
  "sources": [
    {
      "type": "appointment",
      "id": "appt_456",
      "title": "Reunión de equipo"
    }
  ]
}
🔄 Differences from Other Agents
Agent	Responsibility
AgendaAgent	Creates/modifies appointments
QueryAgent	Searches/answers questions about appointments
NoteAgent	Creates/modifies notes
QueryAgent	Searches within notes with NLP
Key Principle: QueryAgent is READ-ONLY. It never creates, modifies, or deletes data.

📂 File Locations
text
src/theaia/agents/query_agent/          # (H10 - to be created)
├── agent.py                             # Main QueryAgent class
├── semantic_search.py                   # Vector search
├── question_answering.py                # QA pipeline
├── entity_extractor.py                  # NER
├── multi_source.py                      # Source aggregation
├── embeddings/                          # Embedding models
├── models/                              # Data models
├── tests/                               # Test suite
└── tools/                               # Utilities
🚀 Roadmap
H10 (February 2026) - ⏳ Planned
Implement semantic search

Question answering pipeline

Multi-source search

40 tests passing

H11 (February 2026) - ⏳ Future
Advanced entity linking

Cross-lingual search (ES ↔ EN)

Query suggestions

H12+ - ⏳ Future
Conversational search

Context-aware queries

Search analytics

💡 Example Use Cases
text
User: "¿Qué notas tengo sobre roadmap?"
QueryAgent:
  → Semantic search in notes
  → Returns: ["Roadmap Q1", "H09 Planning", "Feature Roadmap"]
  → Relevance scores: [0.92, 0.87, 0.81]

User: "¿Cuándo es mi próxima cita?"
QueryAgent:
  → Search in appointments
  → Answer: "Mañana a las 15:00"
  → Citation: [appointment_456]

User: "¿Qué decidimos en la última reunión?"
QueryAgent:
  → Search in meeting notes + events
  → Extract key decisions
  → Show sources
📖 Related Documentation
Agents Overview - All 4 agents comparison

SCHEMA.md - Project architecture

Roadmap Master - H01-H17 timeline

H10 Milestone - Future sprint

Last Updated: 06 January 2026, 17:48 CET
Next Review: February 2026 (H10 start)
Maintained by: Agents Team