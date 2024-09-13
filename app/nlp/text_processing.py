import spacy
from spacy.tokens import Token
import re

nlp = spacy.load('pt_core_news_sm')

def preprocess_text_advanced(text):
    doc = nlp(text)
    corrected_tokens = [token for token in doc if isinstance(token, Token) and token.is_alpha and not token.is_stop]
    processed_tokens = [token.lemma_ for token in corrected_tokens if len(token.lemma_) > 2]
    processed_text = ' '.join(processed_tokens)
    processed_text = re.sub(r'[^a-zA-Záàâãéèêíïóôõöúçñ\s]', '', processed_text)
    return processed_text.strip().lower()

def extract_keywords_advanced(text):
    doc = nlp(text)
    keywords = [token.text for token in doc if not token.is_stop and token.pos_ in ['NOUN', 'VERB', 'ADJ']]
    return keywords
