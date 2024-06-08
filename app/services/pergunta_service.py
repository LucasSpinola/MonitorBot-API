from fastapi import Depends, Form, HTTPException, APIRouter
import json
import httpx
from decouple import config
from app.models.pergunta_models import Pergunta

BD_FIRE = config("URL_DB")

async def criapergunta(pergunta: Pergunta):
    dicionario_pergunta = {'pergunta': pergunta.pergunta, 'resposta': pergunta.resposta}
    json_pergunta = json.dumps(dicionario_pergunta)
    async with httpx.AsyncClient() as client:
        requisicao = await client.post(f'{BD_FIRE}/perguntas/.json', data=json_pergunta)
    if requisicao.status_code // 100 == 2:
        return {"mensagem": "Pergunta criada com sucesso"}
    else:
        raise HTTPException(status_code=500, detail="Erro ao criar a pergunta")

async def editapergunta(id: str, pergunta: Pergunta):
    if pergunta.pergunta == 'pergunta padrão':
        dicionario_pergunta = {'resposta': pergunta.resposta}
    elif pergunta.resposta == 'resposta padrão':
        dicionario_pergunta = {'pergunta': pergunta.pergunta}
    else:
        dicionario_pergunta = {'pergunta': pergunta.pergunta, 'resposta': pergunta.resposta}
    json_pergunta = json.dumps(dicionario_pergunta)
    async with httpx.AsyncClient() as client:
        requisicao = await client.patch(f'{BD_FIRE}/perguntas/{id}/.json', content=json_pergunta)
    if requisicao.status_code // 100 == 2:
        return {"mensagem": "Pergunta editada com sucesso"}
    else:
        raise HTTPException(status_code=500, detail="Erro ao editar a pergunta")
    
async def deletapergunta(id: str):
    async with httpx.AsyncClient() as client:
        get_request = await client.get(f'{BD_FIRE}/perguntas/{id}/.json')
    if get_request.status_code == 200:
        resposta = get_request.json()
        if resposta is not None:
            async with httpx.AsyncClient() as client:
                delete_request = await client.delete(f'{BD_FIRE}/perguntas/{id}/.json')
            if delete_request.status_code // 100 == 2:
                return {"mensagem": "Pergunta deletada com sucesso"}
            else:
                raise HTTPException(status_code=500, detail="Erro ao deletar a pergunta")
    raise HTTPException(status_code=404, detail="Pergunta não encontrada")

async def listaperguntas():
    async with httpx.AsyncClient() as client:
        requisicao = await client.get(f'{BD_FIRE}/perguntas/.json')
    if requisicao.status_code // 100 == 2:
        perguntas = requisicao.json()
        return perguntas
    else:
        raise HTTPException(status_code=500, detail="Erro ao ler as perguntas do banco de dados")
    
async def lepergunta(id: str):
    async with httpx.AsyncClient() as client:
        requisicao = await client.get(f'{BD_FIRE}/perguntas/{id}/.json')
    if requisicao.status_code // 100 == 2:
        pergunta = requisicao.json()
        return pergunta
    else:
        raise HTTPException(status_code=404, detail="Pergunta não encontrada")