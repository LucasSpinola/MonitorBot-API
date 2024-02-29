from pydantic import BaseModel

class NLPCreate(BaseModel):
    id_discord: str
    mensagem: str