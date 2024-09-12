import html
import logging
import requests

import feedparser
import pandas as pd

COLUMNS_TO_SAVE = ["id", "published", "title", "summary"]
logging.basicConfig(level=logging.INFO)

data_path = '../../data/load-data/data.txt'

def data_load(data_path: str) -> None:
    response = requests.get('https://lenta.ru/rss')
    news_feed = feedparser.parse(response.text)
    df = pd.DataFrame(news_feed.entries)[COLUMNS_TO_SAVE]
    df["published"] = pd.to_datetime(df["published"])
    df["title"] = df["title"].map(html.unescape)
    df["summary"] = df["summary"].map(html.unescape)
    logging.info(f"Saving the processed data to '{data_path}'...")
    df.to_csv(data_path, sep="\t", index=False)
    logging.info("Data saved successfully.")






if __name__ == "__main__":
    data_load(data_path)
