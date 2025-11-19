Migraciones Alembic – THEA-IA H02
Visión General
Las migraciones en THEA-IA son el registro de verdad de la evolución del schema. Cada migración es justificada, testeada, y reversible.

Migración: 9ed4975f2bd7_add_last_activity_to_users.py
📌 Problema que resolvemos
Requerimiento: Trackear la última actividad de usuarios para:

Identificar usuarios inactivos

Mejorar análisis de engagement

Soporte a features de "últimas acciones vistas"

Auditoría de seguridad (cuándo fue el último acceso)

Sin esto: No podemos responder "¿Cuándo fue la última vez que este usuario interactuó?"

✅ Solución elegida
python
# Añadir columna a tabla users
ALTER TABLE users ADD COLUMN last_activity TIMESTAMP WITH TIME ZONE;
POR QUÉ esta solución:

TIMESTAMP WITH TIME ZONE (TIMESTAMPTZ): Almacena datetime con zona horaria

Nullable por defecto: Usuarios antiguos tendrán NULL (no han interactuado aún)

Indexed automáticamente: Queries rápidas por fecha

Compatible con aplicación: Python datetime.now(timezone.utc)

🔄 Alternativas consideradas y rechazadas
Alternativa	Pros	Contras	Decisión
TIMESTAMP (sin TZ)	Más simple	Naive datetime, bug en comparaciones	❌ RECHAZADA
BIGINT (Unix timestamp)	Storage mínimo	Menos legible, conversión en app	❌ RECHAZADA
Tabla separada activity_log	Auditaría completa	Overcomplicated para MVP	❌ RECHAZADA
TIMESTAMPTZ (elegida)	UTC-aware, estándar	—	✅ ELEGIDA
💥 Impacto en el sistema
Tabla afectada:

users (agrega columna)

Cambios en aplicación:

BaseRepository: Ya soporta campos adicionales

UserRepository: Nuevo método update_last_activity(user_id)

Tests: Verificar timezone-aware en comparaciones

Performance:

Tamaño tabla: +8 bytes por registro (timestamp)

Queries: Sin índice por defecto (se puede agregar si necesario)

Backward compatibility:

✅ Existing users: last_activity = NULL hasta su próxima acción

✅ New users: Se llena automáticamente con datetime.now(timezone.utc)

🧪 Testing
Cómo verificamos:

python
# En test_update_last_activity():
updated = await repo.update_last_activity(user.id)
assert updated.last_activity is not None
assert updated.last_activity > user.created_at
assert updated.last_activity.tzinfo is not None  # timezone-aware
En QA:

sql
-- Verificar columna existe y es correcta
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name='users' 
AND column_name='last_activity';
-- Expected: timestamp with time zone

-- Verificar datos existentes
SELECT COUNT(*) FROM users WHERE last_activity IS NULL;
-- Expected: todos los usuarios antiguos tienen NULL
🔙 Rollback Plan
Si algo falla en producción:

python
# Rollback manual (si Alembic falla)
def downgrade():
    op.drop_column('users', 'last_activity')
Procedimiento:

alembic downgrade (vuelve a versión anterior)

Redeploy código sin referencia a last_activity

Verificar en producción que users tabla está intacta

Investigar causa

Crear nueva migración mejorada

📊 Contexto histórico
Fecha: 19 Nov 2025

Hito: H02 FASE 8 - Advanced Persistence

Autor: JARVIS + Álvaro (THEA-IA CEO)

Motivación: Engagement tracking + auditoría de seguridad

Status: ✅ APLICADA Y TESTEADA

🔗 Referencias
Modelo: src/theaia/database/models/user.py

Repository: src/theaia/database/repositories/user_repository.py

Tests: src/theaia/tests/database/repositories/test_user_repository.py::test_update_last_activity

BaseModel: src/theaia/database/models/base.py (DateTime handling)

Principios de Migraciones en THEA-IA
Siempre justificar: Por qué, no solo qué

Backward compatible: Existing data NO debe corromerse

Reversible: Downgrade debe funcionar

Testeado: Verificado en dev, staging, producción

Documentado: Este README es la verdad

Timezone-aware: Siempre UTC, siempre TIMESTAMPTZ

Multi-tenant safe: No corromper aislamiento tenant

Próximas migraciones (Roadmap)
 Índices en last_activity para queries de inactividad

 Columna updated_at (ya existe, solo documentar)

 Tabla activity_log cuando sea needed (auditoría completa)