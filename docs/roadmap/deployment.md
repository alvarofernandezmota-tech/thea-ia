# 🚀 Deployment — THEA IA

**Versión:** v0.14.0  
**Última actualización:** 2025-10-31 03:23 CET  
**Responsable:** Álvaro Fernández Mota (CEO THEA IA)

---

## 📍 Ambientes

| Ambiente | Hosting | DB | Observabilidad |
|----------|---------|-----|---|
| **Local** | Localhost | JSON local | Logs console |
| **Staging** | Railway/Heroku | PostgreSQL | Basic |
| **Production** | AWS/GCP + K8s (H09) | PostgreSQL + backup | Prometheus + Grafana + Loki |

---

## 🏗️ Production Deployment (H09+)

### Prerequisitos (H09 — K8s)

- Kubernetes cluster (AWS EKS / GCP GKE)
- Docker registry (ECR / Artifact Registry)
- PostgreSQL managed (RDS / Cloud SQL)
- GitHub Actions para CI/CD

---

## 🐳 Step 1: Build & Push Docker Image

### Build Dockerfile optimizado
Build
docker build -t your-registry/thea-ia:v0.14.0
-f Dockerfile
--build-arg ENVIRONMENT=production
.

Push
docker push your-registry/thea-ia:v0.14.0

text

### Dockerfile (production)
FROM python:3.10-slim

WORKDIR /app

Deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

Code
COPY src/ src/
COPY alembic/ alembic/
COPY alembic.ini .

Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3
CMD python -c "import requests; requests.get('http://localhost:8000/health')"

Run
CMD ["uvicorn", "src.theaia.api:app", "--host", "0.0.0.0", "--port", "8000"]

text

---

## ☸️ Step 2: Kubernetes Deployment (H09)

### k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
name: thea-ia
labels:
app: thea-ia
spec:
replicas: 3
selector:
matchLabels:
app: thea-ia
template:
metadata:
labels:
app: thea-ia
spec:
containers:
- name: thea-ia
image: your-registry/thea-ia:v0.14.0
ports:
- containerPort: 8000
env:
- name: ENVIRONMENT
value: "production"
- name: DATABASE_URL
valueFrom:
secretKeyRef:
name: thea-secrets
key: database-url
- name: JWT_SECRET
valueFrom:
secretKeyRef:
name: thea-secrets
key: jwt-secret
resources:
requests:
memory: "256Mi"
cpu: "250m"
limits:
memory: "512Mi"
cpu: "500m"
livenessProbe:
httpGet:
path: /health
port: 8000
initialDelaySeconds: 30
periodSeconds: 10

text

### k8s/service.yaml
apiVersion: v1
kind: Service
metadata:
name: thea-ia-service
spec:
selector:
app: thea-ia
type: LoadBalancer
ports:

protocol: TCP
port: 80
targetPort: 8000

text

### Deploy
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml

Verificar
kubectl get pods -l app=thea-ia
kubectl logs -f deployment/thea-ia

text

---

## 🗄️ Step 3: Database Setup

### Migraciones (Alembic)
Remote
export DATABASE_URL=postgresql://user:pass@db.host:5432/theaia

Run migrations
alembic upgrade head

Crear índices
psql $DATABASE_URL < scripts/create_indexes.sql

text

---

## 🔐 Step 4: Secrets Management

### K8s secrets
Crear secret
kubectl create secret generic thea-secrets
--from-literal=database-url=postgresql://...
--from-literal=jwt-secret=$(openssl rand -hex 32)

Verificar
kubectl get secrets thea-secrets

text

---

## 🚀 Step 5: CI/CD (GitHub Actions)

### .github/workflows/deploy.yml
name: Deploy to K8s

on:
push:
branches: [main]

jobs:
deploy:
runs-on: ubuntu-latest
steps:
- uses: actions/checkout@v3

text
- name: Build and push Docker
  uses: docker/build-push-action@v4
  with:
    context: .
    push: true
    tags: ${{ secrets.REGISTRY }}/thea-ia:${{ github.sha }}

- name: Deploy to K8s
  run: |
    kubectl set image deployment/thea-ia \
      thea-ia=${{ secrets.REGISTRY }}/thea-ia:${{ github.sha }}
    kubectl rollout status deployment/thea-ia
text

---

## 📊 Step 6: Observabilidad (H11)

### Prometheus scrape
prometheus.yml
global:
scrape_interval: 15s

scrape_configs:

job_name: 'thea-ia'
static_configs:

targets: ['localhost:8000']

text

### Grafana dashboard
http://grafana.your-domain.com

Import: Prometheus datasource

Create: FSM latency, requests/sec, errors

text

---

## 📋 Checklist Pre-deployment

- [ ] Tests pasen ≥90%
- [ ] Build Docker exitoso
- [ ] Secrets configurados en K8s
- [ ] Migraciones DB ejecutadas
- [ ] Health check respondiendo
- [ ] Logs en Loki visibles
- [ ] Métricas Prometheus activas
- [ ] SSL/TLS certificado válido

---

## 🔍 Verificaciones Post-deployment

Health check
curl https://your-domain.com/health

Logs
kubectl logs -f deployment/thea-ia

Métricas
curl https://your-domain.com/metrics

DB connection
psql postgresql://... -c "SELECT 1"

text

---

## 🔄 Rollback

Si algo falla
kubectl rollout undo deployment/thea-ia

Ver historial
kubectl rollout history deployment/thea-ia

text

---

## 📖 Documentación relacionada

- [Quickstart](./quickstart.md) — Desarrollo local
- [Troubleshooting](./troubleshooting.md) — Resolver problemas
- [H09 - Docker/K8s](../roadmap/milestones/H03_17.md)

---

**Última actualización:** 2025-10-31 03:23 CET
