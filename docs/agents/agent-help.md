❓ Agent: Help — THEA IA
Versión: 1.0
Última actualización: 2025-11-08 (Sesión 35)
Responsable: Agents Team
Estado: ✅ Activo
Prioridad: 🟠 Baja (Soporte)

📋 Propósito
El Agente Help proporciona asistencia y documentación al usuario: comandos disponibles, ejemplos, troubleshooting y guías rápidas.

Audiencia:

Usuarios buscando ayuda

Onboarding de nuevos usuarios

🎯 Responsabilidades
Funcionalidad	Descripción
Mostrar ayuda	Lista de comandos disponibles
Ejemplos	Ejemplos de uso por comando
FAQ	Preguntas frecuentes
Troubleshooting	Resolver problemas comunes
Guías	Tutoriales paso a paso
🔧 Configuración
text
agent:
  name: "Help"
  version: "1.0"
  enabled: true
  timeout: 5

docs:
  path: "/docs/guides/"
  cache: true
📥 Entrada
python
{
  "action": "get_help",
  "data": {
    "command": "create event"  # o null para ayuda general
  }
}
📊 Métricas
Métrica	Actual	Target
Help requests	120/day	n/a
Response time	50ms	< 100ms
📌 Meta
Campo	Valor
Archivo	docs/agents/agent_help.md
Estado	✅ Activo
