# Registro de Migraciones – Thea IA 2.0

En este archivo se documentan las migraciones de la base de datos, los cambios estructurales y las recomendaciones para mantener la evolución controlada del modelo de datos en Thea IA 2.0.

---

## 📁 Ubicación y herramienta de migración

- Las migraciones están ubicadas en `/migrations/` creadas y gestionadas por Alembic (Python).
- Toda migración debe referenciar su revisión, fecha y objetivo principal.

---

¿Quieres la siguiente parte con formato de registro, ejemplos y convenciones para migraciones?**MIGRACIONES.md – Parte 2: Formato de registro, ejemplos y convenciones**

📝 Formato de registro y convenciones
Cada migración debe documentarse del siguiente modo:

Revision ID: identificador único generado por Alembic.

Fecha: día en que fue creada la migración.

Descripción: objetivo y campos/tables modificados.

Dependencias: relación con migraciones anteriores (si aplica).

Impacto: resumen del impacto sobre código, modelos y diccionario.

Ejemplo de bloque
text
### [2025-10-08] Revision ID: 001_initial
- Creación de tablas principales: users, events
- Constraints y campos base documentados en ESQUEMAS-DATABASE.md
- Impacto: inicialización del sistema de agentes y eventos
[2025-10-15] Revision ID: 002_add_notifications
Nueva tabla: notifications

Clave foránea a events

Índices programados para scheduled_for y status

-parte 2

--

## 📝 Formato de registro y convenciones

Cada migración debe documentarse del siguiente modo:

- `Revision ID`: identificador único generado por Alembic.
- `Fecha`: día en que fue creada la migración.
- `Descripción`: objetivo y campos/tables modificados.
- `Dependencias`: relación con migraciones anteriores (si aplica).
- `Impacto`: resumen del impacto sobre código, modelos y diccionario.

### Ejemplo de bloque

[2025-10-08] Revision ID: 001_initial
Creación de tablas principales: users, events

Constraints y campos base documentados en ESQUEMAS-DATABASE.md

Impacto: inicialización del sistema de agentes y eventos

text

### [2025-10-15] Revision ID: 002_add_notifications
- Nueva tabla: notifications
- Clave foránea a events
- Índices programados para scheduled_for y status

---
¿Quieres la última parte con recomendaciones de testing, rollback, control de versiones y mantenimiento de migraciones?MIGRACIONES.md – Parte 3: Testing, rollback, control y mantenimiento

text
---

## 🧪 Testing y validación de migraciones

- Prueba cada nueva migración en entorno de desarrollo antes de subirla a main/staging.
- Incluye tests unitarios/e2e que validen los nuevos campos, constraints y relaciones.
- Si la migración es disruptiva (borra datos, cambios de claves), documenta el impacto y el procedimiento en este archivo.

## ⏪ Rollback y control de versiones

- Toda migración debe ser reversible (tener método `downgrade` correctamente definido).
- Realiza backups previos antes de migraciones críticas.
- Anota versiones/tags relevantes y relación con el roadmap en este archivo.

## 🛡️ Mantenimiento y auditoría de migraciones

- Revisa las migraciones antiguas regularmente para evitar inconsistencias.
- Documenta en CHANGELOG.md cualquier revisión o migración especial.
- Si detectas migración huérfana o conflicto, resuélvelo y documenta el proceso.

---

*Este archivo debe ser referencia y registro vivo para la evolución técnica y estructural de la base de datos de Thea IA 2.0.*