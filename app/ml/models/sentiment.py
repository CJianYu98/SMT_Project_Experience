import os

import pandas as pd
from datasets import Dataset
from dotenv import load_dotenv
from tqdm.auto import tqdm
from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline
from transformers.pipelines.pt_utils import KeyDataset

# Load environment variables
load_dotenv()

# Load constants
MODEL_DATA_FOLDER_PATH = os.getenv("MODEL_DATA_FOLDER_PATH")
SENTIMENT_MODEL_PATH = os.getenv("SENTIMENT_MODEL_PATH")

# Load tokenizer and model
tokenizer = AutoTokenizer.from_pretrained(f"{MODEL_DATA_FOLDER_PATH}/{SENTIMENT_MODEL_PATH}")
model = AutoModelForSequenceClassification.from_pretrained(f"{MODEL_DATA_FOLDER_PATH}/{SENTIMENT_MODEL_PATH}")


def classify_sentiment(df: pd.DataFrame) -> pd.DataFrame:
    """
    Takes in a dataframe containing a column with text.
    Returns the same dataframe with a new column with the sentiment label of that text.

    Args:
        df (pd.DataFrame): Input df containing text to be classified.

    Returns:
        pd.DataFrame: Output df containing sentiment label.
    """

    text_column = "cleantext"  # To change accordingly, possible to add it as a argument

    pipe = pipeline("sentiment-analysis", tokenizer=tokenizer, model=model, max_length=512, truncation=True)

    labels_dict = {"LABEL_0": "negative", "LABEL_1": "neutral", "LABEL_2": "positive"}
    labels = []

    for output in tqdm(pipe(KeyDataset(Dataset.from_pandas(df), text_column))):
        current_label = output["label"]
        labels.append(labels_dict[current_label])

    df["sentiment_label"] = labels

    return df
