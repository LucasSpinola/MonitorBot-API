import spacy
from app.nlp.text_processing import preprocess_text
from decouple import config
import requests

nlp = spacy.load('pt_core_news_sm')

BD_FIRE = config("URL_DB")

def buscar_resposta_gabarito(numero_gabarito):
    requisicao = requests.get(f'{BD_FIRE}/narrativo/.json')
    for numero in requisicao.json():
        if numero_gabarito == requisicao.json()[numero]['numero']:
            return requisicao.json()[numero]['texto_base']
    
def calcular_similaridade(resposta_aluno, resposta_gabarito):
    doc_aluno = nlp(resposta_aluno)
    doc_gabarito = nlp(resposta_gabarito)
    similarity = doc_aluno.similarity(doc_gabarito)
    return similarity

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