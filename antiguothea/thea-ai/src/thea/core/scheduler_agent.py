class SchedulerAgent:
    def __init__(self, user_id):
        self.user_id = user_id

    def agendar_cita(self, fecha, hora, descripcion):
        # Simulación básica
        return f"Cita agendada para {fecha} a las {hora}: {descripcion}"

    def modificar_cita(self, evento_id, nueva_fecha, nueva_hora):
        return f"Cita {evento_id} modificada a {nueva_fecha} a las {nueva_hora}"

    def consultar_citas(self):
        # Simple ejemplo
        return ["Cita 1: 5/10 10:00", "Cita 2: 8/10 17:00"]

    def cancelar_cita(self, evento_id):
        return f"Cita {evento_id} cancelada correctamente."
