from fastapi import HTTPException
import json
import httpx
from decouple import config
from models.logs_models import LogsCreate
from models.pergunta_models import Pergunta


BD_FIRE = config("URL_DB")

async def logs(turma_data: LogsCreate):
    url = f'{BD_FIRE}/logs/.json'
    data_dict = turma_data.dict()
    json_turma = json.dumps(data_dict)
    async with httpx.AsyncClient() as client:
        try:
            requisicao = await client.post(url, data=json_turma)
            if requisicao.status_code // 100 == 2:
                return {"mensagem": "Log criado com sucesso"}
            else:
                raise HTTPException(status_code=500, detail=f"Erro ao criar log")
        except httpx.HTTPError as http_err:
            raise HTTPException(status_code=501, detail=f"Erro de conexão")

async def deletarlogs(id: str):
    url = f'{BD_FIRE}/logs/{id}/.json'
    async with httpx.AsyncClient() as client:
        try:
            requisicao = await client.delete(url)
            if requisicao.status_code // 100 == 2:
                return {"mensagem": "Log deletado com sucesso"}
            elif requisicao.status_code == 404:
                raise HTTPException(status_code=404, detail="Log não encontrado")
            else:
                raise HTTPException(status_code=500, detail="Erro ao deletar o log")
        except httpx.HTTPError as http_err:
            raise HTTPException(status_code=501, detail="Erro de conexão")
        
async def listalogs():
    url = f'{BD_FIRE}/logs/.json'
    async with httpx.AsyncClient() as client:
        try:
            requisicao = await client.get(url)
            if requisicao.status_code == 200:
                dados_alunos = requisicao.json()
                return dados_alunos
            elif requisicao.status_code == 404:
                raise HTTPException(status_code=404, detail="Log não encontrada")
            else:
                raise HTTPException(status_code=500, detail="Erro ao listar os logs")
        except httpx.HTTPError as http_err:
            raise HTTPException(status_code=501, detail="Erro de conexão")
    
async def lelogs(id: str):
    url = f'{BD_FIRE}/logs/{id}.json'
    
    async with httpx.AsyncClient() as client:
        try:
            requisicao = await client.get(url)
            if requisicao.status_code == 200:
                detalhes_aluno = requisicao.json()
                return detalhes_aluno
            elif requisicao.status_code == 404:
                raise HTTPException(status_code=404, detail="Log não encontrado no banco de dados")
            else:
                raise HTTPException(status_code=500, detail="Erro ao ler os detalhes do log")
        except httpx.HTTPError as http_err:
            raise HTTPException(status_code=501, detail="Erro de conexão")

async def responderlog(id: str, pergunta: Pergunta):
    delete_url = f'{BD_FIRE}/logs/{id}.json'
    post_url = f'{BD_FIRE}/perguntas/.json'
    
    async with httpx.AsyncClient() as client:
        try:
            delete_requisicao = await client.delete(delete_url)
            if delete_requisicao.status_code // 100 != 2:
                if delete_requisicao.status_code == 404:
                    raise HTTPException(status_code=404, detail="Log não encontrado")
                else:
                    raise HTTPException(status_code=500, detail="Erro ao deletar o log")

            dicionario_pergunta = {'pergunta': pergunta.pergunta, 'resposta': pergunta.resposta}
            json_pergunta = json.dumps(dicionario_pergunta)
            post_requisicao = await client.post(post_url, data=json_pergunta)
            if post_requisicao.status_code // 100 == 2:
                return {"mensagem": "Log respondido com sucesso"}
            else:
                raise HTTPException(status_code=500, detail="Erro ao criar a pergunta")

        except httpx.HTTPError as http_err:
            raise HTTPException(status_code=501, detail="Erro de conexão")