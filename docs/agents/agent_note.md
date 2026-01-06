# 📝 NoteAgent — THEA IA

**Version:** 2.0  
**Last Updated:** 06 January 2026  
**Status:** ⏳ Planned (H10)  
**Priority:** HIGH  
**Milestone:** H10 (February 2026)

---

## 🎯 Purpose

The **NoteAgent** manages user notes with full-text search, tagging, and organization capabilities. It handles creation, modification, deletion, and organization of markdown notes.

**This is the NOTE MANAGEMENT specialist** - it creates and manages notes, while QueryAgent searches within them.

---

## 📋 Core Responsibilities

| Responsibility | Description | Status |
|----------------|-------------|--------|
| **Create Notes** | Create new notes with title and markdown content | ⏳ H10 |
| **Edit Notes** | Modify note title and content | ⏳ H10 |
| **Delete Notes** | Soft delete notes to archive | ⏳ H10 |
| **List Notes** | Retrieve notes with filtering | ⏳ H10 |
| **Full-Text Search** | PostgreSQL ts_vector search | ⏳ H10 |
| **Tagging System** | Manual and auto-generated tags | ⏳ H10 |
| **Auto-Tagging** | NLP-based topic extraction | ⏳ H10 |
| **Duplicate Detection** | Find similar notes (>0.9 similarity) | ⏳ H10 |
| **Archive System** | Soft delete with recovery | ⏳ H10 |

---

## 🏗️ Architecture

### Technology Stack

```yaml
# Database
notes:
  - id, user_id, title, content (markdown)
  - tags (array), created_at, updated_at
  - archived (bool), embedding (vector)

# Indexes
- Full-Text: to_tsvector('spanish', content)
- Tags: GIN index on tags array
- Vector: pgvector for similarity search

# Services
- NoteService: CRUD operations
- FullTextSearchService: PostgreSQL search
- AutoTaggerService: NLP-based topic extraction
- DuplicateDetector: Embedding similarity
- MarkdownProcessor: Parse and validate markdown
Note Structure
text
# Example Note
**Title:** "Roadmap Q1 Planning"
**Content:** (markdown)
  # Q1 Goals
  - Feature A: Timeline and scope
  - Feature B: Dependencies
  
  ## Action Items
  - [ ] Review with team
  - [ ] Create tickets
  
**Tags:** ["planning", "roadmap", "Q1"]
**Auto-Tags:** ["product", "quarterly", "goals"]
**Created:** 2026-01-06 15:00:00
**Updated:** 2026-01-06 15:30:00
🔧 Implementation Plan (H10)
Phase 1: Core CRUD ⏳
⏳ Create note workflow

⏳ Edit note functionality

⏳ Soft delete (archive)

⏳ List with pagination

Phase 2: Search & Tags ⏳
⏳ Full-text search (PostgreSQL)

⏳ Manual tagging system

⏳ Tag-based filtering

⏳ Tag suggestions

Phase 3: Smart Features ⏳
⏳ Auto-tagging with NLP

⏳ Duplicate detection

⏳ Related notes suggestions

⏳ Archive management

Phase 4: Advanced ⏳
⏳ Markdown validation

⏳ Version history (future)

⏳ Note templates (future)

⏳ Export functionality

📊 Testing Strategy
Test Coverage Target: 85%+
Test Type	Count	Status
Unit Tests	25	⏳ H10
Integration Tests	10	⏳ H10
E2E Tests	5	⏳ H10
Total	40	⏳ H10
🌐 API Examples
Create Note
text
POST /api/v1/notes
Content-Type: application/json

{
  "title": "Roadmap Q1",
  "content": "# Q1 Goals\n- Feature A\n- Feature B",
  "tags": ["planning", "roadmap"]
}

Response:
{
  "id": "note_123",
  "title": "Roadmap Q1",
  "tags": ["planning", "roadmap"],
  "auto_tags": ["product", "quarterly"],
  "created_at": "2026-01-06T15:00:00Z"
}
Search Notes
text
GET /api/v1/notes/search?q=roadmap&tags=planning

Response:
{
  "results": [
    {
      "id": "note_123",
      "title": "Roadmap Q1",
      "excerpt": "Q1 Goals - Feature A...",
      "relevance": 0.95,
      "tags": ["planning", "roadmap"]
    }
  ],
  "total": 3
}
Auto-Tag Note
text
POST /api/v1/notes/123/auto-tag

Response:
{
  "suggested_tags": ["planning", "product", "quarterly"],
  "confidence": 0.87
}
Find Duplicates
text
GET /api/v1/notes/123/duplicates

Response:
{
  "duplicates": [
    {
      "id": "note_456",
      "title": "Q1 Roadmap Planning",
      "similarity": 0.93
    }
  ]
}
🔄 Differences from Other Agents
Agent	Responsibility
NoteAgent	Manages notes (create/edit/organize)
QueryAgent	Searches within notes (doesn't modify)
Key Principle: NoteAgent is WRITE-focused (CRUD), QueryAgent is READ-focused (Search).

💡 Smart Features
Auto-Tagging Algorithm
python
# NLP-based topic extraction
Content: "# Q1 Roadmap\nWe need to plan features for Q1..."
  ↓
Topic Extraction (NLP):
  - Keywords: ["roadmap", "plan", "features", "Q1"]
  - Entities: ["Q1"]
  - Topics: ["product", "planning", "quarterly"]
  ↓
Suggested Tags: ["planning", "product", "quarterly"]
Confidence: 0.87
Duplicate Detection
python
# Vector similarity comparison
Note A: "Roadmap Q1 Planning"
Note B: "Q1 Roadmap Plan"
  ↓
Embedding similarity: 0.93 (>0.90 threshold)
  ↓
Result: Potential duplicate detected
Related Notes
python
# Find similar notes by content
Current Note: "Roadmap Q1"
  ↓
Vector Search (top 5 similar):
  1. "H09 Planning" (0.85)
  2. "Feature Roadmap" (0.82)
  3. "Q1 Goals" (0.79)
📂 File Locations
text
src/theaia/agents/note_agent/           # (H10 - to be created)
├── agent.py                             # Main NoteAgent class
├── note_service.py                      # CRUD operations
├── full_text_search.py                  # PostgreSQL search
├── auto_tagger.py                       # NLP topic extraction
├── duplicate_detector.py                # Similarity detection
├── markdown_processor.py                # Parse & validate
├── models/                              # Data models
├── tests/                               # Test suite
└── tools/                               # Utilities
🚀 Roadmap
H10 (February 2026) - ⏳ Planned
Implement full CRUD

Full-text search

Tagging system

Auto-tagging with NLP

40 tests passing

H11 (February 2026) - ⏳ Future
Version history

Note templates

Rich markdown editor support

H12+ - ⏳ Future
Collaborative notes

Real-time sync

Export to PDF/DOCX

Note linking (wiki-style)

💡 Example Use Cases
text
User: "Crea una nota sobre la reunión de hoy"
NoteAgent:
  → Creates note with title "Reunión 06 Ene 2026"
  → Auto-tags: ["meeting", "date:2026-01"]
  → Returns note_id

User: "Edita la nota y añade acción items"
NoteAgent:
  → Opens note for editing
  → User adds content
  → Saves changes
  → Updates updated_at timestamp

User: "Busca notas sobre roadmap"
QueryAgent (not NoteAgent):
  → Performs semantic search
  → Returns matching notes

User: "¿Esta nota es duplicada?"
NoteAgent:
  → Runs duplicate detection
  → Returns similarity scores
  → Suggests merging if >0.9
📖 Related Documentation
Agents Overview - All 4 agents comparison

SCHEMA.md - Project architecture

Roadmap Master - H01-H17 timeline

H10 Milestone - Future sprint

Last Updated: 06 January 2026, 17:51 CET
Next Review: February 2026 (H10 start)
Maintained by: Agents Team
