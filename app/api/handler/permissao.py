from fastapi import APIRouter, Depends
from models.permissao_models import Permissao
from services.user_service import get_current_user
from services.permissao_service import criapermissao, editarpermissao, excluirpermissao, pegarusuariocompermissao, listatodosusuarioscompermissao

permissao_router = APIRouter()

@permissao_router.post("/adicionar/", summary="Cria uma nova permissão no banco de dados")
async def criar_permissao(permissao: Permissao, current_user: str = Depends(get_current_user)):
    return await criapermissao(permissao)

@permissao_router.put("/editar/{permissao_id}/", summary="Editar uma permissão existente")
async def editar_permissao(permissao_id: str, permissao: Permissao, current_user: str = Depends(get_current_user)):
    return await editarpermissao(permissao_id, permissao)

@permissao_router.delete("/excluir/{permissao_id}/", summary="Excluir uma permissão existente")
async def excluir_permissao(permissao_id: str, current_user: str = Depends(get_current_user)):
    return await excluirpermissao(permissao_id)
 
@permissao_router.get("/pegar_permissao/{id_discord}", summary="Pega a permissão de um usuário")
async def listar_usuarios_com_permissao(id_discord: str, current_user: str = Depends(get_current_user)):
    return await pegarusuariocompermissao(id_discord)
        
@permissao_router.get("/listar/", summary="Lista todos os usuarios com permissão existentes")
async def lista_narrativos(current_user: str = Depends(get_current_user)):
    return await listatodosusuarioscompermissao()