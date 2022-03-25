from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline

path = "./app/ml/models/model_data"
emotion = "facebook/bart-large-mnli"

tokenizer = AutoTokenizer.from_pretrained(f"{path}/{emotion}")
model = AutoModelForSequenceClassification.from_pretrained(f"{path}/{emotion}")


def classify_emotions(text: str) -> str:
    """
    Takes in an input text and returns the emotions label.

    Args:
        text (str): Text to be classified.

    Returns:
        str: Label of the given input text.
    """
    # classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
    classifier = pipeline("zero-shot-classification", tokenizer=tokenizer, model=model)

    results = classifier(text, candidate_labels=["anger", "joy", "fear", "sadness"])

    # Classify as neutral if probability score is too low
    return "neutral" if results["scores"][0] < 0.75 else results["labels"][0]
