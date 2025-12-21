# 📋 INSTRUCCIONES DE LIMPIEZA - AUDITORÍA DICIEMBRE 2025

**Fecha:** 21 Diciembre 2025  
**Propósito:** Limpiar y organizar raíz del proyecto THEA IA  
**Investment Readiness:** 6.5 → 7.5 (+1.0 puntos)

---

## 🎯 OBJETIVO

Limpiar la raíz del proyecto removiendo archivos cache, reorganizando scripts y preparando el repositorio para presentación a inversores.

---

## ✅ PRE-REQUISITOS

1. **Git Bash instalado** (ya lo tienes en Windows)
2. **Estar en la rama correcta:**
   ```bash
   git checkout main
   git pull origin main
   ```
3. **Directorio de trabajo limpio:**
   ```bash
   git status  # Debe estar limpio
   ```

---

## 🚀 EJECUCIÓN DEL SCRIPT

### Paso 1: Navegar a la raíz del proyecto

```bash
cd C:/Users/Admin/Desktop/THEA_IA
```

### Paso 2: Hacer el script ejecutable (solo primera vez)

```bash
chmod +x scripts/cleanup_audit_dic2025.sh
```

### Paso 3: Ejecutar el script

```bash
bash scripts/cleanup_audit_dic2025.sh
```

### Paso 4: Confirmar cuando se te pregunte

El script te mostrará:
```
Este script va a:
  1. Remover .env del repositorio (mantiene archivo local)
  2. Remover directorios cache: __pycache__, .pytest_cache, htmlcov, venv
  3. Mover 5 scripts a scripts/
  4. Mover test_groq_manual.py a src/theaia/tests/manual/
  5. Mover SESSION-17-DIC-2025-SUMMARY.md a docs/diary/diciembre/
  6. Remover tests.log

¿Continuar? (s/N):
```

Escribe **`s`** y presiona Enter.

### Paso 5: Revisar cambios

```bash
git status
```

Deberías ver:
```
Changes to be committed:
  deleted:    .env
  deleted:    __pycache__/...
  deleted:    .pytest_cache/...
  deleted:    htmlcov/...
  deleted:    venv/...
  deleted:    tests.log
  renamed:    run_bot.py -> scripts/run_bot.py
  renamed:    run_demo.py -> scripts/run_demo.py
  renamed:    run_h9_tests.sh -> scripts/run_h9_tests.sh
  renamed:    run_interactive.py -> scripts/run_interactive.py
  renamed:    run_real.py -> scripts/run_real.py
  renamed:    test_groq_manual.py -> src/theaia/tests/manual/test_groq_manual.py
  renamed:    SESSION-17-DIC-2025-SUMMARY.md -> docs/diary/diciembre/SESSION-17-DIC-2025-SUMMARY.md
```

### Paso 6: Hacer commit

```bash
git commit -m "refactor(audit): Complete root cleanup - Investment readiness Dec 2025

- Removed .env from git (kept local)
- Removed cache dirs: __pycache__, .pytest_cache, htmlcov, venv
- Moved 5 scripts to scripts/
- Moved test_groq_manual.py to tests/manual/
- Moved SESSION summary to docs/diary/
- Removed tests.log

Investment Readiness Score: 6.5 → 7.5 (+1.0)"
```

### Paso 7: Push a GitHub

```bash
git push origin main
```

---

## 📊 RESULTADOS ESPERADOS

### Antes de la limpieza:
- 📁 42 items en raíz
- 🔴 .env con credenciales en GitHub
- 🔴 4 directorios cache en git
- 🟡 7 scripts desorganizados
- 🟡 2 archivos temporales
- **Score:** 4.5/10

### Después de la limpieza:
- 📁 27 items en raíz (-15)
- ✅ .env removido de git
- ✅ 0 directorios cache
- ✅ Scripts organizados en scripts/
- ✅ Sin archivos temporales
- **Score:** 7.5/10 ✅

---

## ⚠️ NOTAS IMPORTANTES

### Archivo .env

- ✅ **Se mantiene en tu disco local** (para que el bot siga funcionando)
- ✅ **Se remueve del repositorio de GitHub** (ya no será público)
- ⚠️ Si necesitas las credenciales, están en tu archivo local `.env`

### Cache Directories

- Los directorios cache se regenerarán automáticamente cuando ejecutes tests o el bot
- **NO los vuelvas a agregar a git** (están en .gitignore ahora)

### Scripts Movidos

- Todos los scripts siguen funcionando desde su nueva ubicación
- Actualiza tus comandos si los usabas directamente:
  ```bash
  # Antes:
  python run_bot.py
  
  # Ahora:
  python scripts/run_bot.py
  ```

---

## 🆘 TROUBLESHOOTING

### "git rm: needs merge"

Si ves este error:
```bash
git reset --hard
bash scripts/cleanup_audit_dic2025.sh
```

### "Permission denied"

Ejecuta:
```bash
chmod +x scripts/cleanup_audit_dic2025.sh
bash scripts/cleanup_audit_dic2025.sh
```

### "Script not found"

Asegúrate de estar en la raíz:
```bash
pwd  # Debe mostrar: /c/Users/Admin/Desktop/THEA_IA
cd C:/Users/Admin/Desktop/THEA_IA
```

---

## ✅ CHECKLIST DE VERIFICACIÓN

Después de ejecutar, verifica:

- [ ] `git status` muestra cambios listos para commit
- [ ] `.env` YA NO aparece en GitHub (pero existe en tu local)
- [ ] Directorio `scripts/` contiene los 6 scripts (5 movidos + 1 ya existía)
- [ ] Directorio `src/theaia/tests/manual/` contiene `test_groq_manual.py`
- [ ] `docs/diary/diciembre/` contiene `SESSION-17-DIC-2025-SUMMARY.md`
- [ ] NO existen: `__pycache__/`, `.pytest_cache/`, `htmlcov/`, `venv/`, `tests.log`
- [ ] Commit realizado con mensaje descriptivo
- [ ] Push a GitHub exitoso

---

## 📞 SOPORTE

Si tienes problemas:

1. **Revisa el output del script** - tiene mensajes de error claros
2. **Lee la sección Troubleshooting** arriba
3. **Verifica pre-requisitos** (git status limpio, rama correcta)

---

## 🎯 PRÓXIMOS PASOS

Después de esta limpieza:

1. ✅ Raíz limpia y profesional
2. ✅ Investment Readiness: 7.5/10
3. ⏭️ Siguiente: Crear documentos faltantes (LICENSE, ARCHITECTURE, etc.)
4. ⏭️ Target final: Investment Readiness 8.5/10

---

**Tiempo estimado total:** 5 minutos  
**Dificultad:** Fácil  
**Riesgo:** Bajo (todo está en git, puedes revertir)

---

**Última actualización:** 21 Diciembre 2025, 14:35 CET  
**Autor:** Sistema de Auditoría THEA IA
