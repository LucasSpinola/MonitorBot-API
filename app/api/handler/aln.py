from fastapi import APIRouter, Depends
from models.aln_models import Narrativo
from services.user_service import get_current_user
from services.narrativo_service import crianarrativo, lerpergunta, editarnarrativo, deletarnarrativo, listanarrativos, pegarnarrativo

aln_router = APIRouter()

@aln_router.post("/adicionar/", summary="Adiciona um novo narrativo ao banco de dados")
async def cria_narrativo(narrativo: Narrativo, current_user: str = Depends(get_current_user)):
    return await crianarrativo(narrativo)

@aln_router.get("/ler_pergunta/{numero}", summary="Lê a pergunta de um narrativo específico pelo número")
async def ler_pergunta(numero: int, current_user: str = Depends(get_current_user)):
    return await lerpergunta(numero)
    
@aln_router.put("/editar_narrativo/{numero}", summary="Edita um narrativo existente pelo número")
async def editar_narrativo(numero: int, novo_narrativo: Narrativo, current_user: str = Depends(get_current_user)):
    return await editarnarrativo(numero, novo_narrativo)

@aln_router.delete("/deletar_narrativo/{numero}", summary="Deleta um narrativo existente pelo número")
async def deletar_narrativo(numero: int, current_user: str = Depends(get_current_user)):
    return await deletarnarrativo(numero)

@aln_router.get("/lista_narrativos/", summary="Lista todos os narrativos existentes")
async def lista_narrativos(current_user: str = Depends(get_current_user)):
    return await listanarrativos()

@aln_router.get("/pegar_narrativo/", summary="Pega as respostas dos narrativos dos alunos")
async def pegar_narrativo(sigla: str, current_user: str = Depends(get_current_user)):
    return await pegarnarrativo(sigla)
