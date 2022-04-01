import nltk
import pandas as pd
import spacy
from nltk.stem import WordNetLemmatizer

from ...constants.ml import ENTITY_TYPES, STOP_ENTITIES
from .preprocessing import *

nltk.download("wordnet")  # NLTK Package WordNet for WordNetLemmatizer
nltk.download("omw-1.4")  # Open Multilingual Wordnet
ner = spacy.load("en_core_web_sm")
wnl = WordNetLemmatizer()


def extract_entities(text):
    """
    Takes in input text and returns a dictionary of entities with its entity tag

    Args:
        text (str): Text to which NER will be applied on.

    Returns:
        dict: Dictionary with key as entity tag and value as the word itself
    """

    entity_list = []

    ner_text = ner(text)
    for word in ner_text.ents:
        word, label = word.text, word.label_

        if label in ENTITY_TYPES:
            word = word.lower()
            lemma = wnl.lemmatize(word)

            if len(lemma) > 1 and lemma not in STOP_ENTITIES:
                entity_list.append(lemma)

    entity_list += extract_hashtags(text)
    entity_list += extract_mentions(text)

    return entity_list
