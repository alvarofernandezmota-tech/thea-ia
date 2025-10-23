# 📈 Monitorización Empresarial – Thea IA 3.0 Enterprise

Este documento define la arquitectura de observabilidad, las métricas internas, los componentes de monitoreo y la infraestructura recomendada para entornos productivos de **Thea IA Systems S.L.**  

---

## 🧩 Objetivos de Monitorización

- Supervisar la salud del sistema (API, FSM, agentes).  
- Detectar cuellos de botella y errores en tiempo real.  
- Analizar uso de recursos y rendimiento por servicio.  
- Asegurar SLAs corporativos y alertar en caso de degradación.  
- Cumplir estándares de auditoría interna y seguridad de infraestructura.

---

## ⚙️ Arquitectura de Monitorización

La infraestructura empresarial de monitoreo Thea IA usa **Prometheus**, **Grafana** y **Loki**, implementados en Railway, AWS ECS o EKS.  

### Diagrama simplificado

┌──────────────────────┐
│ Thea IA API (FastAPI) │
│ /health  /metrics  /logs │
└──────────┬──────────┘
│
▼
┌───────────────────────┐
│ Prometheus Server     │ — Scrapea /metrics cada 15 s
└──────────┬────────────┘
▼
┌──────────────────────┐
│ Grafana Dashboard   │ — Visualización en tiempo real
└──────────┬───────────┘
▼
┌──────────────────────┐
│ Loki + Promtail     │ — Logs estructurados de FSM y agentes
└──────────────────────┘

text

---

## 🩺 Health Check / Métricas

**Endpoints expuestos por Thea IA:**

| Ruta | Tipo | Descripción |
|------|------|--------------|
| `/health` | GET | Verifica estado API, DB y agentes. |
| `/metrics` | GET | Métricas Prometheus (exporter nativo). |
| `/context/active` | GET | Número de contextos activos por usuario. |
| `/fsm/state` | GET | Estado FSM global y transiciones. |

**Métricas Prometheus por defecto:**
- `thea_api_requests_total`  
- `thea_fsm_transitions_total`  
- `thea_agent_response_time_seconds`  
- `thea_db_pool_usage_ratio`  
- `thea_context_active_sessions`

---

## 🌐 Configuración de Prometheus

Archivo `monitoring/prometheus.yml`:

global:
scrape_interval: 15s

scrape_configs:
- job_name: "thea-ia"
metrics_path: /metrics
static_configs:
- targets: ["localhost:8000"]

text

Para Railway o AWS:
docker run -d 
  --name prometheus 
  -p 9090:9090 
  -v $(pwd)/monitoring/prometheus.yml:/etc/prometheus/prometheus.yml 
  prom/prometheus

text

---

## 📊 Grafana Dashboard

1️⃣ Descarga imagen oficial: `grafana/grafana-enterprise:latest`  
2️⃣ Accede a [http://localhost:3000](http://localhost:3000) (usuario `admin` / `admin`).  
3️⃣ Agrega fuente Prometheus → URL `http://prometheus:9090`  
4️⃣ Importa el dashboard `grafana/thea_ia_dashboard.json`.

### KPIs recomendados

| Indicador | Descripción | Nivel de alerta |
|-------------|--------------|----------------|
| API Error Rate | > 2% en 5 minutos | Medio |
| Latencia Promedio > 1s | Retraso de respuesta | Alto |
| Transiciones FSM por Minuto | Caída repentina | Crítico |
| Sesiones Activas > 1000 | Escalado necesario | Informativo |

---

## 🧾 Logs Estructurados con Loki & Promtail

Thea IA genera logs JSON estructurados desde `structlog`, almacenados en `logs/theaia.log`.

Configuración ejemplo `monitoring/promtail-config.yml`:

server:
http_listen_port: 9080
positions:
filename: /var/log/positions.yaml
clients:
- url: http://loki:3100/loki/api/v1/push
scrape_configs:
- job_name: theaia
static_configs:
- targets:
- localhost
labels:
job: thea_api
path: /app/logs/*.log

text

Comando:
docker run -d --name loki -p 3100:3100 grafana/loki:2.9.0
docker run -d --name promtail -v $(pwd)/logs:/app/logs -v $(pwd)/monitoring/promtail-config.yml:/etc/promtail/config.yml grafana/promtail

text

---

## 🚨 Alertas Empresariales

Archivo `monitoring/alerts.yml`:

groups:
- name: thea_alerts
rules:
- alert: HighErrorRate
expr: rate(thea_api_requests_total{status=~"5.."}[1m]) > 0.05
for: 2m
labels:
severity: critical
annotations:
summary: "Errores HTTP 500 > 5% de tráfico"
description: "Alta tasa de error en Thea IA API"
- alert: SlowAgentResponse
expr: histogram_quantile(0.9, sum(rate(thea_agent_response_time_seconds_bucket[5m])) by (le)) > 1.5
for: 5m
annotations:
summary: "Agente lento"
description: "La respuesta media ≥ 1.5 s durante más de 5 minutos."

text

Alertmanager:
docker run -d --name alertmanager -p 9093:9093 prom/alertmanager 
  -v $(pwd)/monitoring/alerts.yml:/etc/alertmanager/config.yml

text

---

## 🛡️ Seguridad y Auditoría

- Logs de sistema firmados digitalmente y almacenados 90 días.  
- Backups de configuración Prometheus / Grafana en S3 o Railway volumes.  
- Autenticación corporativa en Grafana (SSO con OAuth2).  
- Retention Policie Loki = 30 días / 10 GB.  
- Cumplimiento GDPR para datos observacionales y anónimos.  

---

## 🔐 Integración Cloud Thea IA Systems S.L.

| Servicio | Proveedor | Notas |
|-----------|------------|-------|
| Prometheus | Railway / AWS EC2 | Scraping desde instancias Uvicorn. |
| Grafana | Cloud Pro Plan | Conexión OAuth SSO. |
| Loki | Elastic Railway / ECS | Recibe logs via Promtail. |
| Alertmanager | ECS Container | Push a Slack / MS Teams. |

---

**Thea IA 3.0 Enterprise Monitoring Suite**  
Versión 1.0 (Octubre 2025)  
Copyright © 2025 Thea IA Systems S.L.