from pydantic import BaseModel

class Narrativo(BaseModel):
    pergunta: str
    texto_base: str
    numero: int
    
class RespostaAluno(BaseModel):
    matricula: int
    sigla: str
    numero_gabarito: int
    resposta_aluno: str
    