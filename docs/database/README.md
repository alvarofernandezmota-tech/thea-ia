# Database - Capa de Datos de THEA IA

**Version:** v3.0.0
**Status:** ✅ Production Ready
**Calificación Auditoría:** 8.1/10 - MUY BUENO
**Last Updated:** 06 Enero 2026

## 📋 Índice

- [Visión General](#visión-general)
- [Schema](#schema)
- [Migraciones](#migraciones)
- [Repositories](#repositories)

---

## 🎯 Visión General

Módulo de gestión de base de datos con:

- **SQLAlchemy 2.0:** ORM moderno async/await
- **Alembic:** Migraciones de schema
- **PostgreSQL 14+:** Base de datos principal
- **Repository Pattern:** Abstracción de acceso a datos
- **Multi-tenancy:** Aislamiento por tenant_id

### Ubicación
```
src/theaia/database/
├── alembic/             # Migraciones
├── repositories/        # Repository pattern
├── connection.py        # Pool de conexiones
├── session.py           # Session management
└── __init__.py
```

---

## 🗃️ Schema de Base de Datos

### Tablas Core (H02)

| Tabla | Propósito | Registros Tipo |
|-------|----------|----------------|
| **tenants** | Aislamiento multi-tenant | ~10-50 |
| **users** | Usuarios del sistema | ~100-1000 |
| **conversations** | Sesiones de chat | ~1000-10000 |
| **messages** | Historial de mensajes | ~10000-100000 |
| **agent_configs** | Configuración agentes | ~10-20 |
| **user_preferences** | Preferencias usuario | ~100-1000 |
| **api_keys** | Claves API | ~10-100 |

### Tablas de Agentes (H09-H11)

| Tabla | Agente | Status |
|-------|--------|--------|
| **appointments** | AgendaAgent | 🔴 H09 |
| **availability** | AgendaAgent | 🔴 H09 |
| **notes** | NoteAgent | ⏳ H10 |
| **reminders** | ReminderAgent | ⏳ H11 |

📖 **[Ver schema completo →](./schema.md)**

---

## 📊 Métricas del Database

| Métrica | Valor |
|---------|-------|
| **Total Archivos** | ~8 |
| **Total LOC** | ~800 |
| **Tablas** | 11 (7 core + 4 agents) |
| **Repositories** | 6 |
| **Migraciones** | ~15 |

---

## 🎖️ Resultado Auditoría

**Calificación:** 8.1/10 - MUY BUENO 🟢

### Fortalezas
- ✅ SQLAlchemy 2.0 moderno
- ✅ Alembic bien configurado
- ✅ Repository pattern consistente
- ✅ Multi-tenancy sólido
- ✅ Async/await nativo

### Áreas de Mejora
- ⚠️ Documentación de migraciones faltante
- ⚠️ Estrategia de backup no documentada
- ⚠️ Tests de repositories no visibles

---

## 📚 Documentación Relacionada

- 📖 [Models](../models/README.md) - ORM y Pydantic schemas
- 📖 [Core](../core/README.md) - Lógica central
- 📖 [Architecture](../architecture/overview.md) - Arquitectura general

---

**Fuente:** Auditoría Diciembre 2025 - [03_audit_src](../audit/audit_diciembre_2025/03_audit_src/)
**Mantenido por:** Álvaro Fernández Mota
**Estado:** ✅ Production Ready
