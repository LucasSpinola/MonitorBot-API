import requests
import requests
from decouple import config
from fastapi import HTTPException

BD_FIRE = config("URL_DB")

async def obterrespostasminitestealunosdata(sigla: str):
    url_bd_fire = f'{BD_FIRE}/presencas/{sigla}/.json'
    
    requisicao = requests.get(url_bd_fire)
    if requisicao.status_code == 200:
        alunos_respostas = {}
        presencas = requisicao.json()
        for presenca_info in presencas.values():
            if "matricula" in presenca_info and "miniteste" in presenca_info:
                matricula = presenca_info["matricula"]
                respostas = presenca_info["miniteste"]
                respostas_ordenadas = dict(sorted(respostas.items(), key=lambda item: int(item[0][1:])))
                alunos_respostas[matricula] = respostas_ordenadas
        return alunos_respostas
    else:
        raise HTTPException(status_code=500, detail="Erro ao obter respostas de miniteste dos alunos")