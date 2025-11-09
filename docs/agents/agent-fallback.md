🛡️ Agent: Fallback — THEA IA
Versión: 1.0
Última actualización: 2025-11-08 (Sesión 35)
Responsable: Agents Team
Estado: ✅ Activo
Prioridad: 🟠 Baja (Soporte)

📋 Propósito
El Agente Fallback maneja errores, comandos no reconocidos y casos edge: última línea de defensa cuando ningún otro agente puede procesar la solicitud.

Audiencia:

Desarrolladores mejorando error handling

QA validando casos no happy path

🎯 Responsabilidades
Funcionalidad	Descripción
Manejar errores	Capturar errores no manejados
Comandos desconocidos	Responder a inputs no reconocidos
Sugerir alternativas	Proponer comandos similares
Logging errores	Registrar todos los fallbacks
Escalación	Notificar humano si necesario
🔧 Configuración
text
agent:
  name: "Fallback"
  version: "1.0"
  enabled: true
  timeout: 5

error_handling:
  log_level: "warning"
  notify_threshold: 10  # Notificar si >10 fallbacks/min
📥 Entrada
python
{
  "action": "unknown",
  "data": {
    "original_input": "comando desconocido xyz",
    "error": "No agent could handle this"
  }
}
📤 Salida
python
{
  "status": "fallback",
  "message": "No entendí tu solicitud. ¿Quisiste decir 'crear evento'?",
  "suggestions": ["crear evento", "nueva nota", "ayuda"]
}
📊 Métricas
Métrica	Actual	Target
Fallback rate	2.5%	< 5%
Suggestion accuracy	0.78	> 0.75
📌 Meta
Campo	Valor
Archivo	docs/agents/agent_fallback.md
Estado	✅ Activo
