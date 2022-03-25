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
INTENT_LABELS = ["suggestion", "complaint", "educational", "question", "remark"]

# Emotions classification
EMOTIONS_LABELS = ["anger", "joy", "fear", "sadness"]

# Sentiment classification
TEXT_COLUMN = "cleantext"
SENTIMENT_LABELS_DICT = {"LABEL_0": "negative", "LABEL_1": "neutral", "LABEL_2": "positive"}
