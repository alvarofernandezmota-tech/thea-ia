Callbacks — Event Hooks System
Versión: v1.0
Ubicación: src/theaia/core/callbacks.py
Última actualización: 2025-11-10 16:55 CET (S38)
Estado: ✅ Production Ready

📖 Overview
CallbackManager es un event hook system que permite extensibilidad sin acoplar módulos.

Permite que:

Logging se registre en eventos

Monitoring reporte en tiempo real

Analytics trackee conversaciones

Sistemas externos reaccionen a eventos

Todo sin modificar core

🔑 Clase Principal
python
class CallbackManager:
    def __init__(self):
        self.callbacks: Dict[str, List[Callable]] = {}
    
    def register(self, event_type: str, callback: Callable):
        """Registrar callback para evento."""
        
        if event_type not in self.callbacks:
            self.callbacks[event_type] = []
        
        self.callbacks[event_type].append(callback)
    
    def trigger(self, event_type: str, **kwargs):
        """Disparar todos los callbacks de un evento."""
        
        for callback in self.callbacks.get(event_type, []):
            try:
                callback(**kwargs)
            except Exception as e:
                logger.error(f"Callback error: {e}")
📋 Eventos Disponibles
1. on_message
python
callbacks.trigger('on_message', 
    user_id="alvaro_123",
    message="Agendar reunión",
    timestamp=datetime.now())
Cuándo: Usuario envía un mensaje
Parámetros: user_id, message, timestamp

2. on_state_change
python
callbacks.trigger('on_state_change',
    user_id="alvaro_123",
    old_state="initial",
    new_state="agent_delegated")
Cuándo: Cambio de estado en FSM
Parámetros: user_id, old_state, new_state

3. on_error
python
callbacks.trigger('on_error',
    user_id="alvaro_123",
    error=exception,
    traceback=traceback_str)
Cuándo: Error ocurre
Parámetros: user_id, error, traceback

4. on_session_timeout
python
callbacks.trigger('on_session_timeout',
    user_id="alvaro_123",
    session_id="sess_xxx")
Cuándo: Sesión expira por inactividad
Parámetros: user_id, session_id

5. on_intent_detected
python
callbacks.trigger('on_intent_detected',
    user_id="alvaro_123",
    intent="agenda",
    score=0.95)
Cuándo: Intent detectado
Parámetros: user_id, intent, score

6. on_agent_delegated
python
callbacks.trigger('on_agent_delegated',
    user_id="alvaro_123",
    agent="AgendaAgent",
    intent="agenda")
Cuándo: Agente delegado
Parámetros: user_id, agent, intent

💡 Ejemplo 1: Logging
python
from src.theaia.core.callbacks import CallbackManager
import logging

callbacks = CallbackManager()

# Callback para logging
def log_message(user_id, message, timestamp):
    logging.info(f"[{user_id}] {message} ({timestamp})")

def log_state_change(user_id, old_state, new_state):
    logging.debug(f"[{user_id}] {old_state} → {new_state}")

# Registrar
callbacks.register('on_message', log_message)
callbacks.register('on_state_change', log_state_change)

# En router
def handle_request(user_id, message):
    callbacks.trigger('on_message', 
        user_id=user_id, 
        message=message,
        timestamp=datetime.now())
    
    # ... process ...
    
    callbacks.trigger('on_state_change',
        user_id=user_id,
        old_state='initial',
        new_state='agent_delegated')
💡 Ejemplo 2: Monitoring (Sentry)
python
import sentry_sdk

callbacks = CallbackManager()

# Callback para errores (Sentry)
def monitor_error(user_id, error, traceback):
    sentry_sdk.capture_exception(error)
    logger.error(f"[{user_id}] Error: {error}\n{traceback}")

# Callback para timeouts
def alert_timeout(user_id, session_id):
    sentry_sdk.capture_message(
        f"Session timeout for {user_id}",
        level="warning"
    )

# Registrar
callbacks.register('on_error', monitor_error)
callbacks.register('on_session_timeout', alert_timeout)
💡 Ejemplo 3: Analytics
python
from mixpanel import Mixpanel

callbacks = CallbackManager()
mp = Mixpanel("PROJECT_TOKEN")

# Callback para analytics
def track_message(user_id, message, timestamp):
    mp.track(user_id, 'Message Sent', {
        'message_length': len(message),
        'timestamp': timestamp
    })

def track_state(user_id, old_state, new_state):
    mp.track(user_id, 'State Change', {
        'from': old_state,
        'to': new_state
    })

def track_intent(user_id, intent, score):
    mp.track(user_id, 'Intent Detected', {
        'intent': intent,
        'confidence': score
    })

# Registrar
callbacks.register('on_message', track_message)
callbacks.register('on_state_change', track_state)
callbacks.register('on_intent_detected', track_intent)
💡 Ejemplo 4: Multi-Callback (Combined)
python
from src.theaia.core.callbacks import CallbackManager
import logging
import sentry_sdk
from analytics import Analytics

callbacks = CallbackManager()
analytics = Analytics("api_key")

# LOGGING
def log_all(user_id, **kwargs):
    logging.info(f"[{user_id}] {kwargs}")

callbacks.register('on_message', log_all)
callbacks.register('on_state_change', log_all)
callbacks.register('on_error', log_all)

# MONITORING
def monitor_errors(user_id, error, **kwargs):
    sentry_sdk.capture_exception(error)

callbacks.register('on_error', monitor_errors)

# ANALYTICS
def track_all(user_id, **kwargs):
    analytics.track(user_id, 'Action', kwargs)

callbacks.register('on_message', track_all)
callbacks.register('on_state_change', track_all)
callbacks.register('on_intent_detected', track_all)

# Ahora todos los eventos se registran, monitorean y trackean
🔌 Error Handling
Los callbacks son seguros (try-except):

python
def trigger(self, event_type: str, **kwargs):
    for callback in self.callbacks.get(event_type, []):
        try:
            callback(**kwargs)
        except Exception as e:
            # Error en callback NO rompe el flujo
            logger.error(f"Callback error in {event_type}: {e}")
            # Continúa con próximos callbacks
Ventaja: Si logging falla, monitoring continúa. Si analytics falla, app sigue funcionando.

📊 Evento Matrix
Evento	Logging	Monitoring	Analytics
on_message	✅	✅	✅
on_state_change	✅	✅	✅
on_error	✅	✅	❌
on_session_timeout	✅	✅	✅
on_intent_detected	✅	❌	✅
on_agent_delegated	✅	❌	✅
🎯 Ventajas
1. Desacoplamiento
text
TheaRouter (core)
    ↓
CallbackManager (broker)
    ↓
Logging, Monitoring, Analytics (subscribers)
2. Extensibilidad
text
# Agregar nueva métrica sin tocar router
def my_custom_metric(user_id, **kwargs):
    # custom logic

callbacks.register('on_message', my_custom_metric)
3. Flexibilidad
text
# Múltiples callbacks por evento
callbacks.register('on_error', sentry_handler)
callbacks.register('on_error', slack_handler)
callbacks.register('on_error', pagerduty_handler)

# Todos se ejecutan en paralelo conceptual
4. Resilencia
text
# Si un callback falla, otros continúan
callbacks.trigger('on_message', ...)  # Error safe
🐛 Known Issues
 Sin timeout individual de callbacks (v1.0)

 Sin prioridad/orden de callbacks (v1.0)

 Sin async callbacks (v1.1)

 Sin callback history/logging (v1.1)

📞 Referencias
TheaRouter: router-README.md

SessionManager: session_manager-README.md

Core: core-README.md

Última actualización: 2025-11-10 16:55 CET (S38)
Versión: v1.0
Status: Production Ready ✅