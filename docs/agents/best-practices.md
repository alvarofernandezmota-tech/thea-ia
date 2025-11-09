🎓 Agents Best Practices — THEA IA
Versión: 1.0
Última actualización: 2025-11-08 (Sesión 35)
Responsable: Agents Team / Álvaro Fernández Mota (CEO)
Estado: ✅ Activo

📋 Propósito
Guía de mejores prácticas para diseñar, implementar y mantener agentes en THEA IA: patrones, convenciones, anti-patrones y checklist.

🎯 Principios fundamentales
1. Responsabilidad única
Cada agente hace UNA cosa y la hace bien

❌ NO: Agente que crea eventos Y notas Y búsquedas

✅ SÍ: Agente Agenda solo eventos, Note solo notas

2. Comunicación mediada por FSM
Nunca Agent A → Agent B directamente

Siempre Agent A → FSM → Agent B

FSM es el único orquestador

3. Idempotencia
Mismo input = Mismo output (siempre que sea posible)

Operaciones críticas deben ser idempotentes

4. Error handling robusto
Nunca fallar sin explicación

Siempre retornar error estructurado

Log completo de errores

5. Validación estricta de entrada
Sanitizar TODOS los inputs

Validar tipos y rangos

Rechazar early si input inválido

📐 Estructura de un agente
python
from src.theaia.agents.base import BaseAgent

class MyAgent(BaseAgent):
    def __init__(self):
        super().__init__("MyAgent")
        self.config = self.load_config("my_agent.yaml")
    
    def initialize(self):
        """Cargar recursos: modelos, BD, etc."""
        self.model = load_model(self.config['model'])
        self.db = connect_db()
    
    def process(self, task_data):
        """Lógica principal"""
        # 1. Validar entrada
        if not self.validate_input(task_data):
            return self.error_response("INVALID_INPUT")
        
        # 2. Procesar
        try:
            result = self._execute_task(task_data)
            return self.success_response(result)
        except Exception as e:
            self.log_error(e)
            return self.error_response("PROCESSING_ERROR", str(e))
    
    def shutdown(self):
        """Liberar recursos"""
        self.db.close()
✅ Checklist para nuevo agente
Diseño
 Responsabilidad única y clara

 No duplica funcionalidad de otro agente

 Casos de uso documentados

 Interfaz de entrada/salida definida

Implementación
 Hereda de BaseAgent

 Implementa initialize(), process(), shutdown()

 Validación estricta de entrada

 Error handling robusto

 Logging en pasos clave

 Timeouts configurados

Configuración
 Archivo YAML en config/agents/

 Configuración versionada

 Secrets externalizados (no hardcoded)

Testing
 Tests unitarios (>=85% cobertura)

 Tests integración con FSM

 Tests de error handling

 Tests de edge cases

Documentación
 README en docs/agents/agent_xxx.md

 Ejemplos de uso

 Entrada/salida documentada

 Métricas definidas

🚨 Anti-patrones (NO hacer)
❌ Agent-to-Agent directo
python
# MAL
result = AgentB().process(data)
python
# BIEN
fsm.route_to_agent('agent_b', data)
❌ Estado global compartido
python
# MAL
global_var = {}
class MyAgent:
    def process(self, data):
        global_var['key'] = data  # Estado compartido peligroso
❌ Bloqueos largos
python
# MAL
def process(self, data):
    time.sleep(60)  # Bloquea todo el sistema
python
# BIEN
@async_task
def process_async(self, data):
    await asyncio.sleep(60)
❌ Errores sin contexto
python
# MAL
return {"status": "error"}
python
# BIEN
return {
    "status": "error",
    "error_code": "INVALID_INPUT",
    "message": "Título requerido",
    "details": {"missing": ["title"]}
}
📊 Métricas recomendadas
Todo agente debe exponer:

Response time: Latencia promedio

Success rate: % éxito vs errores

Error rate: % errores

Throughput: Requests/segundo

Availability: Uptime %

🔗 Referencias
Agents Overview

Testing

Architecture

📌 Meta-información
Campo	Valor
Archivo	docs/agents/best_practices.md
Versión	1.0
Última revisión	2025-11-08 (Sesión 35)
Responsable	Agents Team / CEO
Estado	✅ Activo
🛡️ Auditoría
Parte del Hito 35.1.3 (docs/agents/)

Guía de referencia para todos los agentes

Actualizar cuando se agreguen nuevos patrones

Validado en sesión 35