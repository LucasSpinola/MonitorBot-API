from fastapi import APIRouter, HTTPException, Depends
from decouple import config
from app.models.aln_models import Narrativo
import requests
from app.services.user_service import get_current_user
import httpx

aln_router = APIRouter()

BD_FIRE = config("URL_DB")

@aln_router.post("/adicionar/", summary="Adiciona um novo narrativo ao banco de dados")
async def cria_narrativo(narrativo: Narrativo, current_user: str = Depends(get_current_user)):
    requisicao = requests.get(f'{BD_FIRE}/narrativo/.json')
    for id in requisicao.json():
        if narrativo.numero != requisicao.json()[id]['numero']:
            narrativo_dict = narrativo.dict()
            json_miniteste = {'pergunta': narrativo_dict["pergunta"], 'texto_base': narrativo_dict["texto_base"], 'numero': narrativo_dict["numero"]}
            requisicao = requests.post(f'{BD_FIRE}/narrativo/.json', json=json_miniteste)
            if requisicao.status_code == 200:
                return {"mensagem": "Narrativo criado com sucesso"}
            else:
                return {"mensagem": "Erro ao criar narrativo"}
        
        else:
            return {"mensagem": "Número já existente no banco de dados"}

@aln_router.get("/ler_pergunta/{numero}", summary="Lê a pergunta de um narrativo específico pelo número")
async def ler_pergunta(numero: int, current_user: str = Depends(get_current_user)):
    requisicao = requests.get(f'{BD_FIRE}/narrativo.json')
    for id in requisicao.json():
        if numero == requisicao.json()[id]['numero']:
            return {"pergunta": requisicao.json()[id]['pergunta']}
        else:
            return {"mensagem": "Número não encontrado no banco de dados"}
    

@aln_router.put("/editar_narrativo/{numero}", summary="Edita um narrativo existente pelo número")
async def editar_narrativo(numero: int, novo_narrativo: Narrativo, current_user: str = Depends(get_current_user)):
    novo_narrativo_dict = novo_narrativo.dict()
    requisicao = requests.get(f'{BD_FIRE}/narrativo/.json')
    for id in requisicao.json():
        if numero == requisicao.json()[id]['numero']:
            requisicao = requests.patch(f'{BD_FIRE}/narrativo/{id}.json', json=novo_narrativo_dict)
            if requisicao.status_code == 200:
                return {"mensagem": "Narrativo editado com sucesso"}
            else:
                return {"mensagem": "Erro ao editar narrativo"}
    raise HTTPException(status_code=404, detail="Número não encontrado no banco de dados")

@aln_router.delete("/deletar_narrativo/{numero}", summary="Deleta um narrativo existente pelo número")
async def deletar_narrativo(numero: int, current_user: str = Depends(get_current_user)):
    requisicao = requests.get(f'{BD_FIRE}/narrativo.json')
    for id in requisicao.json():
        if numero == requisicao.json()[id]['numero']:
            requisicao = requests.delete(f'{BD_FIRE}/narrativo/{id}.json')
            if requisicao.status_code == 200:
                return {"mensagem": "Narrativo deletado com sucesso"}
            else:
                return {"mensagem": "Erro ao deletar narrativo"}
    raise HTTPException(status_code=404, detail="Número não encontrado no banco de dados")

@aln_router.get("/lista_narrativos/", summary="Lista todos os narrativos existentes")
async def lista_narrativos(current_user: str = Depends(get_current_user)):
    requisicao = requests.get(f'{BD_FIRE}/narrativo.json')
    lista_narrativos = []
    for id in requisicao.json():
        lista_narrativos.append(requisicao.json()[id])
    return lista_narrativos

@aln_router.get("/pegar_narrativo/", summary="Pega as respostas dos narrativos dos alunos")
async def pegar_narrativo(sigla: str, current_user: str = Depends(get_current_user)):
    async with httpx.AsyncClient() as client:
        requisicao_presencas = await client.get(f'{BD_FIRE}/presencas/{sigla}.json')
        presencas = requisicao_presencas.json()
        frequencias_narrativo = {}
        for narrativo_nome, presenca_data in presencas.items():
            matricula = presenca_data.get("matricula")
            narrativo = presenca_data.get("narrativo", {})
            narrativo_frequencia = {"matricula": matricula, "narrativo": narrativo}
            frequencias_narrativo[narrativo_nome] = narrativo_frequencia
        if frequencias_narrativo:
            return {"frequencias": frequencias_narrativo}
        else:
            raise HTTPException(status_code=404, detail="Não foram encontradas respostas do narrativo para esta turma!")
