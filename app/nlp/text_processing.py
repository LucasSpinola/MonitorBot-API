import re
import spacy

nlp = spacy.load('pt_core_news_sm')

def preprocess_text(text):
    processed_text = re.sub(r'\b(?:é|está|estou|estava|estiveram|tem|têm|tinha|tiveram|tenho|temos|tinham|teve|tiveram|faz|fazem|fazia|fizeram|fiz|faço|fez|fazer|estas|esses|estes|aquelas|aqueles|aquele|aquela|isto|isso|assim|essa|esse|estou|esteja|estejam|estejamos|estiver|estiverem|estivermos|estivesse|estivessem|estivéramos|estou|esteja|estejamos|estejam|estava|estivemos|estavam|estivera|estiveram|estivermos|estivesse|estivessem|estivéssemos|estava|estavam|estive|esteve|estivemos|estivermos|estiver|estiverem|esteja|estejam|estejamos|estiver|estiverem|estivermos|estou|estamos|estavam|estivesse|estivéssemos|estiverem|estando|estado|estada|estadas|estados|sou|somos|são|era|éramos|eram|fui|foi|fomos|foram|fora|foram|fôramos|serei|será|seremos|serão|seria|seríamos|seriam|tenho|tem|temos|têm|tinha|tínhamos|tinham|tive|teve|tivemos|tiveram|terei|terá|teremos|terão|teria|teríamos|teriam|vou|vai|vamos|vão|vim|veio|viemos|vieram|viera|vieram|viéramos)\b', '', text, flags=re.IGNORECASE)
    processed_text = re.sub(r'[^a-zA-Záàâãéèêíïóôõöúçñ\s]', '', processed_text)
    return processed_text.strip().lower()

def extract_keywords(text):
    doc = nlp(text)
    keywords = [token.text for token in doc if not token.is_stop and token.pos_ in ['NOUN', 'VERB', 'ADJ']]
    return keywords