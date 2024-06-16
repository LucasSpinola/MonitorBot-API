import torch
from transformers import BertTokenizer, BertModel
import requests
from decouple import config
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

tokenizer = BertTokenizer.from_pretrained('neuralmind/bert-base-portuguese-cased')
model = BertModel.from_pretrained('neuralmind/bert-base-portuguese-cased')

BD_FIRE = config("URL_DB")

def buscar_resposta_gabarito(numero_gabarito):
    requisicao = requests.get(f'{BD_FIRE}/narrativo/.json')
    for numero in requisicao.json():
        if numero_gabarito == requisicao.json()[numero]['numero']:
            return requisicao.json()[numero]['texto_base']
    
def calcular_similaridade(resposta_aluno, resposta_gabarito):
    inputs_aluno = tokenizer(resposta_aluno, return_tensors="pt", padding=True, truncation=True)
    inputs_gabarito = tokenizer(resposta_gabarito, return_tensors="pt", padding=True, truncation=True)

    with torch.no_grad():
        outputs_aluno = model(**inputs_aluno)
        outputs_gabarito = model(**inputs_gabarito)

    embeddings_aluno = outputs_aluno.last_hidden_state[:, 0, :].numpy()
    embeddings_gabarito = outputs_gabarito.last_hidden_state[:, 0, :].numpy()

    similarity = cosine_similarity(embeddings_aluno, embeddings_gabarito)[0][0]
    return float(similarity)

def avaliar_resposta(similarity):
    if similarity > 0.8:
        return "Você escreveu uma boa resposta."
    elif 0.4 <= similarity <= 0.8:
        return "A sua resposta pode ser melhorada."
    else:
        return "Tente novamente, não compreendi bem sua resposta."

def nlp_motor(resposta_aluno, numero_gabarito):
    resposta_gabarito = buscar_resposta_gabarito(numero_gabarito)
    if not resposta_gabarito:
        return "Esse numero não existe no banco de dados."
    
    similarity = calcular_similaridade(resposta_aluno.lower(), resposta_gabarito.lower())
    similarity_round = round(similarity, 2)
    resultado_avaliacao = avaliar_resposta(similarity)
    dicionario = {"resultado": resultado_avaliacao, "similaridade": similarity_round}
    return dicionario