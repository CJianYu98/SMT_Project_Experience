from pydantic import BaseModel

##### Top 20 Keywords API #####
class Top20KeywordAnalysisRes(BaseModel):
    word: str
    count: int
    sentiment: str