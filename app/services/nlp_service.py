from fastapi import Body, HTTPException
from decouple import config
from app.models.nlp_models import NLPCreate
from app.models.logs_models import LogsCreate
from app.models.aln_models import Narrativo, RespostaAluno
import datetime
from app.nlp.nlp import npl_advanced
from app.api.handler.logs import logs
from app.nlp.nlp_narrativo import nlp_motor
import requests
import json
from fastapi.responses import JSONResponse

BD_FIRE = config("URL_DB")

async def nlppergunta(pergunta: NLPCreate = Body(...)):
    user_resposta = pergunta.mensagem
    resposta = npl_advanced(user_resposta)
    data = datetime.datetime.now()

    if resposta == "Lamento, mas parece que não consigo encontrar uma resposta para sua pergunta no momento. Posso tentar ajudar de outra forma ou com uma pergunta diferente, se quiser!":    
        log_data = {"pergunta": pergunta.mensagem, "id_discord": pergunta.id_discord, "data": str(data)[:10]}
        await logs(LogsCreate(**log_data))
    else:
        log_data = {"pergunta": pergunta.mensagem, "id_discord": pergunta.id_discord, "data": str(data)[:10], "resposta": resposta}
        requests.post(f'{BD_FIRE}/pesquisa/.json', data=json.dumps(log_data))

    return resposta

async def avaliarrespostaaluno(resposta):
    requisicao = requests.get(f'{BD_FIRE}/presencas/{resposta.sigla}/.json')
    if requisicao.status_code != 200:
        raise HTTPException(status_code=500, detail="Erro ao acessar os dados de presença")
    
    dados_presencas = requisicao.json()
    for id in dados_presencas:
        if resposta.matricula == dados_presencas[id]['matricula']:
            nome = dados_presencas[id]['nome']
            resultado_final = nlp_motor(resposta.resposta_aluno, resposta.numero_gabarito)
            resultado_final.update({
                "numero_gabarito": resposta.numero_gabarito,
                "resposta": resposta.resposta_aluno
            })
            
            resultado_final["similaridade"] = float(resultado_final["similaridade"])
            
            json_teste = json.dumps(resultado_final)
            add_resposta = requests.patch(f'{BD_FIRE}/presencas/{resposta.sigla}/{id}/narrativo/{resposta.numero_gabarito}/.json', data=json_teste)
            if add_resposta.status_code // 100 != 2:
                return JSONResponse(status_code=400, content={"resultado": "Erro ao adicionar resposta do aluno"})
            
            mensagem = resultado_final.get("resultado", "Não foi possível obter a mensagem")
            resposta_formatada = {"mensagem": f"{nome}, {mensagem}"}
            return JSONResponse(status_code=200, content=resposta_formatada)
    
    raise HTTPException(status_code=404, detail="Aluno não encontrado")
    