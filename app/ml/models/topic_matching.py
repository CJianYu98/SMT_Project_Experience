import os
from dotenv import load_dotenv

from .preprocessing import *

# Load environment variables
load_dotenv()

# Change to file directory
os.chdir(os.path.dirname(os.path.realpath(__file__)))

def get_topics(text):
    """
    Read in dictionary of words for each topic and find the common words between the topic dictionaries and text. Topic will be assigned based on the number of common words.

    Args:
        text (str): social media text

    Returns:
        str: topic label assigned to text
    """

    with open('../data/Trending Topics/dictionary/art.csv') as f:
        art_dict = set([i for i in f][0].split(","))
    with open('../data/Trending Topics/dictionary/covid19.csv') as f:
        covid19_dict = set([i for i in f][0].split(","))
    with open('../data/Trending Topics/dictionary/education.csv') as f:
        edu_dict = set([i for i in f][0].split(","))
    with open('../data/Trending Topics/dictionary/environment.csv') as f:
        env_dict = set([i for i in f][0].split(","))
    with open('../data/Trending Topics/dictionary/fashion.csv') as f:
        fashion_dict = set([i for i in f][0].split(","))
    with open('../data/Trending Topics/dictionary/food.csv') as f:
        food_dict = set([i for i in f][0].split(","))
    with open('../data/Trending Topics/dictionary/healthcare.csv') as f:
        health_dict = set([i for i in f][0].split(","))
    with open('../data/Trending Topics/dictionary/politics.csv') as f:
        politics_dict = set([i for i in f][0].split(","))
    with open('../data/Trending Topics/dictionary/technology.csv') as f:
        tech_dict = set([i for i in f][0].split(","))
    with open('../data/Trending Topics/dictionary/sports.csv') as f:
        sports_dict = set([i for i in f][0].split(","))
    with open('../data/Trending Topics/dictionary/science.csv') as f:
        science_and_med_dict = set([i for i in f][0].split(","))
    with open('../data/Trending Topics/dictionary/law.csv') as f:
        law_and_crime_dict = set([i for i in f][0].split(","))

    topic_dicts = [('art', art_dict), 
                    ('covid19', covid19_dict), 
                    ('education', edu_dict), 
                    ('environment', env_dict), 
                    ('fashion', fashion_dict), 
                    ('food', food_dict), 
                    ('healthcare', health_dict), 
                    ('politics', politics_dict), 
                    ('technology', tech_dict), 
                    ('sports', sports_dict), 
                    ('science and medicine', science_and_med_dict), 
                    ('law and crime', law_and_crime_dict)
                    ]

    topic_match = {'art':0, 'covid19':0, 'education':0, 'environment':0, 'fashion':0, 'food':0, 'health':0, 'politics':0, 'technology':0, 'sports':0, 'science and medicine':0, 'law and crime':0}

    processed_text = topic_preprocessing(text)

    for i in range(len(topic_dicts)):
        match_text = topic_dicts[i][1].intersection(set(processed_text.split()))

        for k in topic_match:
            if k == topic_dicts[i][0]:
                topic_match[k] = len(match_text)

    if all(value == 0 for value in topic_match.values()):
        return 'others'
    else:
        return max(topic_match, key=topic_match.get)