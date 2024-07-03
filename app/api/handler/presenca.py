from fastapi import APIRouter, Depends
from models.presenca_models import PresencaCreate, MarcarPresenca, PresencaGet, PresencaEdit
from services.user_service import get_current_user
from services.presenca_service import cadastrarpresenca, obterpresencas, editarpresenca, obterfrequenciadiaria, obterfrequencias, marcarpresenca

presenca_router = APIRouter()

@presenca_router.post("/", summary="Registrar presença")
async def presencas(presenca: PresencaCreate, current_user: str = Depends(get_current_user)):
    return await cadastrarpresenca(presenca)

@presenca_router.post("/ver_presenca/", summary="Verificar presença de um aluno na sua turma.")
async def obter_presencas(presenca: PresencaGet, current_user: str = Depends(get_current_user)):
    return await obterpresencas(presenca)

@presenca_router.put("/editar-presenca/", summary="Editar presença de um aluno em uma disciplina")
async def editar_presenca(presenca: PresencaEdit, current_user: str = Depends(get_current_user)):
    return await editarpresenca(presenca)

@presenca_router.get("/pegar_frequencias/{sigla}", response_model=dict, summary="Obter frequências de uma disciplina")
async def obter_frequencias(sigla: str, current_user: str = Depends(get_current_user)):
    return await obterfrequencias(sigla)

@presenca_router.get("/pegar_frequencia_hoje/{sigla}", response_model=dict, summary="Obter frequência diária de uma disciplina")
async def obter_frequencia_diaria(sigla: str, current_user: str = Depends(get_current_user)):
    return await obterfrequenciadiaria(sigla)
        
@presenca_router.post("/marcar-presenca/", summary="Marcar presença em uma data específica")
async def marcar_presenca(presenca: MarcarPresenca, current_user: str = Depends(get_current_user)):
    return await marcarpresenca(presenca)