# 🧠 Thea IA 3.0 Enterprise Edition

Bienvenido a la documentación oficial de **Thea IA 3.0**, la plataforma de inteligencia artificial empresarial creada por **Thea IA Systems S.L.**  
Diseñada para entornos corporativos que requieren seguridad, automatización y gestión inteligente de contextos conversacionales.

---

## 🌐 Visión General

**Thea IA 3.0 Enterprise** es un ecosistema modular basado en:
- Arquitectura asíncrona con **FSM Engine v2**.  
- Agentes independientes para gestión de agenda, notas, y hábitos.  
- Núcleo **CoreRouter** orquestado por **FastAPI + SQLAlchemy async**.  
- Persistencia segura de contexto y memoria long term.  

---

## 🚀 Componentes Principales

| Módulo | Descripción |
|---------|--------------|
| **Core Router / FSM** | Motor de estados finito para agentes contextuales. |
| **Agentes inteligentes** | Agenda, Notas, Eventos y Contexto. |
| **Persistencia Contextual** | SQLite / PostgreSQL con migraciones Alembic. |
| **API REST & Webhooks** | Endpoints según estándar OpenAPI 3.1. |
| **Monitorización Avanzada** | Prometheus + Grafana + Loki. |
| **Seguridad GDPR / SOC 2** | Cifrado TLS 1.3 y gestión AES‑256. |

---

## 📘 Documentos Principales

1. [Arquitectura General](architecture.md)  
2. [Referencia API REST](api_reference.md)  
3. [Monitorización Empresarial](monitoring_enterprise.md)  
4. [Despliegue y CI/CD](deployment_enterprise.md)  
5. [Seguridad Corporativa](security_enterprise.md)  
6. [Guía DevOps](devops_readme.md)  
7. [Cumplimiento Legal](legal_compliance.md)  
8. [Roadmap Tecnológico](roadmap_enterprise.md)  
9. [Directorio de Equipo](team_directory.md)  
10. [Onboarding Técnico](training_onboarding.md)  

---

## 💼 Datos de la Compañía

**Thea IA Systems S.L.**  
N.I.F. B‑728 XXXX  
Sede Central: Madrid, España  
Teléfono: +34 676 XXX XXX  
Correo: [contact@theaia.com](mailto:contact@theaia.com)

---

## 🔒 Licencia y Derechos

© 2025 Thea IA Systems S.L. Todos los derechos reservados.  
Reproducción o distribución no autorizada prohibida bajo leyes internacionales de propiedad intelectual.

---

## ⚙️ Acceso Rápido

# Iniciar servidor de desarrollo de documentación
mkdocs serve

text

Visualiza el portal: [http://localhost:8000](http://localhost:8000) → sección centralizada de documentos Thea IA Enterprise.
Estructura final esperada
text
/workspaces/thea-ia/
│
├── mkdocs.yml
├── docs/
│   ├── index.md              ← Página principal del portal
│   ├── architecture.md
│   ├── api_reference.md
│   ├── monitoring_enterprise.md
│   ├── deployment_enterprise.md
│   ├── security_enterprise.md
│   ├── devops_readme.md
│   ├── legal_compliance.md
│   ├── roadmap_enterprise.md
│   ├── team_directory.md
│   ├── training_onboarding.md
│   └── SUMMARY.md
Una vez agregues index.md, bastará con ejecutar:

bash
pip install mkdocs-material
mkdocs serve
para abrir el portal corporativo “Thea IA Docs” localmente antes de publicarlo en docs.theaia.com.