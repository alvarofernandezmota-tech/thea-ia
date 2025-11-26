# ScheduleAgent - DEPRECATED

**Fecha deprecación:** 26 Noviembre 2025, 15:42 CET
**Razón:** Funcionalidad mergeada a AgendaAgent NIVEL 3

## ¿Por qué se eliminó?
ScheduleAgent era redundante con AgendaAgent NIVEL 3:
- Optimización de horarios → AgendaAgent NIVEL 3 (LLM)
- Sugerencias de scheduling → AgendaAgent NIVEL 3
- Detección de conflictos → AgendaAgent NIVEL 3

## Migración
Todo el código de optimización ahora está en:
- `src/theaia/agents/agenda_agent/` (NIVEL 3)

## Código archivado
- Ubicación: `.archive/schedule_agent/`
- Fecha: 26 Noviembre 2025
- Archivos: handler.py, schedule_conversation_manager.py, model/, tests/

## Referencias
- Roadmap H04-H05: FASE 1.2
- Decisión arquitectónica: 25 NOV 2025 (diary)
- Commit: [Se actualizará con hash]
