from fastapi import APIRouter, Depends
from app.services.miniteste_service import criaminiteste, obterminiteste, adicionarrespostaaluno, editarminiteste, obterrespostasminitestealuno, obterrespostasminitestealunos, deletarminiteste, listar_minitestes
from app.models.miniteste_models import Miniteste, MinitesteResposta
from app.services.user_service import get_current_user

miniteste_router = APIRouter()

@miniteste_router.post("/criar", summary="Criar miniteste")
async def criar_miniteste(miniteste: Miniteste, current_user: str = Depends(get_current_user)):
    return await criaminiteste(miniteste)

@miniteste_router.get("/pegar/{teste}", summary="Obter miniteste")
async def obter_miniteste(teste: str, current_user: str = Depends(get_current_user)):
    return await obterminiteste(teste)

@miniteste_router.post("/adicionar/resposta", summary="Adicionar resposta do aluno")
async def adicionar_resposta_aluno(miniteste: MinitesteResposta, current_user: str = Depends(get_current_user)):
    return await adicionarrespostaaluno(miniteste)
    
@miniteste_router.patch("/editar/{miniteste_id}", summary="Editar miniteste")
async def editar_miniteste(miniteste_id: str, miniteste: Miniteste, current_user: str = Depends(get_current_user)):
    return await editarminiteste(miniteste_id, miniteste)

@miniteste_router.get("/aluno/{sigla}/{matricula}", summary="Obter respostas de miniteste de um aluno")
async def obter_respostas_miniteste_aluno(sigla: str, matricula: int, current_user: str = Depends(get_current_user)):
    return await obterrespostasminitestealuno(sigla, matricula)

@miniteste_router.get("/alunos/{sigla}", summary="Obter respostas de miniteste de todos os alunos")
async def obter_respostas_miniteste_alunos(sigla: str, current_user: str = Depends(get_current_user)):
    return await obterrespostasminitestealunos(sigla)

@miniteste_router.delete("/deletar/{miniteste_id}", summary="Deletar miniteste")
async def deletar_miniteste(miniteste_id: str, current_user: str = Depends(get_current_user)):
    return await deletarminiteste(miniteste_id)

@miniteste_router.get("/listar_minitestes/", summary="Listar minitestes")
async def lista_minitestes(current_user: str = Depends(get_current_user)):
    return await listar_minitestes()