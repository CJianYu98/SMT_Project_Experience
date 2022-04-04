from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import topic_analysis, trend_analysis, keyword_analysis, complaint_analysis, noteworthy_analysis

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(topic_analysis.router)
app.include_router(trend_analysis.router)
app.include_router(keyword_analysis.router)
app.include_router(complaint_analysis.router)
app.include_router(noteworthy_analysis.router)
