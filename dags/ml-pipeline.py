from airflow import DAG
import datetime as dt


from operators.data_load import data_load
from operators.model import processing
from operators.aggregate_predictions import aggregate_predictions

res_path = "data/result_data/data.csv"
pred_path = "data/prediction-data/data.csv"
data_path = "data/load-data/data.csv"

with DAG(
    dag_id='ETL_test',
    start_date=dt.datetime(2021, 3, 1),
    schedule='@once'
) as dag:


     processing(data_load(data_path), pred_path)

