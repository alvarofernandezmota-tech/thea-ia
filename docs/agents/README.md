# 🤖 Agents Documentation

**Propósito:** Documentación de agentes inteligentes de THEA IA.

**Última actualización:** 06 Enero 2026

---

## 📋 ¿Qué son los Agents?

Los agents son componentes especializados que ejecutan tareas específicas:
- **BookingAgent** - Gestión de reservas
- **FAQAgent** - Preguntas frecuentes
- **AgentConfig** - Configuración dinámica (H03)
- **Entity Extractors** - NLP español (H03)

---

## 📁 Estructura

agents/
├── booking/ # Agente de reservas
├── faq/ # Agente de FAQ
├── config/ # Sistema AgentConfig
├── extractors/ # Entity extractors NLP
└── README.md # Este archivo

text

---

## 🤖 Agentes Disponibles

### BookingAgent
- **Propósito:** Crear, modificar y cancelar reservas
- **Estado:** ⏳ H05 (Q1 2026)
- **Coverage:** TBD

### FAQAgent
- **Propósito:** Responder preguntas frecuentes
- **Estado:** ⏳ H05 (Q1 2026)
- **Coverage:** TBD

### AgentConfig System
- **Propósito:** Configuración dinámica de agentes
- **Estado:** ✅ Producción (H03)
- **Coverage:** 100%

### Entity Extractors (NLP)
- **DateTimeExtractor** - 91% coverage
- **LocationExtractor** - 100% coverage (35+ ciudades)
- **PersonNameExtractor** - 98% coverage (35+ nombres)
- **Estado:** ✅ Producción (H03)

---

## 🎯 Audiencia

- **Desarrolladores** - Crear nuevos agentes
- **Product Managers** - Entender capacidades de agentes
- **QA Engineers** - Testing de agentes

---

## 📚 Referencias

- [Agent Architecture](../architecture/AGENTS.md)
- [Testing Strategy](../testing/AGENTS-TESTING.md)

---

**Contacto:** alvarofernandezmota@gmail.com