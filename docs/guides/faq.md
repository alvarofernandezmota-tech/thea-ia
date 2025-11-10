❓ FAQ — THEA IA
Versión: v0.14.0
Última actualización: 2025-11-09 19:18 CET (Sesión 37)
Responsable: Álvaro Fernández Mota (CEO THEA IA)
Estado: ✅ Activo

📚 Preguntas Frecuentes
1. ¿Qué es THEA IA?
THEA IA es una plataforma conversacional basada en agentes especializados que entienden intención del usuario, extraen entidades relevantes y ejecutan acciones automáticas. Diseñada para empresas que necesitan automatizar conversaciones complejas.

Características:

Agentes multi-especializados (agenda, soporte, compras, etc.)

Conversaciones naturales en español

Integración con Telegram, WhatsApp, API REST

FSM para flujos controlados

Seguridad enterprise

2. ¿Cuál es la diferencia entre THEA IA y chatbots tradicionales?
Aspecto	THEA IA	Chatbot Tradicional
Arquitectura	Agentes + FSM	Rule-based
Inteligencia	ML (spaCy) + LLM	Regex patterns
Contexto	Mantiene contexto conversacional	Sin contexto
Escalabilidad	Múltiples agentes	Monolítico
Seguridad	Enterprise (OAuth2, RBAC)	Básica
Observabilidad	Completa (Prometheus, Loki, Jaeger)	Sin monitoreo
3. ¿Necesito ML/IA para usar THEA IA?
No. THEA IA incluye:

Modelo spaCy pre-entrenado para NLP español

Intent detection y entity extraction listos para usar

Posibilidad de entrenar con tus datos

Si quieres mejorar:

Entrena modelos custom con python scripts/train_intent_model.py

Usa LLMs (OpenAI, Anthropic, Llama) como agentes

4. ¿Cómo inicio un proyecto THEA IA?
bash
# 1. Instala
git clone https://github.com/thea-ia/thea-ia.git
cd thea-ia

# 2. Setup
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# 3. Configura .env
cp .env.example .env
# Edita con tu TELEGRAM_BOT_TOKEN, etc.

# 4. Ejecuta
uvicorn src.theaia.api:app --reload

# 5. Visita
open http://localhost:8000/docs
Ver: Getting Started o Quickstart

5. ¿Cómo creo mi primer agente?
python
from src.theaia.core.agent import Agent

class MiAgente(Agent):
    name = "MiAgente"
    description = "Mi primer agente"
    
    async def handle(self, intent: str, entities: dict, context: dict):
        if intent == "saludo":
            return {"response": "Hola! En qué te puedo ayudar?"}
        return {"response": "No entendí"}

# Registra en FSM
from src.theaia.core.fsm import FSM
fsm = FSM()
fsm.register_agent(MiAgente())
Ver: Architecture: Agents

6. ¿Cómo integro Telegram?
bash
# 1. Crea bot en BotFather (@BotFather en Telegram)
# Copia TOKEN

# 2. En .env
TELEGRAM_BOT_TOKEN=<tu-token>
TELEGRAM_WEBHOOK_URL=https://tu-domain.com/adapters/telegram/webhook

# 3. Usa ngrok para test local
ngrok http 8000

# 4. Envia mensaje a tu bot
# THEA IA recibe y responde
Ver: Deployment: Telegram

7. ¿Qué BD soporta THEA IA?
Soportadas:

PostgreSQL (recomendado producción)

SQLite (desarrollo/testing)

MySQL (experimental)

En .env:

bash
# PostgreSQL
DATABASE_URL=postgresql://user:pass@host:5432/theaia

# SQLite
DATABASE_URL=sqlite:///thea.db
8. ¿Cómo autenticar usuarios?
THEA IA usa OAuth2 + JWT:

python
# Login
curl -X POST http://localhost:8000/auth/login \
  -d "username=user@example.com&password=..."

# Response
{
  "access_token": "eyJ0eXAi...",
  "token_type": "bearer"
}

# Usar token
curl -H "Authorization: Bearer <token>" \
  http://localhost:8000/chat/...
Ver: Security: Authentication

9. ¿Es THEA IA seguro?
Sí. Incluye:

TLS 1.3 (HTTPS)

OAuth2 + JWT

RBAC (Role-Based Access Control)

AES-256 encryption datos sensibles

GDPR compliance

SOC 2 Type II ready

Ver: Security Overview

10. ¿Cómo escalo THEA IA?
Local:

Aumenta DATABASE_POOL_SIZE

Usa PostgreSQL en lugar de SQLite

Production:

Deploy en Kubernetes (3+ replicas)

Load balancer

Horizontal Pod Autoscaler (HPA)

Redis para caching/sessions

Ver: Architecture: Scalability

11. ¿Qué pasa con mis datos?
THEA IA:

NO almacena conversaciones por defecto (con STORE_CONVERSATIONS=false)

GDPR compliance: derecho a acceso, supresión, portabilidad

Encriptación datos en reposo y en tránsito

Auditoría completa de accesos

Ver: Security: Compliance

12. ¿Cómo monitorieo THEA IA?
Observabilidad incluida:

Prometheus: métricas (request rate, latency, errors)

Loki: logs centralizados

Jaeger: traces distribuidos

Dashboards:

bash
# Prometheus
http://localhost:9090

# Grafana (pre-configured)
http://localhost:3000  # user: admin, pass: admin
Ver: Troubleshooting

13. ¿Cómo contribuyo?
Fork repo: https://github.com/thea-ia/thea-ia

Crea rama: git checkout -b feature/mi-feature

Commitea: git commit -m "Add feature"

Push: git push origin feature/mi-feature

PR a main

Ver: Contributing

14. ¿Dónde está la documentación técnica?
Guides: docs/guides/

Architecture: docs/architecture/

Security: docs/security/

API: http://localhost:8000/docs (Swagger)

15. ¿Cuál es el roadmap?
Ver: Roadmap

Próximas features:

LLM integrations (GPT-4, Claude, Llama)

WhatsApp adapter

Advanced entity linking

Multi-language support (en, pt, fr)

Mobile app

🆘 Soporte
Documentación: docs/guides/

Issues: https://github.com/thea-ia/thea-ia/issues

Email: support@thea-ia.com

Discord: https://discord.gg/thea-ia

📌 Meta-información
Campo	Valor
Archivo	docs/guides/faq.md
Versión	v0.14.0
Última revisión	2025-11-09 19:18 CET (S37)
Responsable	CEO THEA IA
Estado	✅ Activo
Última actualización: 2025-11-09 19:18 CET