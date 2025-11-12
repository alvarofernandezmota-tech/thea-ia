"""
Note Repository para THEA IA
Gestión de notas con tags y categorías

Autor: Álvaro Fernández Mota
Fecha: 12 Nov 2025
Hito: H02 - Database Layer
"""

from typing import Optional, List
from sqlalchemy import select, and_, or_, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.theaia.database.repositories.base_repository import BaseRepository
from src.theaia.database.models.note import Note


class NoteRepository(BaseRepository[Note]):
    """
    Repository para operaciones CRUD de notas.
    
    Extiende BaseRepository con métodos específicos para notas:
    - get_by_user(): Notas de un usuario
    - search(): Búsqueda por contenido/título
    - get_by_tags(): Filtrar por tags
    - get_by_category(): Filtrar por categoría
    - toggle_pin(): Pin/unpin nota
    - get_pinned(): Obtener notas fijadas
    
    Example:
        async with get_db() as session:
            note_repo = NoteRepository(session)
            notes = await note_repo.search(1, "default", "reunión")
    """
    
    def __init__(self, session: AsyncSession):
        """
        Inicializa NoteRepository.
        
        Args:
            session: AsyncSession de SQLAlchemy
        """
        super().__init__(Note, session)
    
    async def get_by_user(
        self,
        user_id: int,
        tenant_id: str,
        skip: int = 0,
        limit: int = 100,
        order_by: str = "created_at"
    ) -> List[Note]:
        """
        Obtiene todas las notas de un usuario.
        
        Args:
            user_id: ID del usuario
            tenant_id: ID del tenant
            skip: Registros a saltar
            limit: Máximo de registros
            order_by: Campo para ordenar (created_at|updated_at|title)
        
        Returns:
            Lista de notas ordenadas
        
        Example:
            # Más recientes primero
            notes = await note_repo.get_by_user(1, "default", order_by="created_at")
            
            # Paginación
            page2 = await note_repo.get_by_user(1, "default", skip=10, limit=10)
        """
        stmt = select(Note).where(
            Note.user_id == user_id,
            Note.tenant_id == tenant_id
        )
        
        # Ordenar por campo especificado
        if order_by == "created_at":
            stmt = stmt.order_by(Note.created_at.desc())
        elif order_by == "updated_at":
            stmt = stmt.order_by(Note.updated_at.desc())
        elif order_by == "title":
            stmt = stmt.order_by(Note.title.asc())
        else:
            stmt = stmt.order_by(Note.created_at.desc())
        
        stmt = stmt.offset(skip).limit(limit)
        
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
    
    async def search(
        self,
        user_id: int,
        tenant_id: str,
        query: str,
        skip: int = 0,
        limit: int = 50
    ) -> List[Note]:
        """
        Busca notas por contenido o título (case-insensitive).
        
        Args:
            user_id: ID del usuario
            tenant_id: ID del tenant
            query: Texto a buscar
            skip: Registros a saltar
            limit: Máximo de registros
        
        Returns:
            Lista de notas que coinciden con la búsqueda
        
        Example:
            # Buscar "reunión"
            results = await note_repo.search(1, "default", "reunión")
            
            # Buscar en título o contenido
            results = await note_repo.search(1, "default", "proyecto")
        """
        search_pattern = f"%{query.lower()}%"
        
        stmt = select(Note).where(
            and_(
                Note.user_id == user_id,
                Note.tenant_id == tenant_id,
                or_(
                    func.lower(Note.title).like(search_pattern),
                    func.lower(Note.content).like(search_pattern)
                )
            )
        ).order_by(Note.updated_at.desc()).offset(skip).limit(limit)
        
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
    
    async def get_by_tags(
        self,
        user_id: int,
        tenant_id: str,
        tags: List[str],
        match_all: bool = False
    ) -> List[Note]:
        """
        Obtiene notas que contienen tags específicos.
        
        Args:
            user_id: ID del usuario
            tenant_id: ID del tenant
            tags: Lista de tags a buscar
            match_all: Si True, debe tener TODOS los tags. Si False, al menos uno.
        
        Returns:
            Lista de notas con los tags
        
        Example:
            # Notas con tag "trabajo" O "personal"
            notes = await note_repo.get_by_tags(1, "default", ["trabajo", "personal"])
            
            # Notas con tag "trabajo" Y "urgente"
            notes = await note_repo.get_by_tags(
                1, "default", ["trabajo", "urgente"], match_all=True
            )
        """
        stmt = select(Note).where(
            Note.user_id == user_id,
            Note.tenant_id == tenant_id
        )
        
        if match_all:
            # Debe contener TODOS los tags
            for tag in tags:
                stmt = stmt.where(Note.tags.contains([tag]))
        else:
            # Al menos uno de los tags
            stmt = stmt.where(Note.tags.overlap(tags))
        
        stmt = stmt.order_by(Note.updated_at.desc())
        
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
    
    async def get_by_category(
        self,
        user_id: int,
        tenant_id: str,
        category: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[Note]:
        """
        Obtiene notas de una categoría específica.
        
        Args:
            user_id: ID del usuario
            tenant_id: ID del tenant
            category: Nombre de la categoría
            skip: Registros a saltar
            limit: Máximo de registros
        
        Returns:
            Lista de notas de la categoría
        
        Example:
            work_notes = await note_repo.get_by_category(1, "default", "trabajo")
        """
        return await self.get_all(
            tenant_id=tenant_id,
            skip=skip,
            limit=limit,
            filters={"user_id": user_id, "category": category}
        )
    
    async def get_pinned(
        self,
        user_id: int,
        tenant_id: str
    ) -> List[Note]:
        """
        Obtiene todas las notas fijadas (pinned) del usuario.
        
        Args:
            user_id: ID del usuario
            tenant_id: ID del tenant
        
        Returns:
            Lista de notas fijadas
        
        Example:
            pinned = await note_repo.get_pinned(1, "default")
            print(f"Tienes {len(pinned)} notas fijadas")
        """
        stmt = select(Note).where(
            Note.user_id == user_id,
            Note.tenant_id == tenant_id,
            Note.is_pinned == True
        ).order_by(Note.updated_at.desc())
        
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
    
    async def toggle_pin(
        self,
        note_id: int,
        tenant_id: str
    ) -> Optional[Note]:
        """
        Alterna el estado de pin de una nota.
        
        Args:
            note_id: ID de la nota
            tenant_id: ID del tenant
        
        Returns:
            Nota actualizada o None
        
        Example:
            # Fijar/desfijar nota
            note = await note_repo.toggle_pin(5, "default")
            if note.is_pinned:
                print("Nota fijada")
            else:
                print("Nota desfijada")
        """
        note = await self.get_by_id(note_id, tenant_id)
        if not note:
            return None
        
        note.is_pinned = not note.is_pinned
        
        await self.session.flush()
        await self.session.refresh(note)
        return note
    
    async def add_tags(
        self,
        note_id: int,
        tenant_id: str,
        new_tags: List[str]
    ) -> Optional[Note]:
        """
        Añade tags a una nota existente.
        
        Args:
            note_id: ID de la nota
            tenant_id: ID del tenant
            new_tags: Lista de tags a añadir
        
        Returns:
            Nota actualizada o None
        
        Example:
            # Añadir tags
            note = await note_repo.add_tags(5, "default", ["urgente", "revisar"])
        """
        note = await self.get_by_id(note_id, tenant_id)
        if not note:
            return None
        
        current_tags = note.tags or []
        # Evitar duplicados
        for tag in new_tags:
            if tag not in current_tags:
                current_tags.append(tag)
        
        note.tags = current_tags
        
        await self.session.flush()
        await self.session.refresh(note)
        return note
    
    async def remove_tags(
        self,
        note_id: int,
        tenant_id: str,
        tags_to_remove: List[str]
    ) -> Optional[Note]:
        """
        Elimina tags de una nota.
        
        Args:
            note_id: ID de la nota
            tenant_id: ID del tenant
            tags_to_remove: Lista de tags a eliminar
        
        Returns:
            Nota actualizada o None
        
        Example:
            # Quitar tag "urgente"
            note = await note_repo.remove_tags(5, "default", ["urgente"])
        """
        note = await self.get_by_id(note_id, tenant_id)
        if not note:
            return None
        
        current_tags = note.tags or []
        note.tags = [tag for tag in current_tags if tag not in tags_to_remove]
        
        await self.session.flush()
        await self.session.refresh(note)
        return note
    
    async def count_by_category(
        self,
        user_id: int,
        tenant_id: str
    ) -> dict:
        """
        Cuenta notas por categoría del usuario.
        
        Args:
            user_id: ID del usuario
            tenant_id: ID del tenant
        
        Returns:
            Dict con categoría: count
        
        Example:
            counts = await note_repo.count_by_category(1, "default")
            # {"trabajo": 15, "personal": 8, None: 3}
        """
        stmt = select(
            Note.category,
            func.count(Note.id)
        ).where(
            Note.user_id == user_id,
            Note.tenant_id == tenant_id
        ).group_by(Note.category)
        
        result = await self.session.execute(stmt)
        return {category: count for category, count in result.all()}
