📦 Despliegue Empresarial – Thea IA 3.0 Enterprise Edition
Este documento define los procesos de despliegue, balanceo, rollback y seguridad continuos usados por Thea IA Systems S.L. en entornos de producción y cloud corporativo.

🧩 Objetivo General
- Estandarizar el pipeline DevOps en Railway, AWS y EKS.
- Asegurar despliegues predecibles con rollback en 90 seg.
- Garantizar la resiliencia de FSM, routers y agentes bajo carga.
- Integrar pos‑despliegue en Prometheus / Grafana / Loki.

⚙️ Infraestructura Base
 Componente 	 Proveedor/Servicio 	 Función 
 API (App) 	 Railway / AWS ECS 	 Servicio asíncrono de FastAPI. 
 DB Primaria 	 AWS RDS (PostgreSQL) 	 Persistencia transaccional. 
 Cache / MQ 	 Redis Cluster / Celery 	 Mensajería y colas FSM. 
 Storage 	 S3 / Railway Volumes 	 Modelos ML y backups. 
 Logs / Metrics 	 Prometheus / Loki / Grafana 	 Observabilidad empresarial. 
☁️ Railway Cloud Workflow (Roadmap Main)
1️⃣ Push → main en GitHub.
2️⃣ GitHub Actions ejecuta el pipeline (ci, test, lint, docker).
3️⃣ Railway CLI implementa el deployment.
4️⃣ Servicio corre en container aislado uvicorn --workers 5.
5️⃣ Métricas se replican a Prometheus.
6️⃣ Rollback se invoca con railway revert --to <id>.

🛳️ Despliegue en AWS ECS (Europe‑West 1)
### 1️⃣ Build + Push Image

bash
aws ecr get-login-password --region eu-west-1 | \
docker login --username AWS --password-stdin ${AWS_ECR}
docker build -t thea-ia:latest -f Dockerfile.optimized .
docker tag thea-ia:latest ${AWS_ECR}/thea-ia:${GITHUB_SHA}
docker push ${AWS_ECR}/thea-ia:${GITHUB_SHA}
### 2️⃣ Nueva Task Definition

json
{
 "family":"thea-ia",
 "containerDefinitions":[{
  "name":"thea-ia",
  "image":"${AWS_ECR}/thea-ia:${GITHUB_SHA}",
  "portMappings":[{"containerPort":8000}],
  "essential":true,
  "logConfiguration":{
   "logDriver":"awslogs",
   "options":{"awslogs-group":"/ecs/thea-ia","awslogs-region":"eu-west-1","awslogs-stream-prefix":"ecs"}
  }
 }]
}
### 3️⃣ Service Update

bash
aws ecs update-service --cluster thea-cluster --service thea-ia --force-new-deployment
### 4️⃣ Autoscaling

bash
aws application-autoscaling register-scalable-target \
 --resource-id service/thea-cluster/thea-ia \
 --scalable-dimension ecs:service:DesiredCount \
 --min-capacity 3 --max-capacity 10
🧱 Despliegue en Kubernetes (EKS)
Archivo deployment/k8s/thea-ia.yaml:

text
apiVersion: apps/v1
kind: Deployment
metadata:
  name: thea-ia
spec:
  replicas: 3
  selector:
    matchLabels:
      app: thea-ia
  template:
    metadata:
      labels:
        app: thea-ia
    spec:
      containers:
        - name: thea-ia
          image: registry.theaia.com/thea-ia:latest
          ports:
            - containerPort: 8000
          envFrom:
            - secretRef:
                name: thea-env
---
apiVersion: v1
kind: Service
metadata:
  name: thea-ia-service
spec:
  type: LoadBalancer
  ports:
    - port: 80
      targetPort: 8000
  selector:
    app: thea-ia
🔄 Rollback Automatizado
Railway

bash
railway revert --service thea-ia --to previous
AWS ECS

bash
aws ecs update-service --cluster thea-cluster --service thea-ia --force-new-deployment
Kubernetes

bash
kubectl rollout undo deployment/thea-ia --to-revision=previous
🧠 Política de Despliegue Segura
 Tipo 	 Medida 
 Build controlado 	 Firmas SHA‑256 con cosign. 
 Rollback 	 90 segundos máximo recovery. 
 LoadBalancer 	 AWS Elastic o Railway router TLS. 
 Scaling mínimo 	 3 réplicas / 2 workers por instancia. 
 Backup code 	 Difusión 24 h (S3 bucket cruzado). 
 Network segura 	 VPC privada con Security Groups. 
🩺 Validación Post Despliegue
1️⃣ Verificar endpoint /health.
2️⃣ Comprobar métricas /metrics.
3️⃣ Ejecutar test de estado FSM: pytest -m fsm_integration.
4️⃣ Reiniciar servicio lento vía CLI.
5️⃣ Registrar build en deployment/logs/releases.log.

📋 Despliegue Enterprise Checklist
 Requisito 	 Estado 
 Pipeline CI/CD GitHub Actions 	 ✅ Activo 
 Firmado de imagen Docker 	 ✅ Cosign 
 Retención 90 días logs 	 ✅ Loki 
 Monitoreo Prometheus 	 ✅ Integrado 
 Alerta Crit. 500s 	 ✅ Active 
 Rollback en Railway 	 ✅ Validado 
© 2025 Thea IA Systems S.L. — Departamento DevOps / Infraestructura

text

---

Este documento consolida el flujo de **despliegue integral**, abarcando Railway, AWS ECS y Kubernetes, con rollback, monitoreo y seguridad incluidos.

¿Quieres que añadamos ahora el **README interno de DevOps** (guía rápida ci/cd + comandos de infraestructura para el equipo técnico)?