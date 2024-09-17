import logging

from airflow.decorators import task
from pandas import read_csv

logging.basicConfig(level=logging.INFO)


@task
def data_load(data_path: str):
    logging.info("Data opend successfully.")
    logging.info("Saving data.")
    df = read_csv(data_path)
    logging.info("Data saved successfully.")
    return df
