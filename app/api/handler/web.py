from fastapi import FastAPI, Body, Depends, APIRouter, HTTPException
from models.user_model import User, UserLogin
from services.web_service import obter_alunos_sem_presenca, obter_respostas_mini_teste_alunos, numero_de_turmas_professor, contar_alunos_professor, contar_alunos_sem_miniteste, contar_alunos_sem_frequencia
from services.turma_services import turmaporprofessor


web_router = APIRouter()

@web_router.get('/alunossemfrequencia/', summary='Alunos sem frequência')
async def alunos_sem_frequencia(id_discord: str):
    return await obter_alunos_sem_presenca(id_discord)

@web_router.get('/alunosemminiteste/', summary='Mostra total de cada turma que fizeram os minitestes')
async def total_alunos_resposta(id_discord: str):
    return await obter_respostas_mini_teste_alunos(id_discord)

@web_router.get('/turmasprofessor/', summary='Turmas do professor')
async def turmas_professor(id_discord: str):
    return await numero_de_turmas_professor(id_discord)

@web_router.get('/total_alunos/', summary='Total de alunos')
async def total_alunos(id_discord: str):
    return await contar_alunos_professor(id_discord)

@web_router.get('/aluno_sem_miniteste/', summary='Alunos sem miniteste')
async def aluno_sem_miniteste(id_discord: str):
    return await contar_alunos_sem_miniteste(id_discord)

@web_router.get('/total_alunos_sem_frequencia/', summary='Alunos sem frequência')
async def alunos_sem_frequencia(id_discord: str):
    return await contar_alunos_sem_frequencia(id_discord)