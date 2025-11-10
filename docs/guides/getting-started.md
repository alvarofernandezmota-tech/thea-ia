🎯 Getting Started — THEA IA
Versión: v0.14.0
Última actualización: 2025-11-09 19:11 CET (Sesión 37)
Responsable: Álvaro Fernández Mota (CEO THEA IA)
Estado: ✅ Activo

👋 Bienvenido a THEA IA
THEA IA es una plataforma conversacional inteligente basada en agentes especializados que entienden intención, extraen entidades y ejecutan acciones automáticas.

Características principales:

🤖 Agentes multi-especializados (agenda, soporte, compras, etc.)

💬 Conversaciones naturales en español

🔗 Integración con Telegram, WhatsApp, REST API

🎯 FSM (Finite State Machine) para flujos controlados

🛡️ Seguridad enterprise (OAuth2, RBAC, AES-256)

📊 Observabilidad completa (Prometheus, Loki, Jaeger)

⚡ 5 Minutos para Empezar
1. Requisitos mínimos
bash
# Verificar Python
python --version  # 3.10+

# Clonar repo
git clone https://github.com/thea-ia/thea-ia.git
cd thea-ia
2. Setup local (dev)
bash
# Crear entorno
python -m venv venv
source venv/bin/activate  # o venv\Scripts\activate en Windows

# Instalar dependencias
pip install -r requirements.txt
3. Ejecutar
bash
# Start dev server
uvicorn src.theaia.api:app --reload

# En otra terminal, probar
curl http://localhost:8000/docs
¡Listo! Ya tienes THEA IA corriendo localmente.

🏗️ Arquitectura de 30 segundos
text
┌─────────────────────────────────────────────────────────────┐
│                    Usuarios (Telegram, REST)                │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────┐
│                   FastAPI Gateway                           │
│  • Autenticación (OAuth2, JWT)                              │
│  • Validación (Pydantic)                                    │
│  • Rate limiting                                            │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────┐
│                    FSM Engine                               │
│  • Estado máquina (processing → disambiguation → action)    │
│  • Context manager                                          │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────┐
│              Agentes Especializados                         │
│  • AgendaAgent (agendar citas)                              │
│  • SupportAgent (soporte técnico)                           │
│  • ComprasAgent (gestión compras)                           │
│  • ...                                                       │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────┐
│              Database (PostgreSQL/SQLite)                   │
│  • Users                                                    │
│  • Conversations                                            │
│  • Events & Audit logs                                      │
└─────────────────────────────────────────────────────────────┘
💡 Primeros Casos de Uso
Caso 1: Usuario agenda cita
text
Usuario: "Quiero agendar cita con el doctor mañana a las 10"

THEA IA:
1. Detecta intent: "schedule_appointment"
2. Extrae entidades: { entity: "doctor", time: "tomorrow 10:00" }
3. Ejecuta: AgendaAgent.schedule()
4. Responde: "Cita agendada ✓ Para confirmar: ...?"
Caso 2: Soporte técnico
text
Usuario: "La app me da error 500 en compras"

THEA IA:
1. Detecta intent: "report_issue"
2. Extrae contexto: { error: "500", module: "purchases" }
3. Ejecuta: SupportAgent.escalate()
4. Responde: "Ticket #1234 creado. Nuestro equipo te contactará."
Caso 3: Consulta de estado
text
Usuario: "¿Cuál es el status de mi pedido 5678?"

THEA IA:
1. Detecta intent: "check_status"
2. Extrae ID: { order_id: "5678" }
3. Ejecuta: ComprasAgent.get_status()
4. Responde: "Tu pedido está en tránsito, llega mañana."
🔧 Estructura de Carpetas
text
thea-ia/
├── src/theaia/
│   ├── core/              # FSM, context, orchestration
│   ├── agents/            # Agentes especializados
│   ├── adapters/          # Telegram, REST, Slack, etc.
│   ├── ml/                # Intent detection, entity extraction
│   ├── api.py             # FastAPI app
│   └── models.py          # Pydantic models
├── docs/
│   ├── guides/            # ← Estás aquí
│   ├── architecture/
│   ├── security/
│   └── ...
├── tests/
├── requirements.txt
├── Dockerfile
└── docker-compose.yml
📚 Próximos Pasos
Necesitas	Ir a	Tiempo
Instalación paso a paso	Installation	10 min
Variables de entorno	Configuration	5 min
Primeros tests	Quickstart	15 min
Deploy a producción	Deployment	20 min
Solucionar problemas	Troubleshooting	5+ min
Preguntas frecuentes	FAQ	5 min
Contribuir al proyecto	Contributing	10 min
🆘 ¿Te estancaste?
Error en setup: → Troubleshooting

App no inicia: → Troubleshooting

¿Cómo funciona X? → FAQ

¿Puedo contribuir? → Contributing

📌 Meta-información
Campo	Valor
Archivo	docs/guides/getting-started.md
Versión	v0.14.0
Última revisión	2025-11-09 19:11 CET (S37)
Responsable	CEO THEA IA
Estado	✅ Activo
Última actualización: 2025-11-09 19:11 CET