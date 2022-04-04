import string
import zipfile
from math import log2

import pandas as pd
import regex as re
from nltk.tokenize import RegexpTokenizer, sent_tokenize, word_tokenize


def replace_characters(text: str) -> str:
    """
    Replace tricky punctuations that can mess up sentence tokenizers

    Args:
        text (str): text with non-standard punctuations

    Returns:
        str: text with standardized punctuations
    """
    replacement_rules = {"“": '"', "”": '"', "’": "'", "--": ","}
    for symbol, replacement in replacement_rules.items():
        text = text.replace(symbol, replacement)
    return text


def topic_preprocessing(text):
    """
    Process social media text for topic classification (match dictionary of words): Remove punctuations and change to lowercase

    Args:
        text (str): Raw social media text

    Returns:
        str: cleaned text
    """
    lowercase_text = text.lower()
    punctuations_removed = re.sub("[^a-z]", " ", lowercase_text)

    return punctuations_removed


def preprocessing(text):  # Facebook
    """
    Clean social media text: Removing non-english characters, markdown elements, unnecessary 'news' tags, links

    Args:
        text (str): Raw social media text

    Returns:
        str: preprocessed text
    """
    if type(text) != str:
        return text
    text = text.encode("ascii", errors="ignore").decode()  # Remove non-english characters
    text = "".join([ch for ch in text if ch in string.printable])
    text = (
        text.replace("\n", "")
        .replace("\nl", "")
        .replace("[", "")
        .replace("]", "")
        .replace("\\", "")
        .replace("--", "")
        .replace("|:-", "")
        .replace("|", " ")
        .replace("&x200B;", "")
        .replace("Read the full story here:", "")
        .replace("More short stories here:", "")
        .replace("Full story here:", "")
        .replace("Full story and details here:", "")
        .replace("More details here:", "")
        .replace("More short stories here:", "")
    )

    remove_reader_contribution_tags = re.sub("<Reader Contribution\W?[\w*\s*]*\>", "", text)
    remove_credits_tags = re.sub("<Credits:\W?[\w*\s*]*\>", "", remove_reader_contribution_tags)
    markdown_removed = re.sub("\*+\W+", "", remove_credits_tags)
    link_removed = re.sub("\(?https?://[A-Za-z0-9./_\-!@#$%^&*+={}[\]<>:;?]*\)?", "", markdown_removed)
    return link_removed


def twitter_preprocessing(text):
    """
    Clean Twitter text: Removing non-english characters, markdown elements, unnecessary 'news' tags, links

    Args:
        text (str): Raw Twitter text

    Returns:
        str: Preprocessed text
    """

    if type(text) != str:
        return text
    text = text.encode("ascii", errors="ignore").decode()
    text = "".join([ch for ch in text if ch in string.printable])
    text = text.replace("\n", "").replace("\nl", "").replace("[", "").replace("]", "").replace("\\--", "")
    markdown_removed = re.sub("\*+\W+", "", text)
    link_removed = re.sub("\(?https?://[A-Za-z0-9./_\-!@#$%^&*+={}[\]<>:;?]*\)?", "", markdown_removed)
    return re.sub("@[\w]+", "", link_removed)


def extract_hashtags(text):
    """
    Extract hashtags (#) used in social media text

    Args:
        text (str): Social media text

    Returns:
        list: A list of hashtags mentioned
    """
    text = text.lower()
    list_of_hashtags = re.findall("#\w+", text)
    return list_of_hashtags


def extract_mentions(text):
    """
    Extract mentions (@) in social media text

    Args:
        text (str): Social media text

    Returns:
        list: A list of users mentioned
    """
    text = text.lower()
    list_of_mentions = re.findall("@\w+", text)
    return list_of_mentions


def generate_tokenized_sentences(paragraph: str):
    """
    Tokenize each sentence in paragraph.
    For each sentence, tokenize each words and return the tokenized sentence one at a time.

    Args:
        paragraph (str): text of paragraph
    """
    word_tokenizer = RegexpTokenizer(r"[-\'\w]+")

    for sentence in sent_tokenize(paragraph):
        tokenized_sentence = word_tokenizer.tokenize(sentence)
        if tokenized_sentence:
            tokenized_sentence.append("[END]")
            yield tokenized_sentence


class UnigramCounter:
    def __init__(self, sentences: list) -> None:
        """
        Initialize unigram counter from tokenized text and count number of unigrams in text
        :param file_name: path of tokenized text. Each line is a sentence with tokens separated by comma.
        """
        ### self.sentence_generator = get_tokenized_sentences(file_name)
        self.sentences = sentences
        self.count()

    def count(self) -> None:
        """
        Count number of unigrams in text, one sentence at a time
        """
        self.sentence_count = 1
        self.token_count = 1
        self.counts = {}

        for sentence in self.sentences:
            self.sentence_count += 1
            self.token_count += len(sentence)
            for unigram in sentence:
                self.counts[unigram] = self.counts.get(unigram, 0) + 1


class UnigramModel:
    def __init__(self, train_counter: UnigramCounter) -> None:
        """
        Initialize unigram model from unigram counter, count the number of unique unigrams (vocab)

        Args:
            train_counter: counted unigram counter
        """
        self.counter = train_counter
        self.counts = train_counter.counts.copy()
        self.counts["[UNK]"] = 0
        self.vocab = set(self.counts.keys())
        self.vocab_size = len(self.vocab)

    def train(self, k: int = 1) -> None:
        """
        For each unigram in the vocab, calculate its probability in the text

        Args:
            k (int): smoothing pseudo-count for each unigram
        """
        self.probs = {}
        for unigram, unigram_count in self.counts.items():
            prob_nom = unigram_count + k
            prob_denom = self.counter.token_count + k * self.vocab_size
            self.probs[unigram] = prob_nom / prob_denom

    def evaluate(self, evaluation_counter: UnigramCounter) -> float:
        """
        Calculate the average log likelihood of the model on the evaluation text

        Args:
            evaluation_counter: unigram counter for the text on which the model is evaluated on

        Returns:
            float: average log likelihood that the unigram model assigns to the evaluation text
        """
        test_log_likelihood = 0
        test_counts = evaluation_counter.counts

        for unigram, test_count in test_counts.items():
            if unigram not in self.vocab:
                unigram = "[UNK]"
            train_prob = self.probs[unigram]
            log_likelihood = test_count * log2(train_prob)
            test_log_likelihood += log_likelihood

        avg_test_log_likelihood = test_log_likelihood / evaluation_counter.token_count
        return avg_test_log_likelihood


def comment_unicounter(text: str) -> UnigramCounter:
    """
    Create a unigram counter object, which store the number of counts for each word in the comment.

    Args:
        text (str): Comment of an user

    Returns:
        UnigramCounter: UnigramCounter object
    """
    text_replaced = replace_characters(text)
    txt = []

    for tokenized_sentence in generate_tokenized_sentences(text_replaced):
        txt.append(tokenized_sentence)

    cmt_text_counter = UnigramCounter(txt)

    return cmt_text_counter


def news_articles_unigram(file_name: str) -> UnigramModel:
    """
    Creating a unigram model for news article by reputatable news sources. This unigram model will be used to calculate average loglikelihood for an user's comment. Feature 2 for thoughtful comment (Lexical feature).

    Args:
        file_name (str): The csv file which contains all the news aricles

    Returns:
        UnigramModel: An unigram object
    """
    with zipfile.ZipFile(file_name, "r") as zip_ref:
        zip_ref.extractall("app/ml/data/Thoughtful_comment")

    df = pd.read_csv("app/ml/data/Thoughtful_comment/articles1.csv")
    df = df[["content", "id", "publication"]]

    corpus = []

    for i, row in df.iterrows():
        article = row["content"]

        article_replaced = replace_characters(article)

        for tokenized_sentence in generate_tokenized_sentences(article_replaced):
            # s = ','.join(tokenized_sentence)
            corpus.append(tokenized_sentence)

    train_counter = UnigramCounter(corpus)

    train_model = UnigramModel(train_counter)
    train_model.train(k=1)

    return train_model
