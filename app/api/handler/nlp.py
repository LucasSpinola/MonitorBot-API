from fastapi import APIRouter, Body, Depends
from decouple import config
from app.models.nlp_models import NLPCreate
from app.models.logs_models import LogsCreate
from app.models.aln_models import Narrativo, RespostaAluno
import datetime
from app.nlp.nlp import npl
from app.api.handler.logs import logs
from app.nlp.nlp_narrativo import nlp_motor
import requests
import json
from fastapi.responses import JSONResponse
from starlette.responses import PlainTextResponse
from app.services.user_service import get_current_user


nlp_router = APIRouter()

BD_FIRE = config("URL_DB")

@nlp_router.post("/pergunta/", summary="Envia uma pergunta para o motor de NLP e retorna a resposta")
async def nlp_pergunta(pergunta: NLPCreate = Body(...), current_user: str = Depends(get_current_user)):
    user_resposta = pergunta.mensagem
    resposta = npl(user_resposta)
    data = datetime.datetime.now()

    if resposta == "Lamento, mas parece que não consigo encontrar uma resposta para sua pergunta no momento. Posso tentar ajudar de outra forma ou com uma pergunta diferente, se quiser!":    
        log_data = {"pergunta": pergunta.mensagem, "id_discord": pergunta.id_discord, "data": str(data)[:10]}
        await logs(LogsCreate(**log_data))

    return resposta


@nlp_router.post("/narrativo/", summary="Envia uma resposta de narrativo para o motor de NLP e retorna a avaliação")
async def avaliar_resposta_aluno(resposta: RespostaAluno = Body(...), current_user: str = Depends(get_current_user)):
    requisicao = requests.get(f'{BD_FIRE}/presencas/{resposta.sigla}/.json')
    for id in requisicao.json():
        if resposta.matricula == requisicao.json()[id]['matricula']:
            nome = requisicao.json()[id]['nome']
            resultado_final = nlp_motor(resposta.resposta_aluno, resposta.numero_gabarito)
            resultado_final["resposta"] = resposta.resposta_aluno
            json_teste = json.dumps(resultado_final)
            add_resposta = requests.patch(f'{BD_FIRE}/presencas/{resposta.sigla}/{id}/narrativo/.json', data=json_teste)
            if add_resposta.status_code // 100 != 2:
                return JSONResponse(status_code=400, content={"resultado": "Erro ao adicionar resposta do aluno"})
            mensagem = resultado_final.get("resultado", "Não foi possível obter a mensagem")
            resposta_formatada = {"mensagem": f"{nome}, {mensagem}"}
            return JSONResponse(status_code=200, content=resposta_formatada)
    