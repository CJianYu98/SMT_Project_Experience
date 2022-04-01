from dotenv import load_dotenv

from ...constants.ml import NOTEWORTHY_INTENT_LABELS

# Load environment variables
load_dotenv()

def classify_noteworthy(row):
    """
    A post/comment is classified as noteworthy as long as it fulfills 2 criteria: 1) The post/comment is a thoughtful one, 2) The intent of the post/comment is educational / a suggestion / giving or seeking advice

    Args:
        row (DataFrame row): a row in the dataframe of social media text

    Returns:
        int: noteworthy label for a given text (1 - noteworthy, 0 - not noteworthy)
    """
    thoughtfulness = row.isThoughtful
    intent_label = row.intent
    noteworthy_label = 0

    if thoughtfulness == 1.0 and intent_label in NOTEWORTHY_INTENT_LABELS:
        noteworthy_label = 1

    return noteworthy_label