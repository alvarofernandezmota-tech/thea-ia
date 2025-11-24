"""
NoteAgent Handler — Gestión inteligente de notas
Pattern: AgendaAgent v2.0 adapted for notes
FSM per-user + ML integration + Database persistence
"""
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta, timezone
import logging

from src.theaia.agents.base_agent import BaseAgent
from src.theaia.agents.note_agent.note_conversation_manager import NoteConversationManager
from src.theaia.agents.note_agent.model.note_fsm import NoteFSM
from src.theaia.database.repositories.note_repository import NoteRepository
from src.theaia.ml.entity_extractor.person_name_extractor import PersonNameExtractor
from src.theaia.ml.entity_extractor.location_extractor import LocationExtractor
from src.theaia.ml.entity_extractor.pipeline import EntityExtractionPipeline


class NoteAgent(BaseAgent):
    """
    NoteAgent — Gestión inteligente de notas con ML y persistencia

    Features:
    - FSM per-user para conversaciones multi-turn
    - ML entity extraction (personas, ubicaciones)
    - Database persistence (NoteRepository)
    - CRUD completo (create, read, update, delete)
    - Search (por tags, categoría, contenido)
    - Pin/unpin notes (notas importantes)
    - Filtros avanzados (fecha, solo fijadas)
    - Multi-tenant isolation

    Architecture:
    - Handler: Este archivo (orchestration)
    - FSM: note_fsm.py (state management)
    - Repository: NoteRepository (persistence)
    - ML: PersonExtractor, LocationExtractor (entity extraction)

    Coverage target: ≥85%
    Pattern: AgendaAgent v2.0 adapted
    """
    def __init__(self, user_id: str):
        super().__init__()
        self.user_id = user_id
        self.conversation_manager = NoteConversationManager(user_id)

        self.user_fsms: Dict[str, NoteFSM] = {}

        self.note_repository: Optional[NoteRepository] = None

        self.person_extractor = PersonNameExtractor()
        self.location_extractor = LocationExtractor()
        self.entity_pipeline = EntityExtractionPipeline()

        self.logger = logging.getLogger(f"{__name__}.NoteAgent")

    async def initialize(self, session):
        self.note_repository = NoteRepository(session)
        self.logger.info(f"NoteAgent initialized for user {self.user_id}")

    def get_supported_intents(self) -> List[str]:
        return ["nota", "notas", "apunte", "apuntes", "recordatorio_texto", "memoria"]

    def _get_or_create_fsm(self, user_id: str) -> NoteFSM:
        if user_id not in self.user_fsms:
            self.user_fsms[user_id] = NoteFSM()
            self.logger.info(f"Created new FSM for user {user_id}")
        return self.user_fsms[user_id]
    
    def _get_tenant_id(self, context: Dict) -> str:
        """✨ FIX: Helper seguro para obtener tenant_id con fallback."""
        return context.get("tenant_id", "default_tenant")

    async def handle(
        self,
        user_id: str,
        message: str,
        context: Dict
    ) -> Tuple[str, str, Dict]:
        try:
            fsm = self._get_or_create_fsm(user_id)
            current_state = fsm.current_state

            self.logger.debug(f"Processing message in state: {current_state}")

            entities = await self._extract_entities(message, context)

            action = self._determine_action(message, current_state, entities)

            self.logger.info(f"Determined action: {action}")

            if action == "create_note":
                return await self._handle_create_note(user_id, message, context, entities, fsm)
            elif action == "list_notes":
                return await self._handle_list_notes(user_id, context, fsm)
            elif action == "search_notes":
                return await self._handle_search_notes(user_id, message, context, entities, fsm)
            elif action == "edit_note":
                return await self._handle_edit_note(user_id, message, context, entities, fsm)
            elif action == "delete_note":
                return await self._handle_delete_note(user_id, message, context, fsm)
            elif action == "pin_note":
                return await self._handle_pin_note(user_id, message, context, fsm)
            elif action == "get_note":
                return await self._handle_get_note(user_id, message, context, fsm)
            elif action == "list_pinned":
                return await self._handle_list_pinned_notes(user_id, context, fsm)
            elif action == "filter_by_date":
                return await self._handle_filter_by_date(user_id, message, context, fsm)
            else:
                return self.conversation_manager.handle_message(user_id, message, context)

        except Exception as e:
            self.logger.error(f"Error handling message: {e}", exc_info=True)
            return (
                f"❌ Error procesando nota: {str(e)}",
                "idle",
                context
            )

    async def _extract_entities(self, message: str, context: Dict) -> Dict:
        entities = {}
        persons = self.person_extractor.extract(message)
        if persons:
            entities["persons"] = persons
            self.logger.debug(f"Extracted persons: {persons}")

        locations = self.location_extractor.extract(message)
        if locations:
            entities["locations"] = locations
            self.logger.debug(f"Extracted locations: {locations}")

        try:
            pipeline_entities = await self.entity_pipeline.extract(
                message,
                context=context
            )
            entities.update(pipeline_entities)
        except Exception as e:
            self.logger.warning(f"Pipeline extraction failed: {e}")

        return entities

    def _determine_action(
        self,
        message: str,
        current_state: str,
        entities: Dict
    ) -> str:
        msg_lower = message.lower()

        # ✨ FIX: Si estamos en flujos específicos, continuar con ellos
        if current_state == "awaiting_edit_content":
            return "edit_note"
        
        if current_state == "awaiting_delete_confirmation":
            return "delete_note"
        
        # Para estados de creación, continuar con create_note
        if current_state not in ["idle", "awaiting_edit_content", "awaiting_delete_confirmation"]:
            return "create_note"

        # SOLO detectar acciones cuando estamos en IDLE
        create_keywords = ["crear", "nueva", "apuntar", "anota", "guarda", "escribe", "añade"]
        if any(keyword in msg_lower for keyword in create_keywords):
            return "create_note"

        # Detectar filtros de fecha
        date_keywords = ["hoy", "esta semana", "este mes", "últimos", "recientes"]
        if any(keyword in msg_lower for keyword in date_keywords):
            return "filter_by_date"

        # Detectar lista de notas fijadas
        pinned_list_keywords = ["fijadas", "pinneadas", "importantes"]
        if any(keyword in msg_lower for keyword in pinned_list_keywords):
            return "list_pinned"

        list_keywords = ["listar", "mostrar todas", "ver notas", "mis notas", "lista"]
        if any(keyword in msg_lower for keyword in list_keywords):
            return "list_notes"

        search_keywords = ["buscar", "encontrar", "filtrar", "busca"]
        if any(keyword in msg_lower for keyword in search_keywords):
            return "search_notes"

        edit_keywords = ["editar", "modificar", "cambiar", "actualizar"]
        if any(keyword in msg_lower for keyword in edit_keywords):
            return "edit_note"

        delete_keywords = ["borrar", "eliminar", "quitar", "borra"]
        if any(keyword in msg_lower for keyword in delete_keywords):
            return "delete_note"

        pin_keywords = ["fijar", "pin", "fija"]
        if any(keyword in msg_lower for keyword in pin_keywords):
            return "pin_note"

        get_keywords = ["mostrar nota", "ver nota", "abrir nota"]
        if any(keyword in msg_lower for keyword in get_keywords):
            return "get_note"

        return "unknown"

    async def _handle_create_note(
        self,
        user_id: str,
        message: str,
        context: Dict,
        entities: Dict,
        fsm: NoteFSM
    ) -> Tuple[str, str, Dict]:
        current_state = fsm.current_state
        note_data = self._parse_note_from_message(message, entities)

        if current_state == "idle":
            if note_data.get("title") and note_data.get("content"):
                fsm.transition_to("awaiting_confirmation")
                fsm.context.update(note_data)
                response = self._format_note_confirmation(fsm.context)
            else:
                fsm.transition_to("awaiting_note_title")
                response = "📝 Perfecto. ¿Qué título quieres para la nota?"

        elif current_state == "awaiting_note_title":
            fsm.context["title"] = message.strip()
            fsm.transition_to("awaiting_note_content")
            response = f"✅ Título: **{message}**\n\n¿Qué contenido tiene la nota?"

        elif current_state == "awaiting_note_content":
            fsm.context["content"] = message.strip()
            category = self._auto_detect_category(entities)
            if category:
                fsm.context["category"] = category
            tags = self._auto_extract_tags(message, entities)
            if tags:
                fsm.context["tags"] = tags
            fsm.transition_to("awaiting_confirmation")
            response = self._format_note_confirmation(fsm.context)

        elif current_state == "awaiting_confirmation":
            if any(word in message.lower() for word in ["sí", "si", "ok", "vale", "confirmar", "guardar", "yes"]):
                try:
                    # ✨ FIX: Uso seguro de tenant_id
                    note = await self.note_repository.create(
                        tenant_id=self._get_tenant_id(context),
                        user_id=user_id,
                        title=fsm.context.get("title"),
                        content=fsm.context.get("content"),
                        category=fsm.context.get("category"),
                        tags=fsm.context.get("tags", [])
                    )
                    fsm.reset()
                    response = f"✅ **Nota guardada correctamente**\n\n📌 ID: {note.id}\n📝 Título: {note.title}"
                except Exception as e:
                    self.logger.error(f"Error saving note: {e}")
                    fsm.reset()
                    response = f"❌ Error guardando nota: {str(e)}"
            else:
                fsm.reset()
                response = "❌ Nota cancelada"
        else:
            response = "⚙️ Estado no esperado en creación de nota."

        return response, fsm.current_state, fsm.context

    async def _handle_list_notes(
        self,
        user_id: str,
        context: Dict,
        fsm: NoteFSM
    ) -> Tuple[str, str, Dict]:
        try:
            # ✨ FIX: Uso seguro de tenant_id
            notes = await self.note_repository.get_by_user(
                tenant_id=self._get_tenant_id(context),
                user_id=user_id,
                limit=10
            )
            if not notes:
                response = "📝 No tienes notas guardadas todavía"
            else:
                response = f"📝 **Tus notas ({len(notes)}):**\n\n"
                for note in notes:
                    pin_emoji = "📌 " if note.is_pinned else ""
                    response += f"{pin_emoji}**{note.title}** (ID: {note.id})\n"
                    content_preview = note.content[:50] + "..." if len(note.content) > 50 else note.content
                    response += f"_{content_preview}_\n\n"
            return response, "idle", {}

        except Exception as e:
            self.logger.error(f"Error listing notes: {e}")
            return f"❌ Error listando notas: {str(e)}", "idle", {}

    async def _handle_search_notes(
        self,
        user_id: str,
        message: str,
        context: Dict,
        entities: Dict,
        fsm: NoteFSM
    ) -> Tuple[str, str, Dict]:
        search_term = message.replace("buscar", "").replace("nota", "").replace("notas", "").strip()
        try:
            # ✨ FIX: Uso seguro de tenant_id
            all_notes = await self.note_repository.get_by_user(
                tenant_id=self._get_tenant_id(context),
                user_id=user_id,
                limit=100
            )
            notes = [
                note for note in all_notes
                if (search_term.lower() in str(note.tags).lower() or
                    (note.category and search_term.lower() == note.category.lower()) or
                    search_term.lower() in note.content.lower())
            ]
            if not notes:
                response = f"🔍 No encontré notas con '{search_term}'"
            else:
                response = f"🔍 **Notas con '{search_term}' ({len(notes)}):**\n\n"
                for note in notes:
                    response += f"**{note.title}** (ID: {note.id})\n"
                    content_preview = note.content[:100] + "..." if len(note.content) > 100 else note.content
                    response += f"{content_preview}\n\n"
            return response, "idle", {}

        except Exception as e:
            self.logger.error(f"Error searching notes: {e}")
            return f"❌ Error buscando notas: {str(e)}", "idle", {}

    async def _handle_edit_note(
        self,
        user_id: str,
        message: str,
        context: Dict,
        entities: Dict,
        fsm: NoteFSM
    ) -> Tuple[str, str, Dict]:
        """Handle note editing flow."""
        current_state = fsm.current_state

        import re

        if current_state == "idle":
            match = re.search(r'\d+', message)
            if match:
                note_id = int(match.group())
                try:
                    # ✨ FIX: Uso seguro de tenant_id
                    note = await self.note_repository.get_by_id(note_id, self._get_tenant_id(context))
                    if not note or str(note.user_id) != str(user_id):
                        return "❌ Nota no encontrada o no te pertenece.", "idle", {}
                    fsm.context["edit_note_id"] = note_id
                    fsm.context["current_title"] = note.title
                    fsm.context["current_content"] = note.content
                    fsm.transition_to("awaiting_edit_content")
                    resp = (
                        f"✏️ **Editando nota {note_id}**\n"
                        f"**Título actual:** {note.title}\n"
                        f"**Contenido actual:**\n{note.content[:100]}...\n\n"
                        "Envía el nuevo contenido para actualizar la nota:"
                    )
                    return resp, fsm.current_state, fsm.context
                except Exception as e:
                    self.logger.error(f"Error buscando nota para editar: {e}")
                    return f"❌ Error buscando nota: {str(e)}", "idle", {}
            else:
                return "❌ Debes indicar el ID de la nota a editar (ej: 'editar nota 5')", "idle", {}

        elif current_state == "awaiting_edit_content":
            try:
                note_id = fsm.context.get("edit_note_id")
                # ✨ FIX: Uso seguro de tenant_id
                note = await self.note_repository.get_by_id(note_id, self._get_tenant_id(context))
                if note:
                    note.content = message.strip()
                    note.updated_at = datetime.now(timezone.utc)
                    await self.note_repository.session.commit()
                    await self.note_repository.session.refresh(note)
                    updated_note = note
                else:
                    updated_note = None
                
                fsm.reset()
                if updated_note:
                    return f"✅ Nota {note_id} actualizada correctamente.", "idle", {}
                else:
                    return "❌ Error actualizando la nota.", "idle", {}
            except Exception as e:
                self.logger.error(f"Error actualizando nota: {e}")
                fsm.reset()
                return f"❌ Error actualizando nota: {str(e)}", "idle", {}

        return "⚙️ Estado no soportado para la edición de nota.", "idle", {}

    async def _handle_delete_note(
        self,
        user_id: str,
        message: str,
        context: Dict,
        fsm: NoteFSM
    ) -> Tuple[str, str, Dict]:
        """Handle note deletion flow (con confirmación)."""
        current_state = fsm.current_state

        import re

        if current_state == "idle":
            match = re.search(r'\d+', message)
            if match:
                note_id = int(match.group())
                try:
                    # ✨ FIX: Uso seguro de tenant_id
                    note = await self.note_repository.get_by_id(note_id, self._get_tenant_id(context))
                    if not note or str(note.user_id) != str(user_id):
                        return "❌ Nota no encontrada o no te pertenece.", "idle", {}
                    
                    fsm.context["delete_note_id"] = note_id
                    fsm.context["delete_note_title"] = note.title
                    fsm.transition_to("awaiting_delete_confirmation")
                    
                    resp = (
                        f"⚠️ **¿Eliminar nota {note_id}?**\n"
                        f"**Título:** {note.title}\n\n"
                        "Responde 'sí' para confirmar o 'no' para cancelar:"
                    )
                    return resp, fsm.current_state, fsm.context
                except Exception as e:
                    self.logger.error(f"Error buscando nota para eliminar: {e}")
                    return f"❌ Error buscando nota: {str(e)}", "idle", {}
            else:
                return "❌ Debes indicar el ID de la nota a eliminar (ej: 'borrar nota 5')", "idle", {}

        elif current_state == "awaiting_delete_confirmation":
            if any(word in message.lower() for word in ["sí", "si", "ok", "confirmar", "yes"]):
                try:
                    note_id = fsm.context.get("delete_note_id")
                    # ✨ FIX: Uso seguro de tenant_id
                    await self.note_repository.delete(note_id, self._get_tenant_id(context))
                    fsm.reset()
                    return f"✅ Nota {note_id} eliminada correctamente.", "idle", {}
                except Exception as e:
                    self.logger.error(f"Error eliminando nota: {e}")
                    fsm.reset()
                    return f"❌ Error eliminando nota: {str(e)}", "idle", {}
            else:
                fsm.reset()
                return "❌ Eliminación cancelada.", "idle", {}

        return "⚙️ Estado no soportado para la eliminación de nota.", "idle", {}

    async def _handle_pin_note(
        self,
        user_id: str,
        message: str,
        context: Dict,
        fsm: NoteFSM
    ) -> Tuple[str, str, Dict]:
        """Handle note pinning/unpinning (toggle)."""
        import re

        match = re.search(r'\d+', message)
        if match:
            note_id = int(match.group())
            try:
                # ✨ FIX: Uso seguro de tenant_id
                note = await self.note_repository.get_by_id(note_id, self._get_tenant_id(context))
                if not note or str(note.user_id) != str(user_id):
                    return "❌ Nota no encontrada o no te pertenece.", "idle", {}
                
                updated_note = await self.note_repository.toggle_pin(note_id, self._get_tenant_id(context))
                
                if updated_note:
                    status = "fijada 📌" if updated_note.is_pinned else "desfijada"
                    return f"✅ Nota {note_id} {status} correctamente.", "idle", {}
                else:
                    return "❌ Error cambiando estado de pin.", "idle", {}
                    
            except Exception as e:
                self.logger.error(f"Error en pin/unpin: {e}")
                return f"❌ Error: {str(e)}", "idle", {}
        else:
            return "❌ Debes indicar el ID de la nota a fijar (ej: 'fijar nota 3')", "idle", {}

    async def _handle_get_note(
        self,
        user_id: str,
        message: str,
        context: Dict,
        fsm: NoteFSM
    ) -> Tuple[str, str, Dict]:
        """Handle getting specific note by ID."""
        import re

        match = re.search(r'\d+', message)
        if match:
            note_id = int(match.group())
            try:
                # ✨ FIX: Uso seguro de tenant_id
                note = await self.note_repository.get_by_id(note_id, self._get_tenant_id(context))
                if not note or str(note.user_id) != str(user_id):
                    return "❌ Nota no encontrada o no te pertenece.", "idle", {}
                
                pin_emoji = "📌 " if note.is_pinned else ""
                response = f"{pin_emoji}**{note.title}** (ID: {note.id})\n\n"
                response += f"**Contenido:**\n{note.content}\n\n"
                
                if note.category:
                    response += f"📁 Categoría: {note.category}\n"
                if note.tags:
                    response += f"🏷️ Tags: {', '.join(note.tags)}\n"
                
                response += f"\n🕐 Creada: {note.created_at.strftime('%Y-%m-%d %H:%M')}"
                response += f"\n📝 Actualizada: {note.updated_at.strftime('%Y-%m-%d %H:%M')}"
                
                return response, "idle", {}
                    
            except Exception as e:
                self.logger.error(f"Error obteniendo nota: {e}")
                return f"❌ Error obteniendo nota: {str(e)}", "idle", {}
        else:
            return "❌ Debes indicar el ID de la nota (ej: 'ver nota 3')", "idle", {}

    async def _handle_list_pinned_notes(
        self,
        user_id: str,
        context: Dict,
        fsm: NoteFSM
    ) -> Tuple[str, str, Dict]:
        """Handle listing only pinned notes."""
        try:
            # ✨ FIX: Uso seguro de tenant_id
            notes = await self.note_repository.get_pinned_notes(
                tenant_id=self._get_tenant_id(context),
                user_id=user_id
            )
            if not notes:
                response = "📌 No tienes notas fijadas"
            else:
                response = f"📌 **Notas fijadas ({len(notes)}):**\n\n"
                for note in notes:
                    response += f"**{note.title}** (ID: {note.id})\n"
                    content_preview = note.content[:50] + "..." if len(note.content) > 50 else note.content
                    response += f"_{content_preview}_\n\n"
            return response, "idle", {}

        except Exception as e:
            self.logger.error(f"Error listando notas fijadas: {e}")
            return f"❌ Error: {str(e)}", "idle", {}

    async def _handle_filter_by_date(
        self,
        user_id: str,
        message: str,
        context: Dict,
        fsm: NoteFSM
    ) -> Tuple[str, str, Dict]:
        """Handle filtering notes by date (today, this week, this month)."""
        try:
            # ✨ FIX: Uso seguro de tenant_id
            all_notes = await self.note_repository.get_by_user(
                tenant_id=self._get_tenant_id(context),
                user_id=user_id,
                limit=100
            )

            now = datetime.now(timezone.utc)
            msg_lower = message.lower()

            # Determinar rango de fecha
            if "hoy" in msg_lower:
                start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
                period_name = "hoy"
            elif "semana" in msg_lower:
                start_date = now - timedelta(days=7)
                period_name = "esta semana"
            elif "mes" in msg_lower:
                start_date = now - timedelta(days=30)
                period_name = "este mes"
            else:
                return "❌ Especifica: hoy, esta semana, o este mes", "idle", {}

            # ✨ FIX: Convertir a naive para comparación correcta
            filtered_notes = [
                note for note in all_notes
                if note.created_at.replace(tzinfo=None) >= start_date.replace(tzinfo=None)
            ]

            if not filtered_notes:
                response = f"📅 No hay notas de {period_name}"
            else:
                response = f"📅 **Notas de {period_name} ({len(filtered_notes)}):**\n\n"
                for note in filtered_notes:
                    pin_emoji = "📌 " if note.is_pinned else ""
                    response += f"{pin_emoji}**{note.title}** (ID: {note.id})\n"
                    response += f"_{note.created_at.strftime('%Y-%m-%d %H:%M')}_\n\n"

            return response, "idle", {}

        except Exception as e:
            self.logger.error(f"Error filtrando por fecha: {e}")
            return f"❌ Error: {str(e)}", "idle", {}

    def _parse_note_from_message(self, message: str, entities: Dict) -> Dict:
        note_data = {}
        lines = message.split("\n")
        if len(lines) >= 2:
            note_data["title"] = lines[0].strip()
            note_data["content"] = "\n".join(lines[1:]).strip()
        else:
            sentences = message.split(".")
            if len(sentences) >= 2:
                note_data["title"] = sentences[0].strip()
                note_data["content"] = ". ".join(sentences[1:]).strip()
            else:
                note_data["content"] = message
        return note_data

    def _auto_detect_category(self, entities: Dict) -> Optional[str]:
        if entities.get("persons"):
            return "personal"
        if entities.get("locations"):
            location_str = str(entities.get("locations")).lower()
            if "oficina" in location_str or "trabajo" in location_str:
                return "trabajo"
            if "casa" in location_str:
                return "personal"
        return "general"

    def _auto_extract_tags(self, message: str, entities: Dict) -> List[str]:
        tags = []
        if entities.get("persons"):
            for person in entities["persons"][:2]:
                if isinstance(person, dict) and "text" in person:
                    tags.append(person["text"])
                elif isinstance(person, str):
                    tags.append(person)
        if entities.get("locations"):
            for location in entities["locations"][:2]:
                if isinstance(location, dict) and "text" in location:
                    tags.append(location["text"])
                elif isinstance(location, str):
                    tags.append(location)
        keywords = ["urgente", "importante", "trabajo", "personal", "proyecto", "reunión", "tarea"]
        for keyword in keywords:
            if keyword in message.lower():
                tags.append(keyword)
        return list(set(tags))[:5]

    def _format_note_confirmation(self, note_context: Dict) -> str:
        response = "📝 **¿Guardar esta nota?**\n\n"
        response += f"**Título:** {note_context.get('title', 'Sin título')}\n\n"
        response += f"**Contenido:**\n{note_context.get('content', '')}\n\n"

        if note_context.get("category"):
            response += f"📁 Categoría: {note_context['category']}\n"
        if note_context.get("tags"):
            response += f"🏷️ Tags: {', '.join(note_context['tags'])}\n"

        response += "\n✅ Responde 'sí' para guardar o 'no' para cancelar"
        return response
