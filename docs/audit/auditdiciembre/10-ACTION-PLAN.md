# 💫 PLAN DE ACCIÓN PRIORIZADO - THEA IA

**Fecha:** 21 Diciembre 2025  
**Objetivo:** Roadmap de implementación para inversión  
**Responsable:** Álvaro Fernández Mota

---

## 🔴 CRÍTICO (Hoy - 2-3 horas)

### 1. Security Fix: Remove .env
**Estimación:** 15 min  
**Impacto:** ALTO
```bash
git rm --cached .env
# Revocar: Telegram token, Groq API key, DB credentials
git commit -m "security: Remove exposed .env"
```

### 2. Move Scripts to scripts/
**Estimación:** 30 min  
**Impacto:** MEDIO
```bash
git mv run_*.py scripts/
git mv run_*.sh scripts/
```

### 3. Remove Cache Directories
**Estimación:** 20 min  
**Impacto:** ALTO
```bash
git rm -r --cached __pycache__ .pytest_cache htmlcov venv
```

### 4. Create LICENSE
**Estimación:** 10 min  
**Impacto:** ALTO (investors require)

### 5. Create GETTING_STARTED.md
**Estimación:** 45 min  
**Impacto:** ALTO

### 6. Create ARCHITECTURE.md
**Estimación:** 1 hour  
**Impacto:** ALTO

### 7. Improve .gitignore
**Estimación:** 15 min  
**Impacto:** MEDIO

---

## 🟡 IMPORTANTE (Esta semana - 4-5 horas)

### 8. Create API_DOCUMENTATION.md
**Estimación:** 1.5 hours  
**Impacto:** MEDIO

### 9. Create DEPLOYMENT_GUIDE.md
**Estimación:** 1 hour  
**Impacto:** MEDIO

### 10. Create CODE_OF_CONDUCT.md
**Estimación:** 30 min  
**Impacto:** BAJO

### 11. Move test_groq_manual.py
**Estimación:** 15 min  
**Impacto:** BAJO

### 12. Document Dockerfiles
**Estimación:** 30 min  
**Impacto:** MEDIO

---

## 🟢 MEDIA (Antes de pitch - 3-4 horas)

### 13. Improve Test Coverage
**Estimación:** 2 hours  
**Target:** >85% coverage

### 14. Performance Benchmarks
**Estimación:** 1 hour

### 15. Setup GitHub Security
**Estimación:** 30 min  
**Actions:** Enable Dependabot, code scanning

---

## 📊 TIMELINE

```
Hoy (21 Dic)
├─ 09:00-11:00: CRÍTICO (#1-7)
├─ 11:00-12:00: Break
└─ 12:00-15:00: Continuaremos

Mañana (22 Dic)
├─ IMPORTANTE (#8-12)
└─ Validar cambios

Miércoles (23 Dic)
├─ MEDIA (#13-15)
└─ Pre-pitch review
```

---

## ✅ SUCCESS METRICS

Después de completar acciones:

- [ ] Investment readiness: 6.5 → 8.5
- [ ] Security: No .env in GitHub
- [ ] Docs: 6 documentos críticos creados
- [ ] Tests: >85% coverage
- [ ] Structure: Raíz limpia y organizada
- [ ] Team: Onboarding ready

---

## 📝 CHECKLIST

### Día 1 (21 Dic)
- [ ] Remove .env from git
- [ ] Revocar credenciales
- [ ] Move scripts
- [ ] Remove cache dirs
- [ ] Create LICENSE
- [ ] Improve .gitignore
- [ ] Create GETTING_STARTED.md
- [ ] Create ARCHITECTURE.md

### Día 2 (22 Dic)
- [ ] Create API_DOCUMENTATION.md
- [ ] Create DEPLOYMENT_GUIDE.md
- [ ] Create CODE_OF_CONDUCT.md
- [ ] Move test files
- [ ] Document Dockerfiles

### Día 3 (23 Dic)
- [ ] Improve test coverage
- [ ] Performance benchmarks
- [ ] Setup GitHub security
- [ ] Final validation

---

## 👥 WHO DOES WHAT

**Álvaro (CEO):**
- Security decisions
- Investment readiness
- Strategic direction

**Development Team:**
- Code quality
- Testing
- Documentation

---

**Plan creado:** 21 Diciembre 2025  
**Responsable:** Álvaro Fernández Mota
