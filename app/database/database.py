"""
RoomChat V2
Database Configuration

This file will NEVER need to be changed again.
"""

import os

from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

# ==========================================================
# LOAD ENVIRONMENT VARIABLES
# ==========================================================

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL is None:

    raise RuntimeError(

        "DATABASE_URL not found inside .env"

    )

# ==========================================================
# DATABASE ENGINE
# ==========================================================

engine = create_engine(

    DATABASE_URL,

    pool_pre_ping=True,

    pool_recycle=300,

    future=True

)

# ==========================================================
# SESSION
# ==========================================================

SessionLocal = sessionmaker(

    bind=engine,

    autoflush=False,

    autocommit=False,

    future=True

)

# ==========================================================
# BASE MODEL
# ==========================================================

Base = declarative_base()

# ==========================================================
# DATABASE DEPENDENCY
# ==========================================================

def get_db():

    db = SessionLocal()

    try:

        yield db

    finally:

        db.close()