from fastapi import UploadFile, File, APIRouter, Depends
from app.api.handler.user import get_current_user
from app.models.unidade_models import Unidade
from app.services.unidades_service import criarunidade, editarunidade, obterunidadespordata, uparunidades, deletarunidade, obterlistaunidades, obteridunidade

unidades_router = APIRouter()

@unidades_router.post("/criar_unidade/{sigla}")
async def criarunidade_endpoint(sigla: str, unidade: Unidade, current_user: str = Depends(get_current_user)):
    return await criarunidade(sigla, unidade)

@unidades_router.put("/editar_unidade/{sigla}/{id_unidade}")
async def editarunidade_endpoint(sigla: str, id_unidade: str, unidade: Unidade, current_user: str = Depends(get_current_user)):
    return await editarunidade(sigla, id_unidade, unidade)

@unidades_router.get("/le_unidade/{sigla}/{data}")
async def obter_unidades_por_data(sigla: str, data: str, current_user: str = Depends(get_current_user)):
    return await obterunidadespordata(sigla, data)

@unidades_router.delete("/deletar_unidade/{sigla}/{id_unidade}")
async def deletar_unidade(sigla: str, id_unidade: str, current_user: str = Depends(get_current_user)):
    return await deletarunidade(sigla, id_unidade)

@unidades_router.post("/upar_unidade/")
async def upar_unidades(sigla: str, file: UploadFile = File(...), current_user: str = Depends(get_current_user)):
    return await uparunidades(sigla, file)

@unidades_router.get("/lista_unidade/{sigla}")
async def obter_lista_unidades(sigla: str, current_user: str = Depends(get_current_user)):
    return await obterlistaunidades(sigla)

@unidades_router.get("/id_unidade/{sigla}/{data}")
async def obter_id_unidade(sigla: str, data: str, current_user: str = Depends(get_current_user)):
    return await obteridunidade(sigla, data)