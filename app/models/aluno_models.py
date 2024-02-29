from pydantic import BaseModel

class Alunos(BaseModel):
    nome: str
    matricula: int
    turma: str
    sub_turma: str
    id_discord: str

class AlunoPres(BaseModel):
    nome: str
    matricula: int
    sub_turma: str
    
class AlunoCadastrar(BaseModel):
    matricula: int
    id_discord: str