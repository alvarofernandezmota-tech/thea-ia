"""
AgendaAgent FSM v2.0 - Simple State Machine
NO hereda BaseStateMachine (independiente del Core)

Responsable: Álvaro Fernández Mota (CEO THEA IA)
Fecha: 21 Noviembre 2025
Filosofía: TRES (Álvaro + Jarvis + THEA IA)
Hito: H03 BLOQUE 3.4A.1.1 - Agent FSM Professional
"""

from typing import Optional, Dict, Any, Callable
import logging
from datetime import datetime

from src.theaia.agents.agenda_agent.model.agent_states import AgendaStates


class AgendaFSM:
    """
    Máquina de estados finitos para AgendaAgent.
    
    Diseño:
    - FSM SIMPLE (NO hereda BaseStateMachine del Core)
    - user_id gestionado en handler (viene en context)
    - Transiciones explícitas y validadas
    - Callbacks pre/post para validación y side effects
    
    Maneja flujos conversacionales:
    1. CREAR evento (título → fecha → hora → ubicación → guardar)
    2. LISTAR eventos (con filtros)
    3. EDITAR evento (seleccionar → modificar → guardar)
    4. ELIMINAR evento (seleccionar → confirmar → eliminar)
    5. BUSCAR eventos (criterios → resultados)
    6. CANCELAR operación (desde cualquier estado)
    
    Estados: 15 estados definidos en AgendaStates
    """
    
    def __init__(self):
        """Inicializa FSM en estado IDLE"""
        self.current_state = AgendaStates.IDLE
        self._event_draft: Optional[Dict[str, Any]] = None
        self._transitions: Dict[str, Dict[str, str]] = {}
        self._callbacks_pre: Dict[str, Callable] = {}
        self._callbacks_post: Dict[str, Callable] = {}
        self.logger = logging.getLogger(__name__)
        
        self._configure_transitions()
        self.logger.info("AgendaFSM initialized (simple state machine)")
    
    def _configure_transitions(self):
        """
        Define todas las transiciones permitidas.
        
        Formato: {estado_origen: {trigger: estado_destino}}
        """
        self._transitions = {
            # ===== FLUJO 1: CREAR EVENTO =====
            AgendaStates.IDLE: {
                'start_create': AgendaStates.AWAITING_TITLE,
                'start_list': AgendaStates.LISTING_EVENTS,
                'start_edit': AgendaStates.SELECTING_EVENT,
                'start_delete': AgendaStates.DELETING_EVENT,
                'start_search': AgendaStates.SEARCHING_EVENTS
            },
            
            AgendaStates.AWAITING_TITLE: {
                'provide_title': AgendaStates.AWAITING_DATE,
                'cancel': AgendaStates.CANCELLED
            },
            
            AgendaStates.AWAITING_DATE: {
                'provide_date': AgendaStates.AWAITING_TIME,
                'cancel': AgendaStates.CANCELLED
            },
            
            AgendaStates.AWAITING_TIME: {
                'provide_time': AgendaStates.AWAITING_LOCATION,
                'cancel': AgendaStates.CANCELLED
            },
            
            AgendaStates.AWAITING_LOCATION: {
                'provide_location': AgendaStates.PROCESSING,
                'skip_location': AgendaStates.PROCESSING,
                'cancel': AgendaStates.CANCELLED
            },
            
            AgendaStates.PROCESSING: {
                'save_event': AgendaStates.EVENT_SAVED,
                'save_update': AgendaStates.EVENT_UPDATED,
                'error': AgendaStates.CANCELLED
            },
            
            AgendaStates.EVENT_SAVED: {
                'finish': AgendaStates.IDLE
            },
            
            # ===== FLUJO 2: LISTAR EVENTOS =====
            AgendaStates.LISTING_EVENTS: {
                'finish_list': AgendaStates.IDLE,
                'cancel': AgendaStates.CANCELLED
            },
            
            # ===== FLUJO 3: EDITAR EVENTO =====
            AgendaStates.SELECTING_EVENT: {
                'select_event': AgendaStates.EDITING_FIELD,
                'cancel': AgendaStates.CANCELLED
            },
            
            AgendaStates.EDITING_FIELD: {
                'update_field': AgendaStates.PROCESSING,
                'cancel': AgendaStates.CANCELLED
            },
            
            AgendaStates.EVENT_UPDATED: {
                'finish': AgendaStates.IDLE
            },
            
            # ===== FLUJO 4: ELIMINAR EVENTO =====
            AgendaStates.DELETING_EVENT: {
                'select_delete': AgendaStates.CONFIRMING_DELETE,
                'cancel': AgendaStates.CANCELLED
            },
            
            AgendaStates.CONFIRMING_DELETE: {
                'confirm_delete': AgendaStates.EVENT_DELETED,
                'cancel': AgendaStates.CANCELLED
            },
            
            AgendaStates.EVENT_DELETED: {
                'finish': AgendaStates.IDLE
            },
            
            # ===== FLUJO 5: BUSCAR EVENTOS =====
            AgendaStates.SEARCHING_EVENTS: {
                'finish_search': AgendaStates.IDLE,
                'cancel': AgendaStates.CANCELLED
            },
            
            # ===== FLUJO 6: CANCELAR =====
            AgendaStates.CANCELLED: {
                'reset': AgendaStates.IDLE
            }
        }
        
        # Registrar callbacks
        self._register_callbacks()
    
    def _register_callbacks(self):
        """Registra callbacks pre y post para transiciones"""
        
        # Callbacks PRE (validación antes de transición)
        self._callbacks_pre = {
            'start_create': self._validate_can_create,
            'provide_title': self._validate_title,
            'provide_date': self._validate_date,
            'provide_time': self._validate_time,
            'save_event': self._validate_can_save
        }
        
        # Callbacks POST (side effects después de transición)
        self._callbacks_post = {
            'start_create': self._init_draft,
            'provide_title': self._store_title,
            'provide_date': self._store_date,
            'provide_time': self._store_time,
            'provide_location': self._store_location,
            'save_event': self._mark_saved,
            'finish': self._cleanup_draft,
            'cancel': self._cleanup_draft,
            'reset': self._cleanup_draft
        }
    
    # ========================================
    # TRANSICIÓN PRINCIPAL
    # ========================================
    
    def transition(self, trigger: str, context: Dict[str, Any]) -> bool:
        """
        Ejecuta transición si es válida.
        
        Flujo:
        1. Verifica si transición permitida
        2. Ejecuta callback PRE (validación)
        3. Cambia estado
        4. Ejecuta callback POST (side effects)
        
        Args:
            trigger: Nombre de la transición
            context: Contexto conversacional (contiene user_id, entities, etc)
            
        Returns:
            True si transición exitosa, False si no permitida
        """
        # Verificar si transición permitida
        current_transitions = self._transitions.get(self.current_state, {})
        
        if trigger not in current_transitions:
            self.logger.warning(
                f"Transición '{trigger}' no permitida desde '{self.current_state}'"
            )
            return False
        
        new_state = current_transitions[trigger]
        
        # Ejecutar callback PRE (validación)
        if trigger in self._callbacks_pre:
            try:
                self._callbacks_pre[trigger](context)
            except ValueError as e:
                self.logger.error(f"Validación PRE falló: {e}")
                return False
        
        # Cambiar estado
        old_state = self.current_state
        self.current_state = new_state
        
        self.logger.info(f"Transición: {old_state} --[{trigger}]--> {new_state}")
        
        # Ejecutar callback POST (side effects)
        if trigger in self._callbacks_post:
            try:
                self._callbacks_post[trigger](context)
            except Exception as e:
                self.logger.error(f"Callback POST falló: {e}")
        
        return True
    
    # ========================================
    # CALLBACKS PRE (VALIDACIÓN)
    # ========================================
    
    def _validate_can_create(self, context: Dict[str, Any]) -> None:
        """Valida que se puede iniciar creación"""
        if not context.get('user_id'):
            raise ValueError("user_id requerido")
        if not context.get('tenant_id'):
            raise ValueError("tenant_id requerido")
    
    def _validate_title(self, context: Dict[str, Any]) -> None:
        """Valida título del evento"""
        title = context.get('event_title', '').strip()
        if not title:
            raise ValueError("Título no puede estar vacío")
        if len(title) > 200:
            raise ValueError("Título muy largo (máx 200 caracteres)")
    
    def _validate_date(self, context: Dict[str, Any]) -> None:
        """Valida fecha del evento"""
        event_date = context.get('event_date')
        if not event_date:
            raise ValueError("Fecha requerida")
    
    def _validate_time(self, context: Dict[str, Any]) -> None:
        """Valida hora del evento"""
        event_time = context.get('event_time')
        if not event_time:
            raise ValueError("Hora requerida")
    
    def _validate_can_save(self, context: Dict[str, Any]) -> None:
        """Valida que se puede guardar evento"""
        if not self._event_draft:
            raise ValueError("No hay borrador para guardar")
        
        required = ['title', 'date', 'time']
        for field in required:
            if field not in self._event_draft:
                raise ValueError(f"Campo requerido faltante: {field}")
    
    # ========================================
    # CALLBACKS POST (SIDE EFFECTS)
    # ========================================
    
    def _init_draft(self, context: Dict[str, Any]) -> None:
        """Inicializa borrador de evento"""
        self._event_draft = {
            'user_id': context.get('user_id'),
            'tenant_id': context.get('tenant_id'),
            'created_at': datetime.utcnow().isoformat()
        }
        context['event_draft'] = self._event_draft
        self.logger.debug("Borrador inicializado")
    
    def _store_title(self, context: Dict[str, Any]) -> None:
        """Guarda título en borrador"""
        title = context.get('event_title', '').strip()
        if self._event_draft:
            self._event_draft['title'] = title
            context['event_draft'] = self._event_draft
            self.logger.debug(f"Título guardado: '{title}'")
    
    def _store_date(self, context: Dict[str, Any]) -> None:
        """Guarda fecha en borrador"""
        date = context.get('event_date')
        if self._event_draft:
            self._event_draft['date'] = str(date)
            context['event_draft'] = self._event_draft
            self.logger.debug(f"Fecha guardada: {date}")
    
    def _store_time(self, context: Dict[str, Any]) -> None:
        """Guarda hora en borrador"""
        time = context.get('event_time')
        if self._event_draft:
            self._event_draft['time'] = time
            context['event_draft'] = self._event_draft
            self.logger.debug(f"Hora guardada: {time}")
    
    def _store_location(self, context: Dict[str, Any]) -> None:
        """Guarda ubicación en borrador"""
        location = context.get('event_location', '').strip()
        if self._event_draft and location:
            self._event_draft['location'] = location
            context['event_draft'] = self._event_draft
            self.logger.debug(f"Ubicación guardada: '{location}'")
    
    def _mark_saved(self, context: Dict[str, Any]) -> None:
        """Marca evento como guardado"""
        context['event_saved'] = True
        context['saved_event_id'] = context.get('db_event_id')
        self.logger.info(f"Evento guardado: id={context.get('db_event_id')}")
    
    def _cleanup_draft(self, context: Dict[str, Any]) -> None:
        """Limpia borrador de evento"""
        self._event_draft = None
        context.pop('event_draft', None)
        self.logger.debug("Borrador limpiado")
    
    # ========================================
    # MÉTODOS PÚBLICOS (API DEL FSM)
    # ========================================
    
    def start_create(self, context: Dict[str, Any]) -> bool:
        """Inicia flujo de creación de evento"""
        return self.transition('start_create', context)
    
    def provide_title(self, context: Dict[str, Any]) -> bool:
        """Proporciona título y avanza"""
        return self.transition('provide_title', context)
    
    def provide_date(self, context: Dict[str, Any]) -> bool:
        """Proporciona fecha y avanza"""
        return self.transition('provide_date', context)
    
    def provide_time(self, context: Dict[str, Any]) -> bool:
        """Proporciona hora y avanza"""
        return self.transition('provide_time', context)
    
    def provide_location(self, context: Dict[str, Any]) -> bool:
        """Proporciona ubicación y avanza"""
        return self.transition('provide_location', context)
    
    def skip_location(self, context: Dict[str, Any]) -> bool:
        """Salta ubicación (opcional) y avanza"""
        return self.transition('skip_location', context)
    
    def save_event(self, context: Dict[str, Any]) -> bool:
        """Guarda evento en DB"""
        return self.transition('save_event', context)
    
    def finish(self, context: Dict[str, Any]) -> bool:
        """Finaliza flujo y vuelve a IDLE"""
        return self.transition('finish', context)
    
    def start_list(self, context: Dict[str, Any]) -> bool:
        """Inicia listado de eventos"""
        return self.transition('start_list', context)
    
    def finish_list(self, context: Dict[str, Any]) -> bool:
        """Finaliza listado"""
        return self.transition('finish_list', context)
    
    def cancel(self, context: Dict[str, Any]) -> bool:
        """Cancela operación actual"""
        return self.transition('cancel', context)
    
    def reset(self, context: Dict[str, Any]) -> bool:
        """Resetea FSM a IDLE"""
        return self.transition('reset', context)
    
    def get_event_draft(self) -> Optional[Dict[str, Any]]:
        """Retorna copia del borrador actual"""
        return self._event_draft.copy() if self._event_draft else None
    
    def is_in_creation_flow(self) -> bool:
        """Verifica si está en flujo de creación"""
        creation_states = [
            AgendaStates.AWAITING_TITLE,
            AgendaStates.AWAITING_DATE,
            AgendaStates.AWAITING_TIME,
            AgendaStates.AWAITING_LOCATION,
            AgendaStates.PROCESSING
        ]
        return self.current_state in creation_states
    
    def get_next_required_field(self) -> Optional[str]:
        """Retorna siguiente campo requerido en creación"""
        state_to_field = {
            AgendaStates.AWAITING_TITLE: 'title',
            AgendaStates.AWAITING_DATE: 'date',
            AgendaStates.AWAITING_TIME: 'time',
            AgendaStates.AWAITING_LOCATION: 'location'
        }
        return state_to_field.get(self.current_state)
