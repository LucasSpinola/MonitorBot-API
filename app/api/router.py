from fastapi import APIRouter
from app.api.handler import user
from app.api.handler.user import user_router
from app.api.handler.unidades import unidades_router
from app.api.handler import unidades
from app.api.handler import turmas
from app.api.handler.turmas import turmas_router
from app.api.handler import presenca
from app.api.handler.presenca import presenca_router
from app.api.handler import perguntas
from app.api.handler.perguntas import perguntas_router
from app.api.handler import logs
from app.api.handler.logs import logs_router
from app.api.handler import aluno
from app.api.handler.aluno import alunos_router
from app.api.handler import nlp
from app.api.handler.nlp import nlp_router
from app.api.handler import miniteste
from app.api.handler.miniteste import miniteste_router
from app.api.handler import aln
from app.api.handler.aln import aln_router
from app.api.handler import permissao
from app.api.handler.permissao import permissao_router
from app.api.handler import whatsapp
from app.api.handler.whatsapp import whatsapp_router


router = APIRouter()

router.include_router(
    user.user_router,
    prefix="/users",
    tags=["Usuários"]
    )

router.include_router(
    aluno.alunos_router,
    prefix="/alunos",
    tags=["Alunos"]
    )

router.include_router(
    logs.logs_router,
    prefix="/logs",
    tags=["Logs"]
    )

router.include_router(
    miniteste.miniteste_router,
    prefix="/miniteste",
    tags=["Miniteste"]
    )

router.include_router(
    nlp.nlp_router,
    prefix="/nlp",
    tags=["NLP"]
    )

router.include_router(
    aln.aln_router,
    prefix="/narrativo",
    tags=["Narrativo"]
    )

router.include_router(
    presenca.presenca_router,
    prefix="/presenca",
    tags=["Presença"]
    )

router.include_router(
    perguntas.perguntas_router,
    prefix="/perguntas",
    tags=["Perguntas"]
    )

router.include_router(
    permissao.permissao_router,
    prefix="/permissao",
    tags=["Permissão"]
    )

router.include_router(
    turmas.turmas_router,
    prefix="/turmas",
    tags=["Turmas"]
    )

router.include_router(
    unidades.unidades_router,
    prefix="/unidades",
    tags=["Unidades"]
    )

router.include_router(
    whatsapp.whatsapp_router,
    prefix="/whatsapp",
    tags=["Whatsapp"]
    )
