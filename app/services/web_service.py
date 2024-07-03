from fastapi import HTTPException, APIRouter, Depends
import json
import httpx
from decouple import config
from models.presenca_models import PresencaCreate, MarcarPresenca, PresencaGet, PresencaEdit
from datetime import datetime
from services.user_service import get_current_user
from services.turma_services import turmaporprofessor
import datetime

BD_FIRE = config("URL_DB")

async def obter_alunos_sem_presenca(id_discord: str):
    try:
        turmas_professor = await turmaporprofessor(id_discord)
        
        if not turmas_professor:
            raise HTTPException(status_code=404, detail="Este professor não tem turmas atribuídas")
        
        alunos_sem_frequencia_total = {}

        for sigla_turma, turma_info in turmas_professor.items():
            try:
                requisicao_presencas = await httpx.AsyncClient().get(f'{BD_FIRE}/presencas/{sigla_turma}.json')
                if requisicao_presencas.status_code == 200:
                    presencas = requisicao_presencas.json()
                    alunos_sem_frequencia = []

                    for presenca_id, presenca_data in presencas.items():
                        frequencia = presenca_data.get("frequencia", {})
                        if not frequencia:
                            alunos_sem_frequencia.append({"matricula": presenca_data.get("matricula"), "nome": presenca_data.get("nome")})

                    if alunos_sem_frequencia:
                        alunos_sem_frequencia_total[sigla_turma] = alunos_sem_frequencia
                
                else:
                    alunos_sem_frequencia_total[sigla_turma] = []

            except httpx.RequestError:
                alunos_sem_frequencia_total[sigla_turma] = {"erro": "Erro ao consultar o banco de dados"}

        return alunos_sem_frequencia_total
    
    except HTTPException as http_exc:
        raise http_exc
    
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Erro interno ao processar a requisição: {str(exc)}")

async def obter_respostas_mini_teste_alunos(id_discord: str):
    try:
        turmas_professor = await turmaporprofessor(id_discord)
        
        if not turmas_professor:
            raise HTTPException(status_code=404, detail="Este professor não tem turmas atribuídas")
        
        respostas_alunos_total = {}

        for sigla_turma, turma_info in turmas_professor.items():
            try:
                async with httpx.AsyncClient() as client:
                    requisicao_respostas = await client.get(f'{BD_FIRE}/presencas/{sigla_turma}.json')
                
                if requisicao_respostas.status_code == 200:
                    respostas = requisicao_respostas.json()
                    total_alunos = 0
                    alunos_com_respostas = 0

                    for resposta_id, resposta_data in respostas.items():
                        total_alunos += 1
                        miniteste = resposta_data.get("miniteste", {})
                        
                        if miniteste:
                            alunos_com_respostas += 1

                    respostas_alunos_total[sigla_turma] = {
                        "total_alunos": total_alunos,
                        "alunos_com_respostas": alunos_com_respostas
                    }
                else:
                    respostas_alunos_total[sigla_turma] = {
                        "total_alunos": 0,
                        "alunos_com_respostas": 0,
                        "erro": f"Erro ao consultar o banco de dados: {requisicao_respostas.status_code}"
                    }

            except httpx.RequestError as e:
                respostas_alunos_total[sigla_turma] = {
                    "total_alunos": 0,
                    "alunos_com_respostas": 0,
                    "erro": "Erro ao consultar o banco de dados"
                }

        return respostas_alunos_total
    
    except HTTPException as http_exc:
        raise http_exc
    
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Erro interno ao processar a requisição: {str(exc)}")

async def numero_de_turmas_professor(id_docente: str):
    url = f'{BD_FIRE}/turmas.json'
    async with httpx.AsyncClient() as client:
        try:
            requisicao = await client.get(url)
            if requisicao.status_code == 200:
                dados_turmas = requisicao.json()
                if not dados_turmas:
                    raise HTTPException(status_code=404, detail="Não há turmas disponíveis no momento")
                
                contador_turmas = 0
                for turma_data in dados_turmas.values():
                    for turma_info in turma_data.values():
                        if isinstance(turma_info, dict) and turma_info.get('id_docente') == id_docente:
                            contador_turmas += 1
                
                if contador_turmas > 0:
                    return {"total_turmas": contador_turmas}
                else:
                    raise HTTPException(status_code=404, detail="Turmas não encontradas para este professor")
            else:
                raise HTTPException(status_code=500, detail="Erro ao obter os dados das turmas")
        except httpx.HTTPError as http_err:
            raise HTTPException(status_code=501, detail="Erro de conexão")
        
async def contar_alunos_professor(id_discord: str):
    try:
        turmas_professor = await turmaporprofessor(id_discord)
        
        if not turmas_professor:
            raise HTTPException(status_code=404, detail="Este professor não tem turmas atribuídas")
        
        total_alunos = 0

        async with httpx.AsyncClient() as client:
            requisicao_alunos = await client.get(f'{BD_FIRE}/alunos.json')
            
            if requisicao_alunos.status_code == 200:
                alunos = requisicao_alunos.json()
                if alunos:  # Verificação adicional
                    for aluno_id, aluno_data in alunos.items():
                        if aluno_data.get('turma') in turmas_professor:
                            total_alunos += 1
                else:
                    raise HTTPException(status_code=404, detail="Nenhum aluno encontrado")
            else:
                raise HTTPException(status_code=500, detail=f"Erro ao consultar o banco de dados: {requisicao_alunos.status_code}")

        return {"total_alunos": total_alunos}
    
    except HTTPException as http_exc:
        raise http_exc
    
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Erro interno ao processar a requisição: {str(exc)}")
    
async def contar_alunos_sem_miniteste(id_discord: str):
    try:
        respostas_alunos_total = await obter_respostas_mini_teste_alunos(id_discord)
        
        total_alunos_sem_miniteste = 0

        for turma, info in respostas_alunos_total.items():
            total_alunos = info.get("total_alunos", 0)
            alunos_com_respostas = info.get("alunos_com_respostas", 0)
            
            alunos_sem_miniteste = total_alunos - alunos_com_respostas
            total_alunos_sem_miniteste += alunos_sem_miniteste
        
        return {
            "total_alunos_sem_miniteste": total_alunos_sem_miniteste
        }

    except HTTPException as http_exc:
        raise http_exc
    
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Erro interno ao processar a requisição: {str(exc)}")
    
async def contar_alunos_sem_frequencia(id_discord: str):
    try:
        turmas_professor = await turmaporprofessor(id_discord)
        
        if not turmas_professor:
            raise HTTPException(status_code=404, detail="Este professor não tem turmas atribuídas")
        
        alunos_sem_frequencia_total = 0

        for sigla_turma, turma_info in turmas_professor.items():
            try:
                requisicao_presencas = await httpx.AsyncClient().get(f'{BD_FIRE}/presencas/{sigla_turma}.json')
                if requisicao_presencas.status_code == 200:
                    presencas = requisicao_presencas.json()

                    for presenca_id, presenca_data in presencas.items():
                        frequencia = presenca_data.get("frequencia", {})
                        if not frequencia:
                            alunos_sem_frequencia_total += 1

            except httpx.RequestError:
                raise HTTPException(status_code=500, detail=f"Erro ao consultar o banco de dados da turma {sigla_turma}")

        return {"total_alunos_sem_frequencia": alunos_sem_frequencia_total}
    
    except HTTPException as http_exc:
        raise http_exc
    
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Erro interno ao processar a requisição: {str(exc)}")