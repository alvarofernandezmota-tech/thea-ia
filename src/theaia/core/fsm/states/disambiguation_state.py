# src/theaia/core/fsm/states/disambiguation_state.py

from typing import Dict, List, Any, Optional
from enum import Enum
import logging

logger = logging.getLogger(__name__)

class DisambiguationType(Enum):
    """Tipos de desambiguación disponibles"""
    
    INTENT_AMBIGUITY = "intent_ambiguity"          # Múltiples intents detectados
    AGENT_AMBIGUITY = "agent_ambiguity"            # Múltiples agentes pueden manejar
    CONTEXT_AMBIGUITY = "context_ambiguity"        # Falta contexto para decidir
    PARAMETER_AMBIGUITY = "parameter_ambiguity"    # Parámetros ambiguos

class DisambiguationHandler:
    """Manejador especializado para procesos de desambiguación"""
    
    def __init__(self):
        self.disambiguation_templates = self._build_templates()
        self.choice_mappings = self._build_choice_mappings()
    
    def _build_templates(self) -> Dict[DisambiguationType, Dict[str, Any]]:
        """Construye plantillas de desambiguación"""
        
        return {
            DisambiguationType.INTENT_AMBIGUITY: {
                "template": "¿Quieres guardar esto como {options}?",
                "retry_template": "Por favor, elige una de estas opciones: {options}",
                "timeout_message": "La desambiguación ha expirado. Por favor, repite tu solicitud.",
                "max_retries": 3,
                "timeout_minutes": 5
            },
            
            DisambiguationType.AGENT_AMBIGUITY: {
                "template": "¿Prefieres que lo maneje {options}?",
                "retry_template": "Especifica cuál de estas opciones prefieres: {options}",
                "timeout_message": "No he recibido una respuesta clara. Intenta de nuevo.",
                "max_retries": 2,
                "timeout_minutes": 3
            },
            
            DisambiguationType.CONTEXT_AMBIGUITY: {
                "template": "Necesito más información. ¿Puedes ser más específico sobre {context}?",
                "retry_template": "Por favor, proporciona más detalles sobre {context}",
                "timeout_message": "No he recibido la información necesaria.",
                "max_retries": 2,
                "timeout_minutes": 10
            },
            
            DisambiguationType.PARAMETER_AMBIGUITY: {
                "template": "¿Te refieres a {options}?",
                "retry_template": "Clarifica tu elección: {options}",
                "timeout_message": "No he podido entender tu elección.",
                "max_retries": 3,
                "timeout_minutes": 5
            }
        }
    
    def _build_choice_mappings(self) -> Dict[str, str]:
        """Construye mapeos de elecciones de usuario a intents"""
        
        return {
            # Nota/Notas
            'nota': 'notas',
            'notas': 'notas',
            'apunte': 'notas',
            'apuntar': 'notas',
            'anotar': 'notas',
            'guardar': 'notas',
            'escribir': 'notas',
            'documentar': 'notas',
            
            # Cita/Agenda/Evento
            'cita': 'agenda',
            'evento': 'agenda',
            'agenda': 'agenda',
            'agendar': 'agenda',
            'reunion': 'agenda',
            'reunión': 'agenda',
            'meeting': 'agenda',
            'encuentro': 'agenda',
            'junta': 'agenda',
            
            # Recordatorio/Alerta
            'recordatorio': 'recordatorio',
            'recordar': 'recordatorio',
            'avisar': 'recordatorio',
            'alerta': 'recordatorio',
            'alertar': 'recordatorio',
            'notificar': 'recordatorio',
            'notificación': 'recordatorio',
            'aviso': 'recordatorio',
            
            # Programación/Schedule
            'programar': 'scheduler',
            'programación': 'scheduler',
            'schedule': 'scheduler',
            'planificar': 'scheduler',
            'planificación': 'scheduler',
            
            # Ayuda/Help
            'ayuda': 'help',
            'help': 'help',
            'ayudar': 'help',
            'asistencia': 'help',
            
            # Consulta/Query
            'consulta': 'query',
            'pregunta': 'query',
            'query': 'query',
            'consultar': 'query',
            'preguntar': 'query'
        }
    
    def generate_disambiguation_question(
        self, 
        disambiguation_type: DisambiguationType,
        options: List[str],
        context: Optional[str] = None
    ) -> str:
        """Genera pregunta de desambiguación"""
        
        template_info = self.disambiguation_templates[disambiguation_type]
        template = template_info["template"]
        
        if disambiguation_type == DisambiguationType.INTENT_AMBIGUITY:
            # Mapear intents técnicos a opciones user-friendly
            user_options = self._map_intents_to_user_options(options)
            options_text = self._format_options_list(user_options)
            return template.format(options=options_text)
        
        elif disambiguation_type == DisambiguationType.CONTEXT_AMBIGUITY:
            return template.format(context=context or "tu solicitud")
        
        else:
            options_text = self._format_options_list(options)
            return template.format(options=options_text)
    
    def generate_retry_message(
        self,
        disambiguation_type: DisambiguationType,
        options: List[str],
        retry_count: int
    ) -> str:
        """Genera mensaje de reintento"""
        
        template_info = self.disambiguation_templates[disambiguation_type]
        retry_template = template_info["retry_template"]
        
        if disambiguation_type == DisambiguationType.INTENT_AMBIGUITY:
            user_options = self._map_intents_to_user_options(options)
            options_text = self._format_options_list(user_options)
        else:
            options_text = self._format_options_list(options)
        
        # Personalizar mensaje según número de reintentos
        if retry_count == 1:
            return retry_template.format(options=options_text)
        elif retry_count == 2:
            return f"Aún no he entendido. {retry_template.format(options=options_text)}"
        else:
            return f"Último intento. {retry_template.format(options=options_text)}"
    
    def parse_user_choice(self, message: str, valid_options: List[str]) -> Optional[str]:
        """Parsea elección del usuario"""
        
        message_lower = message.lower().strip()
        
        # Búsqueda exacta primero
        if message_lower in self.choice_mappings:
            choice = self.choice_mappings[message_lower]
            if choice in valid_options:
                return choice
        
        # Búsqueda parcial
        for keyword, intent in self.choice_mappings.items():
            if keyword in message_lower and intent in valid_options:
                return intent
        
        # Búsqueda por opciones válidas directas
        for option in valid_options:
            if option.lower() in message_lower:
                return option
        
        return None
    
    def _map_intents_to_user_options(self, intents: List[str]) -> List[str]:
        """Mapea intents técnicos a opciones user-friendly"""
        
        mapping = {
            'notas': 'nota',
            'agenda': 'cita',
            'recordatorio': 'recordatorio',
            'event': 'evento',
            'scheduler': 'programación',
            'help': 'ayuda',
            'query': 'consulta',
            'fallback': 'otra opción'
        }
        
        return [mapping.get(intent, intent) for intent in intents]
    
    def _format_options_list(self, options: List[str]) -> str:
        """Formatea lista de opciones para mostrar al usuario"""
        
        if len(options) == 1:
            return options[0]
        elif len(options) == 2:
            return f"{options[0]} o {options[1]}"
        else:
            return f"{', '.join(options[:-1])} o {options[-1]}"
    
    def get_disambiguation_config(self, disambiguation_type: DisambiguationType) -> Dict[str, Any]:
        """Obtiene configuración para un tipo de desambiguación"""
        return self.disambiguation_templates.get(disambiguation_type, {})
    
    def is_valid_choice(self, choice: str, valid_options: List[str]) -> bool:
        """Verifica si una elección es válida"""
        return self.parse_user_choice(choice, valid_options) is not None

class DisambiguationContext:
    """Contexto específico para procesos de desambiguación"""
    
    def __init__(self, user_id: str, disambiguation_type: DisambiguationType):
        self.user_id = user_id
        self.disambiguation_type = disambiguation_type
        self.start_time = None
        self.retry_count = 0
        self.options = []
        self.original_message = ""
        self.context_info = {}
    
    def start_disambiguation(self, options: List[str], original_message: str, **kwargs):
        """Inicia proceso de desambiguación"""
        import time
        
        self.start_time = time.time()
        self.retry_count = 0
        self.options = options
        self.original_message = original_message
        self.context_info = kwargs
        
        logger.info(f"Started disambiguation for user {self.user_id}: type={self.disambiguation_type}, options={options}")
    
    def increment_retry(self):
        """Incrementa contador de reintentos"""
        self.retry_count += 1
        logger.warning(f"Disambiguation retry #{self.retry_count} for user {self.user_id}")
    
    def is_expired(self, timeout_minutes: int) -> bool:
        """Verifica si la desambiguación ha expirado"""
        if self.start_time is None:
            return False
        
        import time
        return (time.time() - self.start_time) > (timeout_minutes * 60)
    
    def reset(self):
        """Resetea el contexto de desambiguación"""
        self.start_time = None
        self.retry_count = 0
        self.options = []
        self.original_message = ""
        self.context_info = {}

# Exportaciones
__all__ = [
    'DisambiguationType',
    'DisambiguationHandler', 
    'DisambiguationContext'
]
