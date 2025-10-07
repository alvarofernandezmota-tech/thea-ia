from sqlalchemy import Column, Integer, String, Date, Time
from sqlalchemy.ext.declarative import declarative_base
DB_URL=sqlite:///thea_ia.db
Base = declarative_base()
class Cita(Base):
    __tablename__ = "citas"
    id = Column(Integer, primary_key=True)
    user_id = Column(String, nullable=False)      # id del usuario Telegram
    fecha = Column(Date, nullable=False)          # fecha de la cita
    hora = Column(Time, nullable=False)           # hora
    descripcion = Column(String, nullable=False)  # motivo o nota
