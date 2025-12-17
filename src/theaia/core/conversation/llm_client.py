"""
LLM Client - Groq OpenAI-compatible Integration with Tools Support
✅ Full H9 Tool Support: check_availability, create_appointment, get_appointments, cancel_appointment, update_appointment
"""

import os
import json
import logging
from typing import Optional, List, Dict, Any
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()
logger = logging.getLogger(__name__)


class LLMConfig:
    """LLM Configuration"""
    
    def __init__(
        self,
        model: str = "llama-3.3-70b-versatile",
        temperature: float = 0.7,
        max_tokens: int = 2048
    ):
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens


class LLMClient:
    """LLM Client using Groq OpenAI-compatible API with Tool Calling Support"""
    
    def __init__(self, config: LLMConfig):
        self.config = config
        
        try:
            api_key = os.getenv("GROQ_API_KEY")
            if not api_key:
                raise ValueError("GROQ_API_KEY not found in .env")
            
            # Use OpenAI client with Groq endpoint
            self.client = OpenAI(
                api_key=api_key,
                base_url="https://api.groq.com/openai/v1"
            )
        except Exception as e:
            raise Exception(f"Groq initialization error: {e}")
        
        self.conversation_history: List[Dict[str, str]] = []
        self.tools_instance: Optional[Any] = None
        self.tools_definitions: List[Dict] = []
    
    # ==================== STANDARD CHAT ====================
    
    async def chat(
        self,
        message: str,
        system_prompt: Optional[str] = None
    ) -> str:
        """Send message to Groq and get response"""
        
        # Add user message to history
        self.conversation_history.append({
            "role": "user",
            "content": message
        })
        
        # Build messages for API
        messages: List[Dict[str, str]] = []
        
        # Add system prompt if provided
        if system_prompt:
            messages.append({
                "role": "system",
                "content": system_prompt
            })
        
        # Add conversation history (keep last 10 for context)
        messages.extend(self.conversation_history[-10:])
        
        try:
            # Call Groq API (OpenAI compatible)
            response = self.client.chat.completions.create(
                model=self.config.model,
                messages=messages,
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens
            )
            
            # Extract answer
            answer = response.choices[0].message.content
            
            # Add assistant response to history
            self.conversation_history.append({
                "role": "assistant",
                "content": answer
            })
            
            return answer
        
        except Exception as e:
            error_msg = f"❌ Groq Error: {str(e)}"
            logger.error(error_msg)
            return error_msg
    
    # ==================== TOOLS SUPPORT ====================
    
    def setup_tools(self, groq_tools_instance: Any) -> None:
        """
        Registra GroqTools en el cliente LLM
        
        Args:
            groq_tools_instance: Instancia de GroqTools con tools implementados
        """
        self.tools_instance = groq_tools_instance
        self.tools_definitions = self._generate_tools_definitions()
        logger.info(f"✅ Tools registrados: {len(self.tools_definitions)} tools disponibles")
    
    def _generate_tools_definitions(self) -> List[Dict]:
        """
        Genera definiciones de tools para Groq API
        ✅ H9 COMPLETE: check_availability, create_appointment, get_appointments, cancel_appointment, update_appointment
        """
        return [
            {
                "type": "function",
                "function": {
                    "name": "check_availability",
                    "description": "Consulta horarios disponibles para una fecha específica",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "date_str": {
                                "type": "string",
                                "description": "Fecha en formato natural (ej: 'mañana', '2025-12-15', 'próximo lunes')"
                            },
                            "duration_minutes": {
                                "type": "integer",
                                "description": "Duración de cita en minutos",
                                "default": 60
                            },
                            "preferred_times": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Horarios preferidos (ej: ['15:00', '16:00'])"
                            }
                        },
                        "required": ["date_str"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "create_appointment",
                    "description": "Crea una cita en el calendario del usuario",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "date_str": {
                                "type": "string",
                                "description": "Fecha (ej: 'mañana', '2025-12-15')"
                            },
                            "time_str": {
                                "type": "string",
                                "description": "Hora (ej: '15:00', '3pm', 'las 3 de la tarde')"
                            },
                            "duration_minutes": {
                                "type": "integer",
                                "description": "Duración en minutos",
                                "default": 60
                            },
                            "description": {
                                "type": "string",
                                "description": "Descripción de la cita"
                            }
                        },
                        "required": ["date_str", "time_str"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_appointments",
                    "description": "Lista todas las citas del usuario",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "status_filter": {
                                "type": "string",
                                "description": "Filtrar por estado ('confirmed', 'cancelled')",
                                "enum": ["confirmed", "cancelled"]
                            },
                            "limit": {
                                "type": "integer",
                                "description": "Máximo de citas a retornar",
                                "default": 10
                            }
                        }
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "cancel_appointment",
                    "description": "Cancela una cita existente",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "appointment_id": {
                                "type": "integer",
                                "description": "ID de la cita a cancelar"
                            }
                        },
                        "required": ["appointment_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "update_appointment",
                    "description": "Actualiza/modifica una cita existente (cambiar hora, fecha, título o duración)",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "appointment_id": {
                                "type": "integer",
                                "description": "ID de la cita a actualizar"
                            },
                            "new_date_str": {
                                "type": "string",
                                "description": "Nueva fecha en formato natural (opcional)"
                            },
                            "new_time_str": {
                                "type": "string",
                                "description": "Nueva hora en formato natural (opcional)"
                            },
                            "new_title": {
                                "type": "string",
                                "description": "Nuevo título/nombre de la cita (opcional)"
                            },
                            "new_duration_minutes": {
                                "type": "integer",
                                "description": "Nueva duración en minutos (opcional)"
                            }
                        },
                        "required": ["appointment_id"]
                    }
                }
            }
        ]
    
    def _normalize_tool_params(self, tool_name: str, tool_input: Dict[str, Any]) -> Dict[str, Any]:
        """
        Normaliza parámetros de tools para asegurar compatibilidad.
        
        ✅ H9 COMPLETE: Incluye normalización para update_appointment
        - date_str vs date
        - time_str vs time
        - new_date_str vs new_date
        - new_time_str vs new_time
        
        Args:
            tool_name: Nombre del tool
            tool_input: Parámetros tal como vienen de Groq
        
        Returns:
            Parámetros normalizados para execute_tool()
        """
        normalized = {}
        
        if tool_name == "check_availability":
            # check_availability espera: date, duration_minutes
            normalized["date"] = tool_input.get("date_str") or tool_input.get("date", "mañana")
            normalized["duration_minutes"] = tool_input.get("duration_minutes", 60)
            
        elif tool_name == "create_appointment":
            # create_appointment espera: date, time, title, duration_minutes, description
            normalized["date"] = tool_input.get("date_str") or tool_input.get("date", "mañana")
            normalized["time"] = tool_input.get("time_str") or tool_input.get("time", "15:00")
            normalized["title"] = tool_input.get("description") or tool_input.get("title", "Cita")
            normalized["duration_minutes"] = tool_input.get("duration_minutes", 60)
            normalized["description"] = tool_input.get("description", "")
            
        elif tool_name == "get_appointments":
            # get_appointments espera: status_filter, limit
            # ✅ FIX: Mapea "confirmed" → "all" porque es conversación fluida
            status = tool_input.get("status_filter", "all")
            if status == "confirmed":
                status = "all"  # Usuario dice "confirmed" pero queremos "all"
            normalized["status_filter"] = status
            normalized["limit"] = tool_input.get("limit", 10)
            
        elif tool_name == "cancel_appointment":
            # cancel_appointment espera: appointment_id, reason
            normalized["appointment_id"] = tool_input.get("appointment_id")
            normalized["reason"] = tool_input.get("reason", "Cancelado por el usuario")
        
        elif tool_name == "update_appointment":
            # ✅ NEW: update_appointment espera: appointment_id, new_date, new_time, new_title, new_duration_minutes
            normalized["appointment_id"] = tool_input.get("appointment_id")
            
            # Normalizar variaciones de nombres de parámetros
            if "new_date_str" in tool_input or "new_date" in tool_input:
                normalized["new_date"] = tool_input.get("new_date_str") or tool_input.get("new_date")
            
            if "new_time_str" in tool_input or "new_time" in tool_input:
                normalized["new_time"] = tool_input.get("new_time_str") or tool_input.get("new_time")
            
            if "new_title" in tool_input:
                normalized["new_title"] = tool_input.get("new_title")
            
            if "new_duration_minutes" in tool_input:
                normalized["new_duration_minutes"] = tool_input.get("new_duration_minutes")
        
        logger.debug(f"✅ Parámetros normalizados para {tool_name}: {normalized}")
        return normalized
    
    async def call_with_tools(
        self,
        messages: List[Dict[str, str]],
        system_prompt: Optional[str] = None,
        max_iterations: int = 5
    ) -> str:
        """
        Llamada a Groq con soporte a tool calling
        Implementa agentic loop: LLM → detecta tool use → ejecuta tool → retorna resultado
        
        Args:
            messages: Historial de conversación
            system_prompt: System prompt opcional
            max_iterations: Máximo de iteraciones (prevenir loops infinitos)
        
        Returns:
            Respuesta final del modelo en español
            
        Example:
            >>> client.setup_tools(groq_tools)
            >>> result = await client.call_with_tools([
            ...     {"role": "user", "content": "Quiero agendar mañana a las 3pm"}
            ... ])
            >>> print(result)
            "✅ Cita confirmada para mañana a las 15:00"
        """
        if not self.tools_instance:
            logger.warning("⚠️ Tools no registrados. Usa setup_tools() primero")
            return "Error: Tools no configurados"
        
        current_messages = messages.copy()
        iteration = 0
        
        # Agregar system prompt si se proporciona
        if system_prompt:
            current_messages.insert(0, {
                "role": "system",
                "content": system_prompt
            })
        
        while iteration < max_iterations:
            iteration += 1
            logger.debug(f"🔄 Iteración {iteration}/{max_iterations}")
            
            try:
                # Llamar a Groq API con tools
                response = self.client.chat.completions.create(
                    model=self.config.model,
                    messages=current_messages,
                    tools=self.tools_definitions,
                    tool_choice="auto",
                    temperature=self.config.temperature,
                    max_tokens=self.config.max_tokens
                )
                
                # Extraer respuesta
                response_message = response.choices[0].message
                
                # Verificar si el modelo quiere usar tools
                if response_message.tool_calls:
                    logger.debug(f"🔧 Detectado {len(response_message.tool_calls)} tool call(s)")
                    
                    # Agregar respuesta del modelo al historial
                    current_messages.append({
                        "role": "assistant",
                        "content": response_message.content or "",
                        "tool_calls": [
                            {
                                "id": tc.id,
                                "type": "function",
                                "function": {
                                    "name": tc.function.name,
                                    "arguments": tc.function.arguments
                                }
                            }
                            for tc in response_message.tool_calls
                        ]
                    })
                    
                    # Ejecutar tools
                    tool_results = []
                    for tool_call in response_message.tool_calls:
                        tool_name = tool_call.function.name
                        
                        try:
                            # Parse arguments
                            tool_input = json.loads(tool_call.function.arguments)
                            
                            # ✅ FIX BUG #2: Normalizar parámetros
                            normalized_params = self._normalize_tool_params(tool_name, tool_input)
                            
                            logger.debug(f"📍 Ejecutando tool: {tool_name} con params: {normalized_params}")
                            
                            # Ejecutar tool con parámetros normalizados
                            result = self.tools_instance.execute_tool(tool_name, **normalized_params)
                            
                            # Preparar resultado para el modelo
                            tool_results.append({
                                "role": "tool",
                                "tool_call_id": tool_call.id,
                                "content": json.dumps({
                                    "success": result.success,
                                    "data": result.data,
                                    "message": result.message,
                                    "error": result.error
                                })
                            })
                            
                            logger.debug(f"✅ Tool {tool_name} ejecutado exitosamente")
                        
                        except json.JSONDecodeError as json_error:
                            logger.error(f"❌ Error parseando JSON para {tool_name}: {str(json_error)}")
                            tool_results.append({
                                "role": "tool",
                                "tool_call_id": tool_call.id,
                                "content": json.dumps({
                                    "success": False,
                                    "error": f"Error parseando parámetros: {str(json_error)}"
                                })
                            })
                        
                        except Exception as tool_error:
                            logger.error(f"❌ Error ejecutando {tool_name}: {str(tool_error)}")
                            tool_results.append({
                                "role": "tool",
                                "tool_call_id": tool_call.id,
                                "content": json.dumps({
                                    "success": False,
                                    "error": f"Error ejecutando tool: {str(tool_error)}"
                                })
                            })
                    
                    current_messages.extend(tool_results)
                
                else:
                    # Respuesta final (no hay tool calls)
                    final_response = response_message.content or "Sin respuesta del modelo"
                    logger.info(f"✅ Respuesta final obtenida en iteración {iteration}")
                    return final_response
            
            except Exception as e:
                error_msg = f"❌ Error en call_with_tools (iteración {iteration}): {str(e)}"
                logger.error(error_msg)
                return error_msg
        
        return "❌ Error: máximo número de iteraciones alcanzado sin respuesta final"
    
    # ==================== UTILITY METHODS ====================
    
    def clear_history(self) -> None:
        """Clear conversation history"""
        self.conversation_history = []
        logger.debug("🧹 Historial de conversación limpiado")
    
    def get_history(self, last_n: Optional[int] = None) -> List[Dict]:
        """Get conversation history"""
        if last_n:
            return self.conversation_history[-last_n:]
        return self.conversation_history
    
    def get_history_length(self) -> int:
        """Get total conversation history length"""
        return len(self.conversation_history)
    
    async def close(self) -> None:
        """Cleanup resources"""
        self.conversation_history = []
        logger.debug("👋 LLMClient cerrado")
