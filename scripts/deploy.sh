#!/bin/bash
# ==============================================
# THEA IA 2.0 – DEPLOY A STAGING/PRODUCCIÓN
# ==============================================

set -e

echo "🚀 Construyendo imagen Docker..."
docker build -t theaia-app:latest .

echo "🐳 Subiendo imagen a registro (ajusta nombre de repositorio)…"
docker tag theaia-app:latest registry.example.com/theaia-app:latest
docker push registry.example.com/theaia-app:latest

echo "✅ Imagen desplegada en registry.example.com/theaia-app:latest"
