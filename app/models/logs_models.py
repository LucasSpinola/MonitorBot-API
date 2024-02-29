from pydantic import BaseModel

class LogsCreate(BaseModel):
    id_discord: int
    pergunta: str
    data: str
