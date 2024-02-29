from pydantic import BaseModel

class PresencaCreate(BaseModel):
    matricula: int
    sigla: str

class Presenca(BaseModel):
    data: str
    presenca: int
    hora: str
    
