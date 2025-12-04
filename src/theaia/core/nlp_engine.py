"""
Core NLP Engine - Motor de procesamiento de lenguaje natural centralizado
Servicio compartido por todos los agentes del ecosistema.

Autor: Álvaro Fernández Mota
Fecha: 04 Dic 2025
Arquitectura: TRES (Álvaro + Jarvis + THEA IA)
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime


@dataclass
class NLPResult:
    """Resultado del procesamiento NLP."""
    intent: str
    confidence: float
    entities: Dict[str, any]
    suggestions: List[str]
    language: str
    processing_time_ms: int


class CoreNLPEngine:
    """
    Motor NLP centralizado para detección de intents y análisis de texto.
    
    Características:
    - Detección de intents multi-agente
    - Extracción de entidades básicas
    - Sugerencias contextuales
    - Score de confianza
    - Multi-idioma (ES/EN)
    """
    
    def __init__(self, default_language: str = "es"):
        """
        Inicializa el motor NLP.
        
        Args:
            default_language: Idioma por defecto ("es" o "en")
        """
        self.default_language = default_language
        
        # Diccionarios por intent (ES)
        self.intent_keywords_es = {
            # AGENDA
            "create_event": {
                "primary": ["crear", "agendar", "programar", "nuevo"],
                "secondary": ["evento", "cita", "reunión", "meeting"],
                "verbs": ["crear", "agendar", "programar", "añadir", "poner"]
            },
            "query_events": {
                "primary": ["mostrar", "listar", "ver", "cuál", "qué"],
                "secondary": ["eventos", "citas", "reuniones", "agenda"],
                "verbs": ["mostrar", "listar", "ver", "buscar"]
            },
            "update_event": {
                "primary": ["modificar", "editar", "cambiar", "actualizar"],
                "secondary": ["evento", "cita", "reunión"],
                "verbs": ["modificar", "editar", "cambiar", "mover"]
            },
            "delete_event": {
                "primary": ["eliminar", "borrar", "cancelar", "quitar"],
                "secondary": ["evento", "cita", "reunión"],
                "verbs": ["eliminar", "borrar", "cancelar"]
            },
            
            # NOTES
            "create_note": {
                "primary": ["nota", "apunte", "anotar", "guardar"],
                "secondary": ["sobre", "de", "para"],
                "verbs": ["crear", "guardar", "anotar", "escribir"]
            },
            "query_notes": {
                "primary": ["mostrar", "listar", "ver"],
                "secondary": ["notas", "apuntes"],
                "verbs": ["mostrar", "listar", "buscar"]
            },
            
            # REMINDERS
            "create_reminder": {
                "primary": ["recordar", "recordatorio", "avisar", "alertar"],
                "secondary": ["me", "que"],
                "verbs": ["recordar", "avisar", "alertar"]
            },
            
            # QUERY
            "query": {
                "primary": ["buscar", "consultar", "encontrar"],
                "secondary": ["dónde", "cuándo", "qué", "cómo"],
                "verbs": ["buscar", "consultar", "encontrar"]
            },
            
            # HELP
            "help": {
                "primary": ["ayuda", "ayudar", "auxilio"],
                "secondary": ["puedes", "hacer", "comandos"],
                "verbs": ["ayudar"]
            }
        }
        
        # Diccionarios por intent (EN)
        self.intent_keywords_en = {
            "create_event": {
                "primary": ["create", "schedule", "book", "new"],
                "secondary": ["event", "meeting", "appointment"],
                "verbs": ["create", "schedule", "book", "add"]
            },
            "query_events": {
                "primary": ["show", "list", "view", "what", "which"],
                "secondary": ["events", "meetings", "appointments"],
                "verbs": ["show", "list", "view", "find"]
            },
        }
    
    
    async def detect_intent(self, message: str, language: Optional[str] = None) -> str:
        """
        Detecta la intención principal del mensaje.
        
        Args:
            message: Mensaje del usuario
            language: Idioma (None = auto-detect)
            
        Returns:
            Intent detectado
        """
        lang = language or self._detect_language(message)
        keywords = self.intent_keywords_es if lang == "es" else self.intent_keywords_en
        
        message_lower = message.lower().strip()
        best_intent = "unknown"
        best_score = 0.0
        
        for intent, intent_keywords in keywords.items():
            score = self._calculate_intent_score(message_lower, intent_keywords)
            if score > best_score:
                best_score = score
                best_intent = intent
        
        # Threshold
        if best_score < 0.3:
            best_intent = "unknown"
        
        return best_intent
    
    
    async def detect_intent_with_confidence(
        self, 
        message: str,
        language: Optional[str] = None
    ) -> Tuple[str, float, List[str]]:
        """
        Detecta intent con score de confianza y keywords matched.
        
        Args:
            message: Mensaje del usuario
            language: Idioma opcional
            
        Returns:
            Tuple (intent, confidence, matched_keywords)
        """
        lang = language or self._detect_language(message)
        keywords = self.intent_keywords_es if lang == "es" else self.intent_keywords_en
        
        message_lower = message.lower().strip()
        best_intent = "unknown"
        best_score = 0.0
        best_matched = []
        
        for intent, intent_keywords in keywords.items():
            score, matched = self._calculate_intent_score_with_matches(
                message_lower, 
                intent_keywords
            )
            
            if score > best_score:
                best_score = score
                best_intent = intent
                best_matched = matched
        
        confidence = min(best_score, 1.0)
        
        if confidence < 0.3:
            best_intent = "unknown"
            confidence = 0.0
            best_matched = []
        
        return best_intent, confidence, best_matched
    
    
    async def process_message(
        self,
        message: str,
        context: Optional[Dict] = None
    ) -> NLPResult:
        """
        Procesa un mensaje completo con NLP.
        
        Args:
            message: Mensaje del usuario
            context: Contexto opcional de la conversación
            
        Returns:
            NLPResult con todos los datos procesados
        """
        start_time = datetime.now()
        
        # Detectar idioma
        language = self._detect_language(message)
        
        # Detectar intent
        intent, confidence, matched = await self.detect_intent_with_confidence(
            message, 
            language
        )
        
        # Extraer entidades básicas
        entities = self._extract_basic_entities(message, intent)
        
        # Generar sugerencias
        suggestions = self._generate_suggestions(intent, entities, context)
        
        # Calcular tiempo
        end_time = datetime.now()
        processing_time = int((end_time - start_time).total_seconds() * 1000)
        
        return NLPResult(
            intent=intent,
            confidence=confidence,
            entities=entities,
            suggestions=suggestions,
            language=language,
            processing_time_ms=processing_time
        )
    
    
    def _detect_language(self, message: str) -> str:
        """
        Detecta el idioma del mensaje (simple heuristic).
        
        Args:
            message: Mensaje a analizar
            
        Returns:
            Código de idioma ("es" o "en")
        """
        spanish_indicators = ["qué", "cómo", "dónde", "cuándo", "ñ", "á", "é", "í", "ó", "ú"]
        
        message_lower = message.lower()
        for indicator in spanish_indicators:
            if indicator in message_lower:
                return "es"
        
        return self.default_language
    
    
    def _calculate_intent_score(
        self, 
        message: str, 
        keywords: Dict[str, List[str]]
    ) -> float:
        """
        Calcula score de un intent basado en keywords.
        
        Args:
            message: Mensaje en minúsculas
            keywords: Dict con primary, secondary, verbs
            
        Returns:
            Score normalizado (0.0-1.0)
        """
        score = 0.0
        
        # Primary keywords (peso 3)
        for keyword in keywords.get("primary", []):
            if keyword in message:
                score += 3.0
        
        # Secondary keywords (peso 2)
        for keyword in keywords.get("secondary", []):
            if keyword in message:
                score += 2.0
        
        # Verbs (peso 1.5)
        for verb in keywords.get("verbs", []):
            if verb in message:
                score += 1.5
        
        # Normalizar (max score posible = ~15)
        return min(score / 10.0, 1.0)
    
    
    def _calculate_intent_score_with_matches(
        self,
        message: str,
        keywords: Dict[str, List[str]]
    ) -> Tuple[float, List[str]]:
        """
        Calcula score y devuelve keywords matched.
        
        Args:
            message: Mensaje en minúsculas
            keywords: Dict con keywords por categoría
            
        Returns:
            Tuple (score, matched_keywords)
        """
        score = 0.0
        matched = []
        
        for keyword in keywords.get("primary", []):
            if keyword in message:
                score += 3.0
                matched.append(keyword)
        
        for keyword in keywords.get("secondary", []):
            if keyword in message:
                score += 2.0
                matched.append(keyword)
        
        for verb in keywords.get("verbs", []):
            if verb in message:
                score += 1.5
                matched.append(verb)
        
        normalized_score = min(score / 10.0, 1.0)
        return normalized_score, matched
    
    
    def _extract_basic_entities(
        self, 
        message: str, 
        intent: str
    ) -> Dict[str, any]:
        """
        Extrae entidades básicas del mensaje.
        
        Args:
            message: Mensaje original
            intent: Intent detectado
            
        Returns:
            Dict con entidades extraídas
        """
        entities = {}
        
        # IDs numéricos
        import re
        id_match = re.search(r'#?(\d+)', message)
        if id_match:
            entities["id"] = id_match.group(1)
        
        # Expresiones temporales
        temporal = ["mañana", "hoy", "pasado mañana", "tomorrow", "today"]
        for keyword in temporal:
            if keyword in message.lower():
                entities["temporal"] = keyword
                break
        
        return entities
    
    
    def _generate_suggestions(
        self,
        intent: str,
        entities: Dict,
        context: Optional[Dict]
    ) -> List[str]:
        """
        Genera sugerencias contextuales.
        
        Args:
            intent: Intent detectado
            entities: Entidades extraídas
            context: Contexto de conversación
            
        Returns:
            Lista de sugerencias
        """
        suggestions = []
        
        # Sugerencias por intent
        if intent == "create_event" and "temporal" not in entities:
            suggestions.append("¿Cuándo quieres agendar el evento?")
        
        if intent == "query_events" and not context:
            suggestions.append("¿Quieres ver los eventos de hoy, mañana o de la semana?")
        
        return suggestions
