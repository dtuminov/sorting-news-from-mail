import logging

import click
import pandas as pd
from transformers import pipeline

LABELS = [
    "Crypto",
    "SEC",
    "Dividend",
    "Economics",
    "Oil or Gas",
    "IPO",
    "Politics",
    "Buffet",
    "Stock",
    "Other",
]

data_path = '../../data/load-data/data.txt'
pred_path = '../../data/prediction-data/data.txt'

logging.basicConfig(level=logging.INFO)


def model_predict(data_path: str, pred_path: str) -> None:
    logging.info("Loading the model...")
    model_hf = pipeline( model="valhalla/distilbart-mnli-12-1", device=-1)
    logging.info("Model loaded successfully.")

    logging.info(f"Reading data from '{data_path}'...")
    df = pd.read_csv(data_path, sep="\t")
    logging.info("Data read successfully.")

    texts_for_pred = (df.title + ". " + df.summary).tolist()

    logging.info("Performing model prediction...")
    pred = model_hf(texts_for_pred, LABELS, multi_label=False)
    logging.info("Prediction completed successfully.")

    df["label"] = [x["labels"][0] for x in pred]

    logging.info(f"Saving the predictions to '{pred_path}'...")
    df.T.to_json(pred_path)
    logging.info("Predictions saved successfully.")


if __name__ == "__main__":
    model_predict(data_path, pred_path)
