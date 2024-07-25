import spacy
import numpy as np
import requests
from decouple import config
from spellchecker import SpellChecker
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report
import torch
from transformers import BertTokenizer, BertForQuestionAnswering
from app.nlp.text_processing import preprocess_text_advanced
# Carregar modelos necessários
nlp = spacy.load('pt_core_news_md')
spell = SpellChecker(language='pt')

# Configurações do banco de dados
BD_FIRE = config("URL_DB")

# Carregar o modelo BERT
tokenizer = BertTokenizer.from_pretrained('neuralmind/bert-base-portuguese-cased')
model = BertForQuestionAnswering.from_pretrained('neuralmind/bert-base-portuguese-cased')

def answer_question(question, context):
    inputs = tokenizer(question, context, return_tensors='pt')
    start_scores, end_scores = model(**inputs)

    start_index = torch.argmax(start_scores)
    end_index = torch.argmax(end_scores) + 1

    answer = tokenizer.convert_tokens_to_string(tokenizer.convert_ids_to_tokens(inputs['input_ids'][0][start_index:end_index]))
    return answer

def le_perguntas():
    requisicao = requests.get(f'{BD_FIRE}/perguntas/.json')
    dados = requisicao.json()
    perguntas = []
    respostas = []

    for id, info in dados.items():
        if 'pergunta' in info and 'resposta' in info:
            pergunta = info['pergunta'].strip()
            resposta = info['resposta'].strip()

            perguntas.append(pergunta)
            respostas.append(resposta)

    return perguntas, respostas

def extract_keywords_advanced(text):
    doc = nlp(text)
    keywords = []
    for ent in doc.ents:
        if ent.label_ in ['PERSON', 'ORG', 'GPE']:
            keywords.append(ent.text)
    for token in doc:
        if token.pos_ in ['NOUN', 'VERB', 'ADJ']:
            keywords.append(token.lemma_)
    return keywords

def train_text_classifier(train_texts, train_labels):
    text_clf = Pipeline([
        ('vect', CountVectorizer()),
        ('clf', MultinomialNB()),
    ])
    text_clf.fit(train_texts, train_labels)
    return text_clf

def evaluate_classifier(clf, test_texts, test_labels):
    predictions = clf.predict(test_texts)
    report = classification_report(test_labels, predictions)
    return report

def compute_tfidf_vectors(texts):
    vectorizer = CountVectorizer()
    tfidf_matrix = vectorizer.fit_transform(texts)
    return tfidf_matrix

def find_most_similar_index_advanced(query_text, database_texts):
    query_text_processed = preprocess_text_advanced(query_text)
    database_texts_processed = [preprocess_text_advanced(text) for text in database_texts]

    tfidf_matrix = compute_tfidf_vectors([query_text_processed] + database_texts_processed)
    query_vector = tfidf_matrix[0]
    database_vectors = tfidf_matrix[1:]

    similarities = np.dot(database_vectors, query_vector.T).toarray().flatten()
    best_match_index = np.argmax(similarities)
    best_similarity = similarities[best_match_index]

    return best_match_index if best_similarity > 0 else None

def npl_advanced(pergunta):
    perguntas, respostas = le_perguntas()
    
    index = find_most_similar_index_advanced(pergunta, perguntas)

    if index is None:
        contexto = 'Lamento, mas parece que não consigo encontrar uma resposta para sua pergunta no momento. Posso tentar ajudar de outra forma ou com uma pergunta diferente, se quiser!'
        return answer_question(pergunta, contexto)

    return respostas[index]
