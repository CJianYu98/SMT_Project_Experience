import os

from dotenv import load_dotenv
from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline

from ...constants.ml import TOPIC_LABELS

# Load environment variables
load_dotenv()

# Load constants
MODEL_DATA_FOLDER_PATH = os.getenv("MODEL_DATA_FOLDER_PATH")
TOPIC_MODEL_PATH = os.getenv("TOPIC_MODEL_PATH")

# Load tokenizer and model
tokenizer = AutoTokenizer.from_pretrained(f"{MODEL_DATA_FOLDER_PATH}/{TOPIC_MODEL_PATH}")
model = AutoModelForSequenceClassification.from_pretrained(f"{MODEL_DATA_FOLDER_PATH}/{TOPIC_MODEL_PATH}")

# Load zeroshot classification pipeline
classifier = pipeline("zero-shot-classification", tokenizer=tokenizer, model=model)


def classify_topics(text):
    """_summary_

    Args:
        text (str): Text to be classified

    Returns:
        str: Topic label of given input text
    """

    # Apply classification model on text
    results_dict = classifier(text, TOPIC_LABELS)
    labels = results_dict["labels"]

    # Return the topic with the highest score as the topic label
    return labels[0]
