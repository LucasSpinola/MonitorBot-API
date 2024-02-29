from pydantic import BaseModel

class Permissao(BaseModel):
    id: str
    nome: str
    cargo: str
    