from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from app.db.db_session import create_tables, close_connection, drop_tables
from app.api import auth, events, collaboration, version_history, change_log
from contextlib import asynccontextmanager
from app.model import *

@asynccontextmanager
async def lifespan(app: FastAPI):    
    # app.state.db = drop_tables()
    # app.state.db = create_tables()
    FastAPICache.init(InMemoryBackend(), prefix="fastapi-cache")
    yield

    # app.state.db = close_connection()



app = FastAPI(lifespan=lifespan)

    




app.include_router(auth.router,prefix= "/api/auth", tags=["Authentication"])
app.include_router(events.router,prefix="/api/events", tags=["Event Management"])
app.include_router(collaboration.router, prefix="/api/events", tags=["Collaboration"])
app.include_router(version_history.router, prefix="/api/events", tags=["Version History"])
app.include_router(change_log.router, prefix="/api/events", tags=["Changelog & Diff"])

@app.get("/")
async def root():
    return {"message":"Welcome to Collaborative Event Management System  --> Navigate to url/docs"}

