import pandas as pd
from transformers import pipeline

# Zero-shot Intent Classification Model
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")


def classify_intent(text):
    labels = ["suggestion", "complaint", "educational", "question", "remark"]

    try:
        results_dict = classifier(text, labels)
    except:
        return None

    labels = results_dict["labels"]
    intent = labels[0]

    return intent
