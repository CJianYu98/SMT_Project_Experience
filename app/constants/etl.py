# Facebook
FACEBOOK_FIELDS = [
    "id",
    "query_type",
    "parent_id",
    "object_id",
    "message",
    "created_time",
    "comments.summary.total_count",
    "reactions.summary.total_count",
    "like.summary.total_count",
    "love.summary.total_count",
    "haha.summary.total_count",
    "wow.summary.total_count",
    "sad.summary.total_count",
    "angry.summary.total_count",
]

FACEBOOK_RENAME_COL_DICT = {
    "query_type": "is_post",
    "comments.summary.total_count": "comments_cnt",
    "reactions.summary.total_count": "reactions_cnt",
    "like.summary.total_count": "likes_cnt",
    "love.summary.total_count": "loves_cnt",
    "haha.summary.total_count": "haha_cnt",
    "wow.summary.total_count": "wow_cnt",
    "sad.summary.total_count": "sad_cnt",
    "angry.summary.total_count": "angry_cnt",
}


def get_time(time_in_seconds):
    hours = time_in_seconds // 3600
    mins = (time_in_seconds % 3600) // 60
    seconds = (time_in_seconds % 3600) % 60
    return int(hours), int(mins), int(seconds)
