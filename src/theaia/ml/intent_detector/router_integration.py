"""Router Integration - H03 FASE 3 BLOQUE 3.2"""
from typing import Dict
from src.theaia.ml.intent_detector.detector import create_and_train_detector
from src.theaia.ml.entity_extractor.pipeline import EntityExtractor

class NLPPipeline:
    def __init__(self, confidence_threshold: float = 0.3):
        self.intent_detector = create_and_train_detector(confidence_threshold, verbose=False)
        self.entity_extractor = EntityExtractor()
    
    def process(self, text: str) -> Dict:
        intent, confidence = self.intent_detector.predict(text)
        entities = self.entity_extractor.extract(text)
        return {'intent': intent, 'confidence': confidence, 'entities': entities, 'text': text}
    
    def process_batch(self, texts: list) -> list:
        return [self.process(text) for text in texts]

if __name__ == "__main__":
    pipeline = NLPPipeline()
    print(pipeline.process("Crear evento mañana a las 15:00 con María"))
