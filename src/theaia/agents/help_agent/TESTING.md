        ❓ Help Agent — Asistente de Ayuda Contextual
        Versión: v1.0.0
        Última actualización: 2025-11-10 20:16 CET (S14)
        Status: ✅ Producción

        📋 Propósito
        El Help Agent proporciona ayuda contextual sobre las funcionalidades de THEA IA. Identifica automáticamente temas de ayuda, ofrece explicaciones detalladas y permite consultas iterativas.

        Responsabilidades principales:

        ✅ Detectar solicitudes de ayuda

        ✅ Identificar tópicos de ayuda automáticamente

        ✅ Proporcionar documentación contextual

        ✅ Listar funcionalidades disponibles

        ✅ Mantener sesiones de ayuda multi-turno

        🏗️ Arquitectura
        text
        help_agent/
        ├── handler.py (HelpAgent class)
        ├── help_conversation_manager.py
        ├── model/help_fsm.py (FSM 5 estados)
        ├── tests/
        └── __init__.py
        Intenciones soportadas: ["ayuda", "soporte", "help", "asistencia"]

        🔄 Flujo Conversacional
        text
        Usuario: "¿necesito ayuda?"
        ↓
        THEA: "¿En qué puedo ayudarte? Puedo explicar: agendamiento, eventos, notas, 
            recordatorios y mucho más."
        [estado: awaiting_topic]
        ↓
        Usuario: "¿cómo agendar una cita?"
        ↓
        THEA: "Para agendar una cita, di 'agendar' y te guiaré paso a paso para crear tu cita.
            ¿Necesitas ayuda con algo más?"
        [estado: providing_help]
        ↓
        Usuario: "no, gracias"
        ↓
        THEA: "Perfecto. Si necesitas más ayuda, solo pregunta."
        [estado: completed]
        💻 Componentes Principales
        HelpAgent (handler.py)
        python
        class HelpAgent(BaseAgent):
            def __init__(self, user_id)
            def get_supported_intents() → ["ayuda", "soporte", "help", "asistencia"]
            def handle(user_id, message, context) → (response, state, context)
        HelpConversationManager (help_conversation_manager.py)
        python
        class HelpConversationManager:
            def __init__(self, user_id: str)
            def handle_message(user_id, message, context) → (response, state, context)
        HelpFSM (model/help_fsm.py)
        5 Estados:

        awaiting_topic — Espera que usuario solicite ayuda sobre un tópico

        providing_help — Proporciona explicación del tópico

        follow_up — Pregunta si necesita más ayuda

        completed — Sesión finalizada

        error — Error en el flujo

        Tópicos de Ayuda Disponibles:

        general: Overview completo de funcionalidades

        agenda: Cómo agendar citas

        notas: Cómo crear notas

        recordatorio: Cómo programar recordatorios

        eventos: Cómo crear eventos

        comandos: Lista de comandos disponibles

        🧪 Testing
        Coverage: 85%+

        Flujos de prueba:

        ✅ Solicitud de ayuda general

        ✅ Identificación automática de tópico

        ✅ Transición awaiting_topic → providing_help

        ✅ Sesiones multi-turno

        ✅ Error handling

        📊 Especificaciones
        Propiedad	Valor
        Versión	v1.0.0
        Estados FSM	5 (awaiting_topic, providing_help, follow_up, completed, error)
        Intenciones	4
        Tópicos	6 (general, agenda, notas, recordatorio, eventos, comandos)
        Test Coverage	85%+
        Status	✅ Production
        Help Agent v1.0 — Asistente Inteligente de Ayuda Contextual