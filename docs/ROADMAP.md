## 🛣️ Roadmap de desarrollo

### Fase 1 – Fundamentos  
| Tarea                                        | Estado        | Estimación |
|----------------------------------------------|---------------|------------|
| Carpeta y archivos de configuración base     | ✅ Completada  | 0.5 días   |
| Entorno local y scripts de setup             | ✅ Completada  | 0.5 días   |
| Convenciones de código (PEP8, Black)         | ✅ Completada  | 1 día      |

## ---Fase 2 – Core (FSM & Context)  
## Punto actual: ~80% completado  

Tarea                                                          | Estado           | Estimación   | Duración Real | Fecha/Hora de Finalización  
---------------------------------------------------------------+------------------+--------------+---------------+----------------------------  
Integrar router en adaptadores                                 | ✅ Completada     | 1 día        | 2h            | 07/10/2025 - 15:00          
Conectar intent_detector al router                             | ✅ Completada     | 2 días       | 3h            | 08/10/2025 - 18:30          
Conectar entity_extractor al router                            | ✅ Completada     | 1 día        | 1h            | 08/10/2025 - 19:30          
Persistir contexto de usuario (DB/Redis)                       | ✅ Completada     | 1 día        | 1.5h          | 09/10/2025 - 14:30          
Diseño/estandarización subagentes (handler.py, vocab, test)    | ✅ Completada     | 0.5 días     | 1h            | 09/10/2025 - 16:00          
Refactorización/alineación de subagentes existentes            | ✅ Completada     | 0.5 días     | 1h            | 09/10/2025 - 16:30          
Implementación 7 agentes (agenda, scheduler, event, note, ...) | ✅ Completada     | 1 día        | 2h            | 09/10/2025 - 17:15          
Adaptación de vocab.json para cada agente                      | ✅ Completada     | 0.5 días     | 0.5h          | 09/10/2025 - 17:20          
Implementación de tests unitarios para cada agente             | ✅ Completada     | 0.5 días     | 1h            | 09/10/2025 - 17:20          
Actualización de imports y registry (paquete raíz “theaia”)    | ✅ Completada     | 0.5 días     | 0.5h          | 09/10/2025 - 19:30          
Generación de reporte automatizado de cobertura (pytest-cov)   | ✅ Completada     | 0.5 días     | 0.25h         | 09/10/2025 - 19:40          
Documentación y actualización README (test unitarios/cobertura)| ✅ Completada     | 0.25 días    | 0.25h         | 09/10/2025 - 19:45          
Roadmap y checklist actualizado                                  | ✅ Completada     | 0.1 días     | 0.1h          | 09/10/2025 - 20:38          

Pruebas end-to-end (flujos sintéticos y reales)                | ⬜ Pendiente      | 3 días       | -             | -                          
Validación arquitectural (diagramas UML, análisis estático)    | ⬜ Pendiente      | 2 días       | -             | -                          
Reforzar registry.py: Validación de INTENT único               | ⬜ Pendiente      | 1 día        | -             | -                          
Reforzar registry.py: Ranking de intenciones y umbral          | ⬜ Pendiente      | 1 día        | -             | -                          
Reforzar registry.py: Fallback dinámico y logging              | ⬜ Pendiente      | 1 día        | -             | -                          
Reforzar registry.py: Hot-reload de agentes                    | ⬜ Pendiente      | 1 día        | -             | -                          
Reforzar registry.py: Métricas de despacho y alertas           | ⬜ Pendiente      | 1 día        | -             | -

### 🤖 Fase 2.5 – TheaScaler Agent (Escalador de Desarrollo)  
**⭐ ACTIVACIÓN: Inmediatamente después de completar Fase 2**  
| Tarea                                                                                  | Estado         | Estimación |
|----------------------------------------------------------------------------------------|----------------|------------|
| **Análisis Repository:** Auditoría completa del estado actual vs roadmap               | ⬜ Planificada  | 1 día      |
| **GitHub API Integration:** Conexión con repositorio para lectura/escritura           | ⬜ Planificada  | 1 día      |
| **Code Generation Engine:** Motor de generación de código inteligente                 | ⬜ Planificada  | 2 días     |
| **Automated Commits/PRs:** Sistema de commits y pull requests automáticos             | ⬜ Planificada  | 1 día      |
| **Progress Tracking:** Dashboard de progreso tiempo real                              | ⬜ Planificada  | 1 día      |
| **Quality Gates:** Validación automática antes de commits                             | ⬜ Planificada  | 1 día      |
| **Integration Testing:** Pruebas de integración del agente con el proyecto            | ⬜ Planificada  | 1 día      |

---

### Fase 3 – Adaptadores **🚀 ACELERADA POR THEASCALER**  
| Tarea                                      | Estado        | Estimación | Con TS  |
|--------------------------------------------|---------------|------------|---------|
| Telegram adapter: integración con router   | ⬜ Planificada  | 1 día      | 0.5 días |
| Webhook handler: integración con router    | ⬜ Planificada  | 1 día      | 0.5 días |
| Validar payloads con Pydantic              | ⬜ Planificada  | 1 día      | 0.5 días |
| Agent Validation (Dialogflow CX)           | ⬜ Planificada  | 1 día      | 0.5 días |
| Pruebas de integración canal ↔ Core        | ⬜ Planificada  | 1 día      | 0.5 días |

---

### Fase 4 – Services (Lógica de negocio) **🚀 ACELERADA POR THEASCALER**  
| Tarea                                    | Estado        | Estimación | Con TS  |
|------------------------------------------|---------------|------------|---------|
| event_service, note_service, scheduler_service | ⬜ Planificada  | 2 días     | 1 día    |
| Validar inputs/outputs con Pydantic      | ⬜ Planificada  | 1 día      | 0.5 días |
| Tests unitarios con mocks de repositorios | ⬜ Planificada  | 2 días     | 1 día    |
| Pruebas de regresión de lógica de negocio | ⬜ Planificada  | 1 día      | 0.5 días |

---

### Fase 5 – Persistencia (Base de datos) **🚀 ACELERADA POR THEASCALER**  
| Tarea                                            | Estado        | Estimación | Con TS  |
|--------------------------------------------------|---------------|------------|---------|
| Modelos SQLAlchemy y migraciones Alembic         | ⬜ Planificada  | 1 día      | 0.5 días |
| Validación de integridad relacional y constraints | ⬜ Planificada  | 1 día      | 0.5 días |
| Pruebas de migraciones en staging                | ⬜ Planificada  | 2 días     | 1 día    |

---

### Fase 6 – ML/NLP (Core & Agentes) **🚀 ACELERADA POR THEASCALER**  
| Tarea                                                       | Estado        | Estimación | Con TS  |
|-------------------------------------------------------------|---------------|------------|---------|
| Estructura ml/intent_detector y ml/ner_extractor            | ⬜ Planificada  | 1 día      | 0.5 días |
| Entrenamiento spaCy v3 (TextCategorizer + EntityRuler)      | ⬜ Planificada  | 2 días     | 1.5 días |
| fastText como alternativa ligera                            | ⬜ Planificada  | 1 día      | 0.5 días |
| Integración Transformer + AdapterHub para embeddings         | ⬜ Planificada  | 2 días     | 1.5 días |
| Métodos ABMS: muestreo de sesiones y validación empírica    | ⬜ Planificada  | 2 días     | 1.5 días |
| Pruebas de precisión, recall y latencia                     | ⬜ Planificada  | 1 día      | 0.5 días |

---

### Fase 7 – API (Endpoints) **🚀 ACELERADA POR THEASCALER**  
| Tarea                             | Estado        | Estimación | Con TS  |
|-----------------------------------|---------------|------------|---------|
| Implementar /health y /metrics    | ⬜ Planificada  | 1 día      | 0.5 días |
| Documentación OpenAPI y validación de esquemas | ⬜ Planificada | 1 día      | 0.5 días |
| Pruebas de contrato (mock server) | ⬜ Planificada  | 1 día      | 0.5 días |

---

### Fase 8 – Testing (Calidad) **🚀 ACELERADA POR THEASCALER**  
| Tarea                                                           | Estado        | Estimación | Con TS  |
|-----------------------------------------------------------------|---------------|------------|---------|
| Unit tests (core, agents, services)                             | ⬜ Planificada  | 2 días     | 1 día    |
| Integration/E2E tests                                           | ⬜ Planificada  | 2 días     | 1 día    |
| Pruebas de estrés y carga                                       | ⬜ Planificada  | 1 día      | 0.5 días |
| Human-in-the-Loop: revisión manual de fallos de baja confianza  | ⬜ Planificada  | 1 día      | 1 día    |

---

### Fase 9 – Infraestructura (Despliegue) **🚀 ACELERADA POR THEASCALER**  
| Tarea                                      | Estado        | Estimación | Con TS  |
|--------------------------------------------|---------------|------------|---------|
| Dockerización y multi-stage builds         | ⬜ Planificada  | 1 día      | 0.5 días |
| Kubernetes manifests y HPA/VPA             | ⬜ Planificada  | 1 día      | 0.5 días |
| CI/CD (GitHub Actions)                     | ⬜ Planificada  | 1 día      | 0.5 días |
| Monitorización Prometheus/Grafana          | ⬜ Planificada  | 1 día      | 0.5 días |
| Validar políticas de autoscaling en staging | ⬜ Planificada  | 1 día      | 0.5 días |

---

### Fase 10 – Documentación (Docs finales) **🚀 ACELERADA POR THEASCALER**  
| Tarea                                             | Estado        | Estimación | Con TS  |
|---------------------------------------------------|---------------|------------|---------|
| Diagramas detallados (ARCHITECTURE.md)            | ⬜ Planificada  | 1 día      | 0.5 días |
| ADRs para decisiones críticas                     | ⬜ Planificada  | 1 día      | 0.5 días |
| Guía de despliegue y playbooks DR                 | ⬜ Planificada  | 1 día      | 0.5 días |
| Changelog diario en `docs/README-diario.md`       | ⬜ Planificada  | 1 día      | 0.5 días |

---

### Fase 11 – MLOps (Operaciones & ML Pipelines) **🚀 ACELERADA POR THEASCALER**  
| Tarea                                      | Estado        | Estimación | Con TS  |
|--------------------------------------------|---------------|------------|---------|
| Pipeline ML automatizado (CI/CD GPU)       | ⬜ Planificada  | 1 día      | 0.5 días |
| Versionado de artefactos (MLflow/S3)       | ⬜ Planificada  | 1 día      | 0.5 días |
| Drift detection y alertas de degradación   | ⬜ Planificada  | 1 día      | 0.5 días |
| Rollback y pruebas de rollback             | ⬜ Planificada  | 2 días     | 1 día    |

---

### 🧠 Fase 12 – Self-Evolution Core (Auto-mejora Integrada)  
| Tarea                                      | Estado        | Estimación |
|--------------------------------------------|---------------|------------|
| Performance Monitor                        | ⬜ Planificada  | 1 día      |
| Feedback Loop System                       | ⬜ Planificada  | 2 días     |
| Meta-learning Engine                       | ⬜ Planificada  | 2 días     |
| Dynamic Code Modification                  | ⬜ Planificada  | 2 días     |
| Self-updating Mechanisms                   | ⬜ Planificada  | 1 día      |
| Safety Constraints                         | ⬜ Planificada  | 1 día      |
| Rollback Capabilities                      | ⬜ Planificada  | 1 día      |

---

### 🌐 Fase 13 – Agent Ecosystem (Ecosistema de Agentes)  
| Tarea                                      | Estado        | Estimación |
|--------------------------------------------|---------------|------------|
| Individual Agent Evolution                 | ⬜ Planificada  | 2 días     |
| Cross-agent Learning                       | ⬜ Planificada  | 2 días     |
| Collaborative Improvement                  | ⬜ Planificada  | 1 día      |
| Ecosystem Orchestration                    | ⬜ Planificada  | 2 días     |
| Knowledge Sharing Protocol                 | ⬜ Planificada  | 1 día      |
| Distributed Learning                       | ⬜ Planificada  | 2 días     |
| Emergence Detection                        | ⬜ Planificada  | 1 día      |

---

## 📊 Cronograma optimizado  
- **Duración total sin TheaScaler:** 8–10 semanas  
- **Duración total con TheaScaler:** 6–7 semanas  
- **Ahorro de tiempo:** 30-40%

---

🚀 **Resultado final:** Thea IA 2.0 completamente funcional, auto-escalable y con capacidades de mejora continua en **6-7 semanas**.  
