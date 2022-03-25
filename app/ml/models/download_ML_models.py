import os

from transformers import AutoModelForSequenceClassification, AutoTokenizer

# Create folder to store ML models offline
path = "app/ml/models/test"
if not os.path.exists(path):
    os.mkdir(path)


# Sentiment analysis
tokenizer = AutoTokenizer.from_pretrained("facebook/bart-large-mnli")
model = AutoModelForSequenceClassification.from_pretrained("facebook/bart-large-mnli")
tokenizer.save_pretrained("../models/model_data/bart-large-mnli")
model.save_pretrained("../models/model_data/bart-large-mnli")
