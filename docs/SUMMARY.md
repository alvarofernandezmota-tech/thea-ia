📚 Índice de Documentación – Thea IA 3.0 Enterprise
Este índice organiza todos los documentos internos de Thea IA Systems S.L., agrupándolos por dominio técnico, operaciones, seguridad y despliegue.

🧠 1. Arquitectura y Ecosistema
 Archivo 	 Descripción 
 architecture.md 	 Diseño arquitectónico completo (Core FSM, Agentes, Contextos, Pipelines). 
 api_reference.md 	 Documentación REST & FastAPI para integraciones. 
 monitoring_enterprise.md 	 Monitoreo empresarial Prometheus + Grafana + Loki. 
 deployment_enterprise.md 	 Despliegue en Railway / AWS ECS / EKS. 
 security_enterprise.md 	 Normas de seguridad SOC2 + GDPR y cifrado corporativo. 
 devops_readme.md 	 Guía DevOps interna – CI/CD + operaciones 24/7. 
🧩 2. Entorno y Configuración
 Archivo 	 Propósito 
 ../.env.example 	 Variables base de entorno Enterprise (Prod/Staging). 
 scripts/setup_env.sh 	 Script automatizado de inicialización y test. 
 scripts/migrate.sh 	 Migraciones DB Alembic. 
 scripts/revert.sh 	 Rollback automático ante fallo CI/CD. 
🚀 3. Integración y Ciclo de Vida CI/CD
 Elemento 	 Ubicación 
 Pipeline CI/CD ( GitHub Actions ) 	 .github/workflows/thea_ci.yml 
 Dockerfile Optimizado 	 /Dockerfile.optimized 
 Docker Registry Privado 	 registry.theaia.com 
 Railway Service Config 	 railway.json (opcional) 
☁️ 4. Infraestructura Cloud Thea IA
- Railway Cloud → entorno principal Europe (Frankfurt).
- AWS ECS → nodos “thea‑core‑cluster”.
- EKS → módulo FSM/Agents auto‑escalable.
- S3 → modelos y backups.
- Prometheus + Grafana → 24/7 monitorización.

🔐 5. Compliance y Auditoría Interna
 Política 	 Área 
 Reglamento GDPR (EU 2016/679) 	 Protección de usuarios y data contextual. 
 SOC 2 Type II 	 Seguridad, Disponibilidad y Confidencialidad. 
 ISO 27001 	 Gestión de seguridad de la información. 
 TLS1.3 + AES256 	 Cifrado integral de tráfico y persistencia. 
🧱 6. Estructura Global de Documentación
text
docs/
├── architecture.md
├── api_reference.md
├── monitoring_enterprise.md
├── deployment_enterprise.md
├── security_enterprise.md
├── devops_readme.md
└── SUMMARY.md
🧾 7. Versionado Documental
 Versión 	 Fecha 	 Autor 	 Descripción 
 3.0.0 	 Oct‑2025 	 Dept. Arquitectura 	 Versión completa Enterprise. 
 3.0.1 	 Pendiente 	 Dept. Legal 	 Anexo Contratos SaaS. 
📩 Contacto Interno
- Infraestructura: infra@theaia.com
- Seguridad: security@theaia.com
- Soporte Técnico: support@theaia.com
- CISO: alvaro.fernandez@theaia.com

© 2025 Thea IA Systems S.L. — Manual de Referencia Interno

text

---

Con este archivo ya cierras el módulo **Thea IA Enterprise Docs Suite**, ideal para entregar a stakeholders e integrarlo en tu portal de documentación técnica.

¿Quieres que te genere ahora el **portal web estático (mkdocs / docsify)** preparado para publicar esta documentación interna en un subdominio (por ejemplo docs.theaia.com)?