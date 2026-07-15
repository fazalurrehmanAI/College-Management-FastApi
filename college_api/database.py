# ============================================
#  database.py
#  Sets up the database engine, session factory,
#  and the Base class all models inherit from.
# ============================================

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Load credentials from .env file (searches in current directory and parent directories)
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# --------------------------------------------
# engine — the actual connection to PostgreSQL
# pool_pre_ping=True checks the connection is
# alive before using it (good practice)
# --------------------------------------------
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# --------------------------------------------
# SessionLocal — a factory that creates DB sessions
# Each request gets its OWN session
# autocommit=False means we control when to save
# autoflush=False means we control when to sync
# --------------------------------------------
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# --------------------------------------------
# Base — all your models (tables) inherit this
# SQLAlchemy uses it to track all your tables
# --------------------------------------------
Base = declarative_base()


# --------------------------------------------
# get_db — dependency function injected into routes
# Opens a session → gives it to the route → closes it
# The 'yield' makes this a generator (context manager)
# --------------------------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db           # FastAPI injects this into your route
    finally:
        db.close()         # always runs, even if an error occurs