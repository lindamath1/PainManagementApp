#%%
from pydantic import BaseModel
from typing import Optional, Any
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker, Session
from utils.parameters import SQLALCHEMY_DATABASE_URL


class GetDBIn(BaseModel):
    url: Optional[str]

def get_db(get_db_in: Optional[GetDBIn] = None):
    """
    Creates a database session for the provided URL.

    Args:
        url: Database URL pointing to the SQLite database
        
    Yields:
        sqlalchemy.orm.Session: A database session.
            The session is created within a context manager to ensure proper
            cleanup after usage.
    """
    if get_db_in:
        url = get_db_in.url
    else:
        url = SQLALCHEMY_DATABASE_URL
    engine = create_engine(
        url,
        connect_args={"check_same_thread": False}
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class InitDBIn(BaseModel):
    url: str
    base: Any

def init_db(init_db_in: InitDBIn):
    """
    Create the SQLAlchemy engine and generate a session.
    The `check_same_thread` argument is specific to SQLite and ensures that the same thread is used for database connections.
    Args:
        url: Database URL pointing to the SQLite database
        base: Declarative Base for database models

    Returns: 
        sessionmaker: Session maker linked to the engine 
        engine
    """
    engine = create_engine(
        init_db_in.url, 
        connect_args={"check_same_thread": False}
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    #check if the tables exist
    inspector = inspect(engine)
    existing_tables = inspector.get_table_names()

    if not existing_tables:
      init_db_in.base.metadata.create_all(engine)
    
    return SessionLocal, engine


def get_session(init_db_params: InitDBIn) -> Session:
    sessionmaker, engine = init_db(init_db_params)
    return sessionmaker()


if __name__ == "__main__":
     import models
     from utils.parameters import SQLALCHEMY_DATABASE_URL
     init_params = InitDBIn(url=SQLALCHEMY_DATABASE_URL, base=models.Base)
     _, engine = init_db(init_params)

    




#%%