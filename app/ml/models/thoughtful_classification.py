import pickle

# ML libraries
from sklearn.naive_bayes import GaussianNB
from sklearn.preprocessing import StandardScaler

from .preprocessing import *
from .ml_features import *

# Load saved model for classifying thoughtful comments
model = pickle.load(open('./finalized_model.sav', 'rb'))

def create_features(df):
    """"
    Create 5 features used to determine if a text is classified as a thoughtful one
    Args:
        df (DataFrame): dataframe of comments/posts

    Returns:
        DataFrame: dataframe with new columns for each feature created
    """
    df["cleantext"] = df["combined_text"].apply(preprocessing)
    df["length"] = df["cleantext"].apply(get_comment_length)
    df["num_discourse"] = df["cleantext"].apply(num_discourse)
    df["num_verbs"] = df["cleantext"].apply(get_num_verbs)
    df["num_pronouns"] = df["cleantext"].apply(get_num_pronouns)
    df["comment_loglikelihood"] = df["cleantext"].apply(get_average_loglikelihood)

    return df

def get_standardized_values(df, features_list):
    """
    Apply standardisation on features 

    Args:
        df (DataFrame): dataframe containing ML features
        features_list (list): list of ML features 

    Returns:
        DataFrame: new dataframe with scales values for features
    """
    scaler = StandardScaler()
    df_scaled = df[features_list]
    df_scaled = scaler.fit_transform(df[features_list])
    df_scaled = pd.DataFrame(df_scaled, columns=features_list)

    return df_scaled

def predict_thoughtfulness(df, features_list):
    """
    Use saved model to predict thoughtfulness of text

    Args:
        df (DataFrame): dataframe of text to be predicted
        features_list (list): list of ML features 

    Returns:
        list: array of predictions (1 - thoughtful, 0 - not thoughtful)
    """
    predictions = model.predict(df, features_list)

    return predictions