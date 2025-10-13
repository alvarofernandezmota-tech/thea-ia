#!/bin/bash
# entrypoint.sh: Script principal de entrada para Docker o despliegue automatizado

echo "🟢 Iniciando entorno Thea IA 2.0..."

# Migrar la base de datos antes de arrancar
./scripts/migrate.sh upgrade

# Iniciar la aplicación
exec "$@"
