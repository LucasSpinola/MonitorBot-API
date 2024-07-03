import requests
from decouple import config
import json
import requests
import json
from decouple import config
from models.miniteste_models import Miniteste, MinitesteResposta
import httpx
from fastapi import HTTPException

BD_FIRE = config("URL_DB")

async def criaminiteste(miniteste: Miniteste):
    resposta_dict = miniteste.resposta.dict()
    dicionario_miniteste = {'pergunta': miniteste.pergunta, 'resposta': resposta_dict, 'teste': miniteste.teste}
    json_miniteste = json.dumps(dicionario_miniteste)
    requisicao = requests.post(f'{BD_FIRE}/minitestes/.json', data=json_miniteste)
    if requisicao.status_code == 200:
        return {"mensagem": "Miniteste criado com sucesso"}
    else:
        raise HTTPException(status_code=requisicao.status_code, detail=f"Erro ao criar miniteste - Mensagem de erro: {requisicao.text}")

async def obterminiteste(teste: str):
    requisicao = requests.get(f'{BD_FIRE}/minitestes/.json')
    teste = "T" + teste
    
    for id, teste_info in requisicao.json().items():
        if teste == teste_info["teste"]:
            return teste_info
    
    raise HTTPException(status_code=404, detail="Miniteste não encontrado")

async def adicionarrespostaaluno(miniteste: MinitesteResposta):
    try:
        url_presencas = f'{BD_FIRE}/presencas/{miniteste.sigla}.json'
        requisicao_presencas = requests.get(url_presencas)

        if requisicao_presencas.status_code == 200:
            presencas = requisicao_presencas.json()
            aluno_encontrado = False

            for id, presenca_info in presencas.items():
                if presenca_info and presenca_info.get("matricula") == miniteste.matricula:
                    aluno_encontrado = True
                    dicionario_miniteste = {str(miniteste.n_teste): miniteste.resposta}
                    json_teste = json.dumps(dicionario_miniteste)
                    url_aluno = f'{BD_FIRE}/presencas/{miniteste.sigla}/{id}/miniteste/.json'
                    requisicao_patch = requests.patch(url_aluno, data=json_teste)
                    
                    if requisicao_patch.status_code == 200:
                        return {"mensagem": "Resposta do aluno adicionada com sucesso"}
                    else:
                        raise HTTPException(status_code=500, detail="Erro ao adicionar resposta do aluno")

            if not aluno_encontrado:
                raise HTTPException(status_code=404, detail="Aluno não encontrado na turma")
        else:
            raise HTTPException(status_code=500, detail="Erro ao obter presenças da turma")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def editarminiteste(miniteste_id: str, miniteste: Miniteste):
    requisicao = requests.get(f'{BD_FIRE}/minitestes/{miniteste_id}.json')
    if requisicao.status_code != 200:
        raise HTTPException(status_code=404, detail="Miniteste não encontrado")
    miniteste_atual = requisicao.json()
    for campo, valor in miniteste.dict().items():
        if campo in miniteste_atual:
            miniteste_atual[campo] = valor
    requisicao_patch = requests.patch(f'{BD_FIRE}/minitestes/{miniteste_id}.json', data=json.dumps(miniteste_atual))
    if requisicao_patch.status_code != 200:
        raise HTTPException(status_code=500, detail="Erro ao editar miniteste")

    return {"mensagem": "Miniteste editado com sucesso"}

async def obterrespostasminitestealuno(sigla: str, matricula: int):
    url_presencas = f'{BD_FIRE}/presencas/{sigla}.json'
    try:
        requisicao_presencas = httpx.get(url_presencas)
        presencas_minitestes = requisicao_presencas.json()
        for aluno_id, aluno_data in presencas_minitestes.items():
            if aluno_data.get('matricula') == matricula:
                if 'miniteste' in aluno_data:
                    return aluno_data['miniteste']
                else:
                    raise HTTPException(status_code=404, detail="Aluno não participou do miniteste")
        raise HTTPException(status_code=404, detail="Aluno não encontrado na turma")
    except httpx.HTTPError as http_err:
        raise HTTPException(status_code=501, detail="Erro de conexão com o banco de dados")
    
async def obterrespostasminitestealunos(sigla: str):
    url_bd_fire = f'{BD_FIRE}/presencas/{sigla}/.json'
    
    requisicao = requests.get(url_bd_fire)
    if requisicao.status_code == 200:
        alunos_respostas = {}
        presencas = requisicao.json()
        for aluno_id, presenca_info in presencas.items():
            if "matricula" in presenca_info and "miniteste" in presenca_info:
                matricula = presenca_info["matricula"]
                respostas = presenca_info["miniteste"]
                alunos_respostas[aluno_id] = {"matricula": matricula, "respostas": respostas}
        return alunos_respostas
    else:
        raise HTTPException(status_code=500, detail="Erro ao obter respostas de miniteste dos alunos")

async def deletarminiteste(miniteste_id: str):
    url_bd_fire = f'{BD_FIRE}/minitestes/{miniteste_id}.json'
    
    requisicao = requests.delete(url_bd_fire)
    if requisicao.status_code == 200:
        return {"mensagem": "Miniteste deletado com sucesso"}
    elif requisicao.status_code == 404:
        raise HTTPException(status_code=404, detail="Miniteste não encontrado")
    else:
        raise HTTPException(status_code=500, detail="Erro ao deletar miniteste")