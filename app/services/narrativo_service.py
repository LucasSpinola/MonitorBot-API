from fastapi import HTTPException
from decouple import config
from app.models.aln_models import Narrativo
import requests
import httpx

BD_FIRE = config("URL_DB")

async def crianarrativo(narrativo: Narrativo):
    requisicao = requests.get(f'{BD_FIRE}/narrativo/.json')
    
    for id in requisicao.json():
        if narrativo.numero != requisicao.json()[id]['numero']:
            narrativo_dict = narrativo.dict()
            json_narrativo = {
                'pergunta': narrativo_dict["pergunta"],
                'texto_base': narrativo_dict["texto_base"],
                'numero': narrativo_dict["numero"]
            }
            requisicao = requests.post(f'{BD_FIRE}/narrativo/.json', json=json_narrativo)
            if requisicao.status_code == 200:
                return {"mensagem": "Narrativo criado com sucesso"}
            else:
                raise HTTPException(status_code=500, detail="Erro ao criar narrativo")
    raise HTTPException(status_code=400, detail="Número já existente no banco de dados")

async def lerpergunta(numero: int):
    requisicao = requests.get(f'{BD_FIRE}/narrativo/.json')
    for id in requisicao.json():
        if numero == requisicao.json()[id]['numero']:
            return requisicao.json()[id]['pergunta']
    raise HTTPException(status_code=404, detail="Número não encontrado no banco de dados")
    
async def editarnarrativo(numero: int, novo_narrativo: Narrativo):
    novo_narrativo_dict = novo_narrativo.dict()
    requisicao = requests.get(f'{BD_FIRE}/narrativo/.json')
    narrativos = requisicao.json()
    
    for id, narrativo in narrativos.items():
        if numero == narrativo['numero']:
            requisicao = requests.patch(f'{BD_FIRE}/narrativo/{id}.json', json=novo_narrativo_dict)
            if requisicao.status_code == 200:
                return {"mensagem": "Narrativo editado com sucesso"}
            else:
                return {"mensagem": "Erro ao editar narrativo"}
    
    raise HTTPException(status_code=404, detail="Número não encontrado no banco de dados")

async def deletarnarrativo(numero: int):
    # Obtém todos os narrativos
    try:
        requisicao = requests.get(f'{BD_FIRE}/narrativo.json')
        requisicao.raise_for_status()  # Levanta uma exceção para erros de solicitação HTTP
        narrativos = requisicao.json()
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Erro ao acessar o banco de dados: {e}")
    
    # Procura o narrativo com o número especificado
    for id, narrativo in narrativos.items():
        if narrativo.get('numero') == numero:
            # Realiza a exclusão do narrativo
            try:
                requisicao_delete = requests.delete(f'{BD_FIRE}/narrativo/{id}.json')
                requisicao_delete.raise_for_status()  # Levanta uma exceção para erros de solicitação HTTP
                return {"mensagem": "Narrativo deletado com sucesso"}
            except requests.RequestException as e:
                return {"mensagem": f"Erro ao deletar narrativo: {e}"}
    
    # Se não encontrar o narrativo com o número especificado
    raise HTTPException(status_code=404, detail="Número não encontrado no banco de dados")

async def listanarrativos():
    requisicao = requests.get(f'{BD_FIRE}/narrativo.json')
    lista_narrativos = []
    for id in requisicao.json():
        lista_narrativos.append(requisicao.json()[id])
    return lista_narrativos

async def pegarnarrativo(sigla: str):
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
