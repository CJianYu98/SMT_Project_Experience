import os

from dotenv import load_dotenv
from transformers import AutoModelForSequenceClassification, AutoTokenizer

# Load environment variables
load_dotenv()

# Load constants
MODEL_DATA_FOLDER_PATH = os.getenv("MODEL_DATA_FOLDER_PATH")
SENTIMENT_MODEL_PATH = os.getenv("SENTIMENT_MODEL_PATH")
EMOTIONS_MODEL_PATH = os.getenv("EMOTIONS_MODEL_PATH")

# Create folder to store ML models offline
if not os.path.exists(MODEL_DATA_FOLDER_PATH):
    os.mkdir(MODEL_DATA_FOLDER_PATH)

# Sentiment
tokenizer_sentiment = AutoTokenizer.from_pretrained(SENTIMENT_MODEL_PATH)
model_sentiment = AutoModelForSequenceClassification.from_pretrained(SENTIMENT_MODEL_PATH)
tokenizer_sentiment.save_pretrained(f"{MODEL_DATA_FOLDER_PATH}/{SENTIMENT_MODEL_PATH}")
model_sentiment.save_pretrained(f"{MODEL_DATA_FOLDER_PATH}/{SENTIMENT_MODEL_PATH}")

# Emotions
tokenizer_emotion = AutoTokenizer.from_pretrained(EMOTIONS_MODEL_PATH)
model_emotion = AutoModelForSequenceClassification.from_pretrained(EMOTIONS_MODEL_PATH)
tokenizer_emotion.save_pretrained(f"{MODEL_DATA_FOLDER_PATH}/{EMOTIONS_MODEL_PATH}")
model_emotion.save_pretrained(f"{MODEL_DATA_FOLDER_PATH}/{EMOTIONS_MODEL_PATH}")
