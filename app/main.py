from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import facebook, topic_analysis

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(facebook.router)
app.include_router(topic_analysis.router)