# ROADMAP — THEA IA (Raíz)

**Proyecto:** THEA IA  
**Actualizado por:** Álvaro Fernández Mota (CEO THEA IA)  
**Última actualización:** 2025-10-31 01:14 CET

---

> **IMPORTANTE**
>
> - El roadmap general orquesta los **17 hitos grandes** y todos los micro-hitos del ecosistema THEA IA.
> - Cada área/carpeta tiene su propio roadmap y guía extendida, enlazada desde aquí para panel de auditoría y equipo.
> - Debe mantenerse actualizado por cada responsable y reflejar estado, porcentaje completado, dependencias y fechas clave.

---

## 🟩 Hitos principales (17)

1. **H01: Organización y compatibilidad de tests, core y ecosistema** ✅ **COMPLETADO**
   - Estructura carpetas, tests unitarios/integración/e2e, FSM base, pytest
   - README/ROADMAP/CHANGELOG por carpeta
   - Tests pasan 100%, coverage ≥80%
   - **Completado:** 2025-10-31

2. **H02: Adapter Telegram y Web (multi-canal integrador)** 🔄 **EN CURSO**
   - Telegram Bot API, webhooks, polling
   - REST API Web adapter, FastAPI/Flask
   - Tests e2e por canal
   - **Deadline estimado:** 2025-11-10

3. **H03: FSM Orquestación, manager universal y contexto multiusuario** ⏳ **PRÓXIMO**
   - FSM transiciones complejas, manager centralizado
   - Contexto persistente por usuario/sesión
   - Tests de flujo multi-turno
   - **Deadline:** 2025-11-15

4. **H04: Persistencia, base de datos y auditoría avanzada**
   - PostgreSQL, migraciones, fallback SQLite
   - Logs auditoría, compliance GDPR
   - **Deadline:** 2025-11-25

5. **H05: Agentes verticales (agenda, notas, eventos, ayuda, fallback, etc)**
   - Implementación completa de handlers
   - Tests unitarios por agente
   - **Deadline:** 2025-12-01

6. **H06: Pipelines de intent ML y extracción de entidades**
   - Modelos spacy, intent classifier, entity extractor
   - Tests de confianza y accuracy
   - **Deadline:** 2025-12-10

7. **H07: E2E Tests y coverage automatizado, checklist QA**
   - Coverage ≥85% global
   - Tests e2e FSM, adapters, agentes
   - Checklist de auditoría
   - **Deadline:** 2025-12-15

8. **H08: Arquitectura multi-empresa y control granular de roles**
   - RBAC, tenant isolation
   - Auditoría por tenant
   - **Deadline:** 2026-01-10

9. **H09: Dockerización, despliegue cloud/K8s, CI/CD auditado**
   - Dockerfile, docker-compose, K8s manifests
   - CI/CD pipeline (GitHub Actions, GitLab CI)
   - **Deadline:** 2026-01-20

10. **H10: Adaptadores WhatsApp, API REST y futuros canales**
    - WhatsApp Business API adapter
    - API REST pública documentada
    - **Deadline:** 2026-02-01

11. **H11: Observabilidad, logging avanzado y panel de métricas**
    - Prometheus, Grafana, Loki
    - Custom dashboards, alertas
    - **Deadline:** 2026-02-15

12. **H12: Integración extendida con recursos externos**
    - Google Calendar, MS Outlook, Slack, etc
    - Webhooks y sincronización
    - **Deadline:** 2026-03-01

13. **H13: Seguridad, gestión de secretos y hardening total**
    - AWS Secrets Manager, Azure KeyVault
    - Auditoría de seguridad profesional
    - Pentesting
    - **Deadline:** 2026-03-15

14. **H14: Onboarding profesional, checklist docs y contribución**
    - Guías de onboarding por rol
    - Documentación viva en docs/
    - **Deadline:** 2026-04-01

15. **H15: Escalabilidad, performance y stress-tests integrados**
    - Load testing, benchmarking
    - Optimización de queries y cache
    - **Deadline:** 2026-04-20

16. **H16: Customizaciones de cliente y plugin integrations**
    - Sistema de plugins
    - Custom agents por cliente
    - **Deadline:** 2026-05-10

17. **H17: Revisión y auditoría final para release público/enterprise**
    - Auditoría técnica final
    - Compliance checklist
    - Go-live producción
    - **Deadline:** 2026-06-01

---

## 📅 Fases y fechas críticas (Actualizado 2025-10-31)

- **Fase 1: Core y FSM** — ✅ **COMPLETADA** (2025-10-31)
  - H01: Tests, core, FSM, documentación raíz
  
- **Fase 2: Multi-agente y adaptadores** — 🔄 **EN CURSO** (2025-11-01 ~ 2025-12-15)
  - H02: Telegram/Web
  - H03: FSM avanzado
  - H04: Persistencia
  - H05: Agentes
  - H06: ML
  - H07: E2E Tests
  
- **Fase 3: Infraestructura, observabilidad y seguridad** — ⏳ **PRÓXIMA** (2025-12-16 ~ 2026-04-01)
  - H08: Multi-empresa
  - H09: Docker/K8s
  - H10: Nuevos adapters
  - H11: Observabilidad
  - H12: Integraciones
  - H13: Seguridad
  - H14: Onboarding
  
- **Fase 4: Escalabilidad, customización y release** — ⏳ **FUTURA** (2026-04-01 ~ 2026-06-01)
  - H15: Performance
  - H16: Plugins
  - H17: Auditoría final y go-live

---

## 🛡️ Auditoría y panel de equipo

- Todos los hitos y cambios están reflejados en el CHANGELOG general y por carpeta.
- Checklist de auditoría extendida en `/docs/audit_checklist.md` y docs/roadmap de cada área.
- Panel de avance y dependencias aquí y en cada README/roadmap.
- **Próxima sesión:** README/ROADMAP/CHANGELOG por carpeta (core, agents, adapters, tests, ml, docs)

---

**Mantén este roadmap vivo.  
Actualízalo tras cada release de hito/versión, micro-hito importante o cambio estructural.  
Así, todas las auditorías y equipos de THEA IA tienen acceso inmediato a la planificación y estado real del ecosistema.**

> Última actualización: 2025-10-31 01:14 CET · Álvaro Fernández Mota (CEO THEA IA)
