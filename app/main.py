from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from app.api import auth, events, collaboration, version_history, change_log
from contextlib import asynccontextmanager
from app.model import *
from app.config import settings
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

@asynccontextmanager
async def lifespan(app: FastAPI):    
    # app.state.db = drop_tables()
    # app.state.db = create_tables()
    FastAPICache.init(InMemoryBackend(), prefix="fastapi-cache")
    yield

    # app.state.db = close_connection()



app = FastAPI(
    title="Collaborative Event Management System",
    version="1.0.0",
    description="API backend for managing events, users, and permissions collaboratively.",
    contact={
        "name": "Dharmraj Rathod",
        "email": "dharmraj98r@gmail.com",
    },    
    docs_url="/docs",          
    redoc_url="/redoc",        
    openapi_url="/openapi.json", 
    lifespan=lifespan
)




origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app.include_router(auth.router,prefix= "/api/auth", tags=["Authentication"])
app.include_router(events.router,prefix="/api/events", tags=["Event Management"])
app.include_router(collaboration.router, prefix="/api/events", tags=["Collaboration"])
app.include_router(version_history.router, prefix="/api/events", tags=["Version History"])
app.include_router(change_log.router, prefix="/api/events", tags=["Changelog & Diff"])

@app.get("/")
async def root():
    return {"message":"Welcome to Collaborative Event Management System"}


if __name__ == "__main__":
    port = settings.database_port
    uvicorn.run(app, host="0.0.0.0", port=port)
