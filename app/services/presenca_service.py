from fastapi import HTTPException, APIRouter, Depends
import json
import httpx
from decouple import config
from app.models.presenca_models import PresencaCreate, MarcarPresenca, PresencaGet, PresencaEdit
from datetime import datetime
from app.services.user_service import get_current_user
import datetime

BD_FIRE = config("URL_DB")

async def cadastrarpresenca(presenca: PresencaCreate):
    data_atual = datetime.datetime.now()
    data_atual_str = data_atual.strftime("%Y-%m-%d")
    hora_atual = data_atual.strftime("%H:%M:%S")

    async with httpx.AsyncClient() as client:
        requisicao_unidade = await client.get(f'{BD_FIRE}/unidades/{presenca.sigla}.json')
        unidades = requisicao_unidade.json()

        presenca_registrada = False

        for key, value in unidades.items():
            data_registrada = value.get("Data")
            hora_inicial = value.get("HoraInicial")
            hora_final = value.get("HoraFinal")
            aula = value.get("Aula")

            if data_atual_str == data_registrada:
                if hora_inicial <= hora_atual <= hora_final:
                    requisicao_presenca = await client.get(f'{BD_FIRE}/presencas/{presenca.sigla}.json')
                    presencas = requisicao_presenca.json()

                    for presenca_key, presenca_value in presencas.items():
                        if presenca_value.get("matricula") == presenca.matricula:
                            if "frequencia" in presenca_value:
                                if data_atual_str in presenca_value["frequencia"]:
                                    if isinstance(presenca_value["frequencia"][data_atual_str], str):
                                        presenca_value["frequencia"][data_atual_str] = [presenca_value["frequencia"][data_atual_str]]
                                    presenca_value["frequencia"][data_atual_str].append("PT" if aula == "TEO" else "PL")
                                else:
                                    presenca_value["frequencia"][data_atual_str] = ["PT" if aula == "TEO" else "PL"]
                            else:
                                presenca_value["frequencia"] = {data_atual_str: ["PT" if aula == "TEO" else "PL"]}

                            url_atualizacao = f'{BD_FIRE}/presencas/{presenca.sigla}/{presenca_key}.json'
                            requisicao_atualizacao = await client.patch(url_atualizacao, data=json.dumps(presenca_value))

                            if requisicao_atualizacao.status_code // 100 == 2:
                                nome_aluno = presenca_value.get("nome")
                                return {"mensagem": f"{nome_aluno}, sua presença foi cadastrada com sucesso"}
                            else:
                                raise HTTPException(status_code=500, detail="Erro ao atualizar a presença")
                    raise HTTPException(status_code=404, detail="Matrícula do aluno não encontrada para esta disciplina")
                else:
                    presenca_registrada = True 
        if presenca_registrada:
            raise HTTPException(status_code=400, detail="Fora do intervalo de tempo para registrar a presença")
        else:
            raise HTTPException(status_code=400, detail="Data de presença não encontrada para esta disciplina")
        
async def obterpresencas(presenca: PresencaGet):
    async with httpx.AsyncClient() as client:
        requisicao_presencas = await client.get(f'{BD_FIRE}/presencas/{presenca.sigla}.json')
        presencas = requisicao_presencas.json()
        presencas_da_matricula = {}
        for presenca_id, presenca_data in presencas.items():
            if presenca_data.get("matricula") == presenca.matricula:
                frequencia = presenca_data.get("frequencia", {})
                presencas_da_matricula[presenca_id] = {"frequencia": frequencia}
        if presencas_da_matricula:
            return {"presencas": presencas_da_matricula}
        else:
            raise HTTPException(status_code=404, detail="Presenças não encontradas para esta matrícula ou turma")
        
async def editarpresenca(presenca: PresencaEdit):
    if presenca.presenca not in ['PT', 'PL']:
        raise HTTPException(status_code=400, detail="A presença deve ser PT (presente na teoria) ou PL (presente no laboratório)")

    async with httpx.AsyncClient() as client:
        requisicao_presencas = await client.get(f'{BD_FIRE}/presencas/{presenca.sigla}.json')
        presencas = requisicao_presencas.json()
        presenca_encontrada = False

        for presenca_id, presenca_data in presencas.items():
            if presenca_data.get("matricula") == presenca.matricula:
                frequencia = presenca_data.get("frequencia", {})
                if presenca.data in frequencia:
                    presenca_encontrada = True
                    # Se a frequência para a data específica for uma string, converta para lista
                    if isinstance(frequencia[presenca.data], str):
                        frequencia[presenca.data] = [frequencia[presenca.data]]
                    
                    # Substitua a presença existente na data específica
                    frequencia[presenca.data] = [presenca.presenca]
                    presenca_data["frequencia"] = frequencia

                    requisicao_atualizacao = await client.put(f'{BD_FIRE}/presencas/{presenca.sigla}/{presenca_id}.json', json=presenca_data)

                    if requisicao_atualizacao.status_code // 100 == 2:
                        return {"mensagem": f"Presença para a data {presenca.data} atualizada com sucesso"}
                    else:
                        raise HTTPException(status_code=500, detail=f"Erro ao atualizar a presença para a data {presenca.data}")

        if not presenca_encontrada:
            raise HTTPException(status_code=404, detail=f"Presença não encontrada para a matrícula {presenca.matricula} e data {presenca.data} nesta disciplina")

async def obterfrequencias(sigla: str):
    async with httpx.AsyncClient() as client:
        requisicao_presencas = await client.get(f'{BD_FIRE}/presencas/{sigla}.json')
        presencas = requisicao_presencas.json()
        frequencias_turma = {}
        for presenca_id, presenca_data in presencas.items():
            matricula = presenca_data.get("matricula")
            frequencia = presenca_data.get("frequencia", {})
            aluno_frequencia = {"matricula": matricula, "frequencia": frequencia}
            frequencias_turma[presenca_id] = aluno_frequencia
        if frequencias_turma:
            return {"frequencias": frequencias_turma}
        else:
            raise HTTPException(status_code=404, detail="Não foram encontradas frequências para esta turma")
       
async def obterfrequenciadiaria(sigla: str):
    data_atual = datetime.datetime.now()
    data_atual_str = str(data_atual)[:10]
    async with httpx.AsyncClient() as client:
        requisicao_presencas = await client.get(f'{BD_FIRE}/presencas/{sigla}.json')
        presencas = requisicao_presencas.json()
        frequencias_diarias = {}
        for presenca_id, presenca_data in presencas.items():
            frequencia = presenca_data.get("frequencia", {})
            if frequencia.get(data_atual_str):
                nome = presenca_data.get("nome")
                matricula = presenca_data.get("matricula")
                frequencias_diarias[matricula] = {"nome": nome, "frequencia": frequencia[data_atual_str]}
        if frequencias_diarias:
            return {"frequencias": frequencias_diarias}
        else:
            raise HTTPException(status_code=404, detail=f"Não foram encontradas frequências para a data {data_atual_str} nesta turma")

async def marcarpresenca(presenca: MarcarPresenca):
    try:
        datetime.datetime.strptime(presenca.data, '%Y-%m-%d')
    except ValueError:
        raise HTTPException(status_code=400, detail="Formato de data inválido. Use o formato YYYY-MM-DD")

    async with httpx.AsyncClient() as client:
        requisicao_presenca = await client.get(f'{BD_FIRE}/presencas/{presenca.sigla}.json')
        presencas = requisicao_presenca.json()

        for presenca_key, presenca_value in presencas.items():
            if presenca_value.get("matricula") == presenca.matricula:
                if "frequencia" not in presenca_value:
                    presenca_value["frequencia"] = {}

                if presenca.data in presenca_value["frequencia"]:
                    nome_aluno = presenca_value.get("nome")
                    return {"mensagem": f"A presença para {nome_aluno} já foi registrada para a data {presenca.data}"}

                if isinstance(presenca_value["frequencia"], str):
                    presenca_value["frequencia"] = {presenca.data: [presenca_value["frequencia"]]}
                else:
                    if presenca.data in presenca_value["frequencia"]:
                        presenca_value["frequencia"][presenca.data].append("PT" if presenca.aula == "TEO" else "PL")
                    else:
                        presenca_value["frequencia"][presenca.data] = ["PT" if presenca.aula == "TEO" else "PL"]

                url_atualizacao = f'{BD_FIRE}/presencas/{presenca.sigla}/{presenca_key}.json'
                requisicao_atualizacao = await client.patch(url_atualizacao, data=json.dumps(presenca_value))

                if requisicao_atualizacao.status_code // 100 == 2:
                    nome_aluno = presenca_value.get("nome")
                    return {"mensagem": f"A presença para {nome_aluno} foi cadastrada com sucesso na data {presenca.data}"}
                else:
                    raise HTTPException(status_code=500, detail="Erro ao atualizar a presença")

        raise HTTPException(status_code=404, detail="Matrícula do aluno não encontrada para esta disciplina")