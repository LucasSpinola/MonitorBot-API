import requests
from decouple import config
import json

BD_FIRE = config("URL_DB")

def cria_miniteste(pergunta, resposta, teste):
    dicionario_miniteste = {'pergunta': pergunta, 'resposta': resposta.dict(), 'teste': teste}
    json_miniteste = json.dumps(dicionario_miniteste)
    requisicao = requests.post(f'{BD_FIRE}/minitestes/.json', data=json_miniteste)
    
    if requisicao.status_code == 200:
        print("Miniteste criado com sucesso")
        return "Miniteste criado com sucesso"
    else:
        print(f"Erro ao criar miniteste - Status code: {requisicao.status_code}, Mensagem de erro: {requisicao.text}")
        return f"Erro ao criar miniteste - Status code: {requisicao.status_code}, Mensagem de erro: {requisicao.text}"
