import pandas as pd
import os
import json
from connect import client

# Select MongoDB collection to work with
fb = client.smt483.facebook

# Read data files
df = pd.read_csv('/data/listeningsquad/facebook/historical/cna_insider.csv', header=1)

# Drop rows with error or missing data
df.drop(df[df['query_status'] == "error (400)"].index, inplace=True)
df.drop(df[df['object_type'] != "data"].index, inplace=True)
df.dropna(subset=['created_time', 'message'], inplace=True)

# Reset index after droppping some rows
df.reset_index(inplace=True, drop=True)

# Set relevant columns
facebook_fields = ["id", "query_type", "parent_id", "object_id", "message", "created_time", "comments.summary.total_count", "reactions.summary.total_count", "like.summary.total_count", "love.summary.total_count", "haha.summary.total_count","wow.summary.total_count", "sad.summary.total_count", "angry.summary.total_count"]

# Filtered data with relevant columns
df_new = df[facebook_fields]

# Rename columns
df_new.rename(columns={
    "query_type": "is_post",
    "comments.summary.total_count": "comments_cnt",
    "reactions.summary.total_count": "reactions_cnt",
    "like.summary.total_count": "likes_cnt",
    "love.summary.total_count": "loves_cnt",
    "haha.summary.total_count": "haha_cnt",
    "wow.summary.total_count": "wow_cnt",
    "sad.summary.total_count": "sad_cnt",
    "angry.summary.total_count": "angry_cnt"
}, inplace=True)

# Label encoding
df_new['is_post'].replace({"Facebook:/<page-id>/posts":1, "Facebook:/<post-id>/comments":0}, inplace=True)

# Save processed data to json file, with each row as a json record
df_new.to_json('/data/listeningsquad/facebook/historical/cna_insider.json', orient='index')

# Read the json date file
f = open('/data/listeningsquad/facebook/historical/cna_insider.json')
data = json.load(f)

# Insert data into MongoDB
num_records = len(data)
fb.insert_many([data[str(i)] for i in range(num_records)])
