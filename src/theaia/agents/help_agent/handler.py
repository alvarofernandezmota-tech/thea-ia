import json
import os

class HelpAgent:
    def __init__(self):
        # Lee comandos soportados desde vocab.json
        dir_path = os.path.dirname(__file__)
        try:
            with open(os.path.join(dir_path, "model", "vocab.json"), encoding="utf-8") as f:
                vocab = json.load(f)
            self.commands = vocab.get("commands", ["agendar", "nota", "recordar", "ayuda", "consultar"])
        except Exception:
            self.commands = ["agendar", "nota", "recordar", "ayuda", "consultar"]

    def process(self, user_id, message, current_state, current_data):
        response = "Puedo ayudarte con: " + ", ".join(self.commands)
        new_state = "initial"
        new_data = {}
        return response, new_state, new_data
