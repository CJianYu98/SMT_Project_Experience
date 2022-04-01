from pydantic import BaseModel

class Top20KeywordAnalysisRes(BaseModel):
    word: str
    count: int
    sentiment: str