from pydantic import BaseModel
from typing import Optional as Opional

class Pesquisa(BaseModel):
    pergunta: str
    id_discord: str
    data: Opional[str] = None
    
