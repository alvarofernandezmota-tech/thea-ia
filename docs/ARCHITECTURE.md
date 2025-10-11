# Arquitectura General – Thea IA 2.0

Este documento describe la arquitectura, flujos y componentes principales del sistema Thea IA 2.0.

---

## 🌐 Visión de alto nivel

Thea IA 2.0 está basada en una arquitectura modular, desacoplada y escalable.  
Cada agente implementa su propia lógica, y la orquestación central (FSM/Router) coordina los estados y rutas, permitiendo una integración sencilla de nuevos módulos y adaptadores.

---

## 🏗️ Componentes principales

- **Agentes (src/theaia/agents/)**: Dialogadores/FSM para agenda, notas, consultas, ayuda, fallback.
- **Adaptadores (src/theaia/adapters/)**: Integración canales externos (Telegram, webhooks, API REST).
- **Core/Router (src/theaia/core/)**: Orquestador, FSM y gestor global de contexto e intenciones.
- **ML/NLP (src/theaia/ml/)**: Modelos de intents, entidades y pipelines configurables.
- **Database/Repositories (src/theaia/database/)**: Modelos ORM/SQL y acceso datos.
- **API REST (src/theaia/api/)**: Endpoints para interacción y control.
- **Servicios y Utils**: Lógica backend, helpers y utilidades compartidas.

---parte 2 

---

## 🔄 Flujo típico de interacción

1. El usuario envía mensaje (por Telegram, API u otro canal).
2. El adaptador recibe la petición y la envía al router/core.
3. El sistema detecta el intent, estado y entidades usando ML/NLP.
4. El router/FSM decide qué agente activa y qué respuesta/generación sigue.
5. El agente elegido procesa contexto, datos y opera sobre base de datos si necesario.
6. Se devuelve respuesta formatada al canal original y se actualizan los logs/contexto.

---

## 🧬 Diagrama simplificado de arquitectura

Usuario → Adaptador → Core/Router/FSM → Agente → DB/ML/NLP → Respuesta/Canal

text

---

## 🚀 Ejemplo de flujo: creación de evento

1. Usuario: “Agendar cita médica mañana a las 12”
2. Telegram Adapter → Router (core)
3. FSM detecta intent: `create_event`, extrae fecha/hora/entidad
4. Agenda Agent crea el evento en DB
5. Respuesta: “Cita médica agendada mañana a las 12”

---

¿Te entrego la siguiente parte con detalles del diseño modular, escalabilidad y buenas prácticas?**ARCHITECTURE.md – Parte 3: Diseño modular, escalabilidad y buenas prácticas**

🧱 Diseño modular y escalabilidad
Cada agente, adaptador y módulo es independiente para facilitar expansión.

Añadir nuevos agentes solo requiere implementar la lógica FSM y acoplarlo al router.

El sistema soporta añadir nuevos modelos NLP, adaptadores de canal o servicios externos (API REST, webhooks).

🔍 Buenas prácticas arquitectónicas
Mantén separation of concerns: lógica de negocio, datos y presentación desacoplados.

Documenta interfaces, variables, estados y flujos en README y diccionario.

Refactoriza periódicamente para modularizar y mejorar la mantenibilidad.

Configura health checks, logs y métricas para robustez y análisis continuo.

Revisa esta arquitectura en cada gran update para garantizar alineación, robustez y capacidad de evolución.

--parte3


