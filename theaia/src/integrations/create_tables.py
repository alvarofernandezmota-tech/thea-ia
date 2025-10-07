from thea.core.models import Base
from antiguothea.settings import engine

Base.metadata.create_all(engine)
