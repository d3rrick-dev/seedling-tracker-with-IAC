import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# Using 'db' for Docker networking

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "admin")
DB_PASS = os.getenv("DB_PASS", "supersecret")
DB_NAME = os.getenv("DB_NAME", "farming_db")

SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/{DB_NAME}"
# SQLALCHEMY_DATABASE_URL = "postgresql://admin:supersecret@db:5432/farming_db"
# local
# SQLALCHEMY_DATABASE_URL = "postgresql://admin:supersecret@localhost:5432/farming_db"
# engine manages the connection pool to the DB
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# sessionmaker creates a factory for database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Modern SQLAlchemy 2.0 Base class
class Base(DeclarativeBase):
    pass