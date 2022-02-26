from fastapi import FastAPI
from .routers import facebook

app = FastAPI()

app.include_router(facebook.router)