import json
from collections import defaultdict
from datetime import datetime, timedelta

from airflow.decorators import task

news_by_labels = defaultdict(list)

@task
def aggregate_predictions(pred_data_path:str, result_path:str) -> None:
    with open(pred_data_path, 'r') as f:
        news = json.load(f)

    for item in news.values():
        news_datetime = datetime.strptime(item['published'], '%Y-%m-%d &H:%M%S')
        if datetime.now() - news_datetime < timedelta(days=1):
            news_by_labels[item['label']].append(item['summary'])

    with open(result_path, "w") as f:
        json.dump(news_by_labels, f)