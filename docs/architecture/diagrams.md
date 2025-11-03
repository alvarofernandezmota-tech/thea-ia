📐 Diagramas de Arquitectura – Thea IA 3.0
Este documento recopila los diagramas técnicos y visuales de todos los flujos clave del ecosistema THEA IA, con leyendas claras y enlaces cruzados a los módulos y documentos relevantes.

Índice
Diagrama general de arquitectura

Flujo conversacional (FSM)

Orquestación multiagente

Interacción adaptadores/entradas

Estructura de persistencia

Otros (añadir subsecciones según evolución)

Referencias y enlaces

1. Diagrama general de arquitectura
(Mermaid, PlantUML o imagen incrustada del flujo principal, con breve explicación y referencias al architecture.md).

2. Flujo FSM — Conversacional
(Diagrama del ciclo de conversación: usuario, FSM, intent/ML, agente, base de datos, respuesta).

3. Orquestación multiagente
(Diagrama describiendo cómo interactúan y se delegan agentes — ejemplo: event_agent → calendar_agent → context_agent).

4. Flujos de integración y adaptadores
(Visualiza cómo REST, Telegram, Web... conectan con el router central).

5. Estructura de persistencia y DB
(Si tienes modelos entidades-DDBB complejos, secciona aquí con diagrama ER básico).

6. Otros diagramas críticos
(Incluye cualquier zoom técnico adicional relevante: escalado, failover, flujos de monitoring).

7. Referencias
architecture.md

fsm.md

agents.md

Documentos legacy en archive/ (vincular si hay diagramas históricos).