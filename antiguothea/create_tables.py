from thea.core.models import Base
from settings import engine

Base.metadata.create_all(engine)
