
from fastapi import FastAPI
from contextlib import asynccontextmanager

from routers import chats
from scheduler import start_scheduler, stop_scheduler

@asynccontextmanager
async def lifespan(app: FastAPI):
    start_scheduler()
    try:
        yield
    finally:
        stop_scheduler()

app = FastAPI(lifespan=lifespan)

app.include_router(chats.router, prefix="/api/v1/user_chats", tags=["chats"])

