# src/theaia/agents/fallback_agent.py

class FallbackAgent:
    def __init__(self):
        pass
    def handle(self, *args, **kwargs):
        return "Intent no reconocido.", "fallback", {}
