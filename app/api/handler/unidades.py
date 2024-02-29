import pandas as pd
import io
import json
from fastapi import UploadFile, File, APIRouter, HTTPException, Depends
import requests
from decouple import config
from app.api.handler.user import get_current_user

unidades_router = APIRouter()

BD_FIRE = config("URL_DB")

@unidades_router.post("/criar_unidade/{sigla}")
async def criar_unidade(sigla: str, data: str, hora_inicial: str, hora_final: str, current_user: str = Depends(get_current_user)):
    nova_unidade = {"Data": data, "HoraInicial": hora_inicial, "HoraFinal": hora_final}
    response = requests.post(f'{BD_FIRE}/unidades/{sigla}/.json', json=nova_unidade)
    if response.status_code == 200:
        return {"message": f"Unidade criada com sucesso para a turma {sigla} na data {data}"}
    else:
        raise HTTPException(status_code=response.status_code, detail="Erro ao criar a unidade no banco de dados")

@unidades_router.put("/editar_unidade/{sigla}/{id_unidade}")
async def editar_unidade(sigla: str, id_unidade: str, data: str, hora_inicial: str, hora_final: str, current_user: str = Depends(get_current_user)):
    url = f'{BD_FIRE}/unidades/{sigla}/{id_unidade}.json'
    response = requests.get(url)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Unidade não encontrada para edição")
    unidade_atualizada = {"Data": data, "HoraInicial": hora_inicial, "HoraFinal": hora_final
    }
    response = requests.put(url, json=unidade_atualizada)
    if response.status_code == 200:
        return {"message": f"Unidade com ID {id_unidade} editada com sucesso na turma {sigla}"}
    else:
        raise HTTPException(status_code=response.status_code, detail="Erro ao editar a unidade no banco de dados")

@unidades_router.get("/le_unidade/{sigla}/{data}")
async def obter_unidades_por_data(sigla: str, data: str, current_user: str = Depends(get_current_user)):
    response = requests.get(f'{BD_FIRE}/unidades/{sigla}/.json')
    if response.status_code == 200:
        unidades_firebase = response.json()
        unidades_por_data = [unidade for unidade in unidades_firebase.values() if unidade.get('Data') == data]
        if unidades_por_data:
            return {"unidades": unidades_por_data}
        else:
            return {"message": f"Nenhuma unidade encontrada para a data {data} na turma {sigla}"}
    else:
        return {"message": "Erro ao obter unidades do banco de dados"}

@unidades_router.delete("/deletar_unidade/{sigla}/{id_unidade}")
async def deletar_unidade(sigla: str, id_unidade: str, current_user: str = Depends(get_current_user)):
    url = f'{BD_FIRE}/unidades/{sigla}/{id_unidade}.json'
    response = requests.get(url)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Unidade não encontrada para exclusão")

    response = requests.delete(url)
    if response.status_code == 200:
        return {"message": f"Unidade com ID {id_unidade} deletada com sucesso na turma {sigla}"}
    else:
        raise HTTPException(status_code=response.status_code, detail="Erro ao deletar a unidade do banco de dados")

@unidades_router.post("/upar_unidade/")
async def upar_unidades(sigla: str, file: UploadFile = File(...), current_user: str = Depends(get_current_user)):
    if file.filename.endswith('.csv'):
        contents = await file.read()
        df = pd.read_csv(io.BytesIO(contents))
        expected_columns = ['Data', 'HoraInicial', 'HoraFinal']
        if not all(col in df.columns for col in expected_columns):
            return {"message": "O arquivo CSV não possui colunas válidas."}
        response = requests.get(f'{BD_FIRE}/unidades/{sigla}/.json')
        if response.status_code == 200:
            alunos_firebase = response.json()
            if alunos_firebase:
                alunos_cadastrados_firebase = [aluno['Data'] for aluno in alunos_firebase.values()]
            else:
                alunos_cadastrados_firebase = []
        else:
            return {"message": "Erro ao obter unidades do banco de dados"}
        unidades_novas = []
        for index, row in df.iterrows():
            data = row['Data']
            hora_inicial = row['HoraInicial']
            hora_final = row['HoraFinal']
            if data not in alunos_cadastrados_firebase:
                dicionario_unidade = {'Data': data, 'HoraInicial': hora_inicial, 'HoraFinal': hora_final}
                json_unidade = json.dumps(dicionario_unidade)
                requisicao = requests.post(f'{BD_FIRE}/unidades/{sigla}/.json', data=json_unidade)
                if requisicao.status_code == 200:
                    unidades_novas.append(data)

        if unidades_novas:
            return {"message": f"Unidades cadastradas com sucesso"}
        else:
            return {"message": "Nenhuma unidade nova cadastrada"}
    else:
        return {"message": "Por favor, faça o upload de um arquivo CSV"}

@unidades_router.get("/id_unidade/{sigla}/{data}")
async def obter_id_unidade(sigla: str, data: str, current_user: str = Depends(get_current_user)):
    response = requests.get(f'{BD_FIRE}/unidades/{sigla}/.json')
    if response.status_code == 200:
        unidades_firebase = response.json()
        for id_unidade, unidade in unidades_firebase.items():
            if unidade.get('Data') == data:
                return {"id_unidade": id_unidade}
        return {"message": f"Nenhuma unidade encontrada para a data {data} na turma {sigla}"}
    else:
        return {"message": "Erro ao obter unidades do banco de dados"}