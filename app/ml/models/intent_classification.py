import os

from dotenv import load_dotenv
from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline

# Load environment variables
load_dotenv()

# Load constants
MODEL_DATA_FOLDER_PATH = os.getenv("MODEL_DATA_FOLDER_PATH")
INTENT_MODEL_PATH = os.getenv("INTENT_MODEL_PATH")

# Load tokenizer and model
tokenizer = AutoTokenizer.from_pretrained(f"{MODEL_DATA_FOLDER_PATH}/{INTENT_MODEL_PATH}")
model = AutoModelForSequenceClassification.from_pretrained(f"{MODEL_DATA_FOLDER_PATH}/{INTENT_MODEL_PATH}")

# Load zeroshot classification pipeline
classifier = pipeline("zero-shot-classification", tokenizer=tokenizer, model=model)


def classify_intent(text: str) -> str:
    """
    Takes in an input text and returns the intention label.

    Args:
        text (str): Text to be classified.

    Returns:
        str: Label of the given input text.
    """

    labels = ["suggestion", "complaint", "educational", "question", "remark"]

    try:
        results_dict = classifier(text, labels)
    except:
        return None

    labels = results_dict["labels"]

    return labels[0]
