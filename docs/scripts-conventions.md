# Scripts Conventions - THEA-IA

## Bash Scripts
- Formato: erb_noun.sh
- Estructura: Header con propósito, uso, versión
- Error handling: set -euo pipefail
- Permisos: 755

## Python Scripts  
- Formato: erb_noun.py
- Estructura: Docstring, argparse, __version__
- Entry point: if __name__ == "__main__"

## Versionado
- Variable VERSION en cada script
- Bump patch version con cambios

## Run Scripts (Planeado P1)
- Unificar un_* en script central
- Estado: EN PLANIFICACIÓN

---
Creado: 2026-01-06 | Refs: 04_audit_scripts/04_SCRIPTS.md
