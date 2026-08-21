from pydantic import BaseModel, ConfigDict

class LivroCreate(BaseModel):   # Pydantic (validação / contrato) -> Representa os dados que entram da aplicação
    titulo: str
    autor: str
    ano: int

class LivroUpdate(BaseModel):
    titulo: str
    autor: str
    ano: int

class LivroResponse(BaseModel):  # Pydantic (validação / contrato) -> Representa os dados que saem da aplicação

    model_config = ConfigDict(from_attributes=True) # Pode criar esse modelo usando os atributos de um objeto Python

    id: int
    titulo: str
    autor: str
    ano: int