from fastapi import APIRouter
from handler import user
from handler.user import user_router
from handler.unidades import unidades_router
from handler import unidades
from handler import turmas
from handler.turmas import turmas_router
from handler import presenca
from handler.presenca import presenca_router
from handler import perguntas
from handler.perguntas import perguntas_router
from handler import logs
from handler.logs import logs_router
from handler import aluno
from handler.aluno import alunos_router
from handler import nlp
from handler.nlp import nlp_router
from handler import miniteste
from handler.miniteste import miniteste_router
from handler import aln
from handler.aln import aln_router
from handler import permissao
from handler.permissao import permissao_router
from handler import whatsapp
from handler.whatsapp import whatsapp_router
from handler import dataviwer
from handler.dataviwer import dataviwer_router
from handler import web
from handler.web import web_router


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

router.include_router(
    dataviwer.dataviwer_router,
    prefix="/dataviwer",
    tags=["DataViwer"]
    )

router.include_router(
    web.web_router,
    prefix="/web",
    tags=["Web"]
    )