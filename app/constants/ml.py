# General
TEXT_COLUMN = "cleantext"

# Keyword analysis
ENTITY_TYPES = ["PERSON", "NORP", "FAC", "ORG", "GPE", "LOC", "PRODUCT", "EVENT", "WORK_OF_ART"]

STOP_ENTITIES = [
    "singapore",
    "singaporean",
    "telegram",
    "#yahoofinance",
    "the new york times",
    "reuters",
    "#singapore",
    "#thebigstory",
    "#stbigstory",
    "facebook",
    "sg",
    "telegram  & twitter",
    "st",
    "the straits times",
    "#ig_sg",
    "#stnewsnight",
    "#sg",
    "#ig_singapore",
    "st news night",
    "afp",
    "cna",
    "@stomp",
    "stomper",
    "youtube",
    "whatsapp 9384 3761",
    "#talkingpoint",
    "mustsharenews.com",
    "#fblive",
]

# Intent classification
INTENT_LABELS = ["suggestion", "complaint", "educational", "question", "remark/news/statement", "seeking/giving advice"]

# Emotions classification
EMOTIONS_LABELS = ["anger", "joy", "fear", "sadness"]

# Sentiment classification
SENTIMENT_LABELS_DICT = {"LABEL_0": "negative", "LABEL_1": "neutral", "LABEL_2": "positive"}

# Topic classification
TOPIC_LABELS = [
    "politics",
    "business and economy",
    "sports",
    "arts and entertainment",
    "covid19",
    "education",
    "environment",
    "fashion",
    "food",
    "technology",
    "science and medicine",
    "law and crime",
    "culture",
    "religion",
    "lifestyle",
    "travel",
    "healthcare",
    "society",
    "transportation",
    "others",
]

# Thoughtful Post/Comments Classification Features
FEATURES_LIST = ['length', 'comment_loglikelihood', 'num_verbs', 'num_discourse','num_pronouns']

# Noteworthy Intent Labels
NOTEWORTHY_INTENT_LABELS = ["suggestion", "educational", "seeking/giving advice"]