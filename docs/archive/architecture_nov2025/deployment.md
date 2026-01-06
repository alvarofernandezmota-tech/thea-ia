🚀 Deployment Strategy — THEA IA
Versión: v0.14.0
Última actualización: 2025-11-08 17:30 CET (Sesión 36)
Responsable: DevOps Team / Álvaro Fernández Mota (CEO)
Estado: ✅ Activo

📋 Propósito
Estrategia de despliegue de THEA IA: local, staging, producción. CI/CD automático, rollback, monitoreo.

Audiencia:

DevOps engineers

Developers entendiendo pipeline

SREs monitoreando deployments

🎯 Entornos
Entorno	Host	BD	Replicas	Auto-scale
Local	Laptop/Docker	JSON fallback	1	❌
Staging	AWS/GCP (dev)	PostgreSQL	2	✅ (0-2)
Producción	AWS/GCP (prod)	PostgreSQL HA	3+	✅ (3-10)
🔧 Stack de Deployment
Local:

bash
docker-compose up
# → localhost:8000
Staging/Prod:

text
GitHub Actions (CI)
    ↓
Build Docker image
    ↓
Push to ECR/GCR
    ↓
Deploy a K8s (Helm)
    ↓
Health checks + Smoke tests
    ↓
Notificar Slack
📊 Pipeline CI/CD
text
1. Commit a main
2. GitHub Actions inicia
   - Run tests (pytest)
   - Coverage check (>85%)
   - Lint (black, flake8)
   - Security scan (bandit)
3. Build Docker image
4. Push a registry (ECR/GCR)
5. Deploy a staging
6. Run smoke tests
7. Await manual approval
8. Deploy a producción (K8s)
9. Monitor por 10 min
10. Rollback auto si error
🔄 Estrategias de Deployment
Blue-Green Deployment
Versión actual (blue) + nueva (green) en paralelo

Traffic switch instantáneo

Rollback fácil (vuelve a blue)

Canary Deployment
Env: 10% tráfico → nueva versión

Monitor métricas

Si OK: 50% → 100%

Si error: rollback automático

Rolling Update
Reemplazar pods gradualmente

1 pod nuevo, 1 pod viejo caído

Tiempo: ~2 min para N replicas

🛠️ Herramientas
Herramienta	Rol
GitHub Actions	CI/CD orchestration
Docker	Containerización
Helm	K8s package manager
ArgoCD	GitOps deployment
Prometheus	Métricas
DataDog	APM (opcional)
📌 Versioning
Semantic Versioning: MAJOR.MINOR.PATCH

MAJOR: Cambios no backward-compatible (API breaking)

MINOR: Features nuevas (backward-compatible)

PATCH: Bug fixes

Tags Docker: ghcr.io/theaia/api:v0.14.0

✅ Pre-deployment Checklist
 Todos tests pasan (100%)

 Coverage >85%

 Docs actualizados

 Secrets rotados

 DB migrations tested

 Rollback plan definido

 Slack notification configured

 Health checks OK

🔙 Rollback
Automático si:

Health checks fallan

Error rate >5%

Latencia promedio >1s

Pod crashes

Manual:

bash
kubectl rollout undo deployment/thea-api
📊 Métricas de Deployment
Métrica	Target
Deployment frequency	1x/día
Lead time for changes	<1 hora
MTTR	<15 min
Change failure rate	<5%
📌 Meta-información
Campo	Valor
Archivo	docs/architecture/deployment.md
Versión	v0.14.0
Última revisión	2025-11-08 17:30 CET (Sesión 36)
Responsable	DevOps Team / CEO
Estado	✅ Activo
🛡️ Auditoría y cumplimiento
Parte del Hito 36.1 (docs/architecture/)

ADR-003 (Docker + K8s) soporta esta estrategia

Validado en sesión 36