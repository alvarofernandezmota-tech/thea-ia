"""
Core Intent Parser - Detección de intenciones centralizada
Basado en AgendaAgent pero genérico para todos los agentes.

Autor: Álvaro Fernández Mota
Fecha: 04 Dic 2025
Arquitectura: TRES (Álvaro + Jarvis + THEA IA)
"""

import re
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass


@dataclass
class IntentMatch:
    """Resultado de detección de intent."""
    intent: str
    confidence: float
    matched_keywords: List[str]
    entities: Dict[str, str]


class CoreIntentParser:
    """
    Parser de intenciones genérico para todos los agentes de THEA.
    
    Usa diccionarios y regex para detección rápida sin IA.
    Cada agente puede registrar sus propios intents.
    """
    
    def __init__(self):
        """Inicializa parser con intents base de todos los agentes."""
        
        # Intents base por agente
        self.intent_patterns = {
            # AGENDA AGENT
            "create_event": [
                r"\b(crear|agendar|programar|nueva?|añadir)\b.*\b(evento|cita|reunión|meeting)\b",
                r"\b(tengo|hay)\b.*\b(reunión|cita|evento|meeting)\b",
                r"\b(agendar|programar)\b",
            ],
            "query_events": [
                r"\b(mostrar|listar|ver|cuál|cuáles|qué)\b.*\b(eventos?|citas?|reuniones?)\b",
                r"\b(mis|próximos?|hoy|mañana)\b.*\b(eventos?|citas?|reuniones?)\b",
                r"\b(agenda|calendario)\b.*\b(hoy|mañana|semana)\b",
            ],
            "update_event": [
                r"\b(modificar|editar|cambiar|actualizar)\b.*\b(evento|cita|reunión)\b",
                r"\b(mover|reprogramar)\b.*\b(evento|cita|reunión)\b",
            ],
            "delete_event": [
                r"\b(eliminar|borrar|cancelar|quitar)\b.*\b(evento|cita|reunión)\b",
                r"\b(cancelar)\b",
            ],
            "mark_complete": [
                r"\b(marcar|completar|finalizar)\b.*\b(evento|cita|tarea)\b",
                r"\b(hecho|completado|terminado)\b",
            ],
            
            # NOTE AGENT
            "create_note": [
                r"\b(crear|guardar|escribir|anotar|nueva?)\b.*\b(nota|apunte)\b",
                r"\b(nota|apunte)\b.*\b(sobre|de|para)\b",
                r"\b(guardar|anotar)\b",
            ],
            "query_notes": [
                r"\b(mostrar|listar|ver|buscar)\b.*\b(notas?|apuntes?)\b",
                r"\b(mis|últimas?)\b.*\b(notas?|apuntes?)\b",
            ],
            "update_note": [
                r"\b(modificar|editar|cambiar|actualizar)\b.*\b(nota|apunte)\b",
            ],
            "delete_note": [
                r"\b(eliminar|borrar|quitar)\b.*\b(nota|apunte)\b",
            ],
            
            # REMINDER AGENT
            "create_reminder": [
                r"\b(recordar|recordatorio|aviso|avisar|alertar)\b",
                r"\b(recuérdame|avisame)\b",
            ],
            "query_reminders": [
                r"\b(mostrar|listar|ver)\b.*\b(recordatorios?|avisos?)\b",
                r"\b(mis|próximos?)\b.*\b(recordatorios?|avisos?)\b",
            ],
            
            # QUERY AGENT
            "query": [
                r"\b(buscar|consultar|encontrar|busca|consulta)\b",
                r"\b(dónde|cuándo|qué|cómo|quién)\b.*\b(está|hay|tengo)\b",
            ],
            
            # HELP AGENT
            "help": [
                r"\b(ayuda|help|ayúdame|auxilio)\b",
                r"\b(qué puedes hacer|comandos|funciones)\b",
            ],
            
            # FALLBACK
            "unknown": []  # Catch-all
        }
        
        # Keywords por intent (para scoring)
        self.intent_keywords = {
            "create_event": ["crear", "agendar", "programar", "evento", "cita", "reunión", "meeting"],
            "query_events": ["mostrar", "listar", "ver", "eventos", "citas", "agenda", "calendario"],
            "update_event": ["modificar", "editar", "cambiar", "actualizar", "mover"],
            "delete_event": ["eliminar", "borrar", "cancelar", "quitar"],
            "mark_complete": ["completar", "finalizar", "hecho", "terminado"],
            "create_note": ["nota", "apunte", "anotar", "guardar"],
            "query_notes": ["notas", "apuntes", "mostrar notas"],
            "update_note": ["modificar nota", "editar nota"],
            "delete_note": ["eliminar nota", "borrar nota"],
            "create_reminder": ["recordar", "recordatorio", "avisar", "recuérdame"],
            "query_reminders": ["recordatorios", "avisos"],
            "query": ["buscar", "consultar", "encontrar"],
            "help": ["ayuda", "help", "comandos"],
        }
    
    
    async def detect_intent(self, message: str) -> str:
        """
        Detecta la intención principal de un mensaje.
        
        Args:
            message: Mensaje del usuario
            
        Returns:
            Intent detectado (string)
        """
        message_lower = message.lower().strip()
        
        # Probar regex patterns
        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                if re.search(pattern, message_lower):
                    return intent
        
        # Fallback a scoring por keywords
        best_intent = self._score_by_keywords(message_lower)
        if best_intent:
            return best_intent
        
        return "unknown"
    
    
    async def detect_intent_with_confidence(self, message: str) -> IntentMatch:
        """
        Detecta intent con score de confianza y keywords matched.
        
        Args:
            message: Mensaje del usuario
            
        Returns:
            IntentMatch con intent, confidence, keywords
        """
        message_lower = message.lower().strip()
        best_intent = "unknown"
        best_score = 0.0
        matched_keywords = []
        
        # Score por regex
        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                if re.search(pattern, message_lower):
                    return IntentMatch(
                        intent=intent,
                        confidence=0.9,
                        matched_keywords=[],
                        entities={}
                    )
        
        # Score por keywords
        for intent, keywords in self.intent_keywords.items():
            score = 0
            matched = []
            for keyword in keywords:
                if keyword in message_lower:
                    score += 1
                    matched.append(keyword)
            
            if score > best_score:
                best_score = score
                best_intent = intent
                matched_keywords = matched
        
        confidence = min(best_score * 0.3, 1.0)
        
        return IntentMatch(
            intent=best_intent if confidence > 0.3 else "unknown",
            confidence=confidence,
            matched_keywords=matched_keywords,
            entities={}
        )
    
    
    async def extract_entities(
        self, 
        message: str, 
        intent: str
    ) -> Dict[str, str]:
        """
        Extrae entidades básicas del mensaje según el intent.
        
        Args:
            message: Mensaje del usuario
            intent: Intent detectado
            
        Returns:
            Dict con entidades extraídas
        """
        entities = {}
        message_lower = message.lower().strip()
        
        # Extraer número de evento/nota/recordatorio
        event_id_match = re.search(r'#?(\d+)', message)
        if event_id_match:
            entities["event_id"] = event_id_match.group(1)
            entities["note_id"] = event_id_match.group(1)
            entities["reminder_id"] = event_id_match.group(1)
        
        # Extraer título/descripción
        title_match = re.search(
            r'(?:crear|agendar|nota sobre|guardar|anotar)\s+["\']?([^"\']+)["\']?',
            message_lower
        )
        if title_match:
            entities["title"] = title_match.group(1).strip()
        
        # Extraer expresiones temporales básicas
        temporal_keywords = ["mañana", "hoy", "pasado mañana", "el viernes", "el lunes"]
        for keyword in temporal_keywords:
            if keyword in message_lower:
                entities["datetime_str"] = keyword
                break
        
        # Extraer horas
        time_match = re.search(r'(\d{1,2}:\d{2}|\d{1,2}\s?(?:am|pm|h))', message_lower)
        if time_match:
            entities["time"] = time_match.group(1)
        
        return entities
    
    
    def _score_by_keywords(self, message: str) -> Optional[str]:
        """
        Calcula score por keywords para cada intent.
        
        Args:
            message: Mensaje en minúsculas
            
        Returns:
            Intent con mayor score o None
        """
        best_intent = None
        best_score = 0
        
        for intent, keywords in self.intent_keywords.items():
            score = sum(1 for keyword in keywords if keyword in message)
            if score > best_score:
                best_score = score
                best_intent = intent
        
        return best_intent if best_score > 0 else None
