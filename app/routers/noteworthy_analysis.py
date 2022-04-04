from collections import Counter

from fastapi import APIRouter

from ..dao.facebook import get_top5_noteworthy_comments
from ..schema.complaint_noteworthy_analysis import Top5ComplaintOrNoteworthyCommentsRes
from ..schema.user_filter import Filter

router = APIRouter(prefix="/noteworthy-analysis", tags=["noteworthy_analysis"])


@router.post(
    "/get-all-top5-noteworthy-comments", response_model=Top5ComplaintOrNoteworthyCommentsRes
)
def get_all_top5_noteworthy_comments(filter: Filter):
    """
    To get top 5 likes comments for noteworthy related comments

    Args:
        filter (Filter): _description_

    Returns:
        Pydantic Model: JSON response object
    """

    # Query selected social media platform MongoDB collection based on user platform filter options
    if "facebook" in filter.platforms:
        fb_comments_by_likes, fb_comments_by_date = get_top5_noteworthy_comments(filter)
    else:
        fb_comments_by_likes = fb_comments_by_date = []

    return {"facebook": {"likes": fb_comments_by_likes, "date": fb_comments_by_date}}
