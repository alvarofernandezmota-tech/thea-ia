"""
NoteRepository — Repository Pattern para gestión de notas
Multi-tenant isolation + CRUD + custom queries
"""
from typing import List, Optional
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from src.theaia.database.repositories.base_repository import BaseRepository
from src.theaia.database.models.note import Note

class NoteRepository(BaseRepository[Note]):
    """Repository para operaciones CRUD de notas con multi-tenant"""
    
    def __init__(self, session: AsyncSession):
        super().__init__(Note, session)

    async def create_note(
        self,
        tenant_id: str,
        user_id: int,
        title: str,
        content: str,
        category: Optional[str] = None,
        tags: Optional[List[str]] = None,
        is_pinned: bool = False
    ) -> Note:
        """Crear nueva nota con multi-tenant isolation"""
        note_data = {
            "tenant_id": tenant_id,
            "user_id": user_id,
            "title": title,
            "content": content,
            "category": category,
            "tags": tags or [],
            "is_pinned": is_pinned,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        return await self.create(note_data)
    
    async def get_by_user(
        self,
        tenant_id: str,
        user_id: int,
        limit: int = 50
    ) -> List[Note]:
        """Obtener notas de un usuario específico"""
        stmt = (
            select(self.model)
            .where(
                and_(
                    self.model.tenant_id == tenant_id,
                    self.model.user_id == user_id,
                )
            )
            .order_by(self.model.created_at.desc())
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
    
    async def search_by_tag(
        self,
        tenant_id: str,
        user_id: int,
        tag: str,
        limit: int = 100
    ) -> List[Note]:
        """Buscar notas por tag (PostgreSQL ARRAY contains)"""
        stmt = (
            select(self.model)
            .where(
                and_(
                    self.model.tenant_id == tenant_id,
                    self.model.user_id == user_id,
                    self.model.tags.contains([tag])  # PostgreSQL ARRAY
                )
            )
            .order_by(self.model.created_at.desc())
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
    
    async def search_by_category(
        self,
        tenant_id: str,
        user_id: int,
        category: str,
        limit: int = 100,
    ) -> List[Note]:
        """Buscar notas por categoría"""
        stmt = (
            select(self.model)
            .where(
                and_(
                    self.model.tenant_id == tenant_id,
                    self.model.user_id == user_id,
                    self.model.category == category
                )
            )
            .order_by(self.model.created_at.desc())
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
    
    async def get_pinned_notes(
        self,
        tenant_id: str,
        user_id: int
    ) -> List[Note]:
        """Obtener notas pinneadas"""
        stmt = (
            select(self.model)
            .where(
                and_(
                    self.model.tenant_id == tenant_id,
                    self.model.user_id == user_id,
                    self.model.is_pinned == True
                )
            )
            .order_by(self.model.updated_at.desc())
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
    
    async def toggle_pin(
        self,
        tenant_id: str,
        note_id: int
    ) -> Optional[Note]:
        """Toggle pin status de una nota"""
        note = await self.get_by_id(tenant_id, note_id)
        if note:
            note.is_pinned = not note.is_pinned
            note.updated_at = datetime.utcnow()
            await self.session.commit()
            await self.session.refresh(note)
        return note
