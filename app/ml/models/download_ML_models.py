import os

from transformers import AutoModelForSequenceClassification, AutoTokenizer

# Path to ml model data folder
path = "./app/ml/models/model_data"

# Create folder to store ML models offline
if not os.path.exists(path):
    os.mkdir(path)

# Sentiment
sentiment = "cardiffnlp/twitter-roberta-base-sentiment"
tokenizer_sentiment = AutoTokenizer.from_pretrained(f"{sentiment}")
model_sentiment = AutoModelForSequenceClassification.from_pretrained(f"{sentiment}")
tokenizer_sentiment.save_pretrained(f"{path}/{sentiment}")
model_sentiment.save_pretrained(f"{path}/{sentiment}")

# Emotion
emotion = "facebook/bart-large-mnli"
tokenizer_emotion = AutoTokenizer.from_pretrained(f"{emotion}")
model_emotion = AutoModelForSequenceClassification.from_pretrained(f"{emotion}")
tokenizer_emotion.save_pretrained(f"{path}/{emotion}")
model_emotion.save_pretrained(f"{path}/{emotion}")
