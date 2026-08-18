from pydantic import BaseModel

class LivroCreate(BaseModel):   # Pydantic (validação / contrato) -> Representa os dados que entram da aplicação
    titulo: str
    autor: str
    ano: int

class LivroResponse(BaseModel):  # Pydantic (validação / contrato) -> Representa os dados que saem da aplicação
    id: int
    titulo: str
    autor: str
    ano: int