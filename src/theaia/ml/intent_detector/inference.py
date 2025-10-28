import os
import joblib

class IntentDetector:
    """
    Intent detector robusto y a prueba de errores para Thea IA.
    Usa ML solo si acierta (no fallback/None/vacío).
    Fallback a keywords siempre.
    Normaliza intents ML a los válidos del sistema (singular, variantes).
    Logging incluido para debugging de decisión.
    """
    def __init__(self, model_filename: str = "model_intent.pkl"):
        self.model = None
        base_dir = os.path.dirname(os.path.abspath(__file__))
        models_dir = os.path.normpath(os.path.join(base_dir, "../models"))
        model_path = os.path.join(models_dir, model_filename)
        try:
            if os.path.exists(model_path):
                self.model = joblib.load(model_path)
        except Exception as e:
            print(f"[IntentDetector MODEL ERROR]: {e}")
            self.model = None

        self.keywords = {
            "nota": [
                "nota", "anota", "apunta", "recordar", "apuntar", "apúntame", "escribe", "escriba", "memoria", "apuntaré"
            ],
            "ayuda": [
                "ayuda", "help", "cómo hago", "cómo puedo", "manual", "tutorial", "explica", "explicación", "dudas", "asistencia", "describir"
            ],
            "evento": [
                "evento", "cita", "reunión", "convocatoria", "quedada", "anota evento", "planear", "programa", "calendariza", "programar", "agenda"
            ],
            "agenda": [
                "ver agenda", "enseña mi agenda", "agenda semanal", "¿tengo algo hoy?", "próximas citas"
            ],
            "consulta": [
                "consulta", "buscar", "información", "averigua", "pregunta", "dime", "resuelve", "define", "qué es", "explica", "explícame", "informarme", "investiga", "detalle"
            ],
            "ocio": [
                "ocio", "recomendar", "entretenimiento", "película", "serie", "libro", "jugar", "juego"
            ],
            "salud": [
                "salud", "bienestar", "consultar médico", "tensión", "calorías", "deporte", "receta"
            ],
            "tiempo": [
                "tiempo", "clima", "pronóstico", "llueve", "hace sol", "meteorología", "temperatura", "paraguas"
            ],
            "recordatorio": [
                "recordatorio", "recuérdame", "alarm", "alarma", "recuerda", "avísame", "alerta", "avisar"
            ],
            "horario": [
                "horario", "turnos", "planning", "calendario", "planificación", "agenda semanal", "agenda diaria"
            ],
        }

    def normalize_intent(self, intent: str, text: str) -> str:
        mapping = {
            "notas": "nota",
            "nota": "nota",
            "ayudas": "ayuda",
            "ayuda": "ayuda",
            "eventos": "evento",
            "evento": "evento",
            "agendas": "agenda",
            "agenda": "agenda",
            "consultas": "consulta",
            "consulta": "consulta",
            "ociosos": "ocio",
            "ocioso": "ocio",
            "ocio": "ocio",
            "salud": "salud",
            "tiempos": "tiempo",
            "tiempo": "tiempo",
            "recordatorios": "recordatorio",
            "recordatorio": "recordatorio",
            "horarios": "horario",
            "horario": "horario",
        }
        # Si texto pide ayuda explícita, forzar ayuda aunque el modelo devuelva otra cosa
        if "ayuda" in text.lower() or "help" in text.lower():
            return "ayuda"
        return mapping.get(intent, intent)

    def detect(self, text: str) -> str:
        msg = text.lower().strip()
        # 1. Prueba ML solo si modelo lo predice bien, y normaliza el intent
        if self.model:
            try:
                intent = self.model.predict([text])[0]
                print(f"[IntentDetector DEBUG] ML predice: {intent!r} para texto: {text!r}")
                intent_norm = self.normalize_intent(str(intent).strip().lower(), text)
                if intent_norm and intent_norm not in ("fallback", "", "none"):
                    return intent_norm
            except Exception as e:
                print(f"[IntentDetector ML ERROR]: {e}")
        # 2. Reglas/keywords (logging incluido)
        for intent, kws in self.keywords.items():
            if any(kw in msg for kw in kws):
                print(f"[IntentDetector DEBUG] Fallback por keyword: {intent} para texto: {text!r}")
                return intent
        if "ayuda" in msg or "help" in msg:
            print(f"[IntentDetector DEBUG] Fallback explícito AYUDA para texto: {text!r}")
            return "ayuda"
        print(f"[IntentDetector DEBUG] Fallback absoluto para texto: {text!r}")
        return "fallback"
