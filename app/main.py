from fastapi import FastAPI
from app.db.db_session import create_tables, close_connection, drop_tables
from app.api import auth, collaboration, events
from contextlib import asynccontextmanager
from app.model import user

@asynccontextmanager
async def lifespan(app: FastAPI):
    # app.state.db = drop_tables()
    # app.state.db = create_tables()
    yield

    # app.state.db = close_connection()



app = FastAPI(lifespan=lifespan)




app.include_router(auth.router,prefix= "/api/auth", tags=["auth"])
app.include_router(collaboration.router, prefix="/api", tags=["collaboration"])
app.include_router(events.router,prefix="/api", tags=["events"])


@app.get("/")
async def root():
    return {"message":"Collaborative Event Management System"}

