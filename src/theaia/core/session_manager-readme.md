SessionManager — Control de Sesiones Activas
Versión: v1.0
Ubicación: src/theaia/core/session_manager.py
Última actualización: 2025-11-10 16:40 CET (S38)
Estado: ✅ Production Ready

📖 Overview
SessionManager gestiona el ciclo de vida de sesiones de usuarios en THEA IA.

Responsabilidades:

Crear sesión por usuario

Validar si sesión está activa (no expirada)

Renovar timeout en cada actividad

Limpiar sesiones expiradas automáticamente

Rastrear historial de sesiones

🔑 Clase Principal
python
class SessionManager:
    def __init__(self, timeout_minutes: int = 30):
        self.sessions: Dict[str, SessionData] = {}
        self.timeout_minutes = timeout_minutes
    
    def create_session(self, user_id: str) → str
    def is_active(self, session_id: str) → bool
    def extend_timeout(self, session_id: str)
    def cleanup_expired()
    def get_session(self, session_id: str) → Optional[SessionData]
📋 Métodos Públicos
create_session(user_id)
Crea nueva sesión:

python
session_id = session_manager.create_session("alvaro_123")
# Retorna: "sess_550e8400-e29b-41d4-a716-446655440000"
Internamente:

Genera UUID único

Crea SessionData (user_id, created_at, last_activity)

Retorna session_id

is_active(session_id)
Verifica si sesión está activa (no expirada):

python
if session_manager.is_active(session_id):
    print("Sesión activa ✅")
else:
    print("Sesión expirada ❌")
Lógica:

Calcula tiempo transcurrido desde last_activity

Si > timeout_minutes → Marca expired

Retorna True/False

extend_timeout(session_id)
Renueva timer de inactividad (en cada mensaje):

python
# Cuando usuario envía un mensaje
session_manager.extend_timeout(session_id)
# last_activity = datetime.now()
Uso: Llamar en TheaRouter.handle_request()

cleanup_expired()
Limpia sesiones expiradas (cron job):

python
# En scheduler (cada 5 min)
session_manager.cleanup_expired()
# Elimina all expired sessions
Típicamente:

python
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()
scheduler.add_job(
    session_manager.cleanup_expired,
    'interval',
    minutes=5
)
scheduler.start()
🕐 Timeouts en THEA IA
Session Timeout: 30 min
Inicia: Cuando se crea sesión

Se reinicia: En cada mensaje (extend_timeout)

Expira: Después de 30 min sin actividad

Acción: Sesión marcada como expired

Ejemplo Timeline:
text
14:00 - User envía mensaje #1
        → session_id creado
        → last_activity = 14:00
        → vigente hasta 14:30

14:15 - User envía mensaje #2
        → extend_timeout()
        → last_activity = 14:15
        → vigente hasta 14:45

14:50 - User intenta enviar mensaje #3
        → is_active() = False (45 min sin actualizar)
        → SESSION TIMEOUT ❌
        → Necesita crear nueva sesión
💾 SessionData Class
python
@dataclass
class SessionData:
    session_id: str
    user_id: str
    created_at: datetime
    last_activity: datetime
    status: str  # 'active', 'expired', 'closed'
💡 Ejemplo Completo
python
from src.theaia.core.session_manager import SessionManager

# Inicializar
sm = SessionManager(timeout_minutes=30)

# Create session
session_id = sm.create_session("alvaro_123")
print(f"Session created: {session_id}")

# Check active
if sm.is_active(session_id):
    print("✅ Session active")

# Simulate activity (en router)
time.sleep(5)
sm.extend_timeout(session_id)
print("✅ Timeout extended")

# Simulate inactivity
time.sleep(1800)  # 30+ minutos
if not sm.is_active(session_id):
    print("❌ Session expired - need new login")

# Cleanup
sm.cleanup_expired()
print("✅ Expired sessions cleaned")
🔌 Integración con Core
En TheaRouter:
python
class TheaRouter:
    def __init__(self):
        self.session_manager = SessionManager()
        self.context_manager = ContextManager()
    
    def handle_request(self, user_id: str, message: str):
        # 1. Get or create session
        context = self.context_manager.get_or_create(user_id)
        session_id = context.session_id
        
        # 2. Check if session is active
        if not self.session_manager.is_active(session_id):
            # Session expired - need new login
            self.session_manager.create_session(user_id)
            return "Sesión expirada. Por favor inicia sesión nuevamente."
        
        # 3. Process message
        response, state, ctx = self.fsm_manager.process(message)
        
        # 4. Extend timeout (reset inactivity timer)
        self.session_manager.extend_timeout(session_id)
        
        # 5. Return response
        return response, ctx
📊 Propiedades
Propiedad	Tipo	Descripción
sessions	Dict	{session_id → SessionData}
timeout_minutes	int	Timeout en minutos (def: 30)
🐛 Known Issues
 Sin persistencia en BD (v1.0 → Redis v1.1)

 Sin notificación previa a expiración (v1.1)

 Sin logout explícito (v1.1)

📞 Referencias
ContextManager: context_manager-README.md

TheaRouter: router-README.md

Core: core-README.md

Última actualización: 2025-11-10 16:40 CET (S38)
Versión: v1.0
Status: Production Ready ✅