#!/bin/bash
# backup.sh: Realiza copia de seguridad de la base de datos principal

BACKUP_DIR="backups"
DB_URL=${DATABASE_URL:-"postgresql://user:pass@localhost:5432/theaia_db"}
TS=$(date +"%Y%m%d_%H%M%S")

mkdir -p "$BACKUP_DIR"
pg_dump "$DB_URL" > "$BACKUP_DIR/theaia_db_${TS}.sql"

if [ $? -eq 0 ]; then
  echo "✅ Backup completado: $BACKUP_DIR/theaia_db_${TS}.sql"
else
  echo "❌ Fallo en el backup de la BD"
  exit 1
fi
