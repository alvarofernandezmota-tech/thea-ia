"""
Router Integration - H03 FASE 3 BLOQUE 3.2

NLP Pipeline con soporte para AgendaAgent.

H03 FASE 3 Updates:
- Añadidos intents de agenda al pipeline
- Entity extraction mejorada para eventos
- Confidence threshold optimizado
"""

from typing import Dict
from .detector import create_and_train_detector
from ..entity_extractor.pipeline import EntityExtractor


class NLPPipeline:
    """
    Pipeline NLP completo para detección de intents y extracción de entidades.
    
    H03 FASE 3: Soporta todos los intents de AgendaAgent.
    
    Intents soportados:
    - crear_evento, agendar, reunion, cita
    - listar_eventos, mis_eventos
    - editar_evento, modificar_evento
    - eliminar_evento, cancelar_evento, borrar_evento
    - nota, crear_nota, guardar, anotar
    - recordatorio, recordar, avisar, recuerdame
    - consulta, buscar, query, listar
    - ayuda, help
    """
    
    def __init__(self, confidence_threshold: float = 0.3):
        """
        Inicializa el pipeline NLP.
        
        Args:
            confidence_threshold: Umbral mínimo de confianza (default: 0.3)
        """
        self.intent_detector = create_and_train_detector(
            confidence_threshold, 
            verbose=False
        )
        self.entity_extractor = EntityExtractor()
        
        # Intents de agenda agregados en H03 FASE 3
        self.agenda_intents = {
            "crear_evento", "evento", "agendar", "calendario",
            "listar_eventos", "mis_eventos", 
            "editar_evento", "modificar_evento",
            "cancelar_evento", "eliminar_evento", "borrar_evento",
            "reunion", "cita"
        }
    
    def process(self, text: str) -> Dict:
        """
        Procesa un mensaje de texto completo.
        
        Args:
            text: Mensaje del usuario
            
        Returns:
            Dict con intent, confidence, entities, text
        """
        intent, confidence = self.intent_detector.predict(text)
        entities = self.entity_extractor.extract(text)
        
        return {
            'intent': intent, 
            'confidence': confidence, 
            'entities': entities, 
            'text': text,
            'is_agenda': intent in self.agenda_intents  # NUEVO H03 FASE 3
        }
    
    def process_batch(self, texts: list) -> list:
        """
        Procesa múltiples mensajes en batch.
        
        Args:
            texts: Lista de mensajes
            
        Returns:
            Lista de resultados procesados
        """
        return [self.process(text) for text in texts]


if __name__ == "__main__":
    # Test con mensaje de agenda (H03 FASE 3)
    pipeline = NLPPipeline()
    
    # Test 1: Crear evento
    result1 = pipeline.process("Crear evento mañana a las 15:00 con María")
    print("Test 1 - Crear evento:")
    print(f"  Intent: {result1['intent']}")
    print(f"  Confidence: {result1['confidence']}")
    print(f"  Is Agenda: {result1['is_agenda']}")
    print(f"  Entities: {result1['entities']}")
    print()
    
    # Test 2: Listar eventos
    result2 = pipeline.process("mostrar mis eventos de hoy")
    print("Test 2 - Listar eventos:")
    print(f"  Intent: {result2['intent']}")
    print(f"  Confidence: {result2['confidence']}")
    print(f"  Is Agenda: {result2['is_agenda']}")
    print(f"  Entities: {result2['entities']}")
    print()
    
    # Test 3: Eliminar evento
    result3 = pipeline.process("cancelar reunión del viernes")
    print("Test 3 - Cancelar evento:")
    print(f"  Intent: {result3['intent']}")
    print(f"  Confidence: {result3['confidence']}")
    print(f"  Is Agenda: {result3['is_agenda']}")
    print(f"  Entities: {result3['entities']}")
