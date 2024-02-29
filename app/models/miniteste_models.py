from pydantic import BaseModel

class Resposta(BaseModel):
    A: str
    B: str
    C: str
    D: str

class Miniteste(BaseModel):
    pergunta: str
    resposta: Resposta
    teste: str

class MinitesteResposta(BaseModel):
    matricula: int
    n_teste: str
    sigla: str
    resposta: str