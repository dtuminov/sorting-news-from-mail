import logging
import ssl

import nltk
import pandas as pd
from airflow.decorators import task
from spacy import load
from spacy.lang.ru import Russian

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

nltk.download('punkt')
nltk.download('stopwords')
from nltk.corpus import stopwords

stopwords_ru = stopwords.words("russian")
stopwords_ru[0:11]

COLUMNS_TO_SAVE = ["id", "published", "title", "summary"]
logging.basicConfig(level=logging.INFO)


@task
def processing(df, pred_path: str):
    logging.info("Data opend successfully.")
    logging.info("Saving data.")
    df = pd.read_table('f.txt')
    df['text'] = df.replace(r'[^\w\s]', ' ', regex=True).replace(r'\s+', ' ', regex=True)
    logging.info("Lemma data.")
    lemma = []
    nlp = Russian()
    load_model = load("ru_core_news_sm")
    for doc in load_model.pipe(df['text'].values):
        lemma.append([n.lemma_ for n in doc])
    df['text'] = lemma
    df['text'] = df['text'].apply(
        lambda x: [item for item in x if item not in stopwords_ru])
    df['text'] = [' '.join(map(str, l)) for l in df['text']]
    df.to_csv(pred_path, index=False, encoding='utf-8')
    logging.info("Data saved successfully.")
