from fastapi import APIRouter, HTTPException, Depends
from decouple import config
from app.models.permissao_models import Permissao
import requests
from app.services.user_service import get_current_user

BD_FIRE = config("URL_DB")

async def criapermissao(permissao: Permissao):
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
    
async def editarpermissao(permissao_id: str, permissao: Permissao):
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

async def excluirpermissao(permissao_id: str):
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
    
async def pegarusuariocompermissao(id_discord: str):
    requisicao = requests.get(f'{BD_FIRE}/permissao/.json')
    for id in requisicao.json():
        if id_discord == requisicao.json()[id]['id']:
            return requisicao.json()[id]
    raise HTTPException(status_code=404, detail="Usuário não encontrado no banco de dados")

async def listatodosusuarioscompermissao():
    requisicao = requests.get(f'{BD_FIRE}/permissao.json')
    if requisicao.status_code != 200:
        raise HTTPException(status_code=500, detail="Erro ao acessar os dados de permissão")
    
    lista_permisssao = []
    for id in requisicao.json():
        lista_permisssao.append(requisicao.json()[id])
    return {"permissoes": lista_permisssao}