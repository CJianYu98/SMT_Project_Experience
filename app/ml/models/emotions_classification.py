import os

from dotenv import load_dotenv
from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline

from ...constants.ml import EMOTIONS_LABELS

# Load environment variables
load_dotenv()

# Load constants
MODEL_DATA_FOLDER_PATH = os.getenv("MODEL_DATA_FOLDER_PATH")
EMOTIONS_MODEL_PATH = os.getenv("EMOTIONS_MODEL_PATH")

# Load tokenizer and model
tokenizer = AutoTokenizer.from_pretrained(f"{MODEL_DATA_FOLDER_PATH}/{EMOTIONS_MODEL_PATH}")
model = AutoModelForSequenceClassification.from_pretrained(f"{MODEL_DATA_FOLDER_PATH}/{EMOTIONS_MODEL_PATH}")

# Load zeroshot classification pipeline
classifier = pipeline("zero-shot-classification", tokenizer=tokenizer, model=model)


def classify_emotions(text: str) -> str:
    """
    Takes in an input text and returns the emotions label.

    Args:
        text (str): Text to be classified.

    Returns:
        str: Label of the given input text.
    """
    try:
        results = classifier(text, candidate_labels=EMOTIONS_LABELS)
    except:
        return None

    # Classify as neutral if probability score is too low
    return "neutral" if results["scores"][0] < 0.75 else results["labels"][0]
