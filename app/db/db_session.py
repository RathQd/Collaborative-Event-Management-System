from sqlmodel import create_engine, SQLModel, Session
from app.config import settings

POSTGRESS_SQL_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}"
#echo for printing the table creation logs
# engine = create_engine(POSTGRESS_SQL_DATABASE_URL, echo=True)
engine = create_engine(POSTGRESS_SQL_DATABASE_URL)


def create_tables():
    print(POSTGRESS_SQL_DATABASE_URL)
    SQLModel.metadata.create_all(bind=engine)
    print("DB tables initiated at", engine.url)
    return "CEMS DB Connected"

def close_connection():
    engine.dispose()
    return "CEMS DB Disconnected"

def drop_tables():
    SQLModel.metadata.drop_all(engine)
    return "CEMS DB Tables Droped"

def get_session() -> Session: # type: ignore
    with Session(engine) as session:
        try:
            yield session
        finally:
            session.close()



