from sqlalchemy import create_engine        # O Engine é o objeto que representa a conexão/configuração de acesso ao banco dentro do SQLAlchemy.
from sqlalchemy.orm import DeclarativeBase, sessionmaker  #

from app.config import settings

# Engine representa a configuração de acesso ao banco
engine = create_engine(settings.database_url)

# Classe base usada pelos Models do SQLAlchemy
class Base(DeclarativeBase):
    pass

# Fábrica de Sessions usadas para interagir com o banco
SessionLocal = sessionmaker(
    bind=engine
)