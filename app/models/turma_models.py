from pydantic import BaseModel

class TurmaCreate(BaseModel):
    sigla: str
    periodo: str
    docente: str
    id_docente: str