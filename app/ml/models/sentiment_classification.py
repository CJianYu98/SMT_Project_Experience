import os

import pandas as pd
from datasets import Dataset
from dotenv import load_dotenv
from tqdm.auto import tqdm
from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline
from transformers.pipelines.pt_utils import KeyDataset

from ...constants.ml import SENTIMENT_LABELS_DICT, TEXT_COLUMN

# Load environment variables
load_dotenv()

# Load constants
MODEL_DATA_FOLDER_PATH = os.getenv("MODEL_DATA_FOLDER_PATH")
SENTIMENT_MODEL_PATH = os.getenv("SENTIMENT_MODEL_PATH")

# Load tokenizer and model
tokenizer = AutoTokenizer.from_pretrained(f"{MODEL_DATA_FOLDER_PATH}/{SENTIMENT_MODEL_PATH}")
model = AutoModelForSequenceClassification.from_pretrained(f"{MODEL_DATA_FOLDER_PATH}/{SENTIMENT_MODEL_PATH}")

# Load sentiment analysis pipeline
classifier = pipeline("sentiment-analysis", tokenizer=tokenizer, model=model, max_length=512, truncation=True)
text_column = "cleantext"  # To change accordingly, possible to add it as a argument


def classify_sentiment(df: pd.DataFrame) -> pd.DataFrame:
    """
    Takes in a dataframe containing a column with text.
    Returns the same dataframe with a new column with the sentiment label of that text.

    Args:
        df (pd.DataFrame): Input df containing text to be classified.

    Returns:
        pd.DataFrame: Output df containing sentiment label.
    """

    labels = [
        SENTIMENT_LABELS_DICT[output["label"]]
        for output in tqdm(classifier(KeyDataset(Dataset.from_pandas(df), TEXT_COLUMN)))
    ]

    df["sentiment_label"] = labels

    return df
