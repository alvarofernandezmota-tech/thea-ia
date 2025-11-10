🏗️ BaseAgent — Clase Base para Todos los Agentes
Archivo: src/theaia/agents/base_agent.py
Versión: v1.0.0
Status: ✅ Producción

📋 Propósito
BaseAgent es la clase abstracta que define la interfaz común que todos los agentes del sistema deben implementar. Proporciona contrato estándar para:

Intenciones soportadas

Verificación de capacidades

Manejo de mensajes

Estandarización de respuestas

💻 Interfaz Pública
python
class BaseAgent:
    def get_supported_intents(self) -> list[str]:
        """Devuelve lista de intenciones que el agente puede manejar"""
        raise NotImplementedError(...)
    
    def can_handle(self, intent: str) -> bool:
        """Verifica si el agente puede manejar una intención"""
        return intent.lower() in [i.lower() for i in self.get_supported_intents()]
    
    def handle(self, user_id: str, message: str, context: dict) -> dict:
        """Procesa mensaje y devuelve respuesta estructurada"""
        return {
            "status": "ok",
            "message": str,
            "context": dict
        }
🔄 Flujo de Ejecución
text
1. Router detecta intención en mensaje usuario
2. Busca agente con can_handle(intent) = True
3. Llama agent.handle(user_id, message, context)
4. Devuelve {"status": "ok", "message": "...", "context": {...}}
📊 Métodos
Método	Firma	Devuelve	Obligatorio
get_supported_intents()	→ list[str]	Intenciones	✅ Sí
can_handle()	(intent: str) → bool	Booleano	No
handle()	(user_id, message, context) → dict	Respuesta	✅ Sí
🎯 Ejemplo Implementación
python
from theaia.agents.base_agent import BaseAgent

class MiAgent(BaseAgent):
    def get_supported_intents(self) -> list[str]:
        return ["mi_intención", "otra_intención"]
    
    def handle(self, user_id: str, message: str, context: dict) -> dict:
        # Procesar lógica
        response = "Procesado: " + message
        return {
            "status": "ok",
            "message": response,
            "context": context
        }
⚠️ Requisitos de Herencia
Todo agente que herede de BaseAgent DEBE:

✅ Implementar get_supported_intents()

✅ Implementar handle()

✅ Mantener contrato de retorno: dict con keys: status, message, context

BaseAgent v1.0 — Clase Abstracta Base