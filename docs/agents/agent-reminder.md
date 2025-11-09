⏰ Agent: Reminder — THEA IA
Versión: 1.0
Última actualización: 2025-11-08 (Sesión 35)
Responsable: Agents Team
Estado: ✅ Activo
Prioridad: 🟡 Media (Util)

📋 Propósito
El Agente Reminder gestiona recordatorios y notificaciones: crear, listar, modificar y eliminar recordatorios con triggers temporales.

Audiencia:

Desarrolladores integrando sistema de notificaciones

Usuarios configurando recordatorios

🎯 Responsabilidades
Funcionalidad	Descripción
Crear recordatorio	Nuevo reminder con mensaje y fecha/hora
Listar recordatorios	Ver todos los recordatorios activos
Modificar recordatorio	Cambiar mensaje o trigger
Eliminar recordatorio	Borrar recordatorio
Notificar	Enviar notificación al usuario
Recurrentes	Recordatorios diarios/semanales
🔧 Configuración
text
agent:
  name: "Reminder"
  version: "1.0"
  enabled: true
  timeout: 10

capabilities:
  - create_reminder
  - list_reminders
  - modify_reminder
  - delete_reminder
  - trigger_notification

notification:
  channels: ["telegram", "email", "push"]
  retry: 3
📥 Entrada
python
{
  "action": "create_reminder",
  "data": {
    "message": "Reunión en 15 minutos",
    "trigger_at": "2025-11-09T09:45:00Z",
    "recurrence": null  # o "daily", "weekly"
  }
}
📊 Métricas
Métrica	Actual	Target
Notification delivery	99.2%	> 99%
Trigger accuracy	±5s	< ±10s
📌 Meta
Campo	Valor
Archivo	docs/agents/agent_reminder.md
Estado	✅ Activo