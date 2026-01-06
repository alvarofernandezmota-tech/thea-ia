# Config - Sistema de Configuración de THEA IA

**Versión:** v3.0.0  
**Status:** ✅ Production Ready  
**Calificación Auditoría:** 8.4/10 - MUY BUENO  
**Last Updated:** 06 Enero 2026

---

## 🎯 Estado Actual

### ✅ Implementado (H02 - Nov 2025)

- **ConfigManager** - Sistema centralizado de configuración
  - Ubicación: `src/theaia/config/`
  - Status: ✅ Production ready
  - Features: Variables de entorno, validación, carga dinámica

- **Archivos de configuración:**
  - `DEPENDENCIES-config.md` - Dependencias del módulo
  - `STRUCTURE-config.md` - Estructura del sistema
  - `config-CHANGELOG.md` - Historial de cambios
  - `config-README.md` - Documentación técnica interna

### 🔧 Componentes Principales

```python
from theaia.config import ConfigManager

# Cargar configuración
config = ConfigManager()

# Acceder a variables
api_key = config.get("GROQ_API_KEY")
database_url = config.get("DATABASE_URL")

# Validar configuración
config.validate()  # Lanza error si falta algo crítico
```

---

## 📚 Configuración del Proyecto

### Variables de Entorno Críticas

**API Keys (H02):**
```bash
GROQ_API_KEY=<tu_clave_groq>
PERPLEXITY_API_KEY=<tu_clave_perplexity>  # H12+
```

**Base de Datos (H02):**
```bash
DATABASE_URL=sqlite:///data/thea.db  # Development
DATABASE_URL=postgresql://...  # Production (H14+)
```

**Telegram Bot (H09):**
```bash
TELEGRAM_BOT_TOKEN=<tu_token>
TELEGRAM_WEBHOOK_URL=https://...  # H14+
```

**Logging y Debug:**
```bash
LOG_LEVEL=INFO  # DEBUG|INFO|WARNING|ERROR
ENVIRONMENT=development  # development|staging|production
```

---

## 🏗️ Arquitectura del Config

### Jerarquía de Carga (H02)

1. **`.env` file** - Variables locales (gitignored)
2. **Variables de sistema** - OS environment variables
3. **Defaults** - Valores por defecto seguros

### Validación (H02)

```python
class ConfigValidator:
    def validate_api_keys(self) -> bool:
        """Verifica que existan las API keys necesarias"""
        
    def validate_database(self) -> bool:
        """Valida la conexión a la base de datos"""
        
    def validate_environment(self) -> bool:
        """Comprueba el entorno (dev/prod)"""
```

---

## 📅 Roadmap de Configuración

### H02 (Nov 2025) ✅
- ✅ Sistema básico de configuración
- ✅ Soporte para `.env`
- ✅ Validación de variables críticas
- ✅ Documentación inicial

### H09 (Ene 2026) 🔴 En Progreso
- 🔴 Configuración específica de Telegram
- 🔴 Gestión de webhooks
- ⏳ Variables de configuración de agentes

### H12 (Mar 2026) ⏳ Planificado
- ⏳ Múltiples entornos (dev/staging/prod)
- ⏳ Configuración de API REST
- ⏳ Sistema de secretos (Vault)

### H14 (Abr 2026) ⏳ Planificado  
- ⏳ Configuración de producción
- ⏳ Gestión de secretos en Railway
- ⏳ Monitoreo de configuración

---

## 🔐 Seguridad

### Mejores Prácticas (H02)

1. **Nunca commitear `.env`** - Siempre en `.gitignore`
2. **Usar `.env.example`** - Template sin valores reales
3. **Rotar API keys** - Cada 90 días mínimo
4. **Validar en inicio** - Fallar rápido si falta config

### Archivos de Configuración

```
/thea-ia
  ├── .env              # ❌ Gitignored - NO COMMITEAR
  ├── .env.example      # ✅ Template público
  ├── .env.test         # ✅ Para tests (valores dummy)
  └── src/theaia/config/
      ├── __init__.py   # ConfigManager
      └── *.md          # Documentación interna
```

---

## 🧪 Testing de Configuración

### Tests Unitarios (H02)

```python
def test_config_loads_from_env():
    """Verifica que se carguen variables del .env"""
    
def test_config_validates_missing_keys():
    """Debe fallar si faltan keys críticas"""
    
def test_config_defaults():
    """Comprueba valores por defecto"""
```

Ubicación: `tests/unit/config/`

---

## 📖 Documentación Relacionada

- [SCHEMA.md](/docs/SCHEMA.md) - Arquitectura completa del sistema
- [H02 Milestone](/docs/roadmap/h02/) - Implementación inicial de config
- [H09 Milestone](/docs/roadmap/h09/) - Config de Telegram
- [Security Docs](/docs/security/README.md) - Prácticas de seguridad
- [Architecture](/docs/architecture/overview.md) - Vista general del sistema

---

## 🔄 Changelog

Ver archivo completo en: `/src/theaia/config/config-CHANGELOG.md`

**v3.0.0 (H02 - Nov 2025)**
- ✅ Sistema de configuración centralizado
- ✅ Soporte para múltiples fuentes
- ✅ Validación automática

**v3.1.0 (H09 - Ene 2026)** - En progreso
- 🔴 Configuración de Telegram Bot
- ⏳ Variables específicas de agentes

---

**Last Updated:** 06 Enero 2026, 21:15 CET  
**Next Update:** H12 (Marzo 2026) - Configuración multi-entorno  
**Maintained by:** Config Team
