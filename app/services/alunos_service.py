from fastapi import HTTPException, UploadFile, File
import json
import httpx
from decouple import config
from models.aluno_models import Alunos, AlunoPres, AlunoCadastrar
import requests
import pandas as pd
import io

BD_FIRE = config("URL_DB")

async def criaaluno(aluno_data: Alunos):
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
        
async def editaaluno(matricula: int, aluno_data: Alunos):
    url_alunos = f'{BD_FIRE}/alunos.json'
    async with httpx.AsyncClient() as client:
        try:
            requisicao_alunos = await client.get(url_alunos)
            if requisicao_alunos.status_code == 200:
                dados_alunos = requisicao_alunos.json()
                for aluno_id, aluno_info in dados_alunos.items():
                    if aluno_info.get('matricula') == matricula:
                        url_aluno = f'{BD_FIRE}/alunos/{aluno_id}.json'
                        data_dict = aluno_data.dict()
                        json_aluno = json.dumps(data_dict)
                        requisicao = await client.put(url_aluno, data=json_aluno)
                        if requisicao.status_code // 100 == 2:
                            return {"mensagem": "Detalhes do aluno atualizados com sucesso"}
                        else:
                            raise HTTPException(status_code=500, detail="Erro ao editar os detalhes do aluno")
                raise HTTPException(status_code=404, detail="Aluno não encontrado na turma")
            else:
                raise HTTPException(status_code=500, detail="Erro ao buscar os alunos da turma")
        except httpx.HTTPError as http_err:
            raise HTTPException(status_code=501, detail="Erro de conexão")
        
async def deletaaluno(matricula: int):
    url_alunos = f'{BD_FIRE}/alunos.json'
    async with httpx.AsyncClient() as client:
        try:
            requisicao_alunos = await client.get(url_alunos)
            if requisicao_alunos.status_code == 200:
                dados_alunos = requisicao_alunos.json()
                for aluno_id, aluno_data in dados_alunos.items():
                    if aluno_data.get('matricula') == matricula:
                        url_aluno = f'{BD_FIRE}/alunos/{aluno_id}.json'
                        await client.delete(url_aluno)
                        
                        turma = aluno_data.get("turma")
                        url_presenca = f'{BD_FIRE}/presencas/{turma}.json'
                        requisicao_presenca = await client.get(url_presenca)
                        if requisicao_presenca.status_code == 200:
                            presencas_turma = requisicao_presenca.json()
                            for id_presenca, presenca_aluno in presencas_turma.items():
                                if presenca_aluno.get("matricula") == matricula:
                                    url_presenca_aluno = f'{BD_FIRE}/presencas/{turma}/{id_presenca}.json'
                                    await client.delete(url_presenca_aluno)
                        
                        return {"mensagem": "Aluno removido da turma com sucesso"}
                raise HTTPException(status_code=404, detail="Aluno não encontrado na turma")
            else:
                raise HTTPException(status_code=500, detail="Erro ao deletar o aluno da turma")
        except httpx.HTTPError as http_err:
            raise HTTPException(status_code=501, detail="Erro de conexão")

async def listaalunos():
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

async def lealuno(id_discord: str):
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
    
async def buscaaluno(matricula: int):
    url = f'{BD_FIRE}/alunos.json'
    async with httpx.AsyncClient() as client:
        try:
            requisicao = await client.get(url)
            if requisicao.status_code == 200:
                dados_alunos = requisicao.json()
                for aluno_id, aluno_data in dados_alunos.items():
                    if aluno_data.get('matricula') == matricula:
                        return {aluno_id: aluno_data}
                raise HTTPException(status_code=404, detail="Aluno não encontrado")
            else:
                raise HTTPException(status_code=500, detail="Erro ao buscar o ID do aluno por matrícula")
        except httpx.HTTPError as http_err:
            raise HTTPException(status_code=501, detail="Erro de conexão")
        
async def alunosporturma(turma: str):
    url = f'{BD_FIRE}/alunos.json'
    
    async with httpx.AsyncClient() as client:
        try:
            requisicao = await client.get(url)
            if requisicao.status_code == 200:
                dados_alunos = requisicao.json()
                alunos_turma_lop = [aluno for aluno in dados_alunos.values() if aluno.get('turma') == turma]
                if not alunos_turma_lop:
                    raise HTTPException(status_code=404, detail="Turma não encontrada")
                return {"alunos": alunos_turma_lop}
            else:
                raise HTTPException(status_code=500, detail="Erro ao buscar os alunos por turma")
        except httpx.HTTPError as http_err:
            raise HTTPException(status_code=501, detail="Erro de conexão")

async def uparalunos(sigla: str, file: UploadFile = File(...)):
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

async def adicionarid(alunos_data: AlunoCadastrar):
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

async def atualizaid(alunos_data: AlunoCadastrar):
    requisicao = requests.get(f'{BD_FIRE}/alunos.json')
    for id in requisicao.json():
        if alunos_data.matricula == requisicao.json()[id]['matricula']:
            if requisicao.json()[id]['id_discord'] == alunos_data.id_discord:
                return {"mensagem": "O ID Discord já está cadastrado para esta matrícula."}
            else:
                dicionario_aluno = {'id_discord': alunos_data.id_discord}
                json_aluno = json.dumps(dicionario_aluno)
                requisicao_patch = requests.patch(f'{BD_FIRE}/alunos/{id}/.json', data=json_aluno)
                if requisicao_patch.status_code == 200:
                    resposta = requisicao_patch.json()
                    if resposta['id_discord'] == alunos_data.id_discord:
                        return {"mensagem": "Id atualizado com sucesso"}
                    else:
                        return {"mensagem": "Erro ao atualizar o ID Discord. Tente novamente."}
    return {"mensagem": "Matricula não encontrada no banco de dados"}

async def testarmatricula(id_discord: str):
    requisicao = requests.get(f'{BD_FIRE}/alunos/.json')
    for id in requisicao.json():
        if id_discord == requisicao.json()[id]['id_discord']:
            return {"mensagem": requisicao.json()[id]['id_discord']}
        else:
            print(id_discord)
            return {"mensagem": "Matricula não encontrada no banco de dados"}
        