import requests
import json
from decouple import config
from app.models.whatsapp_models import WhatsappCreate, WhatsappMatricula
from fastapi import HTTPException
from app.api.auth.jwt_bearer import JWTBearer

BD_FIRE = config("URL_DB")

import requests
import json

async def adicionar_numero(alunos_data: WhatsappCreate):
    requisicao = requests.get(f'{BD_FIRE}/alunos.json')
    if requisicao.status_code != 200:
        raise HTTPException(status_code=500, detail="Erro ao acessar o banco de dados")

    alunos = requisicao.json()
    
    for id, dados_aluno in alunos.items():
        if alunos_data.matricula == dados_aluno['matricula']:
            telefone_existente = dados_aluno.get('telefone')
            if telefone_existente is None:
                dicionario_aluno = {'telefone': alunos_data.telefone}
                json_aluno = json.dumps(dicionario_aluno)
                requisicao_patch = requests.patch(f'{BD_FIRE}/alunos/{id}/.json', data=json_aluno)
                
                if requisicao_patch.status_code == 200:
                    resposta = requisicao_patch.json()
                    if resposta.get('telefone') == alunos_data.telefone:
                        return {"mensagem": "Numero cadastrado com sucesso"}
                    else:
                        raise HTTPException(status_code=500, detail="Erro ao atualizar o numero. Tente novamente.")
            else:
                raise HTTPException(status_code=400, detail="O numero já está cadastrado para esta matrícula.")
    
    raise HTTPException(status_code=404, detail="Matricula não encontrada no banco de dados")

async def excluir_numero(alunos_data: WhatsappMatricula):
    requisicao = requests.get(f'{BD_FIRE}/alunos.json')
    if requisicao.status_code != 200:
        raise HTTPException(status_code=500, detail="Erro ao acessar o banco de dados")

    alunos = requisicao.json()
    
    for id, dados_aluno in alunos.items():
        if alunos_data.matricula == dados_aluno['matricula']:
            telefone_existente = dados_aluno.get('telefone')
            if telefone_existente is not None:
                dicionario_aluno = {'telefone': None}
                json_aluno = json.dumps(dicionario_aluno)
                requisicao_patch = requests.patch(f'{BD_FIRE}/alunos/{id}/.json', data=json_aluno)
                
                if requisicao_patch.status_code == 200:
                    resposta = requisicao_patch.json()
                    if resposta.get('telefone') is None:
                        return {"mensagem": "Número excluído com sucesso"}
                    else:
                        raise HTTPException(status_code=500, detail="Erro ao excluir o número. Tente novamente.")
            else:
                raise HTTPException(status_code=400, detail="O aluno não possui um número cadastrado.")
    
    raise HTTPException(status_code=404, detail="Matricula não encontrada no banco de dados")

async def editar_numero(alunos_data: WhatsappCreate):
    requisicao = requests.get(f'{BD_FIRE}/alunos.json')
    if requisicao.status_code != 200:
        raise HTTPException(status_code=500, detail="Erro ao acessar o banco de dados")
    
    alunos = requisicao.json()
    
    for id, dados_aluno in alunos.items():
        if alunos_data.matricula == dados_aluno['matricula']:
            telefone_existente = dados_aluno.get('telefone')
            if telefone_existente is not None:
                dicionario_aluno = {'telefone': alunos_data.telefone}
                json_aluno = json.dumps(dicionario_aluno)
                requisicao_patch = requests.patch(f'{BD_FIRE}/alunos/{id}/.json', data=json_aluno)
                
                if requisicao_patch.status_code == 200:
                    resposta = requisicao_patch.json()
                    if resposta.get('telefone') == alunos_data.telefone:
                        return {"mensagem": "Número editado com sucesso"}
                    else:
                        raise HTTPException(status_code=500, detail="Erro ao editar o número. Tente novamente.")
            else:
                raise HTTPException(status_code=400, detail="O aluno não possui um número cadastrado.")

    raise HTTPException(status_code=404, detail="Matrícula não encontrada no banco de dados")

async def obter_telefone(alunos_data: WhatsappMatricula):
    requisicao = requests.get(f'{BD_FIRE}/alunos.json')
    if requisicao.status_code != 200:
        raise HTTPException(status_code=500, detail="Erro ao acessar o banco de dados")
    alunos = requisicao.json()
    
    for id, dados_aluno in alunos.items():
        if alunos_data.matricula == dados_aluno['matricula']:
            telefone_existente = dados_aluno.get('telefone')
            if telefone_existente is not None:
                return {"telefone": telefone_existente}
            else:
                raise HTTPException(status_code=404, detail="O aluno não possui um número cadastrado.")

    raise HTTPException(status_code=404, detail="Matrícula não encontrada no banco de dados")