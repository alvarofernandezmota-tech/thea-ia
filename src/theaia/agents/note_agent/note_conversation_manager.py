"""
NoteConversationManager — Gestión de conversaciones para NoteAgent
Pattern: AgendaConversationManager adapted
Fallback handler cuando FSM no está activo
"""
from typing import Dict, Tuple
import logging


class NoteConversationManager:
    """
    Conversation Manager para NoteAgent
    
    Responsabilidades:
    - Fallback cuando no hay FSM activo
    - Manejo de conversaciones simples
    - Respuestas por defecto
    - Integration point con core FSM engine
    
    Pattern: AgendaConversationManager v2.0 adapted
    """
    
    def __init__(self, user_id: str):
        """
        Initialize conversation manager
        
        Args:
            user_id: User identifier
        """
        self.user_id = user_id
        self.logger = logging.getLogger(f"{__name__}.NoteConversationManager")
        self.logger.info(f"NoteConversationManager initialized for user {user_id}")
    
    def handle_message(
        self,
        user_id: str,
        message: str,
        context: Dict
    ) -> Tuple[str, str, Dict]:
        """
        Handle message when FSM not active (fallback)
        
        Args:
            user_id: User ID
            message: User message
            context: Conversation context
            
        Returns:
            Tuple[response, state, context]
        """
        self.logger.debug(f"Handling fallback message: {message[:50]}...")
        
        # Default response para mensajes desconocidos
        response = self._generate_default_response(message)
        
        return response, "idle", context
    
    def _generate_default_response(self, message: str) -> str:
        """
        Generate default response for unknown messages
        
        Args:
            message: User message
            
        Returns:
            Default response string
        """
        msg_lower = message.lower()
        
        # Help patterns
        if any(word in msg_lower for word in ["ayuda", "help", "qué puedes hacer", "comandos"]):
            return self._get_help_message()
        
        # Greeting patterns
        if any(word in msg_lower for word in ["hola", "hi", "hello", "buenas"]):
            return "👋 ¡Hola! Soy tu asistente de notas. Puedo ayudarte a crear, buscar y gestionar tus notas.\n\n" \
                   "Algunos comandos:\n" \
                   "- 'Crear nota' para crear una nueva nota\n" \
                   "- 'Listar notas' para ver tus notas\n" \
                   "- 'Buscar notas [término]' para buscar\n\n" \
                   "¿Qué necesitas?"
        
        # Unknown command
        return "❓ No entendí tu mensaje.\n\n" \
               "Puedo ayudarte con:\n" \
               "📝 Crear notas: 'Crear nueva nota'\n" \
               "📋 Ver notas: 'Listar mis notas'\n" \
               "🔍 Buscar: 'Buscar notas trabajo'\n" \
               "✏️ Editar: 'Editar nota [ID]'\n" \
               "🗑️ Eliminar: 'Borrar nota [ID]'\n\n" \
               "Escribe 'ayuda' para más información."
    
    def _get_help_message(self) -> str:
        """
        Get help message with available commands
        
        Returns:
            Help message string
        """
        return """📚 **Ayuda - NoteAgent**

**Crear notas:**
- "Crear nota" - Iniciar creación guiada
- "Nueva nota: Título. Contenido aquí" - Creación rápida

**Ver notas:**
- "Listar mis notas" - Ver todas tus notas
- "Mostrar notas" - Alias para listar

**Buscar:**
- "Buscar notas [término]" - Buscar por tag o categoría
- "Buscar trabajo" - Buscar notas de trabajo
- "Buscar Juan" - Buscar notas que mencionen a Juan

**Gestión:**
- "Editar nota [ID]" - Editar nota existente
- "Borrar nota [ID]" - Eliminar nota
- "Fijar nota [ID]" - Marcar como importante
- "Ver nota [ID]" - Mostrar nota específica

**Características:**
✅ Auto-detección de categorías (personal, trabajo)
✅ Auto-extracción de tags desde personas y ubicaciones
✅ Búsqueda por tags y categorías
✅ Notas fijadas (importantes)

¿Qué necesitas hacer?"""
