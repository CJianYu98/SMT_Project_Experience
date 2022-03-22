import pandas as pd
from datasets import Dataset
from tqdm.auto import tqdm
from transformers import pipeline
from transformers.pipelines.pt_utils import KeyDataset


############### EMOTIONS ###############
def classify_emotions(text: str) -> str:
    """
    Takes in an input text and returns the emotions label.

    Args:
        text (str): Text to be classified.

    Returns:
        str: Label of the given input text.
    """
    classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
    results = classifier(text, candidate_labels=["anger", "joy", "fear", "sadness"])

    # Classify as neutral if probability score is too low
    return "neutral" if results["scores"][0] < 0.75 else results["labels"][0]


############### SENTIMENT ###############
def classify_sentiment(df: pd.DataFrame) -> pd.DataFrame:

    dataset = Dataset.from_pandas(df)
    MODEL = "cardiffnlp/twitter-roberta-base-sentiment"
    pipe = pipeline("sentiment-analysis", model=MODEL, tokenizer=MODEL, max_length=512, truncation=True)

    labels_dict = {"LABEL_0": "negative", "LABEL_1": "neutral", "LABEL_2": "positive"}
    labels = []

    for out in tqdm(pipe(KeyDataset(dataset, "cleantext"))):
        current_label = out["label"]
        labels.append(labels_dict[current_label])
    df["sentiment_label"] = labels

    return df
