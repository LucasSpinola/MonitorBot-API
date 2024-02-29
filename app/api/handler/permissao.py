from fastapi import APIRouter, HTTPException, Depends
from decouple import config
from app.models.permissao_models import Permissao
import requests
from app.services.user_service import get_current_user

permissao_router = APIRouter()

BD_FIRE = config("URL_DB")

from fastapi import HTTPException

@permissao_router.post("/adicionar/", summary="Cria uma nova permissão no banco de dados")
async def cria_narrativo(permissao: Permissao, current_user: str = Depends(get_current_user)):
    requisicao = requests.get(f'{BD_FIRE}/permissao/.json')
    if requisicao.status_code == 200:
        dados_permissao = requisicao.json()
        if dados_permissao:
            for id_permissao, info_permissao in dados_permissao.items():
                if permissao.nome == info_permissao['nome']:
                    return {"mensagem": f"Permissão para '{permissao.nome}' já existe no banco de dados"}
        permissao_dict = permissao.dict()
        requisicao_nova_permissao = requests.post(f'{BD_FIRE}/permissao/.json', json=permissao_dict)
        if requisicao_nova_permissao.status_code == 200:
            return {"mensagem": "Permissão criada com sucesso"}
        else:
            raise HTTPException(status_code=500, detail="Erro ao criar permissão")
    else:
        raise HTTPException(status_code=500, detail="Erro ao acessar o banco de dados de permissão")

@permissao_router.put("/editar/{permissao_id}/", summary="Editar uma permissão existente")
async def editar_permissao(permissao_id: str, permissao: Permissao, current_user: str = Depends(get_current_user)):
    requisicao = requests.get(f'{BD_FIRE}/permissao/{permissao_id}.json')
    if requisicao.status_code == 200:
        requisicao_json = requisicao.json()
        if requisicao_json:
            dados_atualizados = {**requisicao_json, **permissao.dict()}
            requisicao_atualizacao = requests.put(f'{BD_FIRE}/permissao/{permissao_id}.json', json=dados_atualizados)
            if requisicao_atualizacao.status_code == 200:
                return {"mensagem": "Permissão atualizada com sucesso"}
            else:
                raise HTTPException(status_code=500, detail="Erro ao atualizar permissão")
        else:
            raise HTTPException(status_code=404, detail="Permissão não encontrada")
    else:
        raise HTTPException(status_code=500, detail="Erro ao acessar o banco de dados de permissão")

@permissao_router.delete("/excluir/{permissao_id}/", summary="Excluir uma permissão existente")
async def excluir_permissao(permissao_id: str, current_user: str = Depends(get_current_user)):
    requisicao = requests.get(f'{BD_FIRE}/permissao/{permissao_id}.json')
    if requisicao.status_code == 200:
        requisicao_json = requisicao.json()
        if requisicao_json:
            requisicao_exclusao = requests.delete(f'{BD_FIRE}/permissao/{permissao_id}.json')
            if requisicao_exclusao.status_code == 200:
                return {"mensagem": "Permissão excluída com sucesso"}
            else:
                raise HTTPException(status_code=500, detail="Erro ao excluir permissão")
        else:
            raise HTTPException(status_code=404, detail="Permissão não encontrada")
    else:
        raise HTTPException(status_code=500, detail="Erro ao acessar o banco de dados de permissão")
    
@permissao_router.get("/verificar/", summary="Verifica se um usuário tem permissão")
async def listar_usuarios_com_permissao(id_discord: str, current_user: str = Depends(get_current_user)):
    requisicao = requests.get(f'{BD_FIRE}/permissao/.json')
    for id in requisicao.json():
        if id_discord == requisicao.json()[id]['id']:
            return {"permissao": requisicao.json()[id]['id']}
        else:
            return {"mensagem": "Usuário não encontrado no banco de dados"}
        
@permissao_router.get("/pegar_permissao/", summary="Pega a permissão de um usuário")
async def listar_usuarios_com_permissao(id_discord: str, current_user: str = Depends(get_current_user)):
    requisicao = requests.get(f'{BD_FIRE}/permissao/.json')
    for id in requisicao.json():
        if id_discord == requisicao.json()[id]['id']:
            return requisicao.json()[id]
        else:
            return {"mensagem": "Usuário não encontrado no banco de dados"}
        
@permissao_router.get("/listar/", summary="Lista todos os usuarios com permissão existentes")
async def lista_narrativos(current_user: str = Depends(get_current_user)):
    requisicao = requests.get(f'{BD_FIRE}/permissao.json')
    lista_permisssao = []
    for id in requisicao.json():
        lista_permisssao.append(requisicao.json()[id])
    return lista_permisssao