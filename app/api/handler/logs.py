from fastapi import Depends, APIRouter
from app.models.logs_models import LogsCreate
from app.services.user_service import get_current_user
from app.services.logs_service import logs, deletarlogs, listalogs, lelogs, responderlog
from app.models.pergunta_models import Pergunta

logs_router = APIRouter()

@logs_router.post("/criar_log/", summary="Cria um log no banco de dados") 
async def cria_logs(turma_data: LogsCreate, current_user: str = Depends(get_current_user)):
    return await logs(turma_data)

@logs_router.delete("/deletar_log/{log_id}", summary="Deleta um log no banco de dados")
async def deletar_logs(id: str, current_user: str = Depends(get_current_user)):
    return await deletarlogs(id)

@logs_router.get("/lista_logs/", summary="Lista todos os logs do banco de dados")
async def lista_alunos(current_user: str = Depends(get_current_user)):
    return await listalogs()
    
@logs_router.get("/le_log/{log_id}", summary="Lê os detalhes de um log")
async def le_aluno(id: str, current_user: str = Depends(get_current_user)):
    return await lelogs(id)

@logs_router.post("/responder_log/{log_id}", summary="Responde um log existente no banco de dados")
async def responder_log(id: str, pergunta: Pergunta, current_user: str = Depends(get_current_user)):
    return await responderlog(id, pergunta)