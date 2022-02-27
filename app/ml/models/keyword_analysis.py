import spacy
import pandas as pd
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer 

ner = spacy.load('en_core_web_sm')
stemmer = PorterStemmer()
wnl = WordNetLemmatizer()

# List of entities we want to extract
entity_list = ["PERSON", "NORP", "FAC", "ORG", "GPE", "LOC", "PRODUCT", "EVENT", "WORK_OF_ART", "DATE"]


def extract_entities(text):
    """
    Takes in input text and returns a dictionary of entities with its entity tag

    Args:
        text (str): Text to which NER will be applied on.

    Returns:
        dict: Dictionary with key as entity tag and value as the word itself
    """
    entity_dict = {}
    entities = entity_list

    text = ner(text)
    for word in text.ents:
        word, label = word.text, word.label_

        word = word.lower()
        stemmed_word = stemmer.stem(word)
        lemma = wnl.lemmatize(stemmed_word)

        if len(lemma)>1:
            entity_list.append(lemma)
    return entity_list