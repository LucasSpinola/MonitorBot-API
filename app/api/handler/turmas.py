from fastapi import Depends, APIRouter
from models.turma_models import TurmaCreate
from services.user_service import get_current_user
from services.turma_services import criaturma, editarturmas, listarturmas, lerturma, turmaporprofessor, numeroalunosturma, deletarturma

turmas_router = APIRouter()

@turmas_router.post("/cria_turma/", summary="Cria uma turma no banco de dados") 
async def cria_turma(turma_data: TurmaCreate, current_user: str = Depends(get_current_user)):
    return await criaturma(turma_data)

@turmas_router.put("/editar_turma/{sigla}", summary="Edita uma turma no banco de dados")
async def editar_turma(sigla: str, turma_data: TurmaCreate, current_user: str = Depends(get_current_user)):
    return await editarturmas(sigla, turma_data)

@turmas_router.get("/listar_turmas/", summary="Lista todas as turmas do banco de dados")
async def listar_turmas(current_user: str = Depends(get_current_user)):
    return await listarturmas()
    
@turmas_router.get("/ler_turma_professor/{id_docente}", summary="Lê as turmas de um professor")
async def ler_turma(id_docente: str, current_user: str = Depends(get_current_user)):
    return await turmaporprofessor(id_docente)

@turmas_router.get("/ler_turma_professor/{id_docente}", summary="Lê os detalhes de uma turma a partir do ID do professor")
async def turma_por_professor(id_docente: str, current_user: str = Depends(get_current_user)):
    return await turmaporprofessor(id_docente)

@turmas_router.get("/numero_alunos_turma/{sigla}", summary="Conta o número de alunos de uma turma")
async def numero_alunos_turma(sigla: str, current_user: str = Depends(get_current_user)):
    return await numeroalunosturma(sigla)

@turmas_router.delete("/deletar_turma/{sigla}", summary="Deleta uma turma no banco de dados")
async def deletar_turma(sigla: str, current_user: str = Depends(get_current_user)):
    return await deletarturma(sigla)