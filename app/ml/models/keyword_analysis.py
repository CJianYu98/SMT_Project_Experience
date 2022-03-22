import pandas as pd
import spacy
ner = spacy.load('en_core_web_sm')

import nltk
nltk.download('wordnet') # NLTK Package WordNet for WordNetLemmatizer
nltk.download('omw-1.4') # Open Multilingual Wordnet
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer 

stemmer = PorterStemmer()
wnl = WordNetLemmatizer()

from .preprocessing import *

# List of entities we want to extract
ENTITIES = ["PERSON", "NORP", "FAC", "ORG", "GPE", "LOC", "PRODUCT", "EVENT", "WORK_OF_ART"]


def extract_entities(text):
    """
    Takes in input text and returns a dictionary of entities with its entity tag

    Args:
        text (str): Text to which NER will be applied on.

    Returns:
        dict: Dictionary with key as entity tag and value as the word itself
    """
    entity_list = []
    entities = ENTITIES

    ner_text = ner(text)
    for word in ner_text.ents:
        word, label = word.text, word.label_

        if label in entities:
            word = word.lower()
            stemmed_word = stemmer.stem(word)
            lemma = wnl.lemmatize(stemmed_word)

            if len(lemma)>1:
                entity_list.append(lemma)

    entity_list += extract_hashtags(text)
    entity_list += extract_mentions(text)
                
    return entity_list