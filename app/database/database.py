from sqlalchemy import create_engine        # O Engine é o objeto que representa a conexão/configuração de acesso ao banco dentro do SQLAlchemy.
from sqlalchemy.orm import DeclarativeBase, sessionmaker  #

DATABASE_URL = "sqlite:///biblioteca.db" #  sqlite ──> tipo de banco / //biblioteca.db ──> banco
                                         # Se fosse um PostgreSQL seria algo assim: "postgresql://usuario:senha@servidor:5432/biblioteca"
engine = create_engine(DATABASE_URL)

class Base(DeclarativeBase):
    pass

SessionLocal = sessionmaker(
    bind=engine
)