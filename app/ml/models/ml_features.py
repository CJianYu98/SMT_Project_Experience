from math import log2
import string
import regex as re
import pandas as pd
import contractions
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize, RegexpTokenizer

from .preprocessing import *

####### FEATURE 1: Length of Post/Comment #######
def get_comment_length(text: str) -> int:
    """
    Count the number of words in a comment. (Structural feature). 

    Args:
        text (str): Comment of a user

    Returns:
        int: Number of words in a comment
    """

    word_tokenizer = RegexpTokenizer(r'[-\'\w]+')
    tokenized_text = word_tokenizer.tokenize(text)
    return len(tokenized_text)

####### FEATURE 2: Number of Discourse Markers #######
discourse_keywords = 'although, as though, but, by comparison, even if, even though, however, nevertheless, on the other hand, still, then, though, while, yet, and, meanwhile, in turn, next, ultimately, meantime, also, as if, even as, even still, even then, regardless, when, by contrast, conversely, if, in contrast, instead, nor, or, rather, whereas, while, yet, even after, by contrast, nevertheless, besides, much as, as much as, whereas, neither, nonetheless, even when, on the one hand indeed, finally, in fact, separately, in the end, on the contrary, while'

discourse_keywords = discourse_keywords.split(', ')
discourse_keywords = list(set(discourse_keywords))
discourse_keywords.sort()
for i, word in enumerate(discourse_keywords):
    discourse_keywords[i] = ' ' + word + ' '

def num_discourse(text: str) -> int:
    """
    Count the number of discourse relations in a comment that appear in a comment. (Discourse feature).

    Args:
        text (str): Comment by an user

    Returns:
        int: Number of discourse relations
    """

    count = 0
    word_tokenizer = RegexpTokenizer(r'[-\'\w]+')
    tokenized_text = word_tokenizer.tokenize(text)
    tokenized_text = [w.lower() for w in tokenized_text]

    text_final = " ".join(tokenized_text)

    for ele in discourse_keywords:
        if ele in text_final:
            count += 1

    return count

####### FEATURE 3: Number of Verbs #######
verb_tags = ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ'] # POS tags for verbs 

def get_num_verbs(text: str) -> int:
    """
    Count the number of verbs in a comment based on their POS tags. (Syntactic Feature).

    Args:
        text (str): Comment of an user

    Returns:
        int: Number of verbs in a comment
    """

    word_tokenizer = RegexpTokenizer(r'[-\'\w]+')
    tokenized_text = word_tokenizer.tokenize(text)

    text_tags = nltk.pos_tag(tokenized_text)

    count = 0
    for tag in text_tags:
        if tag[1] in verb_tags:
            count += 1
    
    return count

####### FEATURE 4: Number of Pronouns #######
pronouns = [' i ', ' me ', ' my ', ' mine ', ' myself ', ' we ', ' us ', ' our ', ' ours ', ' ourselves ', ' you ', ' your ', ' yours ', ' yourself ', ' yourselves ']

def get_num_pronouns(text: str) -> int:
    """
    Count the number of first and second person pronouns in a comment. 

    Args:
        text (str): Comment by a user

    Returns:
        int: Number of pronouns
    """

    expanded_tokens = [contractions.fix(word) for word in text.split()]
    expanded_text = " ".join(expanded_tokens)

    word_tokenizer = RegexpTokenizer(r'[-\'\w]+')
    tokenized_text = word_tokenizer.tokenize(expanded_text)
    tokenized_text = [w.lower() for w in tokenized_text]

    count = 0
    for ele in pronouns:
        for token in tokenized_text:
            if token in ele:
                count += 1
    return count

####### FEATURE 5: Average Loglikelihood #######
NEWS_UNIGRAM = news_articles_unigram('../data/articles1.csv')

def get_average_loglikelihood(text):
    cmt_text_counter = comment_unicounter(text)
    cmt_loglikelihood = NEWS_UNIGRAM.evaluate(cmt_text_counter)
    return cmt_loglikelihood