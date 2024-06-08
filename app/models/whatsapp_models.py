from pydantic import BaseModel

class WhatsappCreate(BaseModel):
    matricula: int
    telefone: str
    
class WhatsappMatricula(BaseModel):
    matricula: int
    
