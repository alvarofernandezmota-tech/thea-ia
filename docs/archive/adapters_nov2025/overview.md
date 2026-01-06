🔌 Adapters System Overview — THEA IA
Versión: 1.0
Última actualización: 2025-11-08 17:14 CET (Sesión 36)
Responsable: Adapters Team / Álvaro Fernández Mota (CEO)
Estado: ✅ Activo

📋 Propósito
Visión general del sistema de adapters de THEA IA: arquitectura, catálogo de adapters, ciclo de vida, integración con FSM y mejores prácticas.

Audiencia:

Desarrolladores integrando nuevos adapters

Arquitectos diseñando conectores externos

DevOps desplegando integraciones

Auditores validando comunicación externa

🎯 Filosofía de Adapters
THEA IA usa adapters para comunicarse con servicios externos, cada uno especializado en un canal:

📱 Telegram: Bot conversacional

🌐 REST API: Endpoints HTTP

💬 Slack: Workspace integration

🎮 Discord: Server bot

📞 WhatsApp: Business API

➕ Extensibles: Nuevos canales fácilmente

Flujo arquitectónico
text
Entrada Externa (Telegram/REST/Slack/etc.)
           ↓
    ┌──────────────┐
    │   Adapter    │ ← Normaliza entrada
    └──────────────┘
           ↓
    ┌──────────────┐
    │  FSM Engine  │ ← Procesa lógica
    └──────────────┘
           ↓
    ┌──────────────┐
    │    Agents    │ ← Ejecutan acciones
    └──────────────┘
           ↓
    ┌──────────────┐
    │   Adapter    │ ← Formatea respuesta
    └──────────────┘
           ↓
Salida Externa (mensaje al usuario)
📚 Catálogo de Adapters
Adapters actuales
Adapter	Canal	Rol	Prioridad	Estado
Telegram	Bot messaging	Core	🔴 Alta	✅ Activo
REST	HTTP API	Core	🔴 Alta	✅ Activo
Slack	Workspace bot	Extensión	🟡 Media	⏳ Planificado
Discord	Server bot	Extensión	🟡 Media	⏳ Planificado
WhatsApp	Business API	Extensión	🟠 Baja	⏳ Futuro
🔄 Ciclo de vida de un adapter
1. Inicialización
python
adapter = TelegramAdapter(token="BOT_TOKEN")
adapter.initialize()  # Conecta con API externa
Qué ocurre:

Validar credenciales

Establecer conexión con servicio externo

Registrar webhooks/listeners

Estado = "ready"

2. Registro en FSM
python
fsm = FSMEngine()
fsm.register_adapter('telegram', adapter)
Qué ocurre:

FSM conoce qué adapters disponibles

Se establece canal bidireccional

Adapter entra en pool activo

3. Recepción de mensaje
python
# Mensaje entrante desde Telegram
raw_message = telegram_api.get_updates()
normalized = adapter.normalize_input(raw_message)
Qué ocurre:

Adapter recibe mensaje raw del canal

Normaliza a formato estándar THEA IA

Extrae user_id, message_text, metadata

4. Envío a FSM
python
response = fsm.process_message(normalized)
Qué ocurre:

FSM recibe mensaje normalizado

Ejecuta lógica de agentes

Genera respuesta estructurada

5. Formateo de respuesta
python
formatted = adapter.format_output(response)
adapter.send_message(formatted)
Qué ocurre:

Adapter formatea respuesta para canal específico

Envía mensaje al usuario

Log de transacción completa

6. Cierre (teardown)
python
adapter.shutdown()
Qué ocurre:

Cerrar conexiones con servicio externo

Deregistrar webhooks

Liberar recursos

🗣️ Normalización de mensajes
Todos los adapters normalizan a formato estándar:

python
{
  "user_id": "123456",
  "channel": "telegram",
  "message": "Crear evento mañana 10am",
  "metadata": {
    "timestamp": "2025-11-08T17:14:00Z",
    "chat_id": "123456",
    "message_id": "789"
  }
}
Ventajas:

FSM/Agents no necesitan saber de qué canal viene

Lógica única independiente del canal

Fácil agregar nuevos adapters

🔧 Configuración de adapters
Cada adapter tiene archivo de configuración:

text
# config/adapters/telegram.yaml
adapter:
  name: "Telegram"
  version: "1.0"
  enabled: true
  timeout: 30

credentials:
  token: "${TELEGRAM_BOT_TOKEN}"  # Variable de entorno

features:
  webhooks: true
  polling: false
  markdown: true
  inline_keyboard: true

limits:
  max_message_length: 4096
  rate_limit: 30  # mensajes/segundo
📊 Métricas de adapters
Monitoreadas automáticamente:

Métrica	Propósito
Messages received	Total mensajes entrantes
Messages sent	Total mensajes enviados
Response time	Latencia adapter
Error rate	% errores de conexión
Uptime	% disponibilidad
Acceso:

bash
# Ver métricas
GET /api/adapters/metrics

# Por adapter
GET /api/adapters/telegram/metrics
🔐 Seguridad
Principios
Credenciales externalizadas: Tokens en secrets/env vars

Validación de origen: Verificar webhooks/firma

Rate limiting: Throttle por usuario

Sanitización: Limpiar inputs antes de procesar

Logging seguro: No logear tokens/credenciales

Ejemplo: Validación de webhook
python
def validate_telegram_webhook(request):
    token = request.headers.get('X-Telegram-Bot-Api-Secret-Token')
    expected_token = os.getenv('TELEGRAM_SECRET_TOKEN')
    
    if token != expected_token:
        raise SecurityError("Invalid webhook token")
    
    return True
📚 Estructura de archivos
text
src/theaia/adapters/
├── __init__.py
├── base.py                     # Clase base abstracta
├── telegram.py                 # Adapter Telegram
├── rest.py                     # Adapter REST API
├── slack.py                    # Adapter Slack (futuro)
├── discord.py                  # Adapter Discord (futuro)
├── whatsapp.py                 # Adapter WhatsApp (futuro)
└── config/                     # Configuraciones YAML
    ├── telegram.yaml
    ├── rest.yaml
    └── ...

docs/adapters/
├── overview.md  ← Estás aquí
├── adapter_telegram.md
├── adapter_rest.md
├── adapter_slack.md
├── adapter_discord.md
├── adapter_whatsapp.md
└── best_practices.md
🔗 Referencia rápida por adapter
Adapter	Docs	Casos de uso
Telegram	adapter_telegram.md	Bot conversacional, comandos
REST	adapter_rest.md	API HTTP, webhooks
Slack	adapter_slack.md	Workspace bot
Discord	adapter_discord.md	Server bot gaming
WhatsApp	adapter_whatsapp.md	Business messaging
🎓 Cómo crear un nuevo adapter
Pasos resumidos
Heredar de BaseAdapter

python
from src.theaia.adapters.base import BaseAdapter

class MyAdapter(BaseAdapter):
    def __init__(self, **kwargs):
        super().__init__("MyAdapter")
Implementar métodos clave

python
def initialize(self):
    # Conectar con servicio externo
    pass

def normalize_input(self, raw_message):
    # Convertir a formato estándar
    return normalized

def format_output(self, response):
    # Formatear para canal específico
    return formatted

def send_message(self, formatted):
    # Enviar mensaje al usuario
    pass

def shutdown(self):
    # Cerrar conexiones
    pass
Crear configuración YAML

text
adapter:
  name: "MyAdapter"
  enabled: true
Registrar en FSM

python
fsm.register_adapter('myadapter', MyAdapter())
Ver best_practices.md para detalles.

✅ Checklist de validación de adapters
 Hereda de BaseAdapter

 Implementa initialize(), normalize_input(), format_output(), send_message(), shutdown()

 Tiene configuración YAML

 Documentación README en docs/adapters/adapter_xxx.md

 Tests unitarios en src/theaia/tests/unit/test_adapters_xxx.py

 Tests integración con FSM

 Credenciales externalizadas

 Validación de webhooks

 Rate limiting configurado

 Error handling robusto

 Logging completo

 Métricas registradas

 Seguridad auditada

🔗 Enlaces relacionados
FSM Engine — Orquestador central

Agents Overview — Sistema multi-agente

Best Practices — Convenciones adapters

Testing — Cómo testear adapters

📌 Meta-información
Campo	Valor
Archivo	docs/adapters/overview.md
Versión	1.0
Última revisión	2025-11-08 17:14 CET (Sesión 36)
Responsable	Adapters Team / CEO
Estado	✅ Activo
🛡️ Auditoría y cumplimiento
Parte del Hito 36.1 (docs/adapters/)

Sigue estándar THEA IA: Modular, auditable, escalable

Arquitectura validada y documentada

Cambios deben reflejarse en CHANGELOG

Validado en sesión 36

Nota: Sistema de adapters es el punto de entrada a THEA IA. Cualquier cambio arquitectónico requiere revisión y actualización de estos documentos.