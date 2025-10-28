# src/theaia/agents/scheduler_agent/model/scheduler_fsm.py

class SchedulerFSM:
    """
    FSM para el flujo de programación automática de tareas/rutinas.
    
    Estados:
    - awaiting_task: Espera la descripción de la tarea
    - awaiting_schedule: Espera la frecuencia (diaria, semanal, mensual)
    - confirmation: Espera confirmación antes de activar la rutina
    - scheduled: Rutina programada correctamente
    - cancelled: Flujo cancelado por el usuario
    - error: Error en el flujo
    """

    def __init__(self):
        self.state = "awaiting_task"
        self.context = {}

    def process_message(self, message: str, context: dict):
        self.context.update(context)

        if self.state == "awaiting_task":
            self.context["task_description"] = message.strip()
            self.state = "awaiting_schedule"
            return "¿Con qué frecuencia quieres que se ejecute esta tarea? (diaria/semanal/mensual)", self.state

        elif self.state == "awaiting_schedule":
            freq = message.strip().lower()
            if freq not in ["diaria", "semanal", "mensual"]:
                return "Por favor, elige 'diaria', 'semanal' o 'mensual'.", self.state
            self.context["frequency"] = freq
            self.state = "confirmation"
            return (
                f"¿Confirmas programar '{self.context['task_description']}' cada {freq}? (sí/no)",
                self.state
            )

        elif self.state == "confirmation":
            resp = message.strip().lower()
            if resp in ["sí", "si", "s", "confirmar", "ok"]:
                self.state = "scheduled"
                return "✓ Rutina programada correctamente.", self.state
            else:
                self.state = "cancelled"
                return "Programación cancelada.", self.state

        else:
            self.state = "error"
            return "Ha ocurrido un error en el flujo de programación.", self.state
