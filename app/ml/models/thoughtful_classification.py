import pickle
from dotenv import load_dotenv

# ML libraries
from sklearn.naive_bayes import GaussianNB
from sklearn.preprocessing import StandardScaler

from ...constants.ml import FEATURES_LIST
from .preprocessing import *
from .ml_features import *

# Load environment variables
load_dotenv()

# Load saved model for classifying thoughtful comments
model = pickle.load(open('app/ml/models/model_data/finalized_model.sav', 'rb'))

def create_features(df):
    """"
    Create 5 features used to determine if a text is classified as a thoughtful one
    Args:
        df (DataFrame): dataframe of comments/posts

    Returns:
        DataFrame: dataframe with new columns for each feature created
    """
    # df["cleantext"] = df["combined_text"].apply(preprocessing)
    new_df = df.copy()

    new_df["length"] = new_df["cleantext"].apply(get_comment_length)
    new_df["num_discourse"] = new_df["cleantext"].apply(num_discourse)
    new_df["num_verbs"] = new_df["cleantext"].apply(get_num_verbs)
    new_df["num_pronouns"] = new_df["cleantext"].apply(get_num_pronouns)
    new_df["comment_loglikelihood"] = new_df["cleantext"].apply(get_average_loglikelihood)

    return new_df

def get_standardized_values(df):
    """
    Apply standardisation on features 

    Args:
        df (DataFrame): dataframe containing ML features

    Returns:
        DataFrame: new dataframe with scales values for features
    """
    scaler = StandardScaler()
    df_scaled = df[FEATURES_LIST]
    df_scaled = scaler.fit_transform(df[FEATURES_LIST])
    df_scaled = pd.DataFrame(df_scaled, columns=FEATURES_LIST)

    return df_scaled

def predict_thoughtfulness(df):
    """
    Use saved model to predict thoughtfulness of text

    Args:
        df (DataFrame): dataframe of text to be predicted

    Returns:
        list: array of predictions (1 - thoughtful, 0 - not thoughtful)
    """
    predictions = model.predict(df[FEATURES_LIST])

    return predictions