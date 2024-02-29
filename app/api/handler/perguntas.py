from fastapi import Depends, Form, HTTPException, APIRouter
import json
import httpx
from decouple import config
from app.services.user_service import get_current_user

perguntas_router = APIRouter()

BD_FIRE = config("URL_DB")

@perguntas_router.post("/cria_pergunta/", summary="Cria uma pergunta no banco de dados")
async def cria_pergunta(pergunta: str = Form(...), resposta: str = Form(...), current_user: str = Depends(get_current_user)):
    dicionario_pergunta = {'pergunta': pergunta, 'resposta': resposta}
    json_pergunta = json.dumps(dicionario_pergunta)
    async with httpx.AsyncClient() as client:
        requisicao = await client.post(f'{BD_FIRE}/perguntas/.json', data=json_pergunta)
    if requisicao.status_code // 100 == 2:
        return {"mensagem": "Pergunta criada com sucesso"}
    else:
        print(requisicao.content)
        raise HTTPException(status_code=500, detail="Erro ao criar a pergunta")

@perguntas_router.put("/edita_pergunta/{id}/", summary="Edita uma pergunta no banco de dados")
async def edita_pergunta(id: str, pergunta: str = Form("Nova pergunta"), resposta: str = Form("Nova resposta"), current_user: str = Depends(get_current_user)):
    if pergunta == 'pergunta padrão':
        dicionario_pergunta = {'resposta': resposta}
    elif resposta == 'resposta padrão':
        dicionario_pergunta = {'pergunta': pergunta}
    else:
        dicionario_pergunta = {'pergunta': pergunta, 'resposta': resposta}
    json_pergunta = json.dumps(dicionario_pergunta)
    async with httpx.AsyncClient() as client:
        requisicao = await client.patch(f'{BD_FIRE}/perguntas/{id}/.json', content=json_pergunta)
    if requisicao.status_code // 100 == 2:
        return {"mensagem": "Pergunta editada com sucesso"}
    else:
        raise HTTPException(status_code=500, detail="Erro ao editar a pergunta")
    
@perguntas_router.delete("/deleta_pergunta/{id}/", summary="Deleta uma pergunta no banco de dados")
async def deleta_pergunta(id: str, current_user: str = Depends(get_current_user)):
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

@perguntas_router.get("/lista_perguntas/", summary="Lista todas as perguntas do banco de dados")
async def lista_perguntas(current_user: str = Depends(get_current_user)):
    async with httpx.AsyncClient() as client:
        requisicao = await client.get(f'{BD_FIRE}/perguntas/.json')
    if requisicao.status_code // 100 == 2:
        perguntas = requisicao.json()
        return perguntas
    else:
        raise HTTPException(status_code=500, detail="Erro ao ler as perguntas do banco de dados")
    
@perguntas_router.get("/le_pergunta/{id}/", summary="Lê uma pergunta do banco de dados")
async def le_pergunta(id: str, current_user: str = Depends(get_current_user)):
    async with httpx.AsyncClient() as client:
        requisicao = await client.get(f'{BD_FIRE}/perguntas/{id}/.json')
    if requisicao.status_code // 100 == 2:
        pergunta = requisicao.json()
        return pergunta
    else:
        raise HTTPException(status_code=404, detail="Pergunta não encontrada")