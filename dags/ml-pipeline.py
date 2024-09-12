import json

import pandas as pd
from datetime import timedelta, datetime
from airflow import DAG
from airflow.decorators import task
import datetime as dt
from collections import defaultdict
import sys
import os

import importlib.util


import pipeline.data_load.load as LOAD

news_by_labels = defaultdict(list)

pred_data_path = '../data/prediction-data/data.txt'
data_path = '../../data/load-data/data.txt'
rezult_path = '../data/result_data'

with DAG(
    dag_id='ETL_test',
    start_date=dt.datetime(2021, 3, 1),
    schedule_interval='@once'
) as dag:

    @task
    def load():
        LOAD.data_load(data_path)
    @task
    def agregate_predictions(pred_data_path:str, rezult_path:str) -> None:
        with open(pred_data_path, 'r') as f:
            news = json.load(f)

        for item in news.values():
            news_datetime = datetime.strptime(item['published'], '%Y-%m-%d &H:%M%S')
            if datetime.now() - news_datetime < timedelta(days=1):
                news_by_labels[item['label']].append(item['summary'])

        with open(rezult_path, "w") as f:
            json.dump(news_by_labels, f)

