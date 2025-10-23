⚙️ Guía DevOps Interna – Thea IA 3.0 Enterprise
Este documento define los flujos, comandos y políticas DevOps estándar de Thea IA Systems S.L.
Es de uso interno para el equipo de despliegue, CI/CD, monitoreo y seguridad.

🧩 Objetivo
- Unificar los procesos de build, test, deploy, rollback y auditoría.
- Definir los pipelines CI/CD y manejadores de entorno (local, staging, prod).
- Mantener la observabilidad y seguridad de infraestructura operando 24/7.

🔁 Ciclo de Integración y Despliegue
 Etapa 	 Responsable 	 Descripción 
 Build 	 CI Runner 	 Compila entorno virtual & Docker image. 
 Test 	 QA Auto / Pytest 	 Ejecuta tests unit + integración FSM. 
 Lint 	 CI Check 	 Black / Flake8 / isort. 
 Deploy 	 Actions + RailwayCLI 	 Push a Railway/ECR. 
 Monitor 	 Prometheus / Loki 	 Supervisa servicios activos. 
 Rollback 	 Ops Team / Script 	 Reversión último deploy válido. 
📦 Entornos Definidos
 Nombre 	 Scope 	 Dominio 
 development 	 Codespaces / Docker 	 http://localhost:8000 
 staging 	 Railway pre‑prod 	 https://staging.theaia.com 
 production 	 Railway + ECS 	 https://api.theaia.com 
🧠 Comandos Locales de Desarrollo
bash
# Crear entorno virtual y instalar dependencias
python -m venv .env && source .env/bin/activate
pip install -r requirements.txt

# Ejecutar tests
pytest -v src/theaia/tests/

# Correr servidor local
uvicorn src.theaia.api.main:app --reload

# Alembic Migraciones
alembic revision --autogenerate -m "init"
alembic upgrade head

# Linter rápido
black src/ && isort src/ && flake8 src/
🚀 Pipeline CI/CD
Integrado en .github/workflows/thea_ci.yml

text
on push:
  branches: [main]
jobs:
  setup: { … }
  tests: { … }
  docker: { … }
  deploy: { … }
Rollback Manual:

bash
bash scripts/revert.sh
Rollback Automático:
→ configurado via failure() trigger en pipeline.

🔧 Estructura de Scripts DevOps
text
scripts/
├── setup_env.sh        # Inicialización local automatizada
├── migrate.sh          # Migraciones DB (autogen + upgrade)
├── backup.sh           # Backup diario Drive/S3
├── revert.sh           # Rollback último despliegue
├── lint.sh             # Limpieza de código y verificación
├── deploy.sh           # Despliegue manual
└── test_runner.sh      # Ejecución Pytest integral
📈 Gestión de Logs Internos
- Ruta: logs/theaia.log (estructurado JSON).
- Pipeline Promtail → Loki → Grafana.
- Rotación cada 20 MB / 5 backups.

🩺 Monitorización 24/7
- Despliegues monitorizados por Prometheus (/metrics).
- Alertmanager configurado con Slack (Webhook seguro).
- Grafana — paneles automáticos: FSM Load, API, Agents, DB.

🔒 Seguridad y Autenticación
- Clave privada JWT renovable 90 días.
- No se almacenan secrets en entornos públicos.
- Integración SOC 2 / GDPR auditable.
- TLS Cloudflare Activo en ambientes Railway / AWS.

🧱 Comandos Infraestructura (Ops)
 Comando 	 Acción 
 docker-compose up -d 	 Levanta infraestructura local. 
 aws ecs update-service... 	 Desplegar nueva imagen. 
 railway up 	 Deploy rápido a Railway. 
 kubectl rollout status deployment/thea-ia 	 Verificar deploy K8s. 
 kubectl rollout undo deployment/thea-ia 	 Hacer rollback. 
🧩 KPIs de Operación (2025)
 Categoría 	 Indicador 	 Meta 2025 
 Disponibilidad 	 Uptime API 	 99.94 % 
 Despliegue 	 Build->Deploy 	 < 7 min 
 Rollback 	 Tiempo medio MTTR 	 < 90 s 
 Seguridad 	 Incidentes Altos 	 0 
 Calidad Código 	 Coverage Pytest 	 ≥ 98 % 
📁 Checklist DevOps Pre‑Lanzamiento
☑ pytest  pasa 100 %.
☑ Revisión manual FSM.
☑ Logs limpios sin errores structlog.
☑ Docker construido sin warnings.
☑ Imagen firmada con cosign.
☑ Prometheus recibiendo /metrics.

© 2025 Thea IA Systems S.L. — Departamento DevOps & Infraestructura

text

---

¿Quieres que generemos ahora **`docs/SUMMARY.md`**, un índice navegable que enlace todos los documentos internos (`architecture`, `api_reference`, `monitoring`, `deployment`, `security`, `devops_readme`)?