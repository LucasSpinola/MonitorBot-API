from pydantic import BaseModel

class PresencaCreate(BaseModel):
    matricula: int
    sigla: str
    
class MarcarPresenca(BaseModel):
    sigla: str
    matricula: int
    aula: str
    data: str

class PresencaGet(BaseModel):
    sigla: str
    matricula: int

class PresencaEdit(BaseModel):
    sigla: str
    matricula: int
    data: str
    presenca: str