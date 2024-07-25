from fastapi import APIRouter, Body, Depends
from decouple import config
from app.models.nlp_models import NLPCreate
from app.models.aln_models import Narrativo, RespostaAluno
from app.services.user_service import get_current_user
from app.services.nlp_service import nlppergunta, avaliarrespostaaluno

nlp_router = APIRouter()

BD_FIRE = config("URL_DB")

@nlp_router.post("/pergunta/", summary="Envia uma pergunta para o motor de NLP e retorna a resposta")
async def nlp_pergunta(pergunta: NLPCreate = Body(...), current_user: str = Depends(get_current_user)):
    return await nlppergunta(pergunta)

@nlp_router.post("/narrativo/", summary="Envia uma resposta de narrativo para o motor de NLP e retorna a avaliação")
async def avaliar_resposta_aluno(resposta: RespostaAluno = Body(...), current_user: str = Depends(get_current_user)):
    return await avaliarrespostaaluno(resposta)
    