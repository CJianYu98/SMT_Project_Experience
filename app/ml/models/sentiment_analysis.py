import numpy as np
from datasets import Dataset
from scipy.special import softmax
from tqdm.auto import tqdm
from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline
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
    classifier = pipeline("zero-shot-classification")
    results = classifier(text, candidate_labels=["anger", "joy", "fear", "sadness"])

    # Classify as neutral if probability score is too low
    return "neutral" if results["scores"][0] < 0.75 else results["labels"][0]


############### SENTIMENT ###############
def classify_sentiment(df):
    dataset = Dataset.from_pandas(df)
    MODEL = "cardiffnlp/twitter-roberta-base-sentiment"
    pipe = pipeline("sentiment-analysis", model=MODEL, tokenizer=MODEL, max_length=512, truncation=True)

    labels_dict = {
        "LABEL_0": "negative",
        "LABEL_1": "neutral",
        "LABEL_2": "positive"
    }
    labels = []

    for out in tqdm(pipe(KeyDataset(dataset, "message"))):
        current_label = out["label"]
        labels.append(labels_dict[current_label])
    df['sentiment_label'] = labels
    
    return df




# MODEL = "cardiffnlp/twitter-roberta-base-sentiment"
# tokenizer = AutoTokenizer.from_pretrained(MODEL)
# # tokenizer.save_pretrained(MODEL)
# model = AutoModelForSequenceClassification.from_pretrained(MODEL)
# # model.save_pretrained(MODEL)
# labels = ["negative", "neutral", "positive"]

# def classify_sentiment(text: str) -> str:
#     encoded_input = tokenizer(text, return_tensors="pt")
#     output = model(**encoded_input)
#     scores = output[0][0].detach().numpy()
#     scores = softmax(scores)
#     ranking = np.argsort(scores)
#     ranking = ranking[::-1]
#     return labels[ranking[0]]
