from fastapi import APIRouter, Depends
from api.handler.user import get_current_user
from models.whatsapp_models import WhatsappCreate, WhatsappMatricula
from services.whatsapp_service import adicionar_numero, excluir_numero, editar_numero, obter_telefone

whatsapp_router = APIRouter()

@whatsapp_router.post("/adicionar_numero/", summary="Adicionar numero de telefone ao aluno")
async def adicionar_telefone(alunos_data: WhatsappCreate, current_user: str = Depends(get_current_user)):
    return await adicionar_numero(alunos_data)

@whatsapp_router.patch("/editar_numero/", summary="Editar o numero do telefone ao aluno")
async def excluir_telefone(alunos_data: WhatsappCreate, current_user: str = Depends(get_current_user)):
    return await editar_numero(alunos_data)

@whatsapp_router.post("/obter_numero/", summary="Pegar o numero do telefone do aluno")
async def excluir_telefone(alunos_data: WhatsappMatricula, current_user: str = Depends(get_current_user)):
    return await obter_telefone(alunos_data)

@whatsapp_router.delete("/excluir_numero/", summary="Excluir numero do telefone do aluno")
async def excluir_telefone(alunos_data: WhatsappMatricula, current_user: str = Depends(get_current_user)):
    return await excluir_numero(alunos_data)