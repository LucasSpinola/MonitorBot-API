from fastapi import HTTPException, APIRouter, UploadFile, File, Depends, Body
from app.models.aluno_models import Alunos, AlunoPres, AlunoCadastrar
from app.services.user_service import get_current_user
from app.services.alunos_service import criaaluno, editaaluno, deletaaluno, listaalunos, lealuno, buscaaluno, alunosporturma, uparalunos, adicionarid, atualizaid, testarmatricula

alunos_router = APIRouter()

@alunos_router.post("/cria_aluno/", summary="Cria um aluno no banco de dados")
async def cria_aluno(aluno_data: Alunos, current_user: str = Depends(get_current_user)):
    return await criaaluno(aluno_data)
        
@alunos_router.put("/edita_aluno/{matricula}", summary="Edita um aluno no banco de dados por matrícula")
async def edita_aluno(matricula: int, aluno_data: Alunos, current_user: str = Depends(get_current_user)):
    return await editaaluno(matricula, aluno_data)
        
@alunos_router.delete("/deleta_aluno/{matricula}", summary="Deleta um aluno no banco de dados por matrícula")
async def deleta_aluno(matricula: int, current_user: str = Depends(get_current_user)):
    return await deletaaluno(matricula)

@alunos_router.get("/lista_alunos/", response_model=dict, summary="Lista todos os alunos do banco de dados")
async def lista_alunos(current_user: str = Depends(get_current_user)):
    return await listaalunos()

@alunos_router.get("/le_aluno/{id_discord}", summary="Lê os detalhes de um aluno a partir do ID do aluno")
async def le_aluno(id_discord: str, current_user: str = Depends(get_current_user)):
    return await lealuno(id_discord)
    
@alunos_router.get("/busca_aluno/{matricula}", summary="Busca aluno a partir da matricula")
async def busca_aluno(matricula: int, current_user: str = Depends(get_current_user)):
    return await buscaaluno(matricula)
        
@alunos_router.get("/alunos_por_turma/{turma}", response_model=dict, summary="Lista todos os alunos de uma turma")
async def alunos_por_turma(turma: str, current_user: str = Depends(get_current_user)):
    return await alunosporturma(turma)

@alunos_router.post("/upar_alunos/", summary="Faz o upload de alunos para uma turma")
async def upar_alunos(sigla: str, file: UploadFile = File(...), current_user: str = Depends(get_current_user)):
    return await uparalunos(sigla, file)

@alunos_router.post("/adicionar_id_discord/", summary="Adicionar id do discord ao aluno")
async def adicionar_id(alunos_data: AlunoCadastrar, current_user: str = Depends(get_current_user), ):
    return await adicionarid(alunos_data)

@alunos_router.patch("/atualizar_id_discord/", summary="Atualizar id do discord ao aluno")
async def atualiza_id(alunos_data: AlunoCadastrar, current_user: str = Depends(get_current_user)):
    return await atualizaid(alunos_data)

@alunos_router.get("/testar_matricula/{id_discord}", summary="Testar id para retornar se a matrícula já está cadastrada")
async def testar_matricula(id_discord: str, current_user: str = Depends(get_current_user)):
    return await testarmatricula(id_discord)