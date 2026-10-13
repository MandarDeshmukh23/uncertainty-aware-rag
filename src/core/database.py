from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from src.core.config import settings

# create_engine establishes the connection pool. 
# connect_args={"check_same_thread": False} is required only for SQLite in FastAPI.
engine = create_engine(
    settings.database_url, 
    connect_args={"check_same_thread": False} if settings.database_url.startswith("sqlite") else {}
)

# SessionLocal is a factory that generates new database sessions for each request
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class that our database models will inherit from
Base = declarative_base()

# Dependency to inject the database session into FastAPI routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()