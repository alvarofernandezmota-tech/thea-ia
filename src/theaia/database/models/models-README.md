Database Models – THEA-IA H02
Visión General
Los modelos SQLAlchemy en THEA-IA son la estructura fundamental del sistema. Cada modelo representa una entidad de dominio con reglas claras: multi-tenant, timezone-aware, auditaría integrada.

BaseModel – Fundación de todos los modelos
📌 Problema que resolvemos
Requerimiento: Todos los modelos necesitan:

ID autoincremental único

Tenant ID para multi-tenancy

Timestamps de creación/actualización para auditoría

Timezone consistency (UTC siempre)

Sin esto: Cada modelo repetiría código, timezone bugs cruzarían la app, no habría auditoría.

✅ Solución elegida
python
class BaseModel(Base):
    __abstract__ = True
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    tenant_id = Column(String(50), nullable=False, default='default', index=True)
    
    # ✅ TIMEZONE-AWARE: DateTime(timezone=True) + lambda datetime.now(timezone.utc)
    created_at = Column(
        DateTime(timezone=True), 
        default=lambda: datetime.now(timezone.utc), 
        nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True), 
        default=lambda: datetime.now(timezone.utc), 
        onupdate=lambda: datetime.now(timezone.utc), 
        nullable=False
    )
POR QUÉ esta solución:

DateTime(timezone=True) en PostgreSQL:

Almacena TIMESTAMPTZ (timestamp with time zone)

Siempre UTC internamente

Python recibe datetime con tzinfo=<UTC>

Evita naive vs aware comparison errors

lambda: datetime.now(timezone.utc) (no datetime.utcnow()):

utcnow() está deprecated en Python 3.12+

now(timezone.utc) es el estándar moderno

Lambda se ejecuta en CADA insert/update (fresh timestamp)

tenant_id obligatorio y indexado:

Garantiza multi-tenant aislamiento

Index automático para queries rápidas

Todos los queries filtran por tenant_id

Auditoría integrada:

created_at: Cuándo nació el registro (NUNCA cambia)

updated_at: Cuándo fue modificado (cambia con cada update)

Perfecto para análisis de histórico, debugging

🔄 Alternativas consideradas y rechazadas
Alternativa	Pros	Contras	Decisión
TIMESTAMP sin TZ	Más simple en BD	Naive, comparaciones fallan en tests	❌ RECHAZADA
datetime.utcnow()	Función built-in	Deprecated, problemas Windows asyncpg	❌ RECHAZADA
BIGINT (Unix timestamp)	Storage eficiente	Timestamps ilegibles en queries	❌ RECHAZADA
No tenant_id	Menos columnas	Cross-tenant leakage, seguridad comprometida	❌ RECHAZADA
DateTime(timezone=True) + lambda now(UTC)	UTC-aware, moderno, estándar	—	✅ ELEGIDA
💥 Impacto en el sistema
Modelos que heredan BaseModel:

User (telegram_id, username, preferences, last_activity)

Event (title, description, event_date, location)

Note (content, tags)

Conversation (session_id, current_state, context)

MessageHistory (role, content, intent, confidence)

Cambios en aplicación:

Todos los modelos tienen id, tenant_id, created_at, updated_at

Queries SIEMPRE filtran por tenant_id (seguridad)

Timestamps SIEMPRE son timezone-aware (consistency)

Tests pueden comparar datetimes sin errores

Performance:

4 columnas base por tabla (~32 bytes por registro)

Index en tenant_id: Queries por tenant muy rápidas

No hay overhead de JOINs (todo dentro del modelo)

Backward compatibility:

✅ Migración de legacy systems: tenant_id defaultea a 'default'

✅ Tests crean records con tenant_id explícito

✅ Existing records: created_at/updated_at rellenados automáticamente

🧪 Testing BaseModel
En conftest.py:

python
def test_base_model_timestamps_aware():
    """Verificar que created_at y updated_at son timezone-aware"""
    user = User(tenant_id="test", telegram_id=123, username="test")
    
    assert user.created_at.tzinfo is not None
    assert user.updated_at.tzinfo is not None
    assert user.created_at.tzinfo == timezone.utc
En tests de cada repo:

python
async def test_update_last_activity(self, db_session, test_user_data):
    repo = UserRepository(db_session)
    user = await repo.create(**test_user_data)
    updated = await repo.update_last_activity(user.id)
    
    # ✅ Estos tipos de asserts funcionan gracias a timezone-aware
    assert updated.last_activity > user.created_at
    assert updated.updated_at > user.created_at
🏗️ Estructura detallada
python
# src/theaia/database/models/base.py
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class BaseModel(Base):
    """
    Modelo base del que heredan TODOS los modelos.
    
    Garantiza:
    - Multi-tenancy: tenant_id en todos
    - Auditoría: created_at (nunca cambia), updated_at (siempre actualizado)
    - Timezone consistency: TIMESTAMPTZ (UTC), datetime.now(timezone.utc)
    - Uniqueness: id autoincremental
    """
    __abstract__ = True
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    tenant_id = Column(String(50), nullable=False, default='default', index=True)
    
    created_at = Column(
        DateTime(timezone=True), 
        default=lambda: datetime.now(timezone.utc), 
        nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True), 
        default=lambda: datetime.now(timezone.utc), 
        onupdate=lambda: datetime.now(timezone.utc), 
        nullable=False
    )
    
    def to_dict(self):
        """Convierte el modelo a diccionario para APIs/serialización"""
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }
    
    def __repr__(self):
        return f"<{self.__class__.__name__}(id={self.id}, tenant_id={self.tenant_id})>"
📋 Ejemplo: User Model
python
# src/theaia/database/models/user.py
from sqlalchemy import Column, String, JSON, DateTime
from datetime import datetime, timezone
from .base import BaseModel

class User(BaseModel):
    """
    Modelo de Usuario con Telegram integration y multi-tenant support.
    
    Hereda de BaseModel:
    - id: autoincremental
    - tenant_id: aislamiento multi-tenant
    - created_at: timestamp creación (UTC-aware)
    - updated_at: timestamp actualización (UTC-aware)
    """
    __tablename__ = 'users'
    
    telegram_id = Column(String(50), nullable=False)
    username = Column(String(100), nullable=True)
    first_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)
    language_code = Column(String(10), default='es')
    preferences = Column(JSON, default={})
    last_activity = Column(DateTime(timezone=True), nullable=True)
    
    def __repr__(self):
        return f"<User(id={self.id}, telegram_id={self.telegram_id}, tenant={self.tenant_id})>"
🔗 Relaciones entre modelos
text
BaseModel
├── User (telegram_id, preferences, last_activity)
├── Event (title, event_date, user_id → User)
├── Note (content, tags, user_id → User)
├── Conversation (session_id, user_id → User)
└── MessageHistory (role, content, conversation_id → Conversation)

Constraints:
- TODOS filtran por tenant_id (multi-tenant)
- TODOS tienen created_at/updated_at (auditoría)
- TODOS son timezone-aware (UTC)
🛡️ Principios de diseño
Multi-tenant first: tenant_id en TODOS, sin excepción

Auditoría integrada: created_at (histórico), updated_at (monitoreo)

Timezone consistency: Siempre UTC, siempre TIMESTAMPTZ, siempre Python timezone-aware

Simplicity: Cada modelo = una tabla, sin denormalización prematura

Inheritance: BaseModel centraliza lógica común (DRY)

Contexto histórico
Fecha: 19 Nov 2025

Hito: H02 FASE 8 - Advanced Persistence

Decisión crítica: DateTime(timezone=True) + lambda (no utcnow) para Windows/Linux compatibility

Impacto: Zera timezone bugs, aislamiento tenant perfecto

Próximos refactors
 SQLAlchemy 2.0: cambiar declarative_base() a sqlalchemy.orm.declarative_base

 Añadir constraints UNIQUE en combos como (tenant_id, telegram_id) en User

 Documentar relaciones OneToMany/ForeignKeys cuando se añadan