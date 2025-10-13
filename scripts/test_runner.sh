#!/bin/bash
# test_runner.sh: Lanza todos los tests del sistema Thea IA 2.0

echo "🚀 Lanzando tests unitarios, integración y e2e..."
pytest tests/ -v --cov=src/theaia --cov-report=html

if [ $? -eq 0 ]; then
  echo "✅ Todos los tests completaron con éxito"
else
  echo "❌ Algunos tests fallaron"
  exit 1
fi
