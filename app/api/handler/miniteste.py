from fastapi import APIRouter, HTTPException, Depends
import requests
import json
from decouple import config
from app.services.miniteste_service import cria_miniteste
from app.models.miniteste_models import Miniteste, MinitesteResposta
from app.services.user_service import get_current_user
import httpx

miniteste_router = APIRouter()

BD_FIRE = config("URL_DB")

@miniteste_router.get("/pegar/{teste}", summary="Obter miniteste")
async def obter_miniteste(teste: str, current_user: str = Depends(get_current_user)):
    requisicao = requests.get(f'{BD_FIRE}/minitestes/.json')
    teste = "T" + teste
    
    for id, teste_info in requisicao.json().items():
        if teste == teste_info["teste"]:
            return teste_info
    
    raise HTTPException(status_code=404, detail="Miniteste não encontrado")

@miniteste_router.post("/adicionar/resposta", summary="Adicionar resposta do aluno")
async def adicionar_resposta_aluno(miniteste: MinitesteResposta, current_user: str = Depends(get_current_user)):
    requisicao = requests.get(f'{BD_FIRE}/presencas/{miniteste.sigla}/.json')
    for aluno in requisicao.json():
        if miniteste.matricula == requisicao.json()[aluno]["matricula"]:
            dicionario_miniteste = {str(miniteste.n_teste): miniteste.resposta}
            json_teste = json.dumps(dicionario_miniteste)
            requisicao = requests.patch(f'{BD_FIRE}/presencas/{miniteste.sigla}/{aluno}/miniteste/.json', data=json_teste)
            
            if requisicao.status_code // 100 != 2:
                raise HTTPException(status_code=500, detail="Erro ao adicionar resposta do aluno")
            
            return {"mensagem": "Resposta do aluno adicionada com sucesso"}
        else:
            raise HTTPException(status_code=404, detail="Aluno não encontrado")

@miniteste_router.post("/miniteste/criar", summary="Criar miniteste")
async def criar_miniteste(miniteste: Miniteste, current_user: str = Depends(get_current_user)):
    if cria_miniteste(miniteste.pergunta, miniteste.resposta, miniteste.teste):
        return {"mensagem": "Miniteste criado com sucesso"}
    else:
        raise HTTPException(status_code=500, detail="Erro ao criar miniteste")
    
@miniteste_router.patch("/editar/{miniteste_id}", summary="Editar miniteste")
async def editar_miniteste(miniteste_id: str, miniteste: Miniteste, current_user: str = Depends(get_current_user)):
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

@miniteste_router.get("/aluno/{sigla}/{matricula}", summary="Obter respostas de miniteste de um aluno")
async def obter_respostas_miniteste_aluno(sigla: str, matricula: int, current_user: str = Depends(get_current_user)):
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

    
@miniteste_router.get("/alunos/{sigla}", summary="Obter respostas de miniteste de todos os alunos")
async def obter_respostas_miniteste_alunos(sigla: str, current_user: str = Depends(get_current_user)):
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

@miniteste_router.delete("/{miniteste_id}", summary="Deletar miniteste")
async def deletar_miniteste(miniteste_id: str, current_user: str = Depends(get_current_user)):
    url_bd_fire = f'{BD_FIRE}/minitestes/{miniteste_id}.json'
    
    requisicao = requests.delete(url_bd_fire)
    if requisicao.status_code == 200:
        return {"mensagem": "Miniteste deletado com sucesso"}
    elif requisicao.status_code == 404:
        raise HTTPException(status_code=404, detail="Miniteste não encontrado")
    else:
        raise HTTPException(status_code=500, detail="Erro ao deletar miniteste")