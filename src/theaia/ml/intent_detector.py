import spacy
from typing import Dict

# Carga un modelo multilenguaje de spaCy o uno personalizado
# Nota: instala spaCy y descarga el modelo: `python -m spacy download es_core_news_sm`
nlp = spacy.load("es_core_news_sm")

# Mapeo de palabras clave a intenciones
INTENT_KEYWORDS: Dict[str, str] = {
    "crear evento": "create_event",
    "evento": "create_event",
    "nota": "create_note",
    "recordar": "create_event",
    "qué tengo": "list_events",
    "mostrar agenda": "list_events",
    "cancelar": "delete_event",
    "ayuda": "help",
    # Añade más mapeos según necesidad
}

def predict_intent(text: str) -> str:
    """
    Detecta la intención principal mediante búsqueda de palabras clave.
    Como complemento, usa spaCy para tokenizar y lematizar.
    """
    doc = nlp(text.lower())
    lemmas = {token.lemma_ for token in doc}
    # Busca coincidencias en INTENT_KEYWORDS
    for kw, intent in INTENT_KEYWORDS.items():
        if kw in text.lower() or any(kw in lemma for lemma in lemmas):
            return intent
    # Intención por defecto
    return "unknown"
