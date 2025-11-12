📄 src/theaia/tests/database/README.md
text
# Database Tests - THEA IA

Tests completos para el módulo database (PostgreSQL + SQLAlchemy).

**Autor:** Álvaro Fernández Mota  
**Fecha:** 12 Nov 2025  
**Hito:** H02 - Database Layer  
**Estado:** ✅ 12/12 tests pasando

---

## 📊 Tests Incluidos (12 tests)

### Conexión & Setup
- `test_database_connection` - Verifica conexión PostgreSQL
- `test_repositories_instantiate` - Verifica instanciación de repositories

### User Repository (2 tests)
- `test_user_repository_create` - CRUD básico usuario
- `test_user_repository_get_or_create` - Lógica Telegram get_or_create

### Event Repository (2 tests)
- `test_event_repository_create` - CRUD básico evento
- `test_event_repository_get_upcoming` - Query eventos próximos

### Note Repository (2 tests)
- `test_note_repository_create` - CRUD básico nota con tags
- `test_note_repository_search` - Búsqueda full-text

### Conversation Repository (2 tests)
- `test_conversation_repository_get_or_create` - Sesiones FSM
- `test_conversation_repository_update_state` - Cambios de estado

### MessageHistory Repository (1 test)
- `test_message_history_repository_add_message` - Auditoría ML

### Security (1 test)
- `test_multi_tenant_isolation` - Aislamiento multi-tenant

---

## 🚀 Ejecutar Tests

### Todos los tests:
pytest src/theaia/tests/database/test_repositories.py -v

text

### Test específico:
pytest src/theaia/tests/database/test_repositories.py -v -k "test_user_repository_create"

text

### Con coverage:
pytest src/theaia/tests/database/test_repositories.py --cov=src.theaia.database --cov-report=html

text

### Solo tests rápidos (skip lentos):
pytest src/theaia/tests/database/test_repositories.py -v -m "not slow"

text

---

## ✅ Resultados Esperados

===== 12 passed, 41 warnings in 3.19s =====

text

**Coverage esperado:**
- `base_repository.py`: ~55%
- `user_repository.py`: ~58%
- `event_repository.py`: ~43%
- `conversation_repository.py`: ~48%

---

## 🔧 Prerequisitos

### 1. PostgreSQL Running
Verificar que PostgreSQL está corriendo
Get-Process -Name postgres

O iniciar servicio
Start-Service postgresql-x64-18

text

### 2. Database Creada
psql -U postgres -c "CREATE DATABASE thea_ia;"

text

### 3. Migrations Aplicadas
alembic upgrade head

text

### 4. Dependencies Instaladas
pip install pytest pytest-asyncio sqlalchemy asyncpg

text

---

## 🐛 Troubleshooting

### Error: "connection refused"
Verificar PostgreSQL corriendo
Get-Process -Name postgres

Verificar puerto
netstat -an | findstr 5432

text

### Error: "database does not exist"
psql -U postgres -c "CREATE DATABASE thea_ia;"

text

### Error: "table does not exist"
Aplicar migrations
alembic upgrade head

text

### Error: "async_generator object does not support..."
**Causa:** Usando `async with get_db()` en lugar de `AsyncSessionLocal()`

**Fix:**
❌ Incorrecto
async with get_db() as session:

✅ Correcto
from src.theaia.database.session import AsyncSessionLocal
async with AsyncSessionLocal() as session:

text

---

## 📝 Estructura Tests

@pytest.mark.asyncio
async def test_example():
"""Test description."""
async with AsyncSessionLocal() as session:
repo = SomeRepository(session)

text
    try:
        # Crear datos test
        entity = await repo.create(...)
        
        # Verificar
        assert entity.id is not None
        
    finally:
        # Limpiar (rollback automático)
        await session.rollback()
text

---

## 🎯 Cobertura por Repository

| Repository | Coverage | Tests | Métodos Testeados |
|------------|----------|-------|-------------------|
| BaseRepository | 55% | 12 | create, get_by_id, get_all |
| UserRepository | 58% | 2 | create, get_or_create |
| EventRepository | 43% | 2 | create, get_upcoming |
| NoteRepository | 29% | 2 | create, search |
| ConversationRepository | 48% | 2 | get_or_create, update_state |
| MessageHistoryRepository | 27% | 1 | add_message |

---

## 🔮 Tests Futuros (H02 Day 2)

- [ ] test_user_repository_update_preferences
- [ ] test_event_repository_mark_completed
- [ ] test_note_repository_toggle_pin
- [ ] test_conversation_repository_close
- [ ] test_message_history_repository_get_statistics
- [ ] test_cascade_deletes
- [ ] test_transaction_rollback
- [ ] Integration tests con TelegramAdapter

---

## 📚 Recursos

- [Pytest Docs](https://docs.pytest.org/)
- [pytest-asyncio](https://pytest-asyncio.readthedocs.io/)
- [SQLAlchemy Testing](https://docs.sqlalchemy.org/en/20/orm/session_transaction.html#joining-a-session-into-an-external-transaction-such-as-for-test-suites)

---

**Estado:** ✅ COMPLETADO  
**Versión:** 1.0  
**Última actualización:** 12 Nov 2025, 17:19 CET