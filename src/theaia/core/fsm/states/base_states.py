
# src/theaia/core/fsm/states/base_states.py

from abc import ABC, abstractmethod

class BaseState(ABC):
    """
    Clase base abstracta para todos los estados de la FSM.
    Define la interfaz que cada estado concreto debe implementar.
    """
    
    def on_enter(self, context: dict) -> str:
        """
        Se ejecuta al entrar en el estado. 
        Generalmente, devuelve el mensaje que se le mostrará al usuario.
        
        Args:
            context (dict): El contexto de la conversación.
            
        Returns:
            str: Mensaje para el usuario.
        """
        return ""

    @abstractmethod
    def on_message(self, message: str, context: dict) -> str:
        """
        Procesa el mensaje del usuario y determina el siguiente estado.
        
        Args:
            message (str): El mensaje del usuario.
            context (dict): El contexto de la conversación.
            
        Returns:
            str: El nombre del siguiente estado al que transicionar.
        """
        pass
