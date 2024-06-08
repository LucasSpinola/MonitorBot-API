from pydantic import BaseModel

class Unidade(BaseModel):
    Data: str
    HoraInicial: str
    HoraFinal: str
    Aula: str
    