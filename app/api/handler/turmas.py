from fastapi import Depends, HTTPException, APIRouter
import json
import httpx
import os
from app.models.turma_models import TurmaCreate
from decouple import config
from app.services.user_service import get_current_user
import requests
import logging

turmas_router = APIRouter()

BD_FIRE = config("URL_DB")

@turmas_router.post("/cria_turma/", summary="Cria uma turma no banco de dados") 
async def cria_turma(turma_data: TurmaCreate, current_user: str = Depends(get_current_user)):
    url = f'{BD_FIRE}/turmas/{turma_data.sigla}/.json'
    data_dict = turma_data.dict()
    data_dict.pop('sigla')
    json_turma = json.dumps(data_dict)
    async with httpx.AsyncClient() as client:
        try:
            requisicao = await client.post(url, data=json_turma)
            if requisicao.status_code // 100 == 2:
                return {"mensagem": f"Turma <{turma_data.sigla}> criada com sucesso"}
            else:
                raise HTTPException(status_code=500, detail=f"Erro ao criar a turma <{turma_data.sigla}>")
        except httpx.HTTPError as http_err:
            raise HTTPException(status_code=501, detail=f"Erro de conexão")

@turmas_router.put("/editar_turma/{sigla}", summary="Edita uma turma no banco de dados")
async def editar_turma(sigla: str, turma_data: TurmaCreate, current_user: str = Depends(get_current_user)):
    url = f'{BD_FIRE}/turmas/{sigla}/.json'
    data_dict = turma_data.dict()
    json_turma = json.dumps(data_dict)
    async with httpx.AsyncClient() as client:
        try:
            requisicao = await client.put(url, data=json_turma)
            if requisicao.status_code // 100 == 2:
                return {"mensagem": f"Turma <{sigla}> editada com sucesso"}
            else:
                raise HTTPException(status_code=500, detail=f"Erro ao editar a turma <{sigla}>")
        except httpx.HTTPError as http_err:
            raise HTTPException(status_code=501, detail=f"Erro de conexão")


@turmas_router.get("/listar_turmas/", summary="Lista todas as turmas do banco de dados")
async def listar_turmas(current_user: str = Depends(get_current_user)):
    url = f'{BD_FIRE}/turmas/.json'
    async with httpx.AsyncClient() as client:
        try:
            requisicao = await client.get(url)
            if requisicao.status_code // 100 == 2:
                dados_turmas = requisicao.json()
                return dados_turmas
            else:
                raise HTTPException(status_code=500, detail="Erro ao listar a turma")
        except httpx.HTTPError as http_err:
            raise HTTPException(status_code=501, detail="Erro de conexão")
    
@turmas_router.get("/ler_turma/{sigla}", summary="Lê os detalhes de uma turma")
async def ler_turma(sigla: str, current_user: str = Depends(get_current_user)):
    url = f'{BD_FIRE}/turmas/{sigla}/.json'
    async with httpx.AsyncClient() as client:
        try:
            requisicao = await client.get(url)
            if requisicao.status_code == 200:
                dados_turma = requisicao.json()
                if dados_turma is None:
                    raise HTTPException(status_code=404, detail=f"Turma <{sigla}> não encontrada")
                return dados_turma
            elif requisicao.status_code == 404:
                raise HTTPException(status_code=404, detail=f"Turma <{sigla}> não encontrada")
            else:
                raise HTTPException(status_code=500, detail=f"Erro ao ler a turma <{sigla}>")
        except httpx.HTTPError as http_err:
            raise HTTPException(status_code=501, detail="Erro de conexão")

@turmas_router.get("/ler_turma_professor/{id_docente}", summary="Lê os detalhes de uma turma a partir do ID do professor")
async def turma_por_professor(id_docente: str, current_user: str = Depends(get_current_user)):
    url = f'{BD_FIRE}/turmas.json'
    async with httpx.AsyncClient() as client:
        try:
            requisicao = await client.get(url)
            if requisicao.status_code == 200:
                dados_turmas = requisicao.json()
                if not dados_turmas:
                    raise HTTPException(status_code=404, detail="Não há turmas disponíveis no momento")
                turmas_professor = {}
                for turma_codigo, turma_data in dados_turmas.items():
                    for turma_id, turma_info in turma_data.items():
                        if turma_info.get('id_docente') == id_docente:
                            turmas_professor[turma_codigo] = {turma_id: turma_info}
                if turmas_professor:
                    return turmas_professor
                else:
                    raise HTTPException(status_code=404, detail="Turmas não encontradas para este professor")
            else:
                raise HTTPException(status_code=500, detail="Erro ao obter os dados das turmas")
        except httpx.HTTPError as http_err:
            raise HTTPException(status_code=501, detail="Erro de conexão")


@turmas_router.delete("/deletar_turma/{sigla}", summary="Deleta uma turma no banco de dados")
async def deletar_turma(sigla: str, current_user: str = Depends(get_current_user)):
    url = f'{BD_FIRE}/turmas/{sigla}/.json'
    async with httpx.AsyncClient() as client:
        try:
            requisicao = await client.delete(url)
            if requisicao.status_code // 100 == 2:
                return {"mensagem": f"Turma <{sigla}> deletada com sucesso"}
            elif requisicao.status_code == 404:
                raise HTTPException(status_code=404, detail=f"Turma <{sigla}> não encontrada")
            else:
                raise HTTPException(status_code=500, detail=f"Erro ao deletar a turma <{sigla}>")
        except httpx.HTTPError as http_err:
            raise HTTPException(status_code=501, detail="Erro de conexão")