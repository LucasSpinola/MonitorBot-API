from fastapi import UploadFile, File, APIRouter, HTTPException, Depends
import requests
from models.unidade_models import Unidade
from decouple import config
import pandas as pd
import io
import json

BD_FIRE = config("URL_DB")

async def criarunidade(sigla: str, unidade: Unidade):
    nova_unidade = {"Data": unidade.Data, "HoraInicial": unidade.HoraInicial, "HoraFinal": unidade.HoraFinal, "Aula": unidade.Aula}
    response = requests.post(f'{BD_FIRE}/unidades/{sigla}/.json', json=nova_unidade)
    if response.status_code == 200:
        return {"message": f"Unidade criada com sucesso para a turma {sigla} na data {unidade.Data}"}
    else:
        raise HTTPException(status_code=response.status_code, detail="Erro ao criar a unidade no banco de dados")

async def editarunidade(sigla: str, id_unidade: str, unidade: Unidade):
    url = f'{BD_FIRE}/unidades/{sigla}/{id_unidade}.json'
    response = requests.get(url)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Unidade não encontrada para edição")
    unidade_atualizada = {"Data": unidade.Data, "HoraInicial": unidade.HoraInicial, "HoraFinal": unidade.HoraFinal}
    response = requests.put(url, json=unidade_atualizada)
    if response.status_code == 200:
        return {"message": f"Unidade com ID {id_unidade} editada com sucesso na turma {sigla}"}
    else:
        raise HTTPException(status_code=response.status_code, detail="Erro ao editar a unidade no banco de dados")

async def obterunidadespordata(sigla: str, data: str):
    response = requests.get(f'{BD_FIRE}/unidades/{sigla}/.json')
    if response.status_code == 200:
        unidades_firebase = response.json()
        unidades_por_data = [unidade for unidade in unidades_firebase.values() if unidade.get('Data') == data]
        if unidades_por_data:
            return {"unidades": unidades_por_data}
        else:
            raise HTTPException(status_code=404, detail=f"Nenhuma unidade encontrada para a data {data} na turma {sigla}")
    else:
        raise HTTPException(status_code=500, detail="Erro ao obter unidades do banco de dados")
    
async def uparunidades(sigla: str, file: UploadFile = File(...)):
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
            aula = row['Aula']
            if data not in alunos_cadastrados_firebase:
                dicionario_unidade = {'Data': data, 'HoraInicial': hora_inicial, 'HoraFinal': hora_final, 'Aula': aula}
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

async def obterlistaunidades(sigla: str):
    response = requests.get(f'{BD_FIRE}/unidades/{sigla}/.json')
    if response.status_code == 200:
        unidades_firebase = response.json()
        return {"unidades": unidades_firebase}
    else:
        raise HTTPException(status_code=500, detail="Erro ao obter unidades do banco de dados")

async def obteridunidade(sigla: str, data: str):
    response = requests.get(f'{BD_FIRE}/unidades/{sigla}/.json')
    if response.status_code == 200:
        unidades_firebase = response.json()
        for id_unidade, unidade in unidades_firebase.items():
            if unidade.get('Data') == data:
                return {"id_unidade": id_unidade}
        raise HTTPException(status_code=404, detail=f"Nenhuma unidade encontrada para a data {data} na turma {sigla}")
    else:
        raise HTTPException(status_code=500, detail="Erro ao obter unidades do banco de dados")
    

async def deletarunidade(sigla: str, id_unidade: str):
    url = f'{BD_FIRE}/unidades/{sigla}/{id_unidade}.json'
    response = requests.get(url)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Unidade não encontrada para exclusão")

    response = requests.delete(url)
    if response.status_code == 200:
        return {"message": f"Unidade com ID {id_unidade} deletada com sucesso na turma {sigla}"}
    else:
        raise HTTPException(status_code=response.status_code, detail="Erro ao deletar a unidade do banco de dados")