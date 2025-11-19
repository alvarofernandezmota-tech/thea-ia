"""
TheaRouter: Orquestador multiagente central de Thea IA.
- Router de intents a agentes especializados.
- Mantiene el contexto de sesión y estado conversacional por usuario (FSM).
- 100% compatible con testing automático: exporta `CoreRouter` como alias legacy.

H03 FASE 1 Improvements:
- Pipeline estructurado: preprocess → intent → entities → routing
- Performance tracking (<100ms target)
- Dataclasses tipadas (Message, ProcessedMessage)
- Entity extraction con EntityExtractionPipeline
- Error handling robusto con fallback
- Logging estructurado
"""

from typing import Dict, Tuple, Optional
from dataclasses import dataclass
from datetime import datetime, timezone

# ==================== DATACLASSES H03 ====================

@dataclass
class Message:
    """Mensaje entrante del usuario (H03 compatible)."""
    text: str
    user_id: str
    tenant_id: str = "default"
    session_id: str = ""
    timestamp: datetime = None
    metadata: Optional[Dict] = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now(timezone.utc)
        if not self.session_id:
            self.session_id = self.user_id

@dataclass
class ProcessedMessage:
    """Resultado del procesamiento completo (H03 compatible)."""
    intent: str
    entities: Dict
    confidence: float
    agent_target: str
    processing_time_ms: int
    original_text: str
    fsm_state: str = "idle"
    status: str = "ok"

# ==================== IMPORTS ORIGINALES ====================

from src.theaia.core.session_manager import SessionManager
from src.theaia.ml.intent_detector.inference import IntentDetector
from src.theaia.ml.entity_extractor.pipeline import EntityExtractionPipeline
from src.theaia.agents.note_agent.handler import NoteAgent
from src.theaia.agents.help_agent import HelpAgent
from src.theaia.agents.event_agent.handler import EventAgent
from src.theaia.agents.fallback_agent import FallbackAgent
from src.theaia.agents.query_agent.handler import QueryAgent
from src.theaia.agents.reminder_agent.handler import ReminderAgent

try:
    from src.theaia.agents.schedule_agent.handler import ScheduleAgent
    HAS_SCHEDULE_AGENT = True
except ImportError:
    ScheduleAgent = None
    HAS_SCHEDULE_AGENT = False

# ==================== HELPER FUNCTIONS H03 ====================

def preprocess_text(text: str) -> str:
    """
    Limpia y normaliza texto de entrada (H03).
    
    Operaciones:
    - Lowercase
    - Strip whitespace
    - Normalize multiple spaces
    
    Args:
        text: Texto crudo
        
    Returns:
        Texto limpio y normalizado
    """
    if not text:
        return ""
    
    # Lowercase
    text = text.lower()
    
    # Strip edges
    text = text.strip()
    
    # Normalize multiple spaces to single
    text = " ".join(text.split())
    
    return text

# ==================== THEA ROUTER ====================

class TheaRouter:
    """
    Orquesta el flujo de mensajes, detecta intents y delega en el agente adecuado.
    Guarda y restaura el contexto/fsm de usuario con SessionManager.
    
    H03 Improvements:
    - Pipeline estructurado
    - Performance tracking
    - Entity extraction con EntityExtractionPipeline
    """
    
    def __init__(self):
        self.session_manager = SessionManager()
        self.intent_detector = IntentDetector()
        self.entity_extractor = EntityExtractionPipeline()  # NUEVO H03 TAREA 1.1.2
        self.fallback_agent = FallbackAgent("global")
        self.agent_registry = {
            "nota": NoteAgent,
            "ayuda": HelpAgent,
            "evento": EventAgent,
            "consulta": QueryAgent,
            "recordatorio": ReminderAgent,
        }
        if HAS_SCHEDULE_AGENT and ScheduleAgent:
            self.agent_registry["horario"] = ScheduleAgent

    def handle(self, user_id: str, message: str):
        """
        Pipeline mejorado H03:
        1. Preprocess → limpieza y normalización
        2. Intent Detection → clasificación
        3. Entity Extraction → extracción con EntityExtractionPipeline (H03 NUEVO)
        4. Agent Routing → selección de agente
        5. FSM + Context → mantenimiento de estado
        6. Performance Tracking → métricas <100ms
        
        Args:
            user_id: ID del usuario
            message: Mensaje de texto del usuario
            
        Returns:
            Dict con status, message, state, context, intent, entities, processing_time_ms
        """
        start_time = datetime.now(timezone.utc)
        
        # --- 1. PREPROCESSING (H03) ---
        cleaned_message = preprocess_text(message)
        
        # --- 2. INTENT DETECTION (H03 mejorado) ---
        try:
            raw = self.intent_detector.detect(cleaned_message)
            # Normalización defensiva
            if isinstance(raw, (list, tuple)):
                intents = [str(i).strip().lower() for i in raw if str(i).strip()]
            else:
                intents = [str(raw).strip().lower()] if str(raw).strip() else []
            
            # Confidence básico por ahora
            confidence = 0.8 if intents else 0.0
            
        except Exception as e:
            print(f"[IntentDetector ERROR]: {e}")
            intents = []
            confidence = 0.0
        
        # Determine current intent antes de agent selection
        if intents and intents[0] in self.agent_registry:
            current_intent = intents[0]
        elif intents and intents[0] == "ayuda":
            current_intent = "ayuda"
        else:
            current_intent = "fallback"
            confidence = 0.0
        
        # --- 3. ENTITY EXTRACTION (H03 NUEVO - TAREA 1.1.2) ---
        try:
            # Sync wrapper para el método async
            import asyncio
            try:
                loop = asyncio.get_event_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
            
            entities = loop.run_until_complete(
                self.entity_extractor.extract(cleaned_message, current_intent)
            )
        except Exception as e:
            print(f"[EntityExtractor ERROR]: {e}")
            entities = {}
        
        # --- 4. AGENT SELECTION ---
        if intents and intents[0] in self.agent_registry:
            AgentClass = self.agent_registry[current_intent]
            agent = AgentClass(user_id)
            agent_name = AgentClass.__name__
        elif intents and intents[0] == "ayuda":
            agent = self.agent_registry["ayuda"](user_id)
            agent_name = "HelpAgent"
        else:
            agent = self.fallback_agent
            agent_name = "FallbackAgent"
        
        # --- 5. FSM + CONTEXT MANAGEMENT ---
        context = self.session_manager.get_context(user_id)
        fsm_state = context.get("fsm_state", "idle")
        
        # Execute agent
        try:
            response, new_state, updated_context = agent.handle(user_id, message, context)
            status = "ok"
        except Exception as e:
            print(f"[ERROR agent {current_intent}]: {e}")
            response = "Ha habido un error inesperado, ¿puedes repetir tu petición?"
            new_state = "error"
            updated_context = context
            current_intent = "fallback"
            agent_name = "FallbackAgent"
            status = "error"
        
        # Update context
        updated_context["fsm_state"] = new_state
        updated_context["last_intent"] = current_intent
        self.session_manager.update_context(user_id, updated_context)
        
        # --- 6. PERFORMANCE TRACKING (H03) ---
        end_time = datetime.now(timezone.utc)
        processing_time_ms = int((end_time - start_time).total_seconds() * 1000)
        
        # Log performance warning if >100ms
        if processing_time_ms > 100:
            print(f"[PERFORMANCE WARNING] Processing took {processing_time_ms}ms (target: <100ms)")
        
        # --- 7. STRUCTURED RESPONSE (H03 mejorado) ---
        return {
            "status": status,
            "message": response,
            "state": new_state,
            "context": updated_context,
            "intent": current_intent,
            "confidence": confidence,
            "agent": agent_name,
            "entities": entities,  # AHORA CON DATOS REALES
            "processing_time_ms": processing_time_ms,
            "original_text": message,
            "cleaned_text": cleaned_message,
        }

    async def process(self, message: Message) -> ProcessedMessage:
        """
        Método compatible con tests H03 (async wrapper).
        
        Args:
            message: Message dataclass
            
        Returns:
            ProcessedMessage dataclass
        """
        result = self.handle(message.user_id, message.text)
        
        return ProcessedMessage(
            intent=result["intent"],
            entities=result["entities"],
            confidence=result["confidence"],
            agent_target=result["agent"],
            processing_time_ms=result["processing_time_ms"],
            original_text=result["original_text"],
            fsm_state=result["state"],
            status=result["status"]
        )

    def reset_session(self, user_id: str):
        """
        Elimina completamente el contexto FSM y variables de sesión de un usuario.
        """
        self.session_manager.reset_context(user_id)


# ==================== ALIAS DE COMPATIBILIDAD TESTING ====================
# Exporta CoreRouter para que todos los tests legacy importen correctamente.
CoreRouter = TheaRouter
