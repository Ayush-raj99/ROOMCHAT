"""
RoomChat V2
Database Configuration
"""

from sqlalchemy import create_engine

from sqlalchemy.orm import (

    sessionmaker,

    declarative_base

)

import os

from dotenv import load_dotenv





# =====================================================
# LOAD ENVIRONMENT VARIABLES
# =====================================================

load_dotenv()





# =====================================================
# DATABASE URL
# =====================================================


DATABASE_URL = os.getenv(

    "DATABASE_URL",

    "sqlite:///./roomchat.db"

)





# =====================================================
# ENGINE
# =====================================================


if DATABASE_URL.startswith(

    "sqlite"

):


    engine = create_engine(

        DATABASE_URL,

        connect_args={

            "check_same_thread": False

        }

    )


else:


    engine = create_engine(

        DATABASE_URL

    )







# =====================================================
# SESSION
# =====================================================


SessionLocal = sessionmaker(

    autocommit=False,

    autoflush=False,

    bind=engine

)





# =====================================================
# BASE CLASS
# =====================================================


Base = declarative_base()





# =====================================================
# DATABASE DEPENDENCY
# =====================================================


def get_db():


    db = SessionLocal()


    try:

        yield db


    finally:

        db.close()