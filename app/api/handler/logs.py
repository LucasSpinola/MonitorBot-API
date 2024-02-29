from fastapi import Depends, HTTPException, APIRouter
import json
import httpx
from decouple import config
from app.models.logs_models import LogsCreate
from app.services.user_service import get_current_user

logs_router = APIRouter()

BD_FIRE = config("URL_DB")

@logs_router.post("/criar_log/", summary="Cria um log no banco de dados") 
async def logs(turma_data: LogsCreate, current_user: str = Depends(get_current_user)):
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

@logs_router.delete("/deletar_log/{log_id}", summary="Deleta um log no banco de dados")
async def deletar_turma(id: str, current_user: str = Depends(get_current_user)):
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

@logs_router.get("/lista_logs/", summary="Lista todos os logs do banco de dados")
async def lista_alunos(current_user: str = Depends(get_current_user)):
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
    
@logs_router.get("/le_log/{log_id}", summary="Lê os detalhes de um log")
async def le_aluno(id: str, current_user: str = Depends(get_current_user)):
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