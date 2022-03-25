import pandas as pd
from datasets import Dataset
from tqdm.auto import tqdm
from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline
from transformers.pipelines.pt_utils import KeyDataset

path = "./app/ml/models/model_data"
sentiment = "cardiffnlp/twitter-roberta-base-sentiment"

tokenizer = AutoTokenizer.from_pretrained(f"{path}/{sentiment}")
model = AutoModelForSequenceClassification.from_pretrained(f"{path}/{sentiment}")


def classify_sentiment(df: pd.DataFrame) -> pd.DataFrame:

    dataset = Dataset.from_pandas(df)
    # MODEL = "cardiffnlp/twitter-roberta-base-sentiment"
    pipe = pipeline("sentiment-analysis", tokenizer=tokenizer, model=model, max_length=512, truncation=True)

    labels_dict = {"LABEL_0": "negative", "LABEL_1": "neutral", "LABEL_2": "positive"}
    labels = []

    for out in tqdm(pipe(KeyDataset(dataset, "cleantext"))):
        current_label = out["label"]
        labels.append(labels_dict[current_label])
    df["sentiment_label"] = labels

    return df
