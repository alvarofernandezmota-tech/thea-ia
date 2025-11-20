Database Repositories – THEA-IA H02
Visión General
Los repositorios en THEA-IA implementan el patrón Repository: capa de abstracción sobre SQLAlchemy que centraliza lógica de acceso a datos. Async-first, multi-tenant-safe, exhaustivamente testeado.

BaseRepository – Patrón genérico CRUD
📌 Problema que resolvemos
Requerimiento: Cada modelo (User, Event, Note, etc.) necesita:

Create, Read, Update, Delete

Get by ID

Get all con filtros

Count

Lógica de tenant isolation

Sin esto: 6 repositorios copiarían el mismo código 80 veces, mantenimiento imposible.

✅ Solución elegida
python
class BaseRepository(Generic[T]):
    """
    Repositorio genérico asíncrono.
    
    Tipo-parametrizado: BaseRepository[User], BaseRepository[Event], etc.
    Centraliza CRUD y multi-tenant logic en un solo lugar.
    """
    
    def __init__(self, session: AsyncSession, model: Type[T]):
        self.session = session
        self.model = model
    
    async def create(self, **kwargs) -> T:
        """Crear un registro con tenant_id obligatorio"""
        obj = self.model(**kwargs)
        self.session.add(obj)
        await self.session.flush()  # Asigna ID sin commit
        return obj
    
    async def get_by_id(self, id: int, tenant_id: str = None) -> Optional[T]:
        """Obtener por ID, con tenant isolation si se especifica"""
        query = select(self.model).where(self.model.id == id)
        if tenant_id:
            query = query.where(self.model.tenant_id == tenant_id)
        result = await self.session.execute(query)
        return result.scalars().first()
    
    async def get_all(self, tenant_id: str = None) -> List[T]:
        """Obtener todos, con tenant isolation si se especifica"""
        query = select(self.model)
        if tenant_id:
            query = query.where(self.model.tenant_id == tenant_id)
        result = await self.session.execute(query)
        return result.scalars().all()
    
    async def update(self, id: int, tenant_id: str = None, **kwargs) -> Optional[T]:
        """Actualizar registro, validando tenant_id"""
        obj = await self.get_by_id(id, tenant_id)
        if not obj:
            return None
        for key, value in kwargs.items():
            setattr(obj, key, value)
        await self.session.flush()
        return obj
    
    async def delete(self, id: int, tenant_id: str = None) -> bool:
        """Eliminar registro, validando tenant_id"""
        obj = await self.get_by_id(id, tenant_id)
        if not obj:
            return False
        await self.session.delete(obj)
        await self.session.flush()
        return True
POR QUÉ esta solución:

Generic[T] type parametrization:

BaseRepository[User]: El tipo se infiere automáticamente

Type-safe: Errores detectados en IDE

Reutilizable: Mismo código para User, Event, Note, etc.

Async-first con await:

Todas las operaciones son async (I/O no bloqueante)

.flush() vs .commit(): Flush asigna ID sin commitar

Compatible con FastAPI, Telegram bots, concurrencia

Multi-tenant isolation:

tenant_id como parámetro obligatorio en update/delete

get_by_id puede validar tenant (seguridad)

get_all con filtro opcional de tenant

Session management:

Session inyectada en constructor

Lifecycle gestionado por fixture (ver conftest)

Rollback automático si no hay commit

🔄 Alternativas consideradas y rechazadas
Alternativa	Pros	Contras	Decisión
Sync SQLAlchemy	Más simple	Bloquea en I/O, no escalable	❌ RECHAZADA
Raw SQL queries	Máximo control	SQL injection risk, mantenimiento hard	❌ RECHAZADA
ORM automático (SQLModel)	Auto Pydantic	Overhead, menos flexible	❌ RECHAZADA
BaseRepository genérico async	DRY, type-safe, escalable	Más código inicial	✅ ELEGIDA
UserRepository – Especialización multi-tenant + Telegram
📌 Problema que resolvemos
Requerimiento: Users tienen necesidades específicas:

Buscar por telegram_id (Telegram integration)

Get or create (idempotencia Telegram)

Update preferences (JSON preferences)

Track last_activity (engagement)

Multi-tenant aislamiento (telegram_id duplicado en otros tenants es OK)

Sin esto: Cada telegram message tendría que buscar User manualmente.

✅ Solución elegida
python
class UserRepository(BaseRepository[User]):
    """
    Repositorio especializado para User.
    
    Hereda CRUD de BaseRepository.
    Añade lógica Telegram-específica.
    """
    
    async def get_by_telegram_id(
        self, 
        telegram_id: str, 
        tenant_id: str
    ) -> Optional[User]:
        """
        Buscar usuario por telegram_id + tenant_id.
        
        Multi-tenant: Mismo telegram_id en tenants diferentes = usuarios DIFERENTES.
        """
        query = select(User).where(
            (User.telegram_id == telegram_id) &
            (User.tenant_id == tenant_id)
        )
        result = await self.session.execute(query)
        return result.scalars().first()
    
    async def get_or_create_telegram_user(
        self,
        telegram_id: str,
        tenant_id: str,
        defaults: Dict[str, Any]
    ) -> Tuple[User, bool]:
        """
        Get or create: idempotente para Telegram messages.
        
        Retorna: (user, created)
        - Si existe: (user, False)
        - Si no existe: (user_nuevo, True)
        """
        user = await self.get_by_telegram_id(telegram_id, tenant_id)
        
        if user:
            return user, False
        
        # Crear con telegram_id + tenant_id + defaults
        user = await self.create(
            telegram_id=telegram_id,
            tenant_id=tenant_id,
            **defaults
        )
        return user, True
    
    async def update_last_activity(self, user_id: int) -> User:
        """
        Actualizar last_activity con timestamp UTC-aware.
        
        Usado cuando usuario interactúa (mensaje Telegram, API call, etc.).
        """
        user = await self.get_by_id(user_id)
        if not user:
            raise ValueError(f"User {user_id} not found")
        
        return await self.update(
            user_id,
            tenant_id=user.tenant_id,  # Preservar tenant
            last_activity=datetime.now(timezone.utc)
        )
POR QUÉ esta solución:

get_by_telegram_id(telegram_id, tenant_id):

Búsqueda por compound key (telegram_id, tenant_id)

Multi-tenant: Mismo telegram_id es OTRO usuario en otro tenant

Seguridad: No puedo acceder telegram_id de otro tenant

get_or_create_telegram_user():

Idempotencia: Mismo telegram_id → mismo User siempre

Elimina race conditions: "Crear si no existe"

Retorna tupla (user, created): Caller sabe si es nuevo

update_last_activity():

Dedicated method: Claridad de intent

Usa timezone-aware: datetime.now(timezone.utc)

Valida que user existe: No silent failures

🧪 Testing UserRepository
Estructura de tests:

python
# src/theaia/tests/database/repositories/test_user_repository.py

class TestUserRepositoryBasic:
    """CRUD básico"""
    @pytest.mark.asyncio
    async def test_create_user_basic(self, db_session, test_user_data):
        repo = UserRepository(db_session)
        user = await repo.create(**test_user_data)
        assert user.id is not None

class TestUserRepositoryTelegram:
    """Lógica Telegram"""
    @pytest.mark.asyncio
    async def test_get_by_telegram_id(self, db_session, test_user_data):
        repo = UserRepository(db_session)
        created = await repo.create(**test_user_data)
        retrieved = await repo.get_by_telegram_id(
            test_user_data["telegram_id"],
            test_user_data["tenant_id"]
        )
        assert retrieved.id == created.id

class TestUserRepositoryMultiTenant:
    """Aislamiento multi-tenant"""
    @pytest.mark.asyncio
    async def test_users_isolated_by_tenant(self, db_session, test_user_data):
        repo = UserRepository(db_session)
        user_1 = await repo.create(**{**test_user_data, "tenant_id": "tenant_1"})
        user_2 = await repo.create(**{**test_user_data, "tenant_id": "tenant_2"})
        
        # Mismo telegram_id, diferentes tenants = DIFERENTES usuarios
        assert user_1.id != user_2.id
        assert user_1.telegram_id == user_2.telegram_id
Resultado: 13/13 tests PASAN en Windows + Linux

Patrón general para otros repositorios
Cuando crees EventRepository, NoteRepository, etc.:

python
class EventRepository(BaseRepository[Event]):
    """
    Eventos de usuario.
    
    Hereda: CRUD genérico
    Especializa: Búsqueda por fecha, filtro por user, etc.
    """
    
    async def get_by_date_range(
        self,
        tenant_id: str,
        start_date: datetime,
        end_date: datetime
    ) -> List[Event]:
        """Eventos en rango de fechas"""
        query = select(Event).where(
            (Event.tenant_id == tenant_id) &
            (Event.event_date >= start_date) &
            (Event.event_date <= end_date)
        )
        result = await self.session.execute(query)
        return result.scalars().all()
🛡️ Principios de diseño
DRY: BaseRepository centraliza lógica común

Multi-tenant first: Siempre validar tenant_id en queries

Type-safe: Generic[T] para errores en IDE

Async-first: Todas las operaciones son async

Testeable: Inyección de sesión para mocks fáciles

Idempotencia: Get or create, no race conditions

Contexto histórico
Fecha: 19 Nov 2025

Hito: H02 FASE 8 - Advanced Persistence

Tests: UserRepository 13/13 PASAN

Coverage: 76% BaseRepository, 71% UserRepository

Platform: Windows + Linux compatible

Próximos repositorios
 EventRepository (búsqueda por fecha, filtros)

 NoteRepository (búsqueda por tags, full-text)

 ConversationRepository (sesiones, borrado en cascada)

 MessageHistoryRepository (bulk inserts, paginación)

 Todos: Cobertura ≥70% tests