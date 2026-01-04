# 📦 INSTRUCCIÓN: Mover Archivos de /src/core/agents/ a /src/theaia/

**Fecha:** 04 Enero 2026 16:45 CET  
**Prioridad:** 🔴 ALTA - EJECUTAR ANTES DE CONTINUAR AUDITORÍA

---

## 🎯 Objetivo

Mover los archivos `lifecycle.py`, `metadata.py`, `registry.py` desde `/src/core/agents/` a `/src/theaia/` donde deben estar ubicados correctamente.

---

## 📝 Comandos para Ejecutar

### Opción 1: Ejecutar Localmente (RECOMENDADO)

```bash
# 1. Asegúrate de estar en la raíz del proyecto
cd ~/thea-ia

# 2. Verificar que git está limpio
git status

# 3. Mover archivos con git mv (preserva historial)
git mv src/core/agents/lifecycle.py src/theaia/
git mv src/core/agents/metadata.py src/theaia/
git mv src/core/agents/registry.py src/theaia/

# 4. Verificar que el __init__.py de src/core/agents/ no tiene contenido importante
cat src/core/agents/__init__.py

# 5. Si está vacío o solo tiene imports básicos, eliminar todo el directorio
git rm -r src/core/

# 6. Commit
git commit -m "refactor(structure): Move core agent files to correct location

- Moved lifecycle.py, metadata.py, registry.py from src/core/agents/ to src/theaia/
- Removed empty src/core/ directory
- These files belong in the main theaia package, not in a separate core folder
- Detected during audit_diciembre_2025"

# 7. Push
git push origin main
```

### Opción 2: Script Automático

Guardar como `mover_archivos.sh` y ejecutar con `bash mover_archivos.sh`:

```bash
#!/bin/bash

echo "📦 Moviendo archivos de src/core/agents/ a src/theaia/..."

# Verificar que estamos en la raíz del proyecto
if [ ! -d "src/theaia" ]; then
    echo "❌ Error: No se encuentra src/theaia/. ¿Estás en la raíz del proyecto?"
    exit 1
fi

if [ ! -d "src/core/agents" ]; then
    echo "❌ Error: No se encuentra src/core/agents/"
    exit 1
fi

echo "✅ Directorios encontrados"

# Mover archivos
echo "📦 Moviendo lifecycle.py..."
git mv src/core/agents/lifecycle.py src/theaia/

echo "📦 Moviendo metadata.py..."
git mv src/core/agents/metadata.py src/theaia/

echo "📦 Moviendo registry.py..."
git mv src/core/agents/registry.py src/theaia/

# Verificar contenido de __init__.py
echo "🔍 Revisando __init__.py..."
cat src/core/agents/__init__.py

echo ""
echo "⚠️ ¿El __init__.py mostrado arriba está vacío o solo tiene imports simples?"
echo "Si es así, ejecuta: git rm -r src/core/"
echo ""
echo "✅ Archivos movidos exitosamente!"
echo "📄 Ahora ejecuta:"
echo "   git commit -m 'refactor(structure): Move core agent files to correct location'"
echo "   git push origin main"
```

---

## ✅ Verificación

Después de ejecutar los comandos, verificar:

```bash
# 1. Los archivos están en src/theaia/
ls -la src/theaia/ | grep -E '(lifecycle|metadata|registry)'

# 2. El directorio src/core/ no existe o está vacío
ls src/core/ 2>/dev/null || echo "Directorio eliminado correctamente"

# 3. Git muestra los cambios como renombrados (no como eliminación + creación)
git status
```

**Resultado esperado:**
```
renamed:    src/core/agents/lifecycle.py -> src/theaia/lifecycle.py
renamed:    src/core/agents/metadata.py -> src/theaia/metadata.py
renamed:    src/core/agents/registry.py -> src/theaia/registry.py
deleted:    src/core/
```

---

## 📝 Notas Importantes

1. **Usar `git mv`** - Esto preserva el historial de Git de los archivos
2. **NO copiar y pegar manualmente** - Se perdería el historial
3. **Verificar imports** - Después del movimiento, asegurarse de que no hay imports rotos
4. **Los archivos NO son obsoletos** - Son código reciente (3 semanas) y válido

---

**✅ Ejecutar AHORA antes de continuar con las auditorías**
