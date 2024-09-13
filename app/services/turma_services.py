from fastapi import HTTPException
import json
import httpx
from app.models.turma_models import TurmaCreate
from decouple import config
import httpx

BD_FIRE = config("URL_DB")

async def criaturma(turma_data: TurmaCreate):
    url_turma = f'{BD_FIRE}/turmas/{turma_data.sigla}/.json'
    url_unidade = f'{BD_FIRE}/unidades/{turma_data.sigla}/.json'
    
    data_dict = turma_data.dict()
    data_dict.pop('sigla')
    json_turma = json.dumps(data_dict)
    
    async with httpx.AsyncClient() as client:
        try:
            # Criação da turma
            requisicao_turma = await client.post(url_turma, data=json_turma)
            if requisicao_turma.status_code // 100 == 2:
                # Criação da unidade
                json_unidade = json.dumps({"nome": turma_data.sigla})
                requisicao_unidade = await client.post(url_unidade, data=json_unidade)
                
                if requisicao_unidade.status_code // 100 == 2:
                    return {"mensagem": f"Turma e unidade <{turma_data.sigla}> criadas com sucesso"}
                else:
                    raise HTTPException(status_code=500, detail=f"Erro ao criar a unidade <{turma_data.sigla}>")
            else:
                raise HTTPException(status_code=500, detail=f"Erro ao criar a turma <{turma_data.sigla}>")
        except httpx.HTTPError:
            raise HTTPException(status_code=501, detail=f"Erro de conexão")

async def editarturmas(sigla: str, turma_data: TurmaCreate):
    url = f'{BD_FIRE}/turmas/{sigla}/.json'
    data_dict = turma_data.dict()
    json_turma = json.dumps(data_dict)
    async with httpx.AsyncClient() as client:
        try:
            requisicao = await client.put(url, data=json_turma)
            if requisicao.status_code // 100 == 2:
                return {"mensagem": f"Turma <{sigla}> editada com sucesso"}
            else:
                raise HTTPException(status_code=500, detail=f"Erro ao editar a turma <{sigla}>")
        except httpx.HTTPError as http_err:
            raise HTTPException(status_code=501, detail=f"Erro de conexão")

async def listarturmas():
    url = f'{BD_FIRE}/turmas/.json'
    async with httpx.AsyncClient() as client:
        try:
            requisicao = await client.get(url)
            if requisicao.status_code // 100 == 2:
                dados_turmas = requisicao.json()
                return dados_turmas
            else:
                raise HTTPException(status_code=500, detail="Erro ao listar a turma")
        except httpx.HTTPError as http_err:
            raise HTTPException(status_code=501, detail="Erro de conexão")

async def lerturma(sigla: str):
    url = f'{BD_FIRE}/turmas/{sigla}/.json'
    async with httpx.AsyncClient() as client:
        try:
            requisicao = await client.get(url)
            if requisicao.status_code == 200:
                dados_turma = requisicao.json()
                if dados_turma is None:
                    raise HTTPException(status_code=404, detail=f"Turma <{sigla}> não encontrada")
                return dados_turma
            elif requisicao.status_code == 404:
                raise HTTPException(status_code=404, detail=f"Turma <{sigla}> não encontrada")
            else:
                raise HTTPException(status_code=500, detail=f"Erro ao ler a turma <{sigla}>")
        except httpx.HTTPError as http_err:
            raise HTTPException(status_code=501, detail="Erro de conexão")
        
async def turmaporprofessor(id_docente: str):
    url = f'{BD_FIRE}/turmas.json'
    async with httpx.AsyncClient() as client:
        try:
            requisicao = await client.get(url)
            if requisicao.status_code == 200:
                dados_turmas = requisicao.json()
                if not dados_turmas:
                    raise HTTPException(status_code=404, detail="Não há turmas disponíveis no momento")
                turmas_professor = {}
                for turma_codigo, turma_data in dados_turmas.items():
                    for turma_id, turma_info in turma_data.items():
                        if isinstance(turma_info, dict) and turma_info.get('id_docente') == id_docente:
                            turmas_professor[turma_codigo] = {turma_id: turma_info}
                if turmas_professor:
                    return turmas_professor
                else:
                    raise HTTPException(status_code=404, detail="Turmas não encontradas para este professor")
            else:
                raise HTTPException(status_code=500, detail="Erro ao obter os dados das turmas")
        except httpx.HTTPError as http_err:
            raise HTTPException(status_code=501, detail="Erro de conexão")

async def numeroalunosturma(sigla: str):
    url = f'{BD_FIRE}/presencas/{sigla}/.json'
    async with httpx.AsyncClient() as client:
        try:
            requisicao = await client.get(url)
            if requisicao.status_code == 200:
                dados_alunos = requisicao.json()
                if dados_alunos is None:
                    return {"mensagem": f"Turma <{sigla}> não possui alunos matriculados ainda"}
                else:
                    numero_alunos = len(dados_alunos)
                    return {"numero_alunos": numero_alunos}
            elif requisicao.status_code == 404:
                raise HTTPException(status_code=404, detail=f"Turma <{sigla}> não encontrada")
            else:
                raise HTTPException(status_code=500, detail=f"Erro ao obter o número de alunos da turma <{sigla}>")
        except httpx.HTTPError as http_err:
            raise HTTPException(status_code=501, detail="Erro de conexão")

async def deletarturma(sigla: str):
    url = f'{BD_FIRE}/turmas/{sigla}/.json'
    async with httpx.AsyncClient() as client:
        try:
            requisicao = await client.delete(url)
            if requisicao.status_code // 100 == 2:
                return {"mensagem": f"Turma <{sigla}> deletada com sucesso"}
            elif requisicao.status_code == 404:
                raise HTTPException(status_code=404, detail=f"Turma <{sigla}> não encontrada")
            else:
                raise HTTPException(status_code=500, detail=f"Erro ao deletar a turma <{sigla}>")
        except httpx.HTTPError as http_err:
            raise HTTPException(status_code=501, detail="Erro de conexão")