from sqlalchemy import create_engine, URL
from sqlalchemy.orm import sessionmaker, declarative_base
from constants import environment

environment = environment.EnvironmentApp()

SQLALCHEMY_DATABASE_URL = environment.mssql_host

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
