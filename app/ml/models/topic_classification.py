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

def classify_topics(text):
    """_summary_

    Args:
        text (str): Text to be classified

    Returns:
        str: Topic label of given input text
    """

    # Pre-defined topics
    labels = ["politics", "business and economy", "sports", "arts and entertainment", "covid19", "education", "environment", "fashion", "food", "technology", "science and medicine", "law and crime", "culture", "religion", "lifestyle", "travel", "healthcare", "society", "transportation", "others"]

    # Apply classification model on text
    results_dict = classifier(text, labels)

    labels = results_dict["labels"]

    # Return the topic with the highest score as the topic label
    top_topic = labels[0]

    return top_topic