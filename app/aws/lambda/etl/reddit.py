import json
import pprint

f = open('./2022-01-28.json')
data = json.load(f)

# Iterate through data and begin extracting
for id in data:
    dict = {}
    try:
        dict['author_fullname'] = data[id]['author_fullname']
    except:
        dict['author_fullname'] = None

    try:
        dict['title'] = data[id]['title']
    except:
        dict['title'] = None
    
    try:
        dict['link_flair_text'] = data[id]['link_flair_text']
    except:
        dict['link_flair_text'] = None

    try:
        dict['downs'] = data[id]['downs']
    except:
        dict['downs'] = None

    try:
        dict['ups'] = data[id]['ups']
    except:
        dict['ups'] = None

    try:
        dict['upvote_ratio'] = data[id]['upvote_ratio']
    except:
        dict['upvote_ratio'] = None

    try:
        dict['score'] = data[id]['score']
    except:
        dict['score'] = None

    try:
        dict['is_original_content'] = data[id]['is_original_content']
    except:
        dict['is_original_content'] = None

    try:
        dict['created'] = data[id]['created']
    except:
        dict['created'] = None

    try:
        dict['top_awarded_type'] = data[id]['top_awarded_type']
    except:
        dict['top_awarded_type'] = None

    try:
        dict['id'] = data[id]['id']
    except:
        dict['id'] = None

    try:
        dict['permalink'] = data[id]['permalink']
    except:
        dict['permalink'] = None

    try:
        dict['num_comments'] = data[id]['num_comments']
    except:
        dict['num_comments'] = None

    try:
        dict['media_embed'] = data[id]['media_embed']
    except:
        dict['media_embed'] = None

    try:
        dict['thumbnail'] = data[id]['thumbnail']
    except:
        dict['thumbnail'] = None

    try:
        dict['view_count'] = data[id]['view_count']
    except:
        dict['view_count'] = None

    try:
        dict['over_18'] = data[id]['over_18']
    except:
        dict['over_18'] = None

    try:
        dict['preview'] = data[id]['preview']
    except:
        dict['preview'] = None

    try:
        dict['author'] = data[id]['author']
    except:
        dict['author'] = None

    try:
        dict['all_awardings'] = data[id]['all_awardings']
    except:
        dict['all_awardings'] = None

    try:
        dict['discussion_type'] = data[id]['discussion_type']
    except:
        dict['discussion_type'] = None

    try:
        dict['created_utc'] = data[id]['created_utc']
    except:
        dict['created_utc'] = None

    try:
        dict['body_html'] = data[id]['body_html']
    except:
        dict['body_html'] = None

    # Extracting Comments
    comments = data[id]['comments']
    if comments:
        dict['comments'] = []

        for cid in comments:
            comment_dict = {}

            try:
                comment_dict['comment_type'] = comments[cid]['comment_type']
            except:
                comment_dict['comment_type'] = None

            try:
                comment_dict['total_awards_received'] = comments[cid]['total_awards_received']
            except:
                comment_dict['total_awards_received'] = None

            try:
                comment_dict['likes'] = comments[cid]['likes']
            except:
                comment_dict['likes'] = None

            try:
                comment_dict['author'] = comments[cid]['author']
            except:
                comment_dict['author'] = None

            try:
                comment_dict['created_utc'] = comments[cid]['created_utc']
            except:
                comment_dict['created_utc'] = None

            try:
                comment_dict['_submission'] = comments[cid]['_submission']
            except:
                comment_dict['_submission'] = None

            try:
                comment_dict['score'] = comments[cid]['score']
            except:
                comment_dict['score'] = None

            try:
                comment_dict['body'] = comments[cid]['body']
            except:
                comment_dict['body'] = None

            try:
                comment_dict['downs'] = comments[cid]['downs']
            except:
                comment_dict['downs'] = None

            try:
                comment_dict['top_awarded_type'] = comments[cid]['top_awarded_type']
            except:
                comment_dict['top_awarded_type'] = None

            try:
                comment_dict['permalink'] = comments[cid]['permalink']
            except:
                comment_dict['permalink'] = None

            try:
                comment_dict['ups'] = comments[cid]['ups']
            except:
                comment_dict['ups'] = None

            try:
                comment_dict['score_hidden'] = comments[cid]['score_hidden']
            except:
                comment_dict['score_hidden'] = None

            try:
                comment_dict['depth'] = comments[cid]['depth']
            except:
                comment_dict['depth'] = None

            try:
                comment_dict['parent_id'] = comments[cid]['parent_id']
            except:
                comment_dict['parent_id'] = None

            try:
                comment_dict['id'] = comments[cid]['id']
            except:
                comment_dict['id'] = None

            dict['comments'].append(comment_dict)
    pprint.pprint(dict)

    # Add code to add data to table here
    break
