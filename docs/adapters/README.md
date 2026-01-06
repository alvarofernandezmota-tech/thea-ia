# 🔌 Adapters Documentation

**Propósito:** Documentación de integraciones y adaptadores externos de THEA IA.

**Última actualización:** 06 Enero 2026

---

## 📋 ¿Qué son los Adapters?

Los adapters son componentes que conectan THEA IA con plataformas externas:
- **Telegram** - Bot de Telegram
- **API REST** - Endpoints HTTP/JSON
- **Database** - PostgreSQL integration
- **Future:** WhatsApp, Slack, Discord

---

## 📁 Estructura

adapters/
├── telegram/ # Telegram Bot adapter
├── api/ # REST API adapter
├── database/ # Database adapter
└── README.md # Este archivo

text

---

## 🔗 Documentación por Adapter

### Telegram Adapter
- **Archivo:** `telegram/TELEGRAM.md`
- **Propósito:** Integración con Telegram Bot API
- **Estado:** ✅ Producción (H02)

### API REST Adapter
- **Archivo:** `api/API.md`
- **Propósito:** Endpoints HTTP para integraciones
- **Estado:** ⏳ En desarrollo (H08)

### Database Adapter
- **Archivo:** `database/DATABASE.md`
- **Propósito:** Acceso a PostgreSQL
- **Estado:** ✅ Producción (H02)

---

## 🎯 Audiencia

- **Desarrolladores** - Implementar nuevos adapters
- **Integradores** - Conectar THEA IA con sistemas externos
- **DevOps** - Configurar y desplegar adapters

---

**Contacto:** alvarofernandezmota@gmail.com