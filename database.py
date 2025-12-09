## connect SQLAlchemy to database
from sqlalchemy import create_engine

## creates database sessions (used for queries and transactions).
from sqlalchemy.orm import sessionmaker

## base class used to define ORM models (tables).
from sqlalchemy.ext.declarative import declarative_base

## This string tells SQLAlchemy where the database is and what type of database it is.
SQLALCHEMY_DATABASE_URL = 'sqlite:///./shopershop.db'

## The engine is the core interface to the database. Connects SQLAlchemy to the database.
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False})

## Creates session objects for DB operations
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

## Base class for defining ORM models
Base = declarative_base()
