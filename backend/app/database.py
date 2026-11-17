"""
database.py
-----------
SQLAlchemy setup for the Neon Postgres database. Neon is just regular
Postgres reachable over the internet, so a normal SQLAlchemy engine +
session is all that's needed — no special Neon client required.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from .config import DATABASE_URL

# pool_pre_ping checks a pooled connection is still alive before using
# it — useful for Neon, which can put idle connections to sleep.
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """FastAPI dependency: yields a DB session and always closes it after the request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
