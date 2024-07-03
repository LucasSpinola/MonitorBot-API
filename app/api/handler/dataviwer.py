from fastapi import HTTPException, APIRouter, UploadFile, File, Depends, Body
from services.user_service import get_current_user
from services.dataviwer_service import obterrespostasminitestealunosdata

dataviwer_router = APIRouter()

@dataviwer_router.get("/obter_resposta_miniteste/{sigla}", summary="Obter respostas de miniteste de todos os alunos")
async def obter_respostas_miniteste_alunos(sigla: str, current_user: str = Depends(get_current_user)):
    return await obterrespostasminitestealunosdata(sigla)