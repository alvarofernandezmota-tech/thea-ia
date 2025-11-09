🎓 Adapters Best Practices — THEA IA
Versión: 1.0
Última actualización: 2025-11-08 17:23 CET (Sesión 36)
Responsable: Adapters Team / CEO
Estado: ✅ Activo

📋 Propósito
Guía de mejores prácticas para diseñar, implementar y mantener adapters en THEA IA.

🎯 Principios fundamentales
1. Normalización única
Todos los adapters normalizan a formato estándar THEA IA

Independencia de canal en FSM/Agents

Fácil agregar nuevos adapters

2. Aislamiento de credenciales
Tokens/secrets en variables de entorno

Nunca hardcodear credenciales

Usar ConfigParser

3. Error handling robusto
Retry con backoff exponencial

Timeout en todas las conexiones

Log detallado de fallos

4. Validación de entrada
Verificar webhooks (signing secret)

Sanitizar inputs

Rate limiting por usuario

5. Testing exhaustivo
Tests unitarios mínimo 80%

Tests integración con FSM

Tests de seguridad (credential leak)

📐 Estructura estándar de adapter
python
from src.theaia.adapters.base import BaseAdapter

class MyAdapter(BaseAdapter):
    def __init__(self, config):
        super().__init__("MyAdapter")
        self.config = config
    
    def initialize(self):
        """Conectar con servicio externo"""
        # Validar credenciales
        # Establecer conexión
        pass
    
    def normalize_input(self, raw_input):
        """Convertir a formato THEA IA"""
        return {
            "user_id": "",
            "channel": "mychannel",
            "message": "",
            "metadata": {}
        }
    
    def format_output(self, response):
        """Formatear para canal específico"""
        return formatted
    
    def send_message(self, formatted):
        """Enviar al usuario"""
        pass
    
    def shutdown(self):
        """Liberar recursos"""
        pass
✅ Checklist para nuevo adapter
 Hereda de BaseAdapter

 Implementa todos los métodos core

 Configuración YAML en config/adapters/

 Credenciales externalizadas

 Validación de webhooks

 Rate limiting

 Error handling (retry + timeout)

 Tests unitarios (80%+ cobertura)

 Tests integración con FSM

 Documentación README

 Ejemplos de uso

 Métricas definidas

 Security audit

🚨 Anti-patrones
❌ Hardcodear tokens
python
# MAL
TOKEN = "sk_live_123456"
python
# BIEN
TOKEN = os.getenv("ADAPTER_TOKEN")
❌ Sin timeout
python
# MAL
response = requests.get(url)  # Cuelga si timeout
python
# BIEN
response = requests.get(url, timeout=10)
❌ Sin validación de webhook
python
# MAL
def handle_webhook(data):
    process(data)  # Cualquiera puede enviar
python
# BIEN
def handle_webhook(data, signature):
    if not validate_signature(data, signature):
        raise SecurityError()
📊 Métricas recomendadas
Cada adapter debe exponer:

Response time (latencia)

Success rate (% éxito)

Error rate (% fallos)

Throughput (msg/sec)

Uptime (%)

🔗 Referencias
Adapters Overview

Testing

Architecture

📌 Meta-información
Campo	Valor
Archivo	docs/adapters/best_practices.md
Versión	1.0
Última revisión	2025-11-08 17:23 CET (Sesión 36)
Estado	✅ Activo
🛡️ Auditoría
Parte del Hito 36.1 (docs/adapters/)

Validado en sesión 36