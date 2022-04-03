from pydantic import BaseModel


class Top20ComplaintKeywordAnalysisRes(BaseModel):
    word: str
    count: int
