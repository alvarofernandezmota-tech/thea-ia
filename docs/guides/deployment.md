🚀 Deployment Guide — THEA IA
Versión: v0.14.0
Última actualización: 2025-11-09 19:14 CET (Sesión 37)
Responsable: Álvaro Fernández Mota (CEO THEA IA)
Estado: ✅ Activo

📋 Propósito
Guía práctica para deployar THEA IA en local y producción.

Para documentación técnica detallada de arquitectura deployment:
👉 Architecture: Deployment

🏠 Quick Deploy Local
Opción 1: Docker Compose (recomendado)
bash
# Clonar repo
git clone https://github.com/thea-ia/thea-ia.git
cd thea-ia

# Setup .env
cp .env.example .env
# Editar .env con tus valores

# Start todos los servicios
docker-compose up -d

# Verificar
curl http://localhost:8000/health
Servicios levantados:

FastAPI app (puerto 8000)

PostgreSQL (puerto 5432)

Prometheus (puerto 9090)

Grafana (puerto 3000)

Loki + Promtail (logs)

Opción 2: Manual (dev)
bash
# Setup Python
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Start app
uvicorn src.theaia.api:app --reload --host 0.0.0.0 --port 8000
☁️ Quick Deploy Producción
Opción 1: Kubernetes (recomendado)
bash
# Aplicar manifests
kubectl apply -f k8s/

# Verificar pods
kubectl get pods -n thea-ia

# Ver logs
kubectl logs -f deployment/thea-ia -n thea-ia

# Obtener URL externa
kubectl get svc -n thea-ia
Recursos desplegados:

Deployment (3 replicas)

Service (LoadBalancer)

ConfigMap (.env vars)

Secret (JWT, DB password)

HPA (Horizontal Pod Autoscaler)

Ingress (HTTPS/TLS)

Opción 2: Docker (standalone)
bash
# Build image
docker build -t thea-ia:latest .

# Run container
docker run -d \
  --name thea-ia \
  -p 8000:8000 \
  -e DATABASE_URL=postgresql://... \
  -e JWT_SECRET=... \
  -e TELEGRAM_BOT_TOKEN=... \
  thea-ia:latest

# Check logs
docker logs -f thea-ia
🔐 Variables de Entorno Esenciales
bash
# App
ENVIRONMENT=production
LOG_LEVEL=INFO
SECRET_KEY=<random-string-64-chars>

# Database
DATABASE_URL=postgresql://user:pass@host:5432/theaia

# Auth
JWT_SECRET=<random-string-64-chars>
JWT_ALGORITHM=HS256
JWT_EXPIRATION=3600

# Telegram
TELEGRAM_BOT_TOKEN=<your-bot-token>
TELEGRAM_WEBHOOK_URL=https://your-domain.com/adapters/telegram/webhook

# Observability
PROMETHEUS_PORT=9090
LOKI_URL=http://loki:3100
JAEGER_ENDPOINT=http://jaeger:14268/api/traces
Ver guía completa: Configuration

✅ Verificación Post-Deploy
1. Health check
bash
curl https://your-domain.com/health

# Respuesta esperada:
{
  "status": "healthy",
  "version": "v0.14.0",
  "database": "connected",
  "uptime": 3600
}
2. Logs
bash
# Docker
docker logs thea-ia

# Kubernetes
kubectl logs deployment/thea-ia -n thea-ia

# Loki (Grafana)
# http://your-domain.com:3000 → Explore → Loki → {job="thea-ia"}
3. Métricas
bash
curl https://your-domain.com/metrics

# O visitar Prometheus:
# http://your-domain.com:9090
4. Test funcional
bash
# Crear usuario
curl -X POST https://your-domain.com/users \
  -H "Content-Type: application/json" \
  -d '{"name":"Test","email":"test@example.com"}'

# Enviar mensaje
curl -X POST https://your-domain.com/chat/test_user \
  -H "Content-Type: application/json" \
  -d '{"message":"hola"}'
🔄 CI/CD (GitHub Actions)
Setup automático
text
# .github/workflows/deploy.yml
name: Deploy THEA IA

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Build Docker image
        run: docker build -t thea-ia:${{ github.sha }} .
      
      - name: Push to registry
        run: docker push thea-ia:${{ github.sha }}
      
      - name: Deploy to K8s
        run: |
          kubectl set image deployment/thea-ia \
            thea-ia=thea-ia:${{ github.sha }} \
            -n thea-ia
Ver detalles: Architecture: CI/CD

🐛 Troubleshooting Deploy
Problema	Solución
Pod no inicia	Check logs: kubectl logs pod/thea-ia-xxx
DB connection failed	Verificar DATABASE_URL en ConfigMap
502 Bad Gateway	Service no expone puerto correcto
Memory leak	Aumentar resources.limits.memory
High latency	Escalar replicas: kubectl scale --replicas=5 deployment/thea-ia
Ver guía completa: Troubleshooting

📊 Monitoreo Post-Deploy
Grafana Dashboards
App Performance

Request rate

Error rate

Latency (p50, p95, p99)

FSM Metrics

Transiciones/sec

State distribution

Agent response time

Infrastructure

CPU/Memory usage

Network I/O

Disk I/O

Importar dashboards:

bash
# Dashboard ID: 12345 (THEA IA Overview)
curl -X POST http://grafana:3000/api/dashboards/import \
  -H "Content-Type: application/json" \
  -d '{"dashboard": {...}, "overwrite": true}'
🔒 Seguridad en Producción
 HTTPS habilitado (TLS 1.3)

 Variables secretas en Kubernetes Secrets

 Network policies configuradas

 Rate limiting activo

 Firewall rules (solo puertos necesarios)

 Backup automático DB (diario)

 Monitoring alerts configurados

Ver: Security Overview

📖 Recursos Adicionales
Architecture: Deployment — Detalles técnicos completos

Architecture: Scalability — Escalar horizontal/vertical

Configuration — Variables avanzadas

Troubleshooting — Resolver problemas

📌 Meta-información
Campo	Valor
Archivo	docs/guides/deployment.md
Versión	v0.14.0
Última revisión	2025-11-09 19:14 CET (S37)
Responsable	CEO THEA IA
Estado	✅ Activo
Última actualización: 2025-11-09 19:14 CET