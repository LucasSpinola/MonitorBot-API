import spacy
import numpy as np
import requests
from decouple import config
from app.nlp.text_processing import preprocess_text, extract_keywords

nlp = spacy.load('pt_core_news_sm')

BD_FIRE = config("URL_DB")

def le_perguntas():
    requisicao = requests.get(f'{BD_FIRE}/perguntas/.json')
    return requisicao

def classify_most_similar_question(query_keywords, database_texts):
    best_match_index = None
    max_overlap = 0

    for i, db_text in enumerate(database_texts):
        db_keywords = extract_keywords(db_text)
        overlap = len(set(query_keywords) & set(db_keywords))
        if overlap > max_overlap:
            max_overlap = overlap
            best_match_index = i

    return best_match_index

def find_most_similar_index(query_text, database_texts):
    query_doc = nlp(query_text)
    similarities = [query_doc.similarity(nlp(text)) for text in database_texts]
    return np.argmax(similarities)

def npl(pergunta):
    data = le_perguntas()
    
    try:
        lista_perguntas = [data.json()[id]['pergunta'] for id in data.json() if 'pergunta' in data.json()[id]]
        lista_respostas = [data.json()[id]['resposta'] for id in data.json() if 'resposta' in data.json()[id]]
    except KeyError:
        return "Erro: formato de dados inválido."
    
    pergunta_processada = preprocess_text(pergunta)
    query_keywords = extract_keywords(pergunta_processada)

    index = classify_most_similar_question(query_keywords, lista_perguntas)

    if index is None:
        return "Lamento, mas parece que não consigo encontrar uma resposta para sua pergunta no momento. Posso tentar ajudar de outra forma ou com uma pergunta diferente, se quiser!"

    return lista_respostas[index]
