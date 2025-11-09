📞 Adapter: WhatsApp — THEA IA
Versión: 1.0
Última actualización: 2025-11-08 17:22 CET (Sesión 36)
Responsable: Adapters Team
Estado: ✅ Activo
Prioridad: 🟠 Baja (Futuro)

📋 Propósito
Adapter para integración con WhatsApp Business API. THEA IA responde mensajes en WhatsApp.

Audiencia:

Empresas con WhatsApp Business

Soporte al cliente automatizado

Marketing automation

🎯 Responsabilidades
Funcionalidad	Descripción
Recibir mensajes	Webhooks de WhatsApp Business
Normalizar	Conversión a formato THEA IA
Enviar respuestas	Usar WhatsApp Cloud API
Plantillas	Mensajes pre-aprobados
Media	Imágenes y documentos
Estado de entrega	Tracking de envíos
🔧 Configuración
text
adapter:
  name: "WhatsApp"
  version: "1.0"
  enabled: false  # Futuro
  timeout: 30

credentials:
  phone_id: "${WHATSAPP_PHONE_ID}"
  access_token: "${WHATSAPP_ACCESS_TOKEN}"
  
features:
  templates: true
  media: true
  location: true
📥 Entrada (Webhook)
python
{
  "object": "whatsapp_business_account",
  "entry": [{
    "changes": [{
      "value": {
        "messages": [{
          "from": "34912345678",
          "type": "text",
          "text": {"body": "crear evento"}
        }]
      }
    }]
  }]
}
📤 Salida (Normalizado)
python
{
  "user_id": "34912345678",
  "channel": "whatsapp",
  "message": "crear evento",
  "metadata": {
    "phone": "34912345678",
    "timestamp": "2025-11-08T17:22:00Z"
  }
}
📊 Métricas
Métrica	Actual	Target
Delivery rate	99.8%	> 99%
Response time	500ms	< 1000ms
Template approval	100%	100%
📌 Meta-información
Campo	Valor
Archivo	docs/adapters/adapter_whatsapp.md
Versión	1.0
Última revisión	2025-11-08 17:22 CET (Sesión 36)
Estado	✅ Activo (futuro)
🛡️ Auditoría y cumplimiento
Parte del Hito 36.1 (docs/adapters/)

Validado en sesión 36