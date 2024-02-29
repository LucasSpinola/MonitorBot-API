from fastapi import HTTPException, APIRouter, UploadFile, File, Depends, Body
import json
import httpx
from decouple import config
from app.models.aluno_models import Alunos, AlunoPres, AlunoCadastrar
import requests
import pandas as pd
import io
from app.services.user_service import get_current_user

alunos_router = APIRouter()

BD_FIRE = config("URL_DB")

@alunos_router.post("/cria_aluno/", summary="Cria um aluno no banco de dados")
async def cria_aluno(aluno_data: Alunos, current_user: str = Depends(get_current_user)):
    url = f'{BD_FIRE}/alunos.json'
    url2 = f'{BD_FIRE}/presencas/{aluno_data.turma}/.json'
    aluno_press = AlunoPres(nome=aluno_data.nome, matricula=aluno_data.matricula, sub_turma=aluno_data.sub_turma)
    data_dict = aluno_data.dict()
    data_dict2 = aluno_press.dict()
    json_aluno = json.dumps(data_dict)
    json_aluno2 = json.dumps(data_dict2)
    async with httpx.AsyncClient() as client:
        try:
            requisicao = await client.post(url, data=json_aluno)
            requisicao2 = await client.post(url2, data=json_aluno2)
            if requisicao.status_code // 100 == 2:
                return {"mensagem": "Aluno adicionado à turma com sucesso"}
            else:
                raise HTTPException(status_code=500, detail="Erro ao adicionar o aluno à turma")
        except httpx.HTTPError as http_err:
            raise HTTPException(status_code=501, detail="Erro de conexão")
        
@alunos_router.put("/edita_aluno/{aluno_id}", summary="Edita um aluno no banco de dados")
async def edita_aluno(aluno_id: str, aluno_data: Alunos, current_user: str = Depends(get_current_user)):
    url = f'{BD_FIRE}/alunos/{aluno_id}.json'
    
    data_dict = aluno_data.dict()
    json_aluno = json.dumps(data_dict)
    
    async with httpx.AsyncClient() as client:
        try:
            requisicao = await client.put(url, data=json_aluno)
            if requisicao.status_code // 100 == 2:
                return {"mensagem": "Detalhes do aluno atualizados com sucesso"}
            else:
                raise HTTPException(status_code=500, detail="Erro ao editar os detalhes do aluno")
        except httpx.HTTPError as http_err:
            raise HTTPException(status_code=501, detail="Erro de conexão")
        
@alunos_router.delete("/deleta_aluno/{aluno_id}", summary="Deleta um aluno no banco de dados")
async def deleta_aluno(aluno_id: str, current_user: str = Depends(get_current_user)):
    url = f'{BD_FIRE}/alunos/{aluno_id}.json'
    async with httpx.AsyncClient() as client:
        try:
            requisicao = await client.delete(url)
            if requisicao.status_code // 100 == 2:
                return {"mensagem": "Aluno removido da turma com sucesso"}
            elif requisicao.status_code == 404:
                raise HTTPException(status_code=404, detail="Aluno não encontrado na turma")
            else:
                raise HTTPException(status_code=500, detail="Erro ao deletar o aluno da turma")
        except httpx.HTTPError as http_err:
            raise HTTPException(status_code=501, detail="Erro de conexão")

@alunos_router.get("/lista_alunos/", response_model=dict, summary="Lista todos os alunos do banco de dados")
async def lista_alunos(current_user: str = Depends(get_current_user)):
    url = f'{BD_FIRE}/alunos.json'
    
    async with httpx.AsyncClient() as client:
        try:
            requisicao = await client.get(url)
            if requisicao.status_code == 200:
                dados_alunos = requisicao.json()
                return dados_alunos
            elif requisicao.status_code == 404:
                raise HTTPException(status_code=404, detail="Turma não encontrada")
            else:
                raise HTTPException(status_code=500, detail="Erro ao listar os alunos da turma")
        except httpx.HTTPError as http_err:
            raise HTTPException(status_code=501, detail="Erro de conexão")

@alunos_router.get("/le_aluno/{id_discord}", summary="Lê os detalhes de um aluno a partir do ID do aluno")
async def le_aluno(id_discord: str, current_user: str = Depends(get_current_user)):
    url = f'{BD_FIRE}/alunos.json'
    async with httpx.AsyncClient() as client:
        try:
            requisicao = await client.get(url)
            if requisicao.status_code == 200:
                dados_alunos = requisicao.json()
                for aluno_id, aluno_data in dados_alunos.items():
                    if aluno_data.get('id_discord') == id_discord:
                        return {aluno_id: aluno_data}
                raise HTTPException(status_code=404, detail="Aluno não encontrado")
            else:
                raise HTTPException(status_code=500, detail="Erro ao buscar o ID do aluno por matrícula")
        except httpx.HTTPError as http_err:
            raise HTTPException(status_code=501, detail="Erro de conexão")
    
        
@alunos_router.get("/alunos_por_turma/{turma}", response_model=dict, summary="Lista todos os alunos de uma turma")
async def alunos_por_turma(turma: str, current_user: str = Depends(get_current_user)):
    url = f'{BD_FIRE}/alunos.json'
    
    async with httpx.AsyncClient() as client:
        try:
            requisicao = await client.get(url)
            if requisicao.status_code == 200:
                dados_alunos = requisicao.json()
                alunos_turma_lop = [aluno for aluno in dados_alunos.values() if aluno.get('turma') == turma]
                return alunos_turma_lop
            else:
                raise HTTPException(status_code=500, detail="Erro ao buscar os alunos por turma")
        except httpx.HTTPError as http_err:
            raise HTTPException(status_code=501, detail="Erro de conexão")

@alunos_router.post("/upar_alunos/", summary="Faz o upload de alunos para uma turma")
async def upar_alunos(sigla: str, file: UploadFile = File(...), current_user: str = Depends(get_current_user)):
    if file.filename.endswith('.csv'):
        contents = await file.read()
        df = pd.read_csv(io.BytesIO(contents)) 
        response = requests.get(f'{BD_FIRE}/alunos/.json')
        if response.status_code == 200:
            alunos_firebase = response.json()
            if alunos_firebase:
                alunos_cadastrados_firebase = [aluno['nome'] for aluno in alunos_firebase.values()]
            else:
                alunos_cadastrados_firebase = []
        else:
            return {"message": "Erro ao obter alunos do Firebase."}
        alunos_novos = []
        for index, row in df.iterrows():
            nome = row['Nome']
            matricula = row['Matrícula']
            turma = row['sub_turma']
            if nome not in alunos_cadastrados_firebase:
                dicionario_aluno = {'nome': nome, 'matricula': matricula, 'turma': sigla, 'sub_turma': turma,'id_discord': 0}
                json_aluno = json.dumps(dicionario_aluno)
                requisicao = requests.post(f'{BD_FIRE}/alunos/.json', data=json_aluno)
                dicionario_aluno2 = {'nome': nome, 'matricula': matricula,'sub-turma': turma}
                json_aluno2 = json.dumps(dicionario_aluno2)
                requisicao2 = requests.post(f'{BD_FIRE}/presencas/{sigla}/.json', data=json_aluno2)
                if requisicao.status_code == 200:
                    alunos_novos.append(nome)
        if alunos_novos:
            return {"message": f"Alunos cadastrados com sucesso"}
        else:
            return {"message": "Nenhum aluno novo cadastrado."}
    else:
        return {"message": "Por favor, faça o upload de um arquivo CSV."}


@alunos_router.post("/adicionar_id_discord/", summary="Adicionar id do discord ao aluno")
async def adicionar_id(alunos_data: AlunoCadastrar, current_user: str = Depends(get_current_user), ):
    requisicao = requests.get(f'{BD_FIRE}/alunos.json')
    for id in requisicao.json():
        if alunos_data.matricula == requisicao.json()[id]['matricula']:
            if requisicao.json()[id]['id_discord'] == 0 or requisicao.json()[id]['id_discord'] == '0':
                dicionario_aluno = {'id_discord': alunos_data.id_discord}
                json_aluno = json.dumps(dicionario_aluno)
                requisicao_patch = requests.patch(f'{BD_FIRE}/alunos/{id}/.json', data=json_aluno)
                if requisicao_patch.status_code == 200:
                    resposta = requisicao_patch.json()
                    if resposta['id_discord'] == alunos_data.id_discord:
                        return {"mensagem": "Id cadastrado com sucesso"}
                    else:
                        return {"mensagem": "Erro ao atualizar o ID Discord. Tente novamente."}
            else:
                return {"mensagem": "O ID Discord já está cadastrado para esta matrícula."}
    return {"mensagem": "Matricula não encontrada no banco de dados"}



@alunos_router.get("/testar_matricula/{id_discord}", summary="Testar id para retornar se a matrícula já está cadastrada")
async def testar_matricula(id_discord: str, current_user: str = Depends(get_current_user)):
    requisicao = requests.get(f'{BD_FIRE}/alunos/.json')
    for id in requisicao.json():
        if id_discord == requisicao.json()[id]['id_discord']:
            return {"mensagem": requisicao.json()[id]['id_discord']}
        else:
            print(id_discord)
            return {"mensagem": "Matricula não encontrada no banco de dados"}