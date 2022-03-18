import string
import regex as re
import pandas as pd
from transformers import pipeline

# Text Preprocessing function
def preprocessing(text):
    text = text.encode('ascii', errors="ignore").decode()
    text = "".join([ch for ch in text if ch in string.printable])
    text = text.replace("\n", "").replace("\nl", "").replace("[", "").replace("]", "").replace("\\","").replace("--", "").replace("|:-", "").replace("|", " ").replace("#", "").replace("&x200B;", "").replace("Read the full story here:", "").replace("More short stories here:", "").replace("Full story here:", "").replace("Full story and details here:", "").replace("More details here:", "").replace("More short stories here:", "")

    remove_reader_contribution_tags = re.sub('<Reader Contribution\W?[\w*\s*]*\>', '', text)
    remove_credits_tags = re.sub('<Credits:\W?[\w*\s*]*\>', '', remove_reader_contribution_tags)
    markdown_removed = re.sub('\*+\W+', '', remove_credits_tags)
    link_removed = re.sub('\(?https?://[A-Za-z0-9./_\-!@#$%^&*+={}[\]<>:;?]*\)?', '', markdown_removed)

    return link_removed

# Zero-shot Intent Classification Model 
classifier = pipeline("zero-shot-classification")

def classifyIntent(text):
    labels = ["suggestion", "complaint", "educational", "question", "remark"]

    results_dict = classifier(text, 
                    labels)

    labels = results_dict["labels"]
    intent = labels[0]

    return intent