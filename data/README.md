# Data Directory - THEA-IA

## theaia_db.json
- Primary JSON database for conversational state
- Backup policy: Daily
- Format: JSON with conversations array
- Size typical: 50-500 MB

## Gitignore
- data/*.json - NOT tracked (env-specific)
- data/backups/ - NOT tracked
- data/cache/ - NOT tracked
- data/logs/ - NOT tracked

## Limpieza
- Cache limpieza: Automática 24h (cleanup_audit_dec2025.sh)
- Logs retención: 7 días
- Backups retención: 30 días

---
Documentado: 2026-01-06 | Auditoría: 05_audit_otras_carpetas/05_OTRAS_CARPETAS.md
