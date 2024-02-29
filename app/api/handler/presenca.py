from fastapi import HTTPException, APIRouter, Depends
import json
import httpx
from decouple import config
from app.models.presenca_models import PresencaCreate
from datetime import datetime
from app.services.user_service import get_current_user

presenca_router = APIRouter()

BD_FIRE = config("URL_DB")

from fastapi import HTTPException, Depends
from datetime import datetime
import httpx
import json

@presenca_router.post("/", summary="Registrar presença")
async def presenca(presenca: PresencaCreate, current_user: str = Depends(get_current_user)):
    data_atual = datetime.now()
    data_atual_str = data_atual.strftime("%Y-%m-%d")
    hora_atual = data_atual.strftime("%H:%M:%S")

    async with httpx.AsyncClient() as client:
        requisicao_unidade = await client.get(f'{BD_FIRE}/unidades/{presenca.sigla}.json')
        unidades = requisicao_unidade.json()

        for key, value in unidades.items():
            data_registrada = value.get("Data")
            hora_inicial = value.get("HoraInicial")
            hora_final = value.get("HoraFinal")
            print(data_registrada, hora_inicial, hora_final, hora_atual, data_atual_str, data_atual)

            if data_atual_str == data_registrada:
                if hora_inicial <= hora_atual <= hora_final:
                    requisicao_presenca = await client.get(f'{BD_FIRE}/presencas/{presenca.sigla}.json')
                    presencas = requisicao_presenca.json()
                    print(presencas)

                    for presenca_key, presenca_value in presencas.items():
                        if presenca_value.get("matricula") == presenca.matricula:
                            dicionario_pergunta = {data_atual_str: "P"}
                            json_pergunta = json.dumps(dicionario_pergunta)
                            url_atualizacao = f'{BD_FIRE}/presencas/{presenca.sigla}/{presenca_key}/frequencia.json'
                            requisicao_atualizacao = await client.patch(url_atualizacao, data=json_pergunta)

                            if requisicao_atualizacao.status_code // 100 == 2:
                                nome_aluno = presenca_value.get("nome")
                                return {"mensagem": f"{nome_aluno}, sua presença foi cadastrada com sucesso"}
                            else:
                                raise HTTPException(status_code=500, detail="Erro ao atualizar a presença")

                    raise HTTPException(status_code=404, detail="Matrícula do aluno não encontrada para esta disciplina")
                else:
                    requisicao_presenca = await client.get(f'{BD_FIRE}/presencas/{presenca.sigla}.json')
                    presencas = requisicao_presenca.json()

                    for presenca_key, presenca_value in presencas.items():
                        if not presenca_value.get(data_atual_str):
                            dicionario_pergunta = {data_atual_str: "F"}
                            json_pergunta = json.dumps(dicionario_pergunta)
                            url_atualizacao = f'{BD_FIRE}/presencas/{presenca.sigla}/{presenca_key}/frequencia.json'
                            requisicao_atualizacao = await client.patch(url_atualizacao, data=json_pergunta)

                            if requisicao_atualizacao.status_code // 100 == 2:
                                nome_aluno = presenca_value.get("nome")
                                print(f"{nome_aluno}, sua falta foi registrada com sucesso")
                            else:
                                raise HTTPException(status_code=500, detail="Erro ao registrar a falta")

                    raise HTTPException(status_code=400, detail="Fora do intervalo de tempo para registrar a presença")

    
@presenca_router.get("/ver_presenca/", summary="Verificar presençade um aluno em uma disciplina")
async def obter_presencas(sigla: str, matricula: int, current_user: str = Depends(get_current_user)):
    async with httpx.AsyncClient() as client:
        requisicao_presencas = await client.get(f'{BD_FIRE}/presencas/{sigla}.json')
        presencas = requisicao_presencas.json()
        presencas_da_matricula = {}
        for presenca_id, presenca_data in presencas.items():
            if presenca_data.get("matricula") == matricula:
                frequencia = presenca_data.get("frequencia", {})
                presencas_da_matricula[presenca_id] = {"frequencia": frequencia}
        if presencas_da_matricula:
            return {"presencas": presencas_da_matricula}
        else:
            raise HTTPException(status_code=404, detail="Presenças não encontradas para esta matrícula ou sigla")

@presenca_router.put("/editar-presenca/", summary="Editar presença de um aluno em uma disciplina")
async def editar_presenca(sigla: str, matricula: int, data: str, nova_presenca: str, current_user: str = Depends(get_current_user)):
    if nova_presenca not in ['F', 'P']:
        raise HTTPException(status_code=400, detail="A presença deve ser F (falta) ou P (presente)")
    async with httpx.AsyncClient() as client:
        requisicao_presencas = await client.get(f'{BD_FIRE}/presencas/{sigla}.json')
        presencas = requisicao_presencas.json()
        presenca_encontrada = False
        for presenca_id, presenca_data in presencas.items():
            if presenca_data.get("matricula") == matricula:
                frequencia = presenca_data.get("frequencia", {})
                if data in frequencia:
                    presenca_encontrada = True
                    if nova_presenca == 'F':
                        frequencia[data] = nova_presenca
                    else:
                        frequencia[data] = nova_presenca
                    presenca_data["frequencia"] = frequencia
                    requisicao_atualizacao = await client.put(f'{BD_FIRE}/presencas/{sigla}/{presenca_id}.json', json=presenca_data)
                    if requisicao_atualizacao.status_code // 100 == 2:
                        return {"mensagem": f"Presença para a data {data} atualizada com sucesso"}
                    else:
                        raise HTTPException(status_code=500, detail=f"Erro ao atualizar a presença para a data {data}")
        if not presenca_encontrada:
            raise HTTPException(status_code=404, detail=f"Presença não encontrada para a matrícula {matricula} e data {data} nesta disciplina")

@presenca_router.get("/pegar_frequencias/{sigla}", response_model=dict, summary="Obter frequências de uma disciplina")
async def obter_frequencias(sigla: str, current_user: str = Depends(get_current_user)):
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

@presenca_router.get("/pegar_frequencia_hoje/{sigla}", response_model=dict, summary="Obter frequência diária de uma disciplina")
async def obter_frequencia_diaria(sigla: str, current_user: str = Depends(get_current_user)):
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