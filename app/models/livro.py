from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.database import Base


class Livro(Base):                          # (Base) -> Indica que é um modelo gerenciado pelo SQLAlchemy

    __tablename__ = "livros"                # __tablename__ = "" -> Indica que a classe Livro representa a tabela livros.

    # Removido construtor, pois ao utilizar o SQLAlchemy o Model ORM já possui o comportamento necessário para construir o objeto.
    # def __init__(self, id, titulo, autor, ano):
    #     self.id = id
    #     self.titulo = titulo
    #     self.autor = autor
    #     self.ano = ano

    id: Mapped[int] = mapped_column(        # Mapped[] -> Isso indica o tipo Python daquele atributo que será mapeado, no caso o id é um inteiro Python e será mapeado para uma coluna
        primary_key=True,                   # mapped_column() -> é a declaração da coluna.
        autoincrement=True
    )

    titulo: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )

    autor: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )

    ano: Mapped[int] = mapped_column(
        nullable=False
    )

    def exibir(self):
        print(
            f"ID: {self.id} | "
            f"Título: {self.titulo} | "
            f"Autor: {self.autor} | "
            f"Ano: {self.ano}"
        )

    def to_dict(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "autor": self.autor,
            "ano": self.ano
        }

    @classmethod
    def from_dict(cls, dados):
        return cls( 
            id=dados["id"],         # Necessário mapear utilizando o nome dos campos, pois o SQLAlchemy reclama do nome no construtor padrão, para ter outra forma só declarando um construtor proprio
            titulo=dados["titulo"],
            autor=dados["autor"],
            ano=dados["ano"]
        )